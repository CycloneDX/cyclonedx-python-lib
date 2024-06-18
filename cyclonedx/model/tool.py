from typing import Any, Dict, Iterable, Iterator, List, Optional, Type, Union
from xml.etree.ElementTree import Element  # nosec B405

import serializable
from serializable import ViewType
from serializable.helpers import BaseHelper
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import MutuallyExclusivePropertiesException
from ..exception.serialization import CycloneDxDeserializationException
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

    def __init__(self, *, vendor: Optional[str] = None, name: Optional[str] = None, version: Optional[str] = None,
                 hashes: Optional[Iterable[HashType]] = None,
                 external_references: Optional[Iterable[ExternalReference]] = None) -> None:
        self.vendor = vendor
        self.name = name
        self.version = version
        self.hashes = hashes or []  # type:ignore[assignment]
        self.external_references = external_references or []  # type:ignore[assignment]

    @property
    @serializable.xml_sequence(1)
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


class ToolRepository:
    """
    The repo of tool formats
    """

    def __init__(self, *, components: Optional[Iterable[Component]] = None,
                 services: Optional[Iterable[Service]] = None,
                 tools: Optional[Iterable[Tool]] = None) -> None:
        self._components = components or SortedSet()
        self._services = services or SortedSet()
        # Must use components/services or tools. Cannot use both
        self._tools = tools or SortedSet()

    @property
    def components(self) -> Iterable[Component]:
        """
        Returns:
            A SortedSet of Components
        """
        return self._components

    @components.setter
    def components(self, components: Iterable[Component]) -> None:
        if self._tools:
            raise MutuallyExclusivePropertiesException(
                'Cannot serialize both old (CycloneDX <= 1.4) and new '
                '(CycloneDX >= 1.5) format for tools.'
            )

        self._components = components

    @property
    def services(self) -> Iterable[Service]:
        """
        Returns:
            A SortedSet of Services
        """
        return self._services

    @services.setter
    def services(self, services: Iterable[Service]) -> None:
        if self._tools:
            raise MutuallyExclusivePropertiesException(
                'Cannot serialize both old (CycloneDX <= 1.4) and new '
                '(CycloneDX >= 1.5) format for tools: {o!r}'
            )
        self._services = services

    def __getattr__(self, name: str) -> Any:
        """
        Enables us to behave as list of tools to maintain
        backward compatibility.

        Returns:
            An attribute of SortedSet
        """
        return getattr(self._tools, name)

    def __iter__(self) -> Iterator[Tool]:
        """
        Also part of acting as a list of tools

        Returns Iterator[Tool]
        """
        for t in self._tools:
            yield t


class ToolRepositoryHelper(BaseHelper):
    @classmethod
    def json_normalize(cls, o: ToolRepository, *,
                       view: Optional[Type[ViewType]],
                       **__: Any) -> Any:
        if not any([o._tools, o._components, o._services]):  # pylint: disable=protected-access
            return None

        if o._tools:  # pylint: disable=protected-access
            return [Tool.as_json(t) for t in o._tools]  # pylint: disable=protected-access

        result = {}

        if o._components:  # pylint: disable=protected-access
            result['components'] = [Component.as_json(c) for c in o._components]  # pylint: disable=protected-access

        if o._services:  # pylint: disable=protected-access
            result['services'] = [Service.as_json(s) for s in o._services]  # pylint: disable=protected-access

        return result

    @classmethod
    def json_denormalize(cls, o: Union[List[Dict[str, Any]], Dict[str, Any]],
                         **__: Any) -> ToolRepository:

        components = []
        services = []
        tools = []

        if isinstance(o, Dict):
            if 'components' in o:
                for c in o['components']:
                    components.append(Component.from_json(c))

            if 'services' in o:
                for s in o['services']:
                    services.append(Service.from_json(s))

        elif isinstance(o, Iterable):
            for t in o:
                tools.append(Tool.from_json(t))
        else:
            raise CycloneDxDeserializationException('unexpected: {o!r}')

        return ToolRepository(components=components, services=services, tools=tools)

    @classmethod
    def xml_normalize(cls, o: ToolRepository, *,
                      element_name: str,
                      view: Optional[Type[ViewType]],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        pass

    @classmethod
    def xml_denormalize(cls, o: Element,
                        default_ns: Optional[str],
                        **__: Any) -> ToolRepository:
        return ToolRepository()
