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

from collections.abc import Iterable
from datetime import datetime
from typing import Any, Optional, Union

import py_serializable as serializable
from py_serializable.helpers import XsdDateTime
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.serialization import SerializationOfUnexpectedValueException
from .bom_ref import BomRef
from .component import Component
from .contact import OrganizationalContact, OrganizationalEntity
from .service import Service


class _SubjectsSerializationHelper(serializable.helpers.BaseHelper):
    """THIS CLASS IS NON-PUBLIC API

    JSON: subjects is a plain list of bom-ref strings.
    XML:  subjects wrapper element containing <subject ref="..."/> children.
    """

    @classmethod
    def serialize(cls, o: Any) -> list[str]:
        if isinstance(o, (SortedSet, set, list)):
            return [str(i) for i in o]
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-subjects collection: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> 'set[_AnnotationSubject]':
        subjects: set[_AnnotationSubject] = set()
        if isinstance(o, list):
            for v in o:
                subjects.add(_AnnotationSubject(ref=BomRef(value=str(v))))
        return subjects

    @classmethod
    def xml_denormalize(cls, o: Any, *,
                        default_ns: Any,
                        prop_info: Any,
                        ctx: Any,
                        **kwargs: Any) -> set['_AnnotationSubject']:
        subjects: set[_AnnotationSubject] = set()
        if o is None:
            return subjects
        for child in o:
            ref_val = child.get('ref')
            if ref_val:
                subjects.add(_AnnotationSubject(ref=BomRef(value=ref_val)))
        return subjects


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class _AnnotationSubject:
    """THIS CLASS IS NON-PUBLIC API

    Wrapper that renders as ``<subject ref="..."/>`` in XML.
    """

    def __init__(self, ref: BomRef) -> None:
        self._ref = ref

    @property
    @serializable.type_mapping(BomRef)
    @serializable.xml_attribute()
    def ref(self) -> BomRef:
        return self._ref

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _AnnotationSubject):
            return self._ref == other._ref
        return False

    def __hash__(self) -> int:
        return hash(self._ref)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, _AnnotationSubject):
            return str(self._ref) < str(other._ref)
        return NotImplemented

    def __str__(self) -> str:
        return str(self._ref)


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Annotator:
    """
    The organization, person, component, or service which created the textual content of the annotation.
    """

    def __init__(
        self, *,
        organization: Optional[OrganizationalEntity] = None,
        individual: Optional[OrganizationalContact] = None,
        component: Optional[Component] = None,
        service: Optional[Service] = None,
    ) -> None:
        if sum(x is not None for x in (organization, individual, component, service)) != 1:
            raise ValueError('Exactly one of organization, individual, component, or service must be provided.')

        self.organization = organization
        self.individual = individual
        self.component = component
        self.service = service

    @property
    @serializable.xml_sequence(1)
    def organization(self) -> Optional[OrganizationalEntity]:
        return self._organization

    @organization.setter
    def organization(self, organization: Optional[OrganizationalEntity]) -> None:
        self._organization = organization

    @property
    @serializable.xml_sequence(2)
    def individual(self) -> Optional[OrganizationalContact]:
        return self._individual

    @individual.setter
    def individual(self, individual: Optional[OrganizationalContact]) -> None:
        self._individual = individual

    @property
    @serializable.xml_sequence(3)
    def component(self) -> Optional[Component]:
        return self._component

    @component.setter
    def component(self, component: Optional[Component]) -> None:
        self._component = component

    @property
    @serializable.xml_sequence(4)
    def service(self) -> Optional[Service]:
        return self._service

    @service.setter
    def service(self, service: Optional[Service]) -> None:
        self._service = service

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.organization, self.individual, self.component, self.service
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Annotator):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Annotator):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Annotator id={id(self)}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Annotation:
    """
    A comment, note, explanation, or similar textual content which provides additional context
    to the object(s) being annotated.
    """

    def __init__(
        self, *,
        subjects: Iterable[BomRef],
        annotator: Annotator,
        timestamp: datetime,
        text: str,
        bom_ref: Optional[Union[str, BomRef]] = None,
    ) -> None:
        self._bom_ref = _bom_ref_from_str(bom_ref)
        self.subjects = subjects
        self.annotator = annotator
        self.timestamp = timestamp
        self.text = text

    @property
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRef)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> BomRef:
        """
        An optional identifier which can be used to reference the annotation elsewhere in the BOM.
        """
        return self._bom_ref

    @bom_ref.setter
    def bom_ref(self, bom_ref: BomRef) -> None:
        self._bom_ref = bom_ref

    @property
    @serializable.type_mapping(_SubjectsSerializationHelper)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'subject')
    @serializable.xml_sequence(1)
    def subjects(self) -> 'SortedSet[_AnnotationSubject]':
        """
        The object in the BOM identified by its bom-ref.
        """
        return self._subjects

    @subjects.setter
    def subjects(self, subjects: Iterable[Union[BomRef, '_AnnotationSubject']]) -> None:
        self._subjects = SortedSet(
            s if isinstance(s, _AnnotationSubject) else _AnnotationSubject(ref=s)
            for s in subjects
        )

    @property
    @serializable.xml_sequence(2)
    def annotator(self) -> Annotator:
        """
        The organization, person, component, or service which created the textual content of the annotation.
        """
        return self._annotator

    @annotator.setter
    def annotator(self, annotator: Annotator) -> None:
        self._annotator = annotator

    @property
    @serializable.type_mapping(XsdDateTime)
    @serializable.xml_sequence(3)
    def timestamp(self) -> datetime:
        """
        The date and time (timestamp) when the annotation was created.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime) -> None:
        self._timestamp = timestamp

    @property
    @serializable.xml_sequence(4)
    def text(self) -> str:
        """
        The textual content of the annotation.
        """
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.bom_ref.value, _ComparableTuple(self.subjects),
            self.annotator, self.timestamp, self.text
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Annotation):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Annotation):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Annotation bom-ref={self.bom_ref.value}>'
