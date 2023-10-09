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


"""
Set of helper classes for use with ``serializable`` when conducting (de-)serialization.
"""

from typing import Any, Dict, List, TYPE_CHECKING, Optional, Type
from uuid import UUID

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL
from serializable.helpers import BaseHelper

from ..model.license import LicenseRepository, LicenseExpression, DisjunctiveLicense
from ..model.bom_ref import BomRef

from json import loads as json_loads

if TYPE_CHECKING:  # pragma: no cover
    from serializable import ViewType


class BomRefHelper(BaseHelper):

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, BomRef):
            return o.value

        raise ValueError(f'Attempt to serialize a non-BomRef: {o.__class__}')

    @classmethod
    def deserialize(cls, o: Any) -> BomRef:
        try:
            return BomRef(value=str(o))
        except ValueError:
            raise ValueError(f'BomRef string supplied ({o}) does not parse!')


class PackageUrl(BaseHelper):

    @classmethod
    def serialize(cls, o: Any, ) -> str:
        if isinstance(o, PackageURL):
            return str(o.to_string())

        raise ValueError(f'Attempt to serialize a non-PackageURL: {o.__class__}')

    @classmethod
    def deserialize(cls, o: Any) -> PackageURL:
        try:
            return PackageURL.from_string(purl=str(o))
        except ValueError:
            raise ValueError(f'PURL string supplied ({o}) does not parse!')


class UrnUuidHelper(BaseHelper):

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, UUID):
            return o.urn

        raise ValueError(f'Attempt to serialize a non-UUID: {o.__class__}')

    @classmethod
    def deserialize(cls, o: Any) -> UUID:
        try:
            return UUID(str(o))
        except ValueError:
            raise ValueError(f'UUID string supplied ({o}) does not parse!')


from xml.etree.ElementTree import Element


class LicenseRepositoryHelper(BaseHelper):
    @classmethod
    def json_normalize(cls, o: LicenseRepository, *,
                       view_: Optional[Type['ViewType']]) -> Any:
        if len(o) == 0:
            return None
        expression = next((li for li in o if isinstance(li, LicenseExpression)), None)
        if expression:
            # license expression and a license -- this is an invalid constellation according to schema
            # see https://github.com/CycloneDX/specification/pull/205
            # but models need to allow it for backwards compatibility with JSON CDX < 1.5
            return [{'expression': str(expression.value)}]
        return [{'license': json_loads(li.as_json(view_=view_))} for li in o]

    @classmethod
    def json_deserialize(cls, o: List[Dict[str, Any]]) -> LicenseRepository:
        licenses = LicenseRepository()
        for li in o:
            if 'license' in li:
                licenses.add(DisjunctiveLicense.from_json(li['license']))
            elif 'expression' in li:
                licenses.add(LicenseExpression(li['expression']))
        return licenses

    @classmethod
    def xml_normalize(cls, o: LicenseRepository, *,
                      element_name: str,
                      view_: Optional[Type['ViewType']],
                      xmlns: Optional[str]) -> Optional[Element]:
        if len(o) == 0:
            return None
        elem = Element(element_name)
        expression = next((li for li in o if isinstance(li, LicenseExpression)), None)
        if expression:
            elem.append(expression.as_xml(view_, as_string=False, element_name='expression', xmlns=xmlns))
        else:
            for li in o:
                elem.append(li.as_xml(view_, as_string=False, element_name='license', xmlns=xmlns))
        return elem

    @classmethod
    def xml_deserialize(cls, o: Any) -> Any:
        pass
