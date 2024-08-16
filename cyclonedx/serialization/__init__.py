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

from json import loads as json_loads
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple, Type, Union
from uuid import UUID
from xml.etree.ElementTree import Element  # nosec B405

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL
from serializable.helpers import BaseHelper

from ..exception.serialization import CycloneDxDeserializationException, SerializationOfUnexpectedValueException
from ..model.bom_ref import BomRef
from ..model.component import Component
from ..model.license import DisjunctiveLicense, LicenseExpression, LicenseRepository
from ..model.service import Service
from ..model.tool import Tool, ToolsRepository
from ..schema import SchemaVersion

if TYPE_CHECKING:  # pragma: no cover
    from serializable import ObjectMetadataLibrary, ViewType


class BomRefHelper(BaseHelper):

    @classmethod
    def serialize(cls, o: Any) -> Optional[str]:
        if isinstance(o, BomRef):
            return o.value
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-BomRef: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> BomRef:
        try:
            return BomRef(value=str(o))
        except ValueError as err:
            raise CycloneDxDeserializationException(
                f'BomRef string supplied does not parse: {o!r}'
            ) from err


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
    @classmethod
    def json_normalize(cls, o: LicenseRepository, *,
                       view: Optional[Type['ViewType']],
                       **__: Any) -> Any:
        if len(o) == 0:
            return None
        expression = next((li for li in o if isinstance(li, LicenseExpression)), None)
        if expression:
            # mixed license expression and license? this is an invalid constellation according to schema!
            # see https://github.com/CycloneDX/specification/pull/205
            # but models need to allow it for backwards compatibility with JSON CDX < 1.5
            return [json_loads(expression.as_json(view_=view))]  # type:ignore[attr-defined]
        return [
            {'license': json_loads(
                li.as_json(  # type:ignore[attr-defined]
                    view_=view)
            )}
            for li in o
            if isinstance(li, DisjunctiveLicense)
        ]

    @classmethod
    def json_denormalize(cls, o: List[Dict[str, Any]],
                         **__: Any) -> LicenseRepository:
        repo = LicenseRepository()
        for li in o:
            if 'license' in li:
                repo.add(DisjunctiveLicense.from_json(  # type:ignore[attr-defined]
                    li['license']))
            elif 'expression' in li:
                repo.add(LicenseExpression.from_json(  # type:ignore[attr-defined]
                    li
                ))
            else:
                raise CycloneDxDeserializationException(f'unexpected: {li!r}')
        return repo

    @classmethod
    def xml_normalize(cls, o: LicenseRepository, *,
                      element_name: str,
                      view: Optional[Type['ViewType']],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        if len(o) == 0:
            return None
        elem = Element(element_name)
        expression = next((li for li in o if isinstance(li, LicenseExpression)), None)
        if expression:
            # mixed license expression and license? this is an invalid constellation according to schema!
            # see https://github.com/CycloneDX/specification/pull/205
            # but models need to allow it for backwards compatibility with JSON CDX < 1.5
            elem.append(expression.as_xml(  # type:ignore[attr-defined]
                view_=view, as_string=False, element_name='expression', xmlns=xmlns))
        else:
            elem.extend(
                li.as_xml(  # type:ignore[attr-defined]
                    view_=view, as_string=False, element_name='license', xmlns=xmlns)
                for li in o
                if isinstance(li, DisjunctiveLicense)
            )
        return elem

    @classmethod
    def xml_denormalize(cls, o: Element,
                        default_ns: Optional[str],
                        **__: Any) -> LicenseRepository:
        repo = LicenseRepository()
        for li in o:
            tag = li.tag if default_ns is None else li.tag.replace(f'{{{default_ns}}}', '')
            if tag == 'license':
                repo.add(DisjunctiveLicense.from_xml(  # type:ignore[attr-defined]
                    li, default_ns))
            elif tag == 'expression':
                repo.add(LicenseExpression.from_xml(  # type:ignore[attr-defined]
                    li, default_ns))
            else:
                raise CycloneDxDeserializationException(f'unexpected: {li!r}')
        return repo


class ToolsRepositoryHelper(BaseHelper):

    @staticmethod
    def __all_as_tools(o: ToolsRepository) -> Tuple[Tool, ...]:
        return (
            *o.tools,
            *map(Tool.from_component, o.components),
            *map(Tool.from_service, o.services),
        )

    @staticmethod
    def __supports_components_and_services(view: Any) -> bool:
        try:
            return view is not None and view().schema_version_enum >= SchemaVersion.V1_5
        except Exception:
            return False

    @classmethod
    def json_normalize(cls, o: ToolsRepository, *,
                       view: Optional[Type['ViewType']],
                       **__: Any) -> Any:
        if not o:
            return None
        if len(o.tools) > 0 or not cls.__supports_components_and_services(view):
            return cls.__all_as_tools(o)
        return {
            'components': tuple(o.components) if len(o.components) > 0 else None,
            'services': tuple(o.services) if len(o.services) > 0 else None,
        }

    @classmethod
    def json_denormalize(cls, o: Union[List[Dict[str, Any]], Dict[str, Any]],
                         **__: Any) -> ToolsRepository:
        tools = None
        components = None
        services = None
        if isinstance(o, Dict):
            components = map(lambda c: Component.from_json(  # type:ignore[attr-defined]
                c), o.get('components', ()))
            services = map(lambda s: Service.from_json(  # type:ignore[attr-defined]
                s), o.get('services', ()))
        elif isinstance(o, Iterable):
            tools = map(lambda t: Tool.from_json(t), o)  # type:ignore[attr-defined]
        return ToolsRepository(components=components, services=services, tools=tools)

    @classmethod
    def xml_normalize(cls, o: ToolsRepository, *,
                      element_name: str,
                      view: Optional[Type['ViewType']],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        if not o:
            return None
        elem = Element(element_name)
        if len(o.tools) > 0 or not cls.__supports_components_and_services(view):
            elem.extend(
                ti.as_xml(  # type:ignore[attr-defined]
                    view_=view, as_string=False, element_name='tool', xmlns=xmlns)
                for ti in cls.__all_as_tools(o)
            )
        else:
            if o.components:
                elem_c = Element(f'{{{xmlns}}}components' if xmlns else 'components')
                elem_c.extend(
                    ci.as_xml(  # type:ignore[attr-defined]
                        view_=view, as_string=False, element_name='component', xmlns=xmlns)
                    for ci in o.components)
                elem.append(elem_c)
            if o.services:
                elem_s = Element(f'{{{xmlns}}}services' if xmlns else 'services')
                elem_s.extend(
                    si.as_xml(  # type:ignore[attr-defined]
                        view_=view, as_string=False, element_name='service', xmlns=xmlns)
                    for si in o.services)
                elem.append(elem_s)
        return elem

    @classmethod
    def xml_denormalize(cls, o: Element, *,
                        default_ns: Optional[str],
                        prop_info: 'ObjectMetadataLibrary.SerializableProperty',
                        ctx: Type[Any],
                        **kwargs: Any) -> ToolsRepository:
        tools = []
        components = None
        services = None
        for e in o:
            tag = e.tag if default_ns is None else e.tag.replace(f'{{{default_ns}}}', '')
            if tag == 'tool':
                tools.append(Tool.from_xml(  # type:ignore[attr-defined]
                    e, default_ns))
            elif tag == 'components':
                components = map(lambda s: Component.from_xml(  # type:ignore[attr-defined]
                    s, default_ns), e)
            elif tag == 'services':
                services = map(lambda s: Service.from_xml(  # type:ignore[attr-defined]
                    s, default_ns), e)
            else:
                raise CycloneDxDeserializationException(f'unexpected: {e!r}')
        return ToolsRepository(
            tools=tools,
            components=components,
            services=services)
