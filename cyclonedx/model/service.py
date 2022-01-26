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

from . import ExternalReference, DataClassification, LicenseChoice, OrganizationalEntity, Property, XsUri  # , Signature
from .release_note import ReleaseNotes

"""
This set of classes represents the data that is possible about known Services.

.. note::
    See the CycloneDX Schema extension definition https://cyclonedx.org/docs/1.4/xml/#type_servicesType
"""


class Service:
    """
    Class that models the `service` complex type in the CycloneDX schema.

    .. note::
        See the CycloneDX schema: https://cyclonedx.org/docs/1.4/xml/#type_service
    """

<<<<<<< HEAD
    def __init__(self, name: str, bom_ref: Optional[str] = None, provider: Optional[OrganizationalEntity] = None,
                 group: Optional[str] = None, version: Optional[str] = None, description: Optional[str] = None,
                 endpoints: Optional[List[XsUri]] = None, authenticated: Optional[bool] = None,
                 x_trust_boundary: Optional[bool] = None, data: Optional[List[DataClassification]] = None,
=======
    def __init__(self, name: str, bom_ref: Optional[str] = None,
                 group: Optional[str] = None,
                 version: Optional[str] = None,
                 description: Optional[str] = None,
                 endpoints: Optional[List[str]] = None,
                 authenticated: Optional[bool] = None,
                 x_trust_boundary: Optional[bool] = None,
                 data: Optional[List[Data]] = None,
>>>>>>> cbebae2 (No default values for required fields)
                 licenses: Optional[List[LicenseChoice]] = None,
                 external_references: Optional[List[ExternalReference]] = None,
                 properties: Optional[List[Property]] = None,
                 # services: Optional[List[Service]] = None, -- I have no clue how to do this,
                 # commenting out so someone else can
                 release_notes: Optional[ReleaseNotes] = None,
                 ) -> None:
        self.bom_ref = bom_ref or str(uuid4())
        self.provider = provider
        self.group = group
        self.name = name
        self.version = version
        self.description = description
        self.endpoints = endpoints
        self.authenticated = authenticated
        self.x_trust_boundary = x_trust_boundary
        self.data = data
        self.licenses = licenses or []
        self.external_references = external_references or []
        # self.services = services -- no clue
        self.release_notes = release_notes
        self.properties = properties

    @property
    def bom_ref(self) -> Optional[str]:
        """
        An optional identifier which can be used to reference the service elsewhere in the BOM. Uniqueness is enforced
        within all elements and children of the root-level bom element.

        If a value was not provided in the constructor, a UUIDv4 will have been assigned.

        Returns:
           `str` unique identifier for this Service
        """
        return self._bom_ref

    @bom_ref.setter
    def bom_ref(self, bom_ref: Optional[str]) -> None:
        self._bom_ref = bom_ref

    @property
    def provider(self) -> Optional[OrganizationalEntity]:
        """
        Get the The organization that provides the service.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._provider

    @provider.setter
    def provider(self, provider: Optional[OrganizationalEntity]) -> None:
        self._provider = provider

    @property
    def group(self) -> Optional[str]:
        """
        The grouping name, namespace, or identifier. This will often be a shortened, single name of the company or
        project that produced the service or domain name. Whitespace and special characters should be avoided.

        Returns:
            `str` if provided else `None`
        """
        return self._group

    @group.setter
    def group(self, group: Optional[str]) -> None:
        self._group = group

    @property
    def name(self) -> str:
        """
        The name of the service. This will often be a shortened, single name of the service.

        Returns:
            `str`
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def version(self) -> Optional[str]:
        """
        The service version.

        Returns:
            `str` if set else `None`
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property
    def description(self) -> Optional[str]:
        """
        Specifies a description for the service.

        Returns:
            `str` if set else `None`
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    def endpoints(self) -> Optional[List[XsUri]]:
        """
        A list of endpoints URI's this service provides.

        Returns:
            List of `XsUri` else `None`
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints: Optional[List[XsUri]]) -> None:
        self._endpoints = endpoints

    def add_endpoint(self, endpoint: XsUri) -> None:
        """
        Add an endpoint URI for this Service.

        Args:
            endpoint:
                `XsUri` instance to add

        Returns:
            None
        """
        self.endpoints = (self._endpoints or []) + [endpoint]

    @property
    def authenticated(self) -> Optional[bool]:
        """
        A boolean value indicating if the service requires authentication. A value of true indicates the service
        requires authentication prior to use.

        A value of false indicates the service does not require authentication.

        Returns:
            `bool` if set else `None`
        """
        return self._authenticated

    @authenticated.setter
    def authenticated(self, authenticated: Optional[bool]) -> None:
        self._authenticated = authenticated

    @property
    def x_trust_boundary(self) -> Optional[bool]:
        """
        A boolean value indicating if use of the service crosses a trust zone or boundary. A value of true indicates
        that by using the service, a trust boundary is crossed.

        A value of false indicates that by using the service, a trust boundary is not crossed.

        Returns:
            `bool` if set else `None`
        """
        return self._x_trust_boundary

    @x_trust_boundary.setter
    def x_trust_boundary(self, x_trust_boundary: Optional[bool]) -> None:
        self._x_trust_boundary = x_trust_boundary

    @property
    def data(self) -> Optional[List[DataClassification]]:
        """
        Specifies the data classification.

        Returns:
            List of `DataClassificiation` or `None`
        """
        return self._data

    @data.setter
    def data(self, data: Optional[List[DataClassification]]) -> None:
        self._data = data

    @property
    def licenses(self) -> List[LicenseChoice]:
        """
        A optional list of statements about how this Service is licensed.

        Returns:
            List of `LicenseChoice` else `None`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: List[LicenseChoice]) -> None:
        self._licenses = licenses

    @property
    def external_references(self) -> List[ExternalReference]:
        """
        Provides the ability to document external references related to the Service.

        Returns:
            List of `ExternalReference`s
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: List[ExternalReference]) -> None:
        self._external_references = external_references

    def add_external_reference(self, reference: ExternalReference) -> None:
        """
        Add an `ExternalReference` to this `Service`.

        Args:
            reference:
                `ExternalReference` instance to add.
        """
        self.external_references = self._external_references + [reference]

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
