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
Exceptions relating to specific conditions that occur when factoring a model.
"""

from . import CycloneDxException


class CycloneDxFactoryException(CycloneDxException):
    """
    Base exception that covers all exceptions that may be thrown during model factoring..
    """
    pass


class LicenseChoiceFactoryException(CycloneDxFactoryException):
    """
    Base exception that covers all LicenseChoiceFactory exceptions.
    """
    pass


class InvalidSpdxLicenseException(LicenseChoiceFactoryException):
    """
    Thrown when an invalid SPDX License is provided.
    """
    pass


class LicenseFactoryException(CycloneDxFactoryException):
    """
    Base exception that covers all LicenseFactory exceptions.
    """
    pass


class InvalidLicenseExpressionException(LicenseFactoryException):
    """
    Thrown when an invalid License expressions is provided.
    """
    pass
