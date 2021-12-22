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


class InvalidLocaleTypeException(CycloneDxException):
    """
    Raised when the supplied locale does not conform to ISD-639 specification.

    Good examples:
        - en
        - en-US
        - en-GB
        - fr
        - fr-CA

    The language code MUST be lower case. If the country code is specified, the country code MUST be upper case.
    The language code and country code MUST be separated by a minus sign.
    """
    pass


class InvalidUriException(CycloneDxException):
    """
    Raised when a `str` is provided that needs to be a valid URI, but isn't.
    """
    pass
