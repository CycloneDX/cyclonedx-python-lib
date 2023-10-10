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

from typing import TYPE_CHECKING, Optional

from ..exception.factory import InvalidLicenseExpressionException, InvalidSpdxLicenseException
from ..model.license import DisjunctiveLicense, LicenseExpression
from ..spdx import fixup_id as spdx_fixup, is_compound_expression as is_spdx_compound_expression

if TYPE_CHECKING:  # pragma: no cover
    from ..model import AttachedText, XsUri
    from ..model.license import License


class LicenseFactory:
    """Factory for :class:`cyclonedx.model.license.License`."""

    def make_from_string(self, value: str, *,
                         license_text: Optional['AttachedText'] = None,
                         license_url: Optional['XsUri'] = None) -> 'License':
        """Make a :class:`cyclonedx.model.license.License` from a string."""
        try:
            return self.make_with_id(value, text=license_text, url=license_url)
        except InvalidSpdxLicenseException:
            pass
        try:
            return self.make_with_expression(value)
        except InvalidLicenseExpressionException:
            pass
        return self.make_with_name(value, text=license_text, url=license_url)

    def make_with_expression(self, expression: str) -> LicenseExpression:
        """Make a :class:`cyclonedx.model.license.LicenseExpression` with a compound expression.

        Utilizes :func:`cyclonedx.spdx.is_compound_expression`.

        :raises InvalidLicenseExpressionException: if param `value` is not known/supported license expression
        """
        if is_spdx_compound_expression(expression):
            return LicenseExpression(expression)
        raise InvalidLicenseExpressionException(expression)

    def make_with_id(self, spdx_id: str, *,
                     text: Optional['AttachedText'] = None,
                     url: Optional['XsUri'] = None) -> DisjunctiveLicense:
        """Make a :class:`cyclonedx.model.license.DisjunctiveLicense` from an SPDX-ID.

        :raises InvalidSpdxLicenseException: if param `spdx_id` was not known/supported SPDX-ID
        """
        spdx_license_id = spdx_fixup(spdx_id)
        if spdx_license_id is None:
            raise InvalidSpdxLicenseException(spdx_id)
        return DisjunctiveLicense(id=spdx_license_id, text=text, url=url)

    def make_with_name(self, name: str, *,
                       text: Optional['AttachedText'] = None,
                       url: Optional['XsUri'] = None) -> DisjunctiveLicense:
        """Make a :class:`cyclonedx.model.license.DisjunctiveLicense` with a name."""
        return DisjunctiveLicense(name=name, text=text, url=url)
