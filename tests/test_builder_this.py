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

from typing import Any, Dict, Iterable, Tuple, Union
from unittest import TestCase

from cyclonedx.builder.this import this_component, this_tool
from cyclonedx.model import ExternalReference, ExternalReferenceType
from cyclonedx.model.component import ComponentType
from cyclonedx.model.license import License, LicenseAcknowledgement
from tests import load_pyproject


class ExtRefsTestMixin:

    @staticmethod
    def __first_ers_uri(t: ExternalReferenceType, ers: Iterable[ExternalReference]) -> str:
        return next(filter(lambda r: r.type is t, ers)).url.uri

    def assertExtRefs(  # noqa:N802
        self: Union[TestCase, 'ExtRefsTestMixin'],
        p: Dict[str, Any], ers: Iterable[ExternalReference]
    ) -> None:
        self.assertEqual(p['tool']['poetry']['homepage'], self.__first_ers_uri(
            ExternalReferenceType.WEBSITE, ers))
        self.assertEqual(p['tool']['poetry']['repository'], self.__first_ers_uri(
            ExternalReferenceType.VCS, ers))
        self.assertEqual(p['tool']['poetry']['documentation'], self.__first_ers_uri(
            ExternalReferenceType.DOCUMENTATION, ers))
        self.assertEqual(p['tool']['poetry']['urls']['Bug Tracker'], self.__first_ers_uri(
            ExternalReferenceType.ISSUE_TRACKER, ers))


class TestThisComponent(TestCase, ExtRefsTestMixin):
    def test_basics(self) -> None:
        p = load_pyproject()
        c = this_component()
        self.assertIs(ComponentType.LIBRARY, c.type)
        self.assertEqual('CycloneDX', c.group)
        self.assertEqual(p['tool']['poetry']['name'], c.name)
        self.assertEqual(p['tool']['poetry']['version'], c.version)
        self.assertEqual(p['tool']['poetry']['description'], c.description)

    def test_license(self) -> None:
        p = load_pyproject()
        ls: Tuple[License, ...] = tuple(this_component().licenses)
        self.assertEqual(1, len(ls))
        l = ls[0]  # noqa:E741
        self.assertIs(LicenseAcknowledgement.DECLARED, l.acknowledgement)
        # this uses the fact that poetry expect license declarations as valid SPDX-license-id
        self.assertEqual(p['tool']['poetry']['license'], l.id)

    def test_extrefs(self) -> None:
        p = load_pyproject()
        ers: Tuple[ExternalReference, ...] = tuple(this_component().external_references)
        self.assertExtRefs(p, ers)


class TestThisTool(TestCase, ExtRefsTestMixin):
    def test_basics(self) -> None:
        p = load_pyproject()
        t = this_tool()
        self.assertEqual('CycloneDX', t.vendor)
        self.assertEqual(p['tool']['poetry']['name'], t.name)
        self.assertEqual(p['tool']['poetry']['version'], t.version)

    def test_extrefs(self) -> None:
        p = load_pyproject()
        ers: Tuple[ExternalReference, ...] = tuple(this_tool().external_references)
        self.assertExtRefs(p, ers)
