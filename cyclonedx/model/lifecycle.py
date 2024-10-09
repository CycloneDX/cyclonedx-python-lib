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
    See the CycloneDX Schema for lifecycles: https://cyclonedx.org/docs/1.5/#metadata_lifecycles
"""

from enum import Enum
from json import loads as json_loads
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union
from xml.etree.ElementTree import Element  # nosec B405

import serializable
from serializable.helpers import BaseHelper
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.serialization import CycloneDxDeserializationException

if TYPE_CHECKING:  # pragma: no cover
    from serializable import ViewType


@serializable.serializable_enum
class Phase(str, Enum):
    DESIGN = 'design'
    PREBUILD = 'pre-build'
    BUILD = 'build'
    POSTBUILD = 'post-build'
    OPERATIONS = 'operations'
    DISCOVERY = 'discovery'
    DECOMISSION = 'decommission'


@serializable.serializable_class
class PredefinedPhase:
    """
    Object that defines pre-defined phases in the product lifecycle.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.5/#metadata_lifecycles
    """

    def __init__(self, phase: Phase) -> None:
        self._phase = phase

    @property
    def phase(self) -> Phase:
        return self._phase

    @phase.setter
    def phase(self, phase: Phase) -> None:
        self._phase = phase

    def __hash__(self) -> int:
        return hash(self._phase)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PredefinedPhase):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, PredefinedPhase):
            return self._phase < other._phase
        if isinstance(other, CustomPhase):
            return True  # put PredefinedPhase before any CustomPhase
        return NotImplemented

    def __repr__(self) -> str:
        return f'<PredefinedPhase name={self._phase}>'


@serializable.serializable_class
class CustomPhase:
    def __init__(self, name: str, description: Optional[str] = None) -> None:
        self._name = name
        self._description = description

    @property
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def name(self) -> str:
        """
        Name of the lifecycle phase.

        Returns:
             `str`
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    @serializable.xml_sequence(2)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def description(self) -> Optional[str]:
        """
        Description of the lifecycle phase.

        Returns:
             `str`
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    def __hash__(self) -> int:
        return hash((self._name, self._description))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CustomPhase):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CustomPhase):
            return _ComparableTuple((self._name, self._description)) < _ComparableTuple(
                (other._name, other._description)
            )
        if isinstance(other, PredefinedPhase):
            return False  # put CustomPhase after any PredefinedPhase
        return NotImplemented

    def __repr__(self) -> str:
        return f'<CustomPhase name={self._name}>'


Lifecycle = Union[PredefinedPhase, CustomPhase]
"""TypeAlias for a union of supported lifecycle models.

- :class:`PredefinedPhase`
- :class:`CustomPhase`
"""

if TYPE_CHECKING:  # pragma: no cover
    # workaround for https://github.com/python/mypy/issues/5264
    # this code path is taken when static code analysis or documentation tools runs through.
    class LifecycleRepository(SortedSet[Lifecycle]):
        """Collection of :class:`Lifecycle`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        """

else:

    class LifecycleRepository(SortedSet):
        """Collection of :class:`Lifecycle`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        """


class _LifecycleRepositoryHelper(BaseHelper):
    @classmethod
    def json_normalize(cls, o: LifecycleRepository, *,
                       view: Optional[Type['ViewType']],
                       **__: Any) -> Any:
        if len(o) == 0:
            return None

        return [json_loads(li.as_json(  # type:ignore[union-attr]
            view_=view)) for li in o]

    @classmethod
    def json_denormalize(cls, o: List[Dict[str, Any]],
                         **__: Any) -> LifecycleRepository:
        repo = LifecycleRepository()
        for li in o:
            if 'phase' in li:
                repo.add(PredefinedPhase.from_json(li))  # type:ignore[attr-defined]
            elif 'name' in li:
                repo.add(CustomPhase.from_json(li))  # type:ignore[attr-defined]
            else:
                raise CycloneDxDeserializationException(f'unexpected: {li!r}')

        return repo

    @classmethod
    def xml_normalize(cls, o: LifecycleRepository, *,
                      element_name: str,
                      view: Optional[Type['ViewType']],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        if len(o) == 0:
            return None

        elem = Element(element_name)
        for li in o:
            elem.append(li.as_xml(  # type:ignore[union-attr]
                view_=view, as_string=False, element_name='lifecycle', xmlns=xmlns))

        return elem

    @classmethod
    def xml_denormalize(cls, o: Element,
                        default_ns: Optional[str],
                        **__: Any) -> LifecycleRepository:
        repo = LifecycleRepository()

        for li in o:
            tag = li.tag if default_ns is None else li.tag.replace(f'{{{default_ns}}}', '')

            if tag == 'lifecycle':
                stages = list(li)

                predefined_phase = next((el for el in stages if 'phase' in el.tag), None)
                custom_phase = next((el for el in stages if 'name' in el.tag), None)
                if predefined_phase is not None:
                    repo.add(PredefinedPhase.from_xml(li, default_ns))  # type:ignore[attr-defined]
                elif custom_phase is not None:
                    repo.add(CustomPhase.from_xml(li, default_ns))  # type:ignore[attr-defined]
            else:
                raise CycloneDxDeserializationException(f'unexpected: {li!r}')

        return repo
