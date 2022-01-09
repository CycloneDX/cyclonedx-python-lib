# encoding: utf-8

# This file is part of CycloneDX Python Lib
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

import warnings
from enum import Enum
from os.path import exists
from typing import List, Optional

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore

from . import ExternalReference, HashAlgorithm, HashType, OrganizationalEntity, sha1sum, LicenseChoice, Property
from .release_note import ReleaseNotes
from .vulnerability import Vulnerability


class ComponentScope(Enum):
    """
    Enum object that defines the permissable 'scopes' for a Component according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_scope
    """
    REQUIRED = 'required'
    OPTIONAL = 'optional'
    EXCLUDED = 'excluded'


class ComponentType(Enum):
    """
    Enum object that defines the permissible 'types' for a Component according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_classification
    """
    APPLICATION = 'application'
    CONTAINER = 'container'
    DEVICE = 'device'
    FILE = 'file'
    FIRMWARE = 'firmware'
    FRAMEWORK = 'framework'
    LIBRARY = 'library'
    OPERATING_SYSTEM = 'operating-system'


class Component:
    """
    This is our internal representation of a Component within a Bom.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_component
    """

    @staticmethod
    def for_file(absolute_file_path: str, path_for_bom: Optional[str]) -> 'Component':
        """
        Helper method to create a Component that represents the provided local file as a Component.

        Args:
            absolute_file_path:
                Absolute path to the file you wish to represent
            path_for_bom:
                Optionally, if supplied this is the path that will be used to identify the file in the BOM

        Returns:
            `Component` representing the supplied file
        """
        if not exists(absolute_file_path):
            raise FileExistsError('Supplied file path \'{}\' does not exist'.format(absolute_file_path))

        sha1_hash: str = sha1sum(filename=absolute_file_path)
        return Component(
            name=path_for_bom if path_for_bom else absolute_file_path,
            version='0.0.0-{}'.format(sha1_hash[0:12]),
            hashes=[
                HashType(algorithm=HashAlgorithm.SHA_1, hash_value=sha1_hash)
            ],
            component_type=ComponentType.FILE,
            package_url_type='generic'
        )

    def __init__(self, name: str, component_type: ComponentType = ComponentType.LIBRARY,
                 mime_type: Optional[str] = None, bom_ref: Optional[str] = None,
                 supplier: Optional[OrganizationalEntity] = None, author: Optional[str] = None,
                 publisher: Optional[str] = None, group: Optional[str] = None, version: Optional[str] = None,
                 description: Optional[str] = None, scope: Optional[ComponentScope] = None,
                 hashes: Optional[List[HashType]] = None, licenses: Optional[List[LicenseChoice]] = None,
                 copyright: Optional[str] = None, purl: Optional[PackageURL] = None,
                 external_references: Optional[List[ExternalReference]] = None,
                 properties: Optional[List[Property]] = None, release_notes: Optional[ReleaseNotes] = None,
                 package_url_type: str = 'pypi', package_url_qualifiers: Optional[str] = None,
                 package_url_subpath: Optional[str] = None,
                 # Deprecated parameters kept for backwards compatibility
                 namespace: Optional[str] = None, qualifiers: Optional[str] = None, subpath: Optional[str] = None,
                 license_str: Optional[str] = None
                 ) -> None:
        # Must be first - not part of the CycloneDX Spec, but used by our model
        self.__purl_qualifiers: Optional[str] = package_url_qualifiers or qualifiers
        self.__purl_subpath: Optional[str] = package_url_subpath or subpath
        self.__purl_type: str = package_url_type
        self.__vulnerabilites: List[Vulnerability] = []

        self.type = component_type
        self.mime_type = mime_type
        self.supplier = supplier
        self.author = author
        self.publisher = publisher
        self.group = group
        self.name = name
        self.version = version
        self.description = description
        self.scope = scope
        self.hashes = hashes or []
        self.licenses = licenses or []
        self.copyright = copyright
        self.purl = purl.to_string() if purl else None
        self.external_references = external_references if external_references else []
        self.properties = properties

        # Deprecated for 1.4, but kept for some backwards compatibility
        if namespace:
            warnings.warn(
                '`namespace` is deprecated and has been replaced with `group` to align with the CycloneDX standard',
                DeprecationWarning
            )
            if not group:
                self.group = namespace

        if qualifiers:
            warnings.warn(
                '`qualifiers` is deprecated - if your Component is best represented with qualifiers, provide a '
                'PackageURL via `purl` or use `package_url_qualifiers`', DeprecationWarning
            )

        if subpath:
            warnings.warn(
                '`subpath` is deprecated - if your Component is best represented with a subpath, provide a '
                'PackageURL via `purl` or use `package_url_subpath`', DeprecationWarning
            )

        if license_str:
            warnings.warn(
                '`license_str` is deprecated and has been replaced with `licenses` to align with the CycloneDX '
                'standard', DeprecationWarning
            )
            if not licenses:
                self.licenses = [LicenseChoice(license_expression=license_str)]

        # Added for 1.4
        self.release_notes = release_notes

        # Last as depends on others having being set
        self.bom_ref = bom_ref or self.to_package_url().to_string()

    @property
    def type(self) -> ComponentType:
        """
        Get the type of this Component.

        Returns:
            Declared type of this Component as `ComponentType`.
        """
        return self._type

    @type.setter
    def type(self, component_type: ComponentType) -> None:
        self._type = component_type

    @property
    def mime_type(self) -> Optional[str]:
        """
        Get any declared mime-type for this Component.

        When used on file components, the mime-type can provide additional context about the kind of file being
        represented such as an image, font, or executable. Some library or framework components may also have an
        associated mime-type.

        Returns:
            `str` if set else `None`
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type: Optional[str]) -> None:
        self._mime_type = mime_type

    @property
    def bom_ref(self) -> Optional[str]:
        """
        An optional identifier which can be used to reference the component elsewhere in the BOM. Every bom-ref MUST be
        unique within the BOM.

        Returns:
            `str` as a unique identifiers for this Component if set else `None`
        """
        return self._bom_ref

    @bom_ref.setter
    def bom_ref(self, bom_ref: Optional[str]) -> None:
        self._bom_ref = bom_ref

    @property
    def supplier(self) -> Optional[OrganizationalEntity]:
        """
        The organization that supplied the component. The supplier may often be the manufacture, but may also be a
        distributor or repackager.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._supplier

    @supplier.setter
    def supplier(self, supplier: Optional[OrganizationalEntity]) -> None:
        self._supplier = supplier

    @property
    def author(self) -> Optional[str]:
        """
        The person(s) or organization(s) that authored the component.

        Returns:
            `str` if set else `None`
        """
        return self._author

    @author.setter
    def author(self, author: Optional[str]) -> None:
        self._author = author

    @property
    def publisher(self) -> Optional[str]:
        """
        The person(s) or organization(s) that published the component

        Returns:
            `str` if set else `None`
        """
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: Optional[str]) -> None:
        self._publisher = publisher

    @property
    def group(self) -> Optional[str]:
        """
        The grouping name or identifier. This will often be a shortened, single name of the company or project that
        produced the component, or the source package or domain name. Whitespace and special characters should be
        avoided.

        Examples include: `apache`, `org.apache.commons`, and `apache.org`.

        Returns:
            `str` if set else `None`
        """
        return self._group

    @group.setter
    def group(self, group: Optional[str]) -> None:
        self._group = group
        self._recalculate_purl()

    @property
    def name(self) -> str:
        """
        The name of the component.

        This will often be a shortened, single name of the component.

        Examples: `commons-lang3` and `jquery`.

        Returns:
            `str`
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name
        self._recalculate_purl()

    @property
    def version(self) -> Optional[str]:
        """
        The component version. The version should ideally comply with semantic versioning but is not enforced.

        This is NOT optional for CycloneDX Schema Version < 1.4 but was agreed to default to an empty string where a
        version was not supplied for schema versions < 1.4

        Returns:
            Declared version of this Component as `str` or `None`
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version
        self._recalculate_purl()

    @property
    def description(self) -> Optional[str]:
        """
        Get the description of this Component.

        Returns:
            `str` if set, else `None`.
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    def scope(self) -> Optional[ComponentScope]:
        """
        Specifies the scope of the component.

        If scope is not specified, 'required' scope should be assumed by the consumer of the BOM.

        Returns:
            `ComponentScope` or `None`
        """
        return self._scope

    @scope.setter
    def scope(self, scope: Optional[ComponentScope]) -> None:
        self._scope = scope

    @property
    def hashes(self) -> List[HashType]:
        """
        Optional list of hashes that help specifiy the integrity of this Component.

        Returns:
             List of `HashType` or `None`
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes: List[HashType]) -> None:
        self._hashes = hashes

    def add_hash(self, a_hash: HashType) -> None:
        """
        Adds a hash that pins/identifies this Component.

        Args:
            a_hash:
                `HashType` instance
        """
        self.hashes = self.hashes + [a_hash]

    @property
    def licenses(self) -> List[LicenseChoice]:
        """
        A optional list of statements about how this Component is licensed.

        Returns:
            List of `LicenseChoice` else `None`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: List[LicenseChoice]) -> None:
        self._licenses = licenses

    @property
    def copyright(self) -> Optional[str]:
        """
        An optional copyright notice informing users of the underlying claims to copyright ownership in a published
        work.

        Returns:
            `str` or `None`
        """
        return self._copyright

    @copyright.setter
    def copyright(self, copyright: Optional[str]) -> None:
        self._copyright = copyright

    @property
    def purl(self) -> Optional[str]:
        """
        Specifies the package-url (PURL).

        The purl, if specified, must be valid and conform to the specification defined at:
        https://github.com/package-url/purl-spec

        This method returns a string representation as JSON Serialisation would incorrectly encode the PackageURL
        NamedTuple for us. You can get the PackageURL by calling `Component.to_package_url()`.

        Returns:
            `str`
        """
        return self._purl

    @purl.setter
    def purl(self, purl: Optional[str]) -> None:
        if purl:
            self._purl = purl
        else:
            self._purl = self.to_package_url().to_string()

    def _recalculate_purl(self) -> None:
        if self.group and self.name and self.version:
            self.purl = self.to_package_url().to_string()

    @property
    def external_references(self) -> List[ExternalReference]:
        """
        Provides the ability to document external references related to the component or to the project the component
        describes.

        Returns:
            List of `ExternalReference`s
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: List[ExternalReference]) -> None:
        self._external_references = external_references

    def add_external_reference(self, reference: ExternalReference) -> None:
        """
        Add an `ExternalReference` to this `Component`.

        Args:
            reference:
                `ExternalReference` instance to add.
        """
        self.external_references = self._external_references + [reference]

    @property
    def properties(self) -> Optional[List[Property]]:
        """
        Provides the ability to document properties in a key/value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions.

        Return:
            List of `Property` or `None`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Optional[List[Property]]) -> None:
        self._properties = properties

    @property
    def release_notes(self) -> Optional[ReleaseNotes]:
        """
        Specifies optional release notes.

        Returns:
            `ReleaseNotes` or `None`
        """
        return self._release_notes

    @release_notes.setter
    def release_notes(self, release_notes: Optional[ReleaseNotes]) -> None:
        self._release_notes = release_notes

    def add_vulnerability(self, vulnerability: Vulnerability) -> None:
        """
        Add a Vulnerability to this Component.

        Args:
            vulnerability:
                `cyclonedx.model.vulnerability.Vulnerability` instance to add to this Component.

        Returns:
            None
        """
        self.__vulnerabilites.append(vulnerability)

    def get_vulnerabilities(self) -> List[Vulnerability]:
        """
        Get all the Vulnerabilities for this Component.

        Returns:
             List of `Vulnerability` objects assigned to this Component.
        """
        return self.__vulnerabilites

    def has_vulnerabilities(self) -> bool:
        """
        Does this Component have any vulnerabilities?

        Returns:
             `True` if this Component has 1 or more vulnerabilities, `False` otherwise.
        """
        return bool(self.get_vulnerabilities())

    def get_pypi_url(self) -> str:
        if self.version:
            return f'https://pypi.org/project/{self.name}/{self.version}'
        else:
            return f'https://pypi.org/project/{self.name}'

    def get_subpath(self) -> Optional[str]:
        """
        Get the subpath of this Component.

        Returns:
            Declared subpath of this Component as `str` if declared, else `None`.
        """
        p = self.to_package_url()
        return p.subpath if hasattr(p, 'subpath') else None

    def to_package_url(self) -> PackageURL:
        """
        Return a PackageURL representation of this Component.

        Returns:
            `packageurl.PackageURL` instance which represents this Component.
        """""
        return PackageURL(type=self.__purl_type, namespace=self.group, name=self.name, version=self.version,
                          qualifiers=self.__purl_qualifiers, subpath=self.__purl_subpath)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Component):
            return other.purl == self.purl
        return False

    def __repr__(self) -> str:
        return f'<Component {self._name}={self._version}>'

    # Deprecated methods
    def get_namespace(self) -> Optional[str]:
        """
        Get the namespace of this Component.

        Returns:
            Declared namespace of this Component as `str` if declared, else `None`.
        """
        warnings.warn('`Component.get_namespace()` is deprecated - use `Component.group`', DeprecationWarning)
        return self._group
