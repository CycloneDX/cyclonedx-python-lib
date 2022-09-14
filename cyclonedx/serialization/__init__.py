# encoding: utf-8

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

"""
Set of helper classes for use with ``serializable`` when conducting (de-)serialization.
"""

from uuid import UUID

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore
from serializable.helpers import BaseHelper

from ..model.bom_ref import BomRef


class BomRefHelper(BaseHelper):

    @classmethod
    def serialize(cls, o: object) -> str:
        if isinstance(o, BomRef):
            return o.value

        raise ValueError(f'Attempt to serialize a non-BomRef: {o.__class__}')

    @classmethod
    def deserialize(cls, o: object) -> BomRef:
        try:
            return BomRef(value=str(o))
        except ValueError:
            raise ValueError(f'BomRef string supplied ({o}) does not parse!')


class PackageUrl(BaseHelper):

    @classmethod
    def serialize(cls, o: object) -> str:
        if isinstance(o, PackageURL):
            return str(o.to_string())

        raise ValueError(f'Attempt to serialize a non-PackageURL: {o.__class__}')

    @classmethod
    def deserialize(cls, o: object) -> PackageURL:
        try:
            return PackageURL.from_string(purl=str(o))
        except ValueError:
            raise ValueError(f'PURL string supplied ({o}) does not parse!')


class UrnUuidHelper(BaseHelper):

    @classmethod
    def serialize(cls, o: object) -> str:
        if isinstance(o, UUID):
            return o.urn

        raise ValueError(f'Attempt to serialize a non-UUID: {o.__class__}')

    @classmethod
    def deserialize(cls, o: object) -> PackageURL:
        try:
            return UUID(str(o))
        except ValueError:
            raise ValueError(f'UUID string supplied ({o}) does not parse!')
