from json import loads as json_loads
from typing import Any, Dict, Iterable, List, Optional, Type, Union
from warnings import warn
from xml.etree.ElementTree import Element  # nosec B405

import serializable
from serializable import ObjectMetadataLibrary, ViewType
from serializable.helpers import BaseHelper
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import MutuallyExclusivePropertiesException
from ..model import ExternalReference, HashType, _HashTypeRepositorySerializationHelper
from ..model.component import Component
from ..model.service import Service
from ..schema.schema import SchemaVersion1Dot4, SchemaVersion1Dot5, SchemaVersion1Dot6


@serializable.serializable_class
class Tool:
    """
    This is our internal representation of the `toolType` complex type within the CycloneDX standard.

    Tool(s) are the things used in the creation of the CycloneDX document.

    Tool might be deprecated since CycloneDX 1.5, but it is not deprecated in this library.
    In fact, this library will try to provide a compatibility layer if needed.

    .. note::
        See the CycloneDX Schema for toolType: https://cyclonedx.org/docs/1.3/#type_toolType
    """

    def __init__(
        self, *,
        vendor: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        hashes: Optional[Iterable[HashType]] = None,
        external_references: Optional[Iterable[ExternalReference]] = None,
    ) -> None:
        self.vendor = vendor
        self.name = name
        self.version = version
        self.hashes = hashes or []  # type:ignore[assignment]
        self.external_references = external_references or []  # type:ignore[assignment]

    @property
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def vendor(self) -> Optional[str]:
        """
        The name of the vendor who created the tool.

        Returns:
            `str` if set else `None`
        """
        return self._vendor

    @vendor.setter
    def vendor(self, vendor: Optional[str]) -> None:
        self._vendor = vendor

    @property
    @serializable.xml_sequence(2)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def name(self) -> Optional[str]:
        """
        The name of the tool.

        Returns:
             `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    @serializable.xml_sequence(3)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def version(self) -> Optional[str]:
        """
        The version of the tool.

        Returns:
             `str` if set else `None`
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property
    @serializable.type_mapping(_HashTypeRepositorySerializationHelper)
    @serializable.xml_sequence(4)
    def hashes(self) -> 'SortedSet[HashType]':
        """
        The hashes of the tool (if applicable).

        Returns:
            Set of `HashType`
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes: Iterable[HashType]) -> None:
        self._hashes = SortedSet(hashes)

    @property
    @serializable.view(SchemaVersion1Dot4)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    @serializable.xml_sequence(5)
    def external_references(self) -> 'SortedSet[ExternalReference]':
        """
        External References provides a way to document systems, sites, and information that may be relevant but which
        are not included with the BOM.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tool):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Tool):
            return _ComparableTuple((
                self.vendor, self.name, self.version
            )) < _ComparableTuple((
                other.vendor, other.name, other.version
            ))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.vendor, self.name, self.version, tuple(self.hashes), tuple(self.external_references)))

    def __repr__(self) -> str:
        return f'<Tool name={self.name}, version={self.version}, vendor={self.vendor}>'


class ToolsRepository:
    """
    The repository of tool formats

    This is done so we can maintain backward-compatibility with CycloneDX <= 1.4
    If using a SortedSet of tools, the object will behave like a sorted set of
    tools. Otherwise, it will behave like an object with `components`
    and `services` attributes (which are SortedSets of their respective types).
    """
    def __init__(self, *, components: Optional[Iterable[Component]] = None,
                 services: Optional[Iterable[Service]] = None,
                 # Deprecated in v1.5
                 tools: Optional[Iterable[Tool]] = None) -> None:

        if tools and (components or services):
            # Must use components/services or tools. Cannot use both
            raise MutuallyExclusivePropertiesException(
                'Cannot define both old (CycloneDX <= 1.4) and new '
                '(CycloneDX >= 1.5) format for tools.'
            )

        if tools:
            warn('Using Tool is deprecated as of CycloneDX v1.5. Components and Services should be used now. '
                 'See https://cyclonedx.org/docs/1.5/', DeprecationWarning)

        self._components = SortedSet(components or ())
        self._services = SortedSet(services or ())
        self._tools = SortedSet(tools or ())

    @property
    def components(self) -> 'SortedSet[Component]':
        """
        Returns:
            A SortedSet of Components
        """
        return self._components

    @components.setter
    def components(self, components: Iterable[Component]) -> None:
        if self._tools:
            raise MutuallyExclusivePropertiesException(
                'Cannot define both old (CycloneDX <= 1.4) and new '
                '(CycloneDX >= 1.5) format for tools.'
            )

        self._components = SortedSet(components)

    @property
    def services(self) -> 'SortedSet[Service]':
        """
        Returns:
            A SortedSet of Services
        """
        return self._services

    @services.setter
    def services(self, services: Iterable[Service]) -> None:
        if self._tools:
            raise MutuallyExclusivePropertiesException(
                'Cannot define both old (CycloneDX <= 1.4) and new '
                '(CycloneDX >= 1.5) format for tools.'
            )
        self._services = SortedSet(services)

    @property
    def tools(self) -> 'SortedSet[Tool]':
        """
        Returns:
            A SortedSet of Tools
        """
        return self._tools

    @tools.setter
    def tools(self, tools: Iterable[Tool]) -> None:
        if (self._components or self._tools):
            raise MutuallyExclusivePropertiesException(
                'Cannot define both old (CycloneDX <= 1.4) and new '
                '(CycloneDX >= 1.5) format for tools.'
            )
        self._tools = SortedSet(tools)

    def __len__(self) -> int:
        return len(self._tools) + len(self._components) + len(self._services)

    def __bool__(self) -> bool:
        return any([self._tools, self._components, self._services])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ToolsRepository):
            return False

        return (all([
            self._tools == other._tools,
            self._components == other._components,
            self._services == other._services,
        ]))


