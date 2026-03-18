# This file is part of CycloneDX Python Library
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

from collections.abc import Callable
from os.path import join
from typing import Any
from unittest import TestCase
from unittest.mock import patch

from ddt import ddt, named_data

from cyclonedx.model.bom import Bom
from cyclonedx.schema import OutputFormat, SchemaVersion
from tests import OWN_DATA_DIRECTORY, DeepCompareMixin, SnapshotMixin, mksname
from tests._data.models import (
    all_get_bom_funct_valid_immut,
    all_get_bom_funct_valid_reversible_migrate,
    all_get_bom_funct_with_incomplete_deps,
)

_LATEST_SCHEMA = SchemaVersion.V1_7


@ddt
class TestDeserializeXml(TestCase, SnapshotMixin, DeepCompareMixin):

    @named_data(*all_get_bom_funct_valid_immut,
                *all_get_bom_funct_valid_reversible_migrate)
    @patch('cyclonedx.contrib.this.builders.__ThisVersion', 'TESTING')
    def test_prepared(self, get_bom: Callable[[], Bom], *_: Any, **__: Any) -> None:
        # only latest schema will have all data populated in serialized form
        snapshot_name = mksname(get_bom, _LATEST_SCHEMA, OutputFormat.XML)
        expected = get_bom()
        self._apply_xml_only_workarounds(expected)
        with open(self.getSnapshotFile(snapshot_name)) as s:
            bom = Bom.from_xml(s)
        self.assertBomDeepEqual(expected, bom,
                                fuzzy_deps=get_bom in all_get_bom_funct_with_incomplete_deps)

    def test_component_evidence_identity(self) -> None:
        xml_file = join(OWN_DATA_DIRECTORY, 'xml',
                        SchemaVersion.V1_6.to_version(),
                        'component_evidence_identity.xml')
        with open(xml_file) as f:
            bom: Bom = Bom.from_xml(f)  # <<< is expected to not crash
        self.assertIsNotNone(bom)

    @classmethod
    def _apply_xml_only_workarounds(cls, bom: Bom) -> None:
        """Adjust expected BOM for known XML serialization gaps (spec issue #726)."""
        cls._strip_model_card_properties(bom)

    @classmethod
    def _strip_model_card_properties(cls, bom: Bom) -> None:
        # ModelCard.properties are currently omitted from XML output until spec issue #726 is resolved.
        # To keep the XML deserialize snapshot test accurate, remove those properties from the expected BOM.
        for component in bom.components:
            cls._strip_component_model_card_properties(component)

        metadata_component = getattr(bom.metadata, 'component', None)
        if metadata_component is not None:
            cls._strip_component_model_card_properties(metadata_component)

    @classmethod
    def _strip_component_model_card_properties(cls, component: Any) -> None:
        model_card = getattr(component, 'model_card', None)
        if model_card is not None and getattr(model_card, 'properties', None):
            model_card.properties = []

        sub_components = getattr(component, 'components', None)
        if sub_components:
            for child in sub_components:
                cls._strip_component_model_card_properties(child)
