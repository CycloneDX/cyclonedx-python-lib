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
#

"""
Exceptions relating to specific conditions that occur when modelling CycloneDX BOM.
"""

from . import CycloneDxException


class CycloneDxModelException(CycloneDxException):
    """
    Base exception that covers all exceptions that may be thrown during model creation.
    """
    pass


class InvalidLocaleTypeException(CycloneDxModelException):
    """
    Raised when the supplied locale does not conform to ISO-639 specification.

    Good examples:
        - en
        - en-US
        - en-GB
        - fr
        - fr-CA

    The language code MUST be lowercase. If the country code is specified, the country code MUST be upper case.
    The language code and country code MUST be separated by a minus sign.
    """
    pass


class InvalidUriException(CycloneDxModelException):
    """
    Raised when a `str` is provided that needs to be a valid URI, but isn't.
    """
    pass


class MutuallyExclusivePropertiesException(CycloneDxModelException):
    """
    Raised when mutually exclusive properties are provided.
    """
    pass


class NoPropertiesProvidedException(CycloneDxModelException):
    """
    Raised when attempting to construct a model class and providing NO values (where all properites are defined as
    Optional, but at least one is required).

    """
    pass


class UnknownComponentDependencyException(CycloneDxModelException):
    """
    Exception raised when a dependency has been noted for a Component that is NOT a Component BomRef in this Bom.
    """


class UnknownHashTypeException(CycloneDxModelException):
    """
    Exception raised when we are unable to determine the type of hash from a composite hash string.
    """
    pass
