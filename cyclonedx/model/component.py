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

from enum import Enum
from os.path import exists
from typing import List, Optional

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore

from . import ExternalReference, HashAlgorithm, HashType, sha1sum
from .vulnerability import Vulnerability


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

    def __init__(self, name: str, version: str, namespace: Optional[str] = None, qualifiers: Optional[str] = None,
                 subpath: Optional[str] = None, hashes: Optional[List[HashType]] = None, author: Optional[str] = None,
                 description: Optional[str] = None, license_str: Optional[str] = None,
                 component_type: ComponentType = ComponentType.LIBRARY, package_url_type: str = 'pypi') -> None:
        self._package_url_type: str = package_url_type
        self._namespace: Optional[str] = namespace
        self._name: str = name
        self._version: str = version
        self._type: ComponentType = component_type
        self._qualifiers: Optional[str] = qualifiers
        self._subpath: Optional[str] = subpath

        self._author: Optional[str] = author
        self._description: Optional[str] = description
        self._license: Optional[str] = license_str

        self._hashes: List[HashType] = hashes if hashes else []
        self._vulnerabilites: List[Vulnerability] = []
        self._external_references: List[ExternalReference] = []

    def add_external_reference(self, reference: ExternalReference) -> None:
        """
        Add an `ExternalReference` to this `Component`.

        Args:
            reference:
                `ExternalReference` instance to add.
        """
        self._external_references.append(reference)

    def add_hash(self, a_hash: HashType) -> None:
        """
        Adds a hash that pins/identifies this Component.

        Args:
            a_hash:
                `HashType` instance
        """
        self._hashes.append(a_hash)

    def add_vulnerability(self, vulnerability: Vulnerability) -> None:
        """
        Add a Vulnerability to this Component.

        Args:
            vulnerability:
                `cyclonedx.model.vulnerability.Vulnerability` instance to add to this Component.

        Returns:
            None
        """
        self._vulnerabilites.append(vulnerability)

    def get_author(self) -> Optional[str]:
        """
        Get the author of this Component.

        Returns:
            Declared author of this Component as `str` if set, else `None`.
        """
        return self._author

    def get_description(self) -> Optional[str]:
        """
        Get the description of this Component.

        Returns:
            Declared description of this Component as `str` if set, else `None`.
        """
        return self._description

    def get_external_references(self) -> List[ExternalReference]:
        """
        List of external references for this Component.

        Returns:
            `List` of `ExternalReference` objects where there are any, else an empty `List`.
        """
        return self._external_references

    def get_hashes(self) -> List[HashType]:
        """
        List of cryptographic hashes that identify this Component.

        Returns:
            `List` of `HashType` objects where there are any hashes, else an empty `List`.
        """
        return self._hashes

    def get_license(self) -> Optional[str]:
        """
        Get the license of this Component.

        Returns:
            Declared license of this Component as `str` if set, else `None`.
        """
        return self._license

    def get_name(self) -> str:
        """
        Get the name of this Component.

        Returns:
            Declared name of this Component as `str`.
        """
        return self._name

    def get_namespace(self) -> Optional[str]:
        """
        Get the namespace of this Component.

        Returns:
            Declared namespace of this Component as `str` if declared, else `None`.
        """
        return self._namespace

    def get_purl(self) -> str:
        """
        Get the PURL for this Component.

        Returns:
            PackageURL or 'PURL' that reflects this Component as `str`.
        """
        return str(self.to_package_url().to_string())

    def get_pypi_url(self) -> str:
        return f'https://pypi.org/project/{self.get_name()}/{self.get_version()}'

    def get_subpath(self) -> Optional[str]:
        """
        Get the subpath of this Component.

        Returns:
            Declared subpath of this Component as `str` if declared, else `None`.
        """
        return self._subpath

    def get_type(self) -> ComponentType:
        """
        Get the type of this Component.

        Returns:
            Declared type of this Component as `ComponentType`.
        """
        return self._type

    def get_version(self) -> str:
        """
        Get the version of this Component.

        Returns:
            Declared version of this Component as `str`.
        """
        return self._version

    def get_vulnerabilities(self) -> List[Vulnerability]:
        """
        Get all the Vulnerabilities for this Component.

        Returns:
             List of `Vulnerability` objects assigned to this Component.
        """
        return self._vulnerabilites

    def has_vulnerabilities(self) -> bool:
        """
        Does this Component have any vulnerabilities?

        Returns:
             `True` if this Component has 1 or more vulnerabilities, `False` otherwise.
        """
        return bool(self.get_vulnerabilities())

    def set_author(self, author: str) -> None:
        """
        Set the author of this Component.

        Args:
            author:
                `str` to set the author to

        Returns:
            None
        """
        self._author = author

    def set_description(self, description: str) -> None:
        """
        Set the description of this Component.

        Args:
            description:
                `str` to set the description to

        Returns:
            None
        """
        self._description = description

    def set_license(self, license_str: str) -> None:
        """
        Set the license for this Component.

        Args:
            license_str:
                `str` to set the license to

        Returns:
            None
        """
        self._license = license_str

    def to_package_url(self) -> PackageURL:
        """
        Return a PackageURL representation of this Component.

        Returns:
            `packageurl.PackageURL` instance which represents this Component.
        """""
        return PackageURL(
            type=self._package_url_type,
            namespace=self._namespace,
            name=self._name,
            version=self._version,
            qualifiers=self._qualifiers,
            subpath=self._subpath
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Component):
            return other.get_purl() == self.get_purl()
        else:
            raise NotImplementedError

    def __repr__(self) -> str:
        return f'<Component {self._name}={self._version}>'
