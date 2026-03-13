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

from abc import ABC
from typing import ClassVar, Optional
from warnings import warn

from . import SchemaVersion

__all__ = [
    'SchemaDeprecationWarning',
    'DeprecationWarning1Dot1',
    'DeprecationWarning1Dot2',
    'DeprecationWarning1Dot3',
    'DeprecationWarning1Dot4',
    'DeprecationWarning1Dot5',
    'DeprecationWarning1Dot6',
    'DeprecationWarning1Dot7',
]


class SchemaDeprecationWarning(DeprecationWarning, ABC):
    SCHEMA_VERSION: ClassVar[SchemaVersion]

    @classmethod
    def _warn(cls, deprecated: str, instead: Optional[str] = None,
              *, stacklevel: int = 1) -> None:
        """Internal API. Not part of the public interface."""
        msg = f'`{deprecated}` is deprecated from CycloneDX v{cls.SCHEMA_VERSION.to_version()} onwards.'
        if instead:
            msg += f' Please use `{instead}` instead.'
        warn(msg, cls, stacklevel=stacklevel + 1)


class DeprecationWarning1Dot7(SchemaDeprecationWarning):
    SCHEMA_VERSION = SchemaVersion.V1_7


class DeprecationWarning1Dot6(SchemaDeprecationWarning):
    SCHEMA_VERSION = SchemaVersion.V1_6


class DeprecationWarning1Dot5(SchemaDeprecationWarning):
    SCHEMA_VERSION = SchemaVersion.V1_5


class DeprecationWarning1Dot4(SchemaDeprecationWarning):
    SCHEMA_VERSION = SchemaVersion.V1_4


class DeprecationWarning1Dot3(SchemaDeprecationWarning):
    SCHEMA_VERSION = SchemaVersion.V1_3


class DeprecationWarning1Dot2(SchemaDeprecationWarning):
    _schema_version_enum = SchemaVersion.V1_2


class DeprecationWarning1Dot1(SchemaDeprecationWarning):
    _schema_version_enum = SchemaVersion.V1_1
