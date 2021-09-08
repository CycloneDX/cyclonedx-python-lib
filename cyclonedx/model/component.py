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

PURL_TYPE_PREFIX = 'pypi'


class ComponentType(Enum):
    """
    Enum object that defines the permissible 'types' for a Component according to the CycloneDX
    schemas.
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
    An object that mirrors the Component type in the CycloneDX schema.
    """
    _type: ComponentType
    _name: str
    _version: str
    _qualifiers: str

    _author: str = None
    _description: str = None
    _license: str = None

    def __init__(self, name: str, version: str, qualifiers: str = None,
                 component_type: ComponentType = ComponentType.LIBRARY):
        self._name = name
        self._version = version
        self._type = component_type
        self._qualifiers = qualifiers

    def get_author(self) -> str:
        return self._author

    def get_description(self) -> str:
        return self._description

    def get_license(self) -> str:
        return self._license

    def get_name(self) -> str:
        return self._name

    def get_purl(self) -> str:
        base_purl = 'pkg:{}/{}@{}'.format(PURL_TYPE_PREFIX, self._name, self._version)
        if self._qualifiers:
            base_purl = '{}?{}'.format(base_purl, self._qualifiers)
        return base_purl

    def get_type(self) -> ComponentType:
        return self._type

    def get_version(self) -> str:
        return self._version

    def set_author(self, author: str):
        self._author = author

    def set_description(self, description: str):
        self._description = description

    def set_license(self, license_str: str):
        self._license = license_str

    def __eq__(self, other):
        return other.get_purl() == self.get_purl()

    def __repr__(self):
        return '<Component {}={}>'.format(self._name, self._version)
