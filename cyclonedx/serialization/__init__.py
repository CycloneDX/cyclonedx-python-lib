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


"""
Set of helper classes for use with ``serializable`` when conducting (de-)serialization.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type
from uuid import UUID
from xml.etree.ElementTree import Element  # nosec B405

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL
from serializable.helpers import BaseHelper

from ..exception.serialization import CycloneDxDeserializationException, SerializationOfUnexpectedValueException
from ..model.bom_ref import BomRef
from ..model.license import LicenseRepository, _LicenseRepositorySerializationHelper

if TYPE_CHECKING:  # pragma: no cover
    from serializable import ViewType


class BomRefHelper(BaseHelper):
    # TODO: remove, no longer needed

    @classmethod
    def serialize(cls, o: Any) -> Optional[str]:
        return BomRef.serialize(o)

    @classmethod
    def deserialize(cls, o: Any) -> BomRef:
        return BomRef.deserialize(o)


class PackageUrl(BaseHelper):

    @classmethod
    def serialize(cls, o: Any, ) -> str:
        if isinstance(o, PackageURL):
            return str(o.to_string())
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-PackageURL: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> PackageURL:
        try:
            return PackageURL.from_string(purl=str(o))
        except ValueError as err:
            raise CycloneDxDeserializationException(
                f'PURL string supplied does not parse: {o!r}'
            ) from err


class UrnUuidHelper(BaseHelper):

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, UUID):
            return o.urn
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-UUID: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> UUID:
        try:
            return UUID(str(o))
        except ValueError as err:
            raise CycloneDxDeserializationException(
                f'UUID string supplied does not parse: {o!r}'
            ) from err


class LicenseRepositoryHelper(BaseHelper):
    # TODO: remove, no longer needed

    @classmethod
    def json_normalize(cls, o: LicenseRepository, *,
                       view: Optional[Type['ViewType']],
                       **__: Any) -> Any:
        return _LicenseRepositorySerializationHelper.json_normalize(o, view=view)

    @classmethod
    def json_denormalize(cls, o: List[Dict[str, Any]],
                         **__: Any) -> LicenseRepository:
        return _LicenseRepositorySerializationHelper.json_denormalize(o)

    @classmethod
    def xml_normalize(cls, o: LicenseRepository, *,
                      element_name: str,
                      view: Optional[Type['ViewType']],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        return _LicenseRepositorySerializationHelper.xml_normalize(o, element_name=element_name, view=view, xmlns=xmlns)

    @classmethod
    def xml_denormalize(cls, o: Element,
                        default_ns: Optional[str],
                        **__: Any) -> LicenseRepository:
        return _LicenseRepositorySerializationHelper.xml_denormalize(o, default_ns)
