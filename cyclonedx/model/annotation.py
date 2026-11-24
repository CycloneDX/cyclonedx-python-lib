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
from xml.etree.ElementTree import Element as XmlElement  # nosec B405

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
    def json_normalize(cls, o: Any, *,
                       view: Optional[type[serializable.ViewType]] = None,
                       **__: Any) -> Optional[list[str]]:
        if isinstance(o, (SortedSet, set, list)):
            return [str(i) for i in o]
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-subjects collection: {o!r}')

    @classmethod
    def json_denormalize(cls, o: Any, **__: Any) -> set[BomRef]:
        subjects: set[BomRef] = set()
        if isinstance(o, list):
            for v in o:
                subjects.add(BomRef(value=str(v)))
        return subjects

    @classmethod
    def xml_normalize(cls, o: Any, *,
                      element_name: str,
                      view: Optional[type[serializable.ViewType]] = None,
                      xmlns: Optional[str] = None,
                      **__: Any) -> Optional[XmlElement]:
        if not o:
            return None
        elem = XmlElement(element_name)
        ref_attr = f'{{{xmlns}}}ref' if xmlns else 'ref'
        for b in o:
            sub = XmlElement(f'{{{xmlns}}}subject' if xmlns else 'subject')
            sub.set(ref_attr, str(b))
            elem.append(sub)
        return elem

    @classmethod
    def xml_denormalize(cls, o: XmlElement, *,
                        default_ns: Optional[str] = None,
                        **__: Any) -> set[BomRef]:
        subjects: set[BomRef] = set()
        ns_map = {'bom': default_ns} if default_ns else None
        sub_elements = o.findall('bom:subject', ns_map) if ns_map else o.findall('subject')
        for child in sub_elements:
            ref_val = (child.get(f'{{{default_ns}}}ref') if default_ns else None) or child.get('ref')
            if ref_val:
                subjects.add(BomRef(value=ref_val))
        return subjects


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Annotator:
    """
    The organization, person, component, or service which created the textual content of the annotation.

    .. note::
        Exactly one of ``organization``, ``individual``, ``component``, or ``service`` must be provided.
        While properties can be modified independently after construction, having none or multiple
        set will produce schema-invalid output.
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
        return (
            f'<Annotator organization={self.organization!r}, '
            f'individual={self.individual!r}, '
            f'component={self.component!r}, '
            f'service={self.service!r}>'
        )


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Annotation:
    """
    A comment, note, explanation, or similar textual content which provides additional context
    to the object(s) being annotated.

    .. note::
        While CycloneDX schema does not enforce ``minItems`` for subjects, an annotation with no subjects
        is semantically meaningless and may produce invalid XML output.
    """

    def __init__(
        self, *,
        subjects: Iterable[Union[BomRef, str]],
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
    @serializable.xml_sequence(1)
    def subjects(self) -> 'SortedSet[BomRef]':
        """
        The object(s) in the BOM identified by its bom-ref.

        .. note::
            While CycloneDX schema does not enforce ``minItems`` for subjects, an annotation with no subjects
            is semantically meaningless and may produce invalid XML output.
        """
        return self._subjects

    @subjects.setter
    def subjects(self, subjects: Iterable[Union[BomRef, str]]) -> None:
        self._subjects = SortedSet(
            s if isinstance(s, BomRef) else BomRef(value=str(s))
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
