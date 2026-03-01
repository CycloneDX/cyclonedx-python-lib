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

"""
    This set of classes represents the lifecycles types in the CycloneDX standard.

.. note::
    Introduced in CycloneDX v1.5

.. note::
    See the CycloneDX Schema for lifecycles: https://cyclonedx.org/docs/1.7/xml/#metadata_lifecycles
"""

from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Union

import attrs
from sortedcontainers import SortedSet

from ..serialization import METADATA_KEY_XML_SEQUENCE


class LifecyclePhase(str, Enum):
    """
    Enum object that defines the permissible 'phase' for a Lifecycle according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_classification
    """
    DESIGN = 'design'
    PRE_BUILD = 'pre-build'
    BUILD = 'build'
    POST_BUILD = 'post-build'
    OPERATIONS = 'operations'
    DISCOVERY = 'discovery'
    DECOMMISSION = 'decommission'


@attrs.define
class PredefinedLifecycle:
    """
    Object that defines pre-defined phases in the product lifecycle.

    .. note::
        See the CycloneDX Schema definition:
        https://cyclonedx.org/docs/1.7/json/#tab-pane_metadata_lifecycles_items_oneOf_i0
    """
    phase: LifecyclePhase

    def __hash__(self) -> int:
        return hash(self.phase)

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, PredefinedLifecycle):
            return self.phase.value < other.phase.value
        if isinstance(other, NamedLifecycle):
            return True  # put PredefinedLifecycle before any NamedLifecycle
        return NotImplemented

    def __repr__(self) -> str:
        return f'<PredefinedLifecycle phase={self.phase}>'


@attrs.define
class NamedLifecycle:
    """
    Object that defines custom state in the product lifecycle.

    .. note::
        See the CycloneDX Schema definition:
        https://cyclonedx.org/docs/1.7/json/#tab-pane_metadata_lifecycles_items_oneOf_i1
    """
    name: str = attrs.field(
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    description: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )

    def __hash__(self) -> int:
        return hash((self.name, self.description))

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, NamedLifecycle):
            return (self.name, self._cmp(self.description)) < (other.name, self._cmp(other.description))
        if isinstance(other, PredefinedLifecycle):
            return False  # put NamedLifecycle after any PredefinedLifecycle
        return NotImplemented

    def __repr__(self) -> str:
        return f'<NamedLifecycle name={self.name}>'


Lifecycle = Union[PredefinedLifecycle, NamedLifecycle]
"""TypeAlias for a union of supported lifecycle models.

- :class:`PredefinedLifecycle`
- :class:`NamedLifecycle`
"""

if TYPE_CHECKING:  # pragma: no cover
    # workaround for https://github.com/python/mypy/issues/5264
    class LifecycleRepository(SortedSet[Lifecycle]):
        """Collection of :class:`Lifecycle`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        """
else:
    class LifecycleRepository(SortedSet):
        """Collection of :class:`Lifecycle`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        """
