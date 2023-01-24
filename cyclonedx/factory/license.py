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
# Copyright (c) OWASP Foundation. All Rights Reserved.

from typing import Optional

from ..exception.factory import InvalidLicenseExpressionException, InvalidSpdxLicenseException
from ..model import AttachedText, License, LicenseChoice, XsUri
from ..spdx import fixup_id as spdx_fixup, is_compound_expression as is_spdx_compound_expression


class LicenseFactory:
    """Factory for :class:`cyclonedx.model.License`."""

    @staticmethod
    def make_from_string(name_or_spdx: str, *,
                         license_text: Optional[AttachedText] = None,
                         license_url: Optional[XsUri] = None) -> License:
        """Make a :class:`cyclonedx.model.License` from a string."""
        try:
            return LicenseFactory.make_with_id(name_or_spdx, text=license_text, url=license_url)
        except InvalidSpdxLicenseException:
            return LicenseFactory.make_with_name(name_or_spdx, text=license_text, url=license_url)

    @staticmethod
    def make_with_id(spdx_id: str, *, text: Optional[AttachedText] = None, url: Optional[XsUri] = None) -> License:
        """Make a :class:`cyclonedx.model.License` from an SPDX-ID.

        :raises InvalidSpdxLicenseException: if `spdx_id` was not known/supported SPDX-ID
        """
        spdx_license_id = spdx_fixup(spdx_id)
        if spdx_license_id is None:
            raise InvalidSpdxLicenseException(spdx_id)
        return License(id_=spdx_license_id, text=text, url=url)

    @staticmethod
    def make_with_name(name: str, *, text: Optional[AttachedText] = None, url: Optional[XsUri] = None) -> License:
        """Make a :class:`cyclonedx.model.License` with a name."""
        return License(name=name, text=text, url=url)


class LicenseChoiceFactory:
    """Factory for :class:`cyclonedx.model.LicenseChoice`."""

    def __init__(self, *, license_factory: LicenseFactory) -> None:
        self.license_factory = license_factory

    def make_from_string(self, expression_or_name_or_spdx: str) -> LicenseChoice:
        """Make a :class:`cyclonedx.model.LicenseChoice` from a string."""
        try:
            return LicenseChoiceFactory.make_with_compound_expression(expression_or_name_or_spdx)
        except InvalidLicenseExpressionException:
            return self.make_with_license(expression_or_name_or_spdx)

    @staticmethod
    def make_with_compound_expression(compound_expression: str) -> LicenseChoice:
        """Make a :class:`cyclonedx.model.LicenseChoice` with a compound expression.

        Utilizes :func:`cyclonedx.spdx.is_compound_expression`.

        :raises InvalidLicenseExpressionException: if `expression` is not known/supported license expression
        """
        if is_spdx_compound_expression(compound_expression):
            return LicenseChoice(expression=compound_expression)
        raise InvalidLicenseExpressionException(compound_expression)

    def make_with_license(self, name_or_spdx: str, *,
                          license_text: Optional[AttachedText] = None,
                          license_url: Optional[XsUri] = None) -> LicenseChoice:
        """Make a :class:`cyclonedx.model.LicenseChoice` with a license (name or SPDX-ID)."""
        return LicenseChoice(license_=self.license_factory.make_from_string(
            name_or_spdx, license_text=license_text, license_url=license_url))
