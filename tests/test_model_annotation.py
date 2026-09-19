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

from datetime import datetime, timezone
from unittest import TestCase

from cyclonedx.model.annotation import Annotation, Annotator
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.contact import OrganizationalContact, OrganizationalEntity
from tests import reorder

_TIMESTAMP = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


class TestModelAnnotator(TestCase):

    def test_invalid_no_args(self) -> None:
        with self.assertRaises(ValueError):
            Annotator()

    def test_invalid_multiple_args(self) -> None:
        with self.assertRaises(ValueError):
            Annotator(
                organization=OrganizationalEntity(name='A'),
                individual=OrganizationalContact(name='B'),
            )

    def test_sort(self) -> None:
        # expected sort order: (organization, individual, component, service)
        expected_order = [0, 2, 1]
        annotators = [
            Annotator(organization=OrganizationalEntity(name='Acme')),
            Annotator(individual=OrganizationalContact(name='Zoe')),
            Annotator(individual=OrganizationalContact(name='Alice')),
        ]
        self.assertListEqual(sorted(annotators), reorder(annotators, expected_order))


class TestModelAnnotation(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (bom_ref.value, subjects, annotator, timestamp, text)
        annotator = Annotator(organization=OrganizationalEntity(name='Acme'))
        expected_order = [0, 2, 1]
        annotations = [
            Annotation(bom_ref='a', subjects=[BomRef('s')], annotator=annotator,
                       timestamp=_TIMESTAMP, text='alpha'),
            Annotation(bom_ref='c', subjects=[BomRef('s')], annotator=annotator,
                       timestamp=_TIMESTAMP, text='gamma'),
            Annotation(bom_ref='b', subjects=[BomRef('s')], annotator=annotator,
                       timestamp=_TIMESTAMP, text='beta'),
        ]
        self.assertListEqual(sorted(annotations), reorder(annotations, expected_order))