class ToolsRepositoryHelper(BaseHelper):
    @classmethod
    def json_normalize(cls, o: ToolsRepository, *,
                       view: Optional[Type[ViewType]],
                       **__: Any) -> Any:
        if not any([o._tools, o.components, o.services]):  # pylint: disable=protected-access
            return None

        result = {}

        if view().schema_version_enum >= SchemaVersion1Dot5().schema_version_enum:  # type: ignore[union-attr, misc]
            if o.components:
                result['components'] = [json_loads(Component.as_json(c, view_=view))  # type: ignore[attr-defined]
                                        for c in o.components]

            if o.services:
                result['services'] = [json_loads(Service.as_json(s, view_=view))  # type: ignore[attr-defined]
                                      for s in o.services]

            if result:
                return result

        if (o.components or o.services) and view().schema_version_enum < SchemaVersion1Dot5().schema_version_enum:  # type: ignore[union-attr, misc]
            # We "down-convert" Components and Services to Tools so we can render to older schemas
            tools_to_render: SortedSet[Tool] = SortedSet()

            for c in o.components:
                tools_to_render.add(Tool(
                    name=c.name,
                    vendor=c.group,
                    version=c.version,
                    hashes=c.hashes,
                    external_references=c.external_references,
                ))

            for s in o.services:
                if s.provider:
                    vendor = s.provider.name
                else:
                    vendor = None
                tools_to_render.add(Tool(
                    vendor=vendor,
                    version=s.version,
                    external_references=s.external_references,
                ))

        else:
            tools_to_render = o.tools


        return [json_loads(Tool.as_json(t, view_=view)) for t in tools_to_render]  # type: ignore[attr-defined]

    @classmethod
    def json_denormalize(cls, o: Union[List[Dict[str, Any]], Dict[str, Any]],
                         **__: Any) -> ToolsRepository:

        components = []
        services = []
        tools = []

        if isinstance(o, Dict):
            if 'components' in o:
                for c in o['components']:
                    components.append(Component.from_json(c))  # type: ignore[attr-defined]

            if 'services' in o:
                for s in o['services']:
                    services.append(Service.from_json(s))  # type: ignore[attr-defined]

        elif isinstance(o, Iterable):
            for t in o:
                tools.append(Tool.from_json(t))  # type: ignore[attr-defined]

        return ToolsRepository(components=components, services=services, tools=tools)

    @classmethod
    def xml_normalize(cls, o: ToolsRepository, *,
                      element_name: str,
                      view: Optional[Type[ViewType]],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        if not any([o._tools, o.components, o.services]):  # pylint: disable=protected-access
            return None

        elem = Element(element_name)

        if view().schema_version_enum >= SchemaVersion1Dot5().schema_version_enum:  # type: ignore[union-attr, misc]
            if o.components:
                c_elem = Element('{' + xmlns + '}' + 'components')  # type: ignore[operator]

                c_elem.extend(
                    c.as_xml(  # type: ignore[attr-defined]
                        view_=view, as_string=False, element_name='component', xmlns=xmlns)
                    for c in o.components
                )

                elem.append(c_elem)

            if o.services:
                s_elem = Element('{' + xmlns + '}' + 'services')  # type: ignore[operator]

                s_elem.extend(
                    s.as_xml(  # type: ignore[attr-defined]
                        view_=view, as_string=False, element_name='service', xmlns=xmlns)
                    for s in o.services
                )

                elem.append(s_elem)

            if len(elem) > 0:
                return elem

        elem.extend(
            t.as_xml(  # type: ignore[attr-defined]
                view_=view, as_string=False, element_name='tool', xmlns=xmlns)
            for t in o.tools
        )

        return elem

    @classmethod
    def xml_denormalize(cls, o: Element, *,
                        default_ns: Optional[str],
                        prop_info: ObjectMetadataLibrary.SerializableProperty,
                        ctx: Type[Any],
                        **kwargs: Any) -> ToolsRepository:
        tools: List[Tool] = []
        components: List[Component] = []
        services: List[Service] = []

        for e in o:
            tag = e.tag if default_ns is None else e.tag.replace(f'{{{default_ns}}}', '')
            if tag == 'tool':
                tools.append(Tool.from_xml(e))  # type: ignore[attr-defined]
            if tag == 'components':
                for c in e:
                    components.append(Component.from_xml(c))  # type: ignore[attr-defined]
            if tag == 'services':
                for s in e:
                    services.append(Service.from_xml(s))  # type: ignore[attr-defined]

        return ToolsRepository(tools=tools, components=components, services=services)
