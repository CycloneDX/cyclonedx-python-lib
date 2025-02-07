# This file is part of CycloneDX Python Library
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


__all__ = [
    'is_supported_id', 'fixup_id',
    'is_simple_expression', 'is_compound_expression', 'is_spdx_license_id', 'is_spdx_expression'
]

from typing import TYPE_CHECKING, Dict, Optional, Set

from boolean.boolean import Expression  # type:ignore[import-untyped]
from license_expression import (  # type:ignore[import-untyped]
    AND,
    OR,
    ExpressionError,
    LicenseSymbol,
    LicenseWithExceptionSymbol,
    get_license_index,
    get_spdx_licensing,
)

if TYPE_CHECKING:  # pragma: no cover
    from license_expression import Licensing

# region init
# python's internal module loader will assure that this init-part runs only once.

__SPDX_EXPRESSION_LICENSING: 'Licensing' = get_spdx_licensing()
__KNOWN_IDS = ([entry['spdx_license_key'] for entry in get_license_index()
               if entry['spdx_license_key'] and not entry['is_exception']]
               + [item for license_entry in get_license_index()
                  for item in license_entry['other_spdx_license_keys'] if not license_entry['is_exception']])
__IDS: Set[str] = set(__KNOWN_IDS)
__IDS_LOWER_MAP: Dict[str, str] = {**{entry['spdx_license_key'].lower(): entry['spdx_license_key']
                                      for entry in get_license_index()
                                      if entry['spdx_license_key'] and not entry['is_exception']},
                                   **{item.lower(): item for license_entry in get_license_index()
                                      for item in license_entry['other_spdx_license_keys']
                                      if not license_entry['is_exception']}}

# endregion


def is_supported_id(value: str) -> bool:
    """Validate an SPDX-ID according to current spec."""
    return value in __IDS


def fixup_id(value: str) -> Optional[str]:
    """Fixup an SPDX-ID.

    :returns: repaired value string, or `None` if fixup was unable to help.
    """
    return __IDS_LOWER_MAP.get(value.lower())


def is_simple_expression(value: str, validate: bool = False) -> bool:
    """Indicates an SPDX simple expression (SPDX license identifier or license ref).

        .. note::
        Utilizes `license-expression library`_ to
        validate SPDX simple expression according to `SPDX license expression spec`_.
        DocumentRef- references are not in scope for CycloneDX.

    .. _SPDX license expression spec: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
    .. _license-expression library: https://github.com/nexB/license-expression
    """
    if not value:
        return False
    try:
        expression = __SPDX_EXPRESSION_LICENSING.parse(value, strict=True, validate=validate)
    except (NameError, ExpressionError):
        return False
    if type(expression) in [OR, AND]:
        return False
    if str(expression).startswith('LicenseRef-'):
        # It is a custom license ref
        return True
    # It should be an official SPDX license identifier
    result = __SPDX_EXPRESSION_LICENSING.validate(value, strict=True)
    if result.errors:
        # The value was not understood
        return False
    if result.original_expression == result.normalized_expression:
        # The given value is identical to normalized, so it is a valid identifier
        return True
    if result.original_expression.upper() != result.normalized_expression.upper():
        # It is not a capitalization issue, ID was normalized to another valid ID, so it is OK.
        return True
    return False


def is_compound_expression(value: str) -> bool:
    """Indicates whether value is an SPDX compound expression.

    .. note::
        Utilizes `license-expression library`_ to
        validate SPDX compound expression according to `SPDX license expression spec`_.
        DocumentRef- references are not in scope for CycloneDX.

    .. _SPDX license expression spec: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
    .. _license-expression library: https://github.com/nexB/license-expression
    """
    def is_valid_item(expression: Expression) -> bool:
        if type(expression) in [OR, AND]:
            for item in expression.args:
                if not is_valid_item(item):
                    return False
            return True
        elif type(expression) in [LicenseSymbol, LicenseWithExceptionSymbol]:
            return is_simple_expression(str(expression))
        return False

    if not value:
        return False
    try:
        parsed_expression = __SPDX_EXPRESSION_LICENSING.parse(value)
        if type(parsed_expression) in [OR, AND] or isinstance(parsed_expression, LicenseWithExceptionSymbol):
            return is_valid_item(parsed_expression)
        else:
            return False
    except (NameError, ExpressionError):
        return False


def is_spdx_license_id(value: str) -> bool:
    """Indicates whether value is an SPDX license identifier from official list.

        .. note::
        Utilizes `license-expression library`_ to
        validate SPDX compound expression according to `SPDX license expression spec`_.
        DocumentRef- references are not in scope for CycloneDX.

    .. _SPDX license expression spec: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
    .. _license-expression library: https://github.com/nexB/license-expression
    """
    return is_simple_expression(value, validate=True) and not value.startswith('LicenseRef-')


def is_spdx_expression(value: str) -> bool:
    """Indicates whether value is an SPDX simple or compound expression.

        .. note::
        Utilizes `license-expression library`_ to
        validate SPDX compound expression according to `SPDX license expression spec`_.
        DocumentRef- references are not in scope for CycloneDX.

    .. _SPDX license expression spec: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
    .. _license-expression library: https://github.com/nexB/license-expression
    """
    return is_simple_expression(value) or is_compound_expression(value)
