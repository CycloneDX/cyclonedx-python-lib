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

from typing import Any, Dict, List
from uuid import UUID

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL
from serializable.helpers import BaseHelper

from ..model.license import LicenseRepository, LicenseExpression, DisjunctiveLicense
from ..model.bom_ref import BomRef


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


from json import loads as json_loads


class LicenseRepositoryHelper(BaseHelper):
    @classmethod
    def json_serialize(cls, o: LicenseRepository) -> Any:
        if len(o) == 0:
            return None
        expression = next((li for li in o if isinstance(li, LicenseExpression)), None)
        if expression:
            return [{'expression': str(expression.value)}]
        return [{'license': json_loads(li.as_json())} for li in o]

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
    def xml_serialize(cls, o: Any) -> Any:
        pass

    @classmethod
    def xml_deserialize(cls, o: Any) -> Any:
        pass
