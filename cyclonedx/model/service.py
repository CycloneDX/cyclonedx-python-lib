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

from typing import List, Optional
from uuid import uuid4

from ..exception.model import NoPropertiesProvidedException
from .release_note import ReleaseNotes
from . import ExternalReference, Data, Signature, LicenseChoice, Property

class Service:
    """
    Class that models the `vulnerabilityType` complex type in the CycloneDX schema (version >= 1.4).

    This class also provides data support for schema versions < 1.4 where Vulnerabilites were possible through a schema
    extension (in XML only).

    .. note::
        See the CycloneDX schema: https://cyclonedx.org/docs/1.4/#type_vulnerabilityType
    """

    def __init__(self, bom_ref: Optional[str] = None,
                 group: Optional[str] = None,
                 name: str = None,
                 version: Optional[str] = None,
                 description: Optional[str] = None,
                 endpoints: Optional[List[str]] = None,
                 authenticated: Optional[bool] = None,
                 x_trust_boundary: Optional[bool] = None,
                 data: Optional[List[Data]] = None,
                 licenses: Optional[List[LicenseChoice]] = None,
                 external_references: Optional[List[ExternalReference]] = None,
                 # services: Optional[List[Service]] = None, -- I have no clue how to do this, commenting out so someone else can
                 release_notes: Optional[ReleaseNotes] = None,
                 properties: Optional[List[Property]] = None,
                 signature: Optional[Signature] = None):
        if not name:
            raise NoPropertiesProvidedException(
                '`name` was not provideed - it must be provided.'
            )

        self.bom_ref = bom_ref or str(uuid4())
        self.group = group
        self.name = name
        self.version = version
        self.description = description
        self.endpoints = endpoints
        self.authenticated = authenticated
        self.x_trust_boundary = x_trust_boundary
        self.data = data
        self.licenses = licenses
        self.external_references = external_references
        # self.services = services -- no clue
        self.release_notes = release_notes
        self.properties = properties
        self.signature = signature
    
    @property
    def bom_ref(self) -> Optional[str]:
        """
        Get the unique reference for this Service in this BOM.

        If a value was not provided in the constructor, a UUIDv4 will have been assigned.

        Returns:
           `str` unique identifier for this Service
        """
        return self._bom_ref

    @bom_ref.setter
    def bom_ref(self, bom_ref: Optional[str]) -> None:
        self._bom_ref = bom_ref

    @property
    def group(self) -> Optional[str]:
        """
        A group of the service as provided by the source.
        """
        return self._group

    @group.setter
    def group(self, group: Optional[str]) -> None:
        self._group = group

    @property
    def name(self) -> str:
        """
        A name of the service as provided by the source.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def version(self) -> Optional[str]:
        """
        A version of the service as provided by the source.
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property
    def description(self) -> Optional[str]:
        """
        A description of the service as provided by the source.
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    def endpoints(self) -> Optional[List[str]]:
        """
        A list of endpoints for the service as provided by the source.
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints: Optional[List[str]]) -> None:
        self._endpoints = endpoints

    @property
    def authenticated(self) -> Optional[bool]:
        """
        A True/False or None value of if the service requires authentication as provided by the source.
        """
        return self._authenticated

    @authenticated.setter
    def authenticated(self, authenticated: Optional[bool]) -> None:
        self._authenticated = authenticated

    @property
    def x_trust_boundary(self) -> Optional[bool]:
        """
        A True/False or None value of if the service has a X-Trust-Boundary as provided by the source.
        """
        return self._x_trust_boundary

    @x_trust_boundary.setter
    def x_trust_boundary(self, x_trust_boundary: Optional[bool]) -> None:
        self._x_trust_boundary = x_trust_boundary

    @property
    def data(self) -> Optional[List[Data]]:
        """
        A list of data information for the service as provided by the source.
        """
        return self._data

    @data.setter
    def data(self, data: Optional[List[Data]]) -> None:
        self._data = data

    @property
    def licenses(self) -> Optional[List[LicenseChoice]]:
        """
        A list of licenses for the service as provided by the source.
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Optional[List[LicenseChoice]]) -> None:
        self._licenses = licenses

    @property
    def external_references(self) -> Optional[List[ExternalReference]]:
        """
        A list of externalReferences for the service as provided by the source.
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Optional[List[ExternalReference]]) -> None:
        self._external_references = external_references

    @property
    def release_notes(self) -> Optional[ReleaseNotes]:
        """
        A release note for the service as provided by the source.
        """
        return self._release_notes

    @release_notes.setter
    def release_notes(self, release_notes: Optional[ReleaseNotes]) -> None:
        self._release_notes = release_notes

    @property
    def properties(self) -> Optional[List[Property]]:
        """
        A list of properties for the service as provided by the source.
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Optional[List[Property]]) -> None:
        self._properties = properties

    @property
    def signature(self) -> Optional[Signature]:
        """
        A JSF signature for the service as provided by the source.
        """
        return self._signature

    @signature.setter
    def signature(self, signature: Optional[Signature]) -> None:
        self._signature = signature
