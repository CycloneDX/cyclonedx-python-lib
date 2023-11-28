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


from enum import Enum
from itertools import chain
from os.path import join
from typing import Generator, Type
from unittest import TestCase
from xml.etree.ElementTree import parse as xml_parse
from json import load as json_load

from ddt import ddt, idata, named_data

from cyclonedx.schema._res import BOM_XML as SCHEMA_XML, BOM_JSON as SCHEMA_JSON
from cyclonedx.schema import SchemaVersion, OutputFormat
from cyclonedx.output import make_outputter
from cyclonedx.validation import make_schemabased_validator
from cyclonedx.model.bom import Bom

from tests import SnapshotMixin

# region SUT

from cyclonedx.model import DataFlow, Encoding, HashAlgorithm, ExternalReferenceType
from cyclonedx.model.component import ComponentScope, ComponentType, PatchClassification
from cyclonedx.model.impact_analysis import ImpactAnalysisAffectedStatus, ImpactAnalysisJustification, \
    ImpactAnalysisResponse, ImpactAnalysisResponse, ImpactAnalysisState
from cyclonedx.model.issue import IssueClassification
from cyclonedx.model.vulnerability import VulnerabilityScoreSource, VulnerabilitySeverity

# endregion SUT


SCHEMA_NS = '{http://www.w3.org/2001/XMLSchema}'


def dp_enum_from_xml_schemas(xpath: str) -> Generator[str, None, None]:
    for sf in SCHEMA_XML.values():
        if sf is None:
            continue
        yield from (
            el.get('value')
            for el in
            xml_parse(sf).getroot().iterfind(f'{xpath}/{SCHEMA_NS}restriction/{SCHEMA_NS}enumeration')
        )


def dp_cases_from_json_schemas(*jsonpath: str) -> Generator[str, None, None]:
    for sf in SCHEMA_JSON.values():
        if sf is None:
            continue
        with open(sf) as sfh:
            data = json_load(sfh)
        try:
            for pp in jsonpath:
                data = data[pp]
        except KeyError:
            pass
        else:
            for value in data['enum']:
                yield value


UNSUPPORTED_OF_SV = frozenset([
    (OutputFormat.JSON, SchemaVersion.V1_1),
    (OutputFormat.JSON, SchemaVersion.V1_0),
])

NAMED_OF_SV = tuple(
    (f'{of.name}-{sv.to_version()}', of, sv)
    for of in OutputFormat
    for sv in SchemaVersion
    if (of, sv) not in UNSUPPORTED_OF_SV
)


class _EnumTestCase(TestCase, SnapshotMixin):

    def _test_knows_value(self, enum: Type[Enum], value: str) -> None:
        ec = enum(value)  # throws valueError if value unknown
        self.assertTrue(ec.name)  # TODO test for an expected name

    def _test_cases_render_valid(self, bom: Bom, of: OutputFormat, sv: SchemaVersion) -> None:
        snapshot_name = join(f'enum_{type(self).__name__.removeprefix("TestEnum")}-{sv.to_version()}.{of.name.lower()}')

        output = make_outputter(bom, of, sv).output_as_string(indent=2)
        validation_errors = make_schemabased_validator(of, sv).validate_str(output)

        self.assertIsNone(validation_errors)
        self.assertEqualSnapshot(output, snapshot_name)


@ddt
class TestEnumDataFlow(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='dataFlowType']"),
        dp_cases_from_json_schemas('definitions', 'dataFlowDirection'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(DataFlow, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion) -> None:
        from cyclonedx.model.service import Service, DataClassification
        bom = Bom(services=[Service(name='dummy', data=(
            DataClassification(flow=df, classification=df.name) for df in DataFlow
        ))])
        super()._test_cases_render_valid(bom, of, sv)
