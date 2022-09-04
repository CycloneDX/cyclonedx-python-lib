from datetime import datetime, timezone
from typing import Iterable, Optional

from sortedcontainers import SortedSet

from cyclonedx.model import LicenseChoice, OrganizationalContact, OrganizationalEntity, Property, ThisTool, Tool
from cyclonedx.model.component import Component


class BomMetaData:
    """
    This is our internal representation of the metadata complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for Bom metadata: https://cyclonedx.org/docs/1.4/#type_metadata
    """

    def __init__(self, *, tools: Optional[Iterable[Tool]] = None,
                 authors: Optional[Iterable[OrganizationalContact]] = None, component: Optional[Component] = None,
                 manufacture: Optional[OrganizationalEntity] = None,
                 supplier: Optional[OrganizationalEntity] = None,
                 licenses: Optional[Iterable[LicenseChoice]] = None,
                 properties: Optional[Iterable[Property]] = None) -> None:
        self.timestamp = datetime.now(tz=timezone.utc)
        self.tools = tools or []  # type: ignore
        self.authors = authors or []  # type: ignore
        self.component = component
        self.manufacture = manufacture
        self.supplier = supplier
        self.licenses = licenses or []  # type: ignore
        self.properties = properties or []  # type: ignore

        if not tools:
            self.tools.add(ThisTool)

    @property
    def timestamp(self) -> datetime:
        """
        The date and time (in UTC) when this BomMetaData was created.

        Returns:
            `datetime` instance in UTC timezone
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime) -> None:
        self._timestamp = timestamp

    @property
    def tools(self) -> "SortedSet[Tool]":
        """
        Tools used to create this BOM.

        Returns:
            `Set` of `Tool` objects.
        """
        return self._tools

    @tools.setter
    def tools(self, tools: Iterable[Tool]) -> None:
        self._tools = SortedSet(tools)

    @property
    def authors(self) -> "SortedSet[OrganizationalContact]":
        """
        The person(s) who created the BOM.

        Authors are common in BOMs created through manual processes.

        BOMs created through automated means may not have authors.

        Returns:
            Set of `OrganizationalContact`
        """
        return self._authors

    @authors.setter
    def authors(self, authors: Iterable[OrganizationalContact]) -> None:
        self._authors = SortedSet(authors)

    @property
    def component(self) -> Optional[Component]:
        """
        The (optional) component that the BOM describes.

        Returns:
            `cyclonedx.model.component.Component` instance for this Bom Metadata.
        """
        return self._component

    @component.setter
    def component(self, component: Component) -> None:
        """
        The (optional) component that the BOM describes.

        Args:
            component
                `cyclonedx.model.component.Component` instance to add to this Bom Metadata.

        Returns:
            None
        """
        self._component = component

    @property
    def manufacture(self) -> Optional[OrganizationalEntity]:
        """
        The organization that manufactured the component that the BOM describes.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._manufacture

    @manufacture.setter
    def manufacture(self, manufacture: Optional[OrganizationalEntity]) -> None:
        self._manufacture = manufacture

    @property
    def supplier(self) -> Optional[OrganizationalEntity]:
        """
        The organization that supplied the component that the BOM describes.

        The supplier may often be the manufacturer, but may also be a distributor or repackager.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._supplier

    @supplier.setter
    def supplier(self, supplier: Optional[OrganizationalEntity]) -> None:
        self._supplier = supplier

    @property
    def licenses(self) -> "SortedSet[LicenseChoice]":
        """
        A optional list of statements about how this BOM is licensed.

        Returns:
            Set of `LicenseChoice`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[LicenseChoice]) -> None:
        self._licenses = SortedSet(licenses)

    @property
    def properties(self) -> "SortedSet[Property]":
        """
        Provides the ability to document properties in a key/value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions.

        Property names of interest to the general public are encouraged to be registered in the CycloneDX Property
        Taxonomy - https://github.com/CycloneDX/cyclonedx-property-taxonomy. Formal registration is OPTIONAL.

        Return:
            Set of `Property`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BomMetaData):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.timestamp, self.tools, self.component
        ))

    def __repr__(self) -> str:
        return f'<BomMetaData timestamp={self.timestamp.utcnow()}>'

    def update(self, new_metadata: Optional["BomMetaData"]) -> None:
        if not new_metadata or self == new_metadata:
            return

        # TODO Add support of whole metadata and define update policy
        if new_metadata.component:
            self.component = new_metadata.component
