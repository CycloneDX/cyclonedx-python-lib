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

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from ..serialization import ALL_VERSIONS, VERSIONS_1_1_AND_LATER
from ..schema import SchemaVersion
from .release_note import ReleaseNotes
from .license import License, LicenseRepository
from .issue import IssueType
from .dependency import Dependable
from .crypto import CryptoProperties
from .contact import OrganizationalContact, OrganizationalEntity
from .component_evidence import ComponentEvidence
from .bom_ref import BomRef
from . import AttachedText, ExternalReference, HashAlgorithm, HashType, IdentifiableAction, Property, XsUri
from ..serialization import (
    METADATA_KEY_INCLUDE_NONE,
    METADATA_KEY_JSON_NAME,
    METADATA_KEY_VERSIONS,
    METADATA_KEY_XML_ATTR,
    METADATA_KEY_XML_NAME,
    METADATA_KEY_XML_SEQUENCE,
    VERSIONS_1_0_THROUGH_1_3,
    VERSIONS_1_1_AND_LATER,
    VERSIONS_1_2_AND_LATER,
    VERSIONS_1_3_AND_LATER,
    VERSIONS_1_4_AND_LATER,
    VERSIONS_1_6_AND_LATER,
)
from ..exception.serialization import CycloneDxDeserializationException, SerializationOfUnexpectedValueException
from ..exception.model import InvalidOmniBorIdException, InvalidSwhidException
from .._internal.compare import ComparablePackageURL as _ComparablePackageURL
import re
import sys
from collections.abc import Iterable
from enum import Enum
from typing import Any, Optional, Union
from warnings import warn

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

import attrs
from packageurl import PackageURL
from sortedcontainers import SortedSet


def _sortedset_converter(value: Any) -> SortedSet:
    """Converter to ensure values are always SortedSet."""
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
        return SortedSet(value)
    return SortedSet([value])


def _bom_ref_converter(value: Optional[Union[str, BomRef]]) -> BomRef:
    """Convert string or BomRef to BomRef."""
    return _bom_ref_from_str(value)


def _sortedset_factory() -> SortedSet:
    return SortedSet()


def _license_repository_factory() -> LicenseRepository:
    return LicenseRepository()


def _license_repository_converter(value: Any) -> LicenseRepository:
    if value is None:
        return LicenseRepository()
    if isinstance(value, LicenseRepository):
        return value
    # Convert generators, lists, etc. to LicenseRepository
    return LicenseRepository(value)


@attrs.define
class Commit:
    """
    Our internal representation of the `commitType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_commitType
    """
    uid: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    url: Optional[XsUri] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    author: Optional[IdentifiableAction] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )
    committer: Optional[IdentifiableAction] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    message: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 5}
    )

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Commit):
            c = self._cmp
            return (c(self.uid), c(self.url), c(self.author), c(self.committer), c(self.message)) < (
                c(other.uid), c(other.url), c(other.author), c(other.committer), c(other.message))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.uid, self.url, self.author, self.committer, self.message))

    def __repr__(self) -> str:
        return f'<Commit uid={self.uid}, url={self.url}, message={self.message}>'


class ComponentScope(str, Enum):
    """
    Enum object that defines the permissable 'scopes' for a Component according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_scope
    """
    REQUIRED = 'required'
    OPTIONAL = 'optional'
    EXCLUDED = 'excluded'  # Only supported in >= 1.1


# Component scope support by schema version
COMPONENT_SCOPE_VERSIONS: dict[ComponentScope, set[SchemaVersion]] = {
    ComponentScope.REQUIRED: ALL_VERSIONS,
    ComponentScope.OPTIONAL: ALL_VERSIONS,
    ComponentScope.EXCLUDED: VERSIONS_1_1_AND_LATER,
}


class ComponentType(str, Enum):
    """
    Enum object that defines the permissible 'types' for a Component according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_classification
    """
    APPLICATION = 'application'
    CONTAINER = 'container'  # Only supported in >= 1.2
    CRYPTOGRAPHIC_ASSET = 'cryptographic-asset'  # Only supported in >= 1.6
    DATA = 'data'  # Only supported in >= 1.5
    DEVICE = 'device'
    DEVICE_DRIVER = 'device-driver'  # Only supported in >= 1.5
    FILE = 'file'  # Only supported in >= 1.1
    FIRMWARE = 'firmware'  # Only supported in >= 1.2
    FRAMEWORK = 'framework'
    LIBRARY = 'library'
    MACHINE_LEARNING_MODEL = 'machine-learning-model'  # Only supported in >= 1.5
    OPERATING_SYSTEM = 'operating-system'
    PLATFORM = 'platform'  # Only supported in >= 1.5


@attrs.define
class Diff:
    """
    Our internal representation of the `diffType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_diffType
    """
    text: Optional[AttachedText] = attrs.field(default=None)
    url: Optional[XsUri] = attrs.field(default=None)

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Diff):
            return (self._cmp(self.url), self._cmp(self.text)) < (self._cmp(other.url), self._cmp(other.text))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.url, self.text))

    def __repr__(self) -> str:
        return f'<Diff url={self.url}>'


class PatchClassification(str, Enum):
    """
    Enum object that defines the permissible `patchClassification`s.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_patchClassification
    """
    BACKPORT = 'backport'
    CHERRY_PICK = 'cherry-pick'
    MONKEY = 'monkey'
    UNOFFICIAL = 'unofficial'


@attrs.define
class Patch:
    """
    Our internal representation of the `patchType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_patchType
    """
    type: PatchClassification = attrs.field(
        metadata={METADATA_KEY_XML_ATTR: True}
    )
    diff: Optional[Diff] = attrs.field(default=None)
    resolves: 'SortedSet[IssueType]' = attrs.field(factory=_sortedset_factory, converter=_sortedset_converter)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Patch):
            return (self.type, self.diff, tuple(self.resolves)) == (
                other.type, other.diff, tuple(other.resolves))
        return NotImplemented

    @staticmethod
    def _cmp_patch(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Patch):
            c = self._cmp_patch
            return (self.type, c(self.diff), tuple(self.resolves)) < (
                other.type, c(other.diff), tuple(other.resolves))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.type, self.diff, tuple(self.resolves)))

    def __repr__(self) -> str:
        return f'<Patch type={self.type}, id={id(self)}>'


@attrs.define
class Pedigree:
    """
    Our internal representation of the `pedigreeType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_pedigreeType
    """
    ancestors: 'SortedSet[Component]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    descendants: 'SortedSet[Component]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    variants: 'SortedSet[Component]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )
    commits: 'SortedSet[Commit]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    patches: 'SortedSet[Patch]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_2_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 5,
        }
    )
    notes: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 6}
    )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Pedigree):
            return (
                tuple(self.ancestors), tuple(self.descendants), tuple(self.variants),
                tuple(self.commits), tuple(self.patches), self.notes
            ) < (
                tuple(other.ancestors), tuple(other.descendants), tuple(other.variants),
                tuple(other.commits), tuple(other.patches), other.notes
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            tuple(self.ancestors), tuple(self.descendants), tuple(self.variants),
            tuple(self.commits), tuple(self.patches), self.notes
        ))

    def __repr__(self) -> str:
        return f'<Pedigree id={id(self)}, hash={hash(self)}>'


@attrs.define
class Swid:
    """
    Our internal representation of the `swidType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_swidType
    """
    tag_id: str = attrs.field(metadata={METADATA_KEY_JSON_NAME: 'tagId', METADATA_KEY_XML_ATTR: True})
    name: str = attrs.field(metadata={METADATA_KEY_XML_ATTR: True})
    version: Optional[str] = attrs.field(default=None, metadata={METADATA_KEY_XML_ATTR: True})
    tag_version: Optional[int] = attrs.field(
        default=None, metadata={METADATA_KEY_JSON_NAME: 'tagVersion', METADATA_KEY_XML_ATTR: True})
    patch: Optional[bool] = attrs.field(default=None, metadata={METADATA_KEY_XML_ATTR: True})
    text: Optional[AttachedText] = attrs.field(default=None)
    url: Optional[XsUri] = attrs.field(default=None)

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Swid):
            c = self._cmp
            return (
                self.tag_id, self.name, c(self.version), c(self.tag_version),
                c(self.patch), c(self.url), c(self.text)
            ) < (
                other.tag_id, other.name, c(other.version), c(other.tag_version),
                c(other.patch), c(other.url), c(other.text)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.tag_id, self.name, self.version, self.tag_version,
            self.patch, self.url, self.text
        ))

    def __repr__(self) -> str:
        return f'<Swid tagId={self.tag_id}, name={self.name}, version={self.version}>'


class OmniborId:
    """
    Helper class that allows us to perform validation on data strings that must conform to
    https://www.iana.org/assignments/uri-schemes/prov/gitoid.
    """

    _VALID_OMNIBOR_ID_REGEX = re.compile(r'^gitoid:(blob|tree|commit|tag):sha(1|256):([a-z0-9]+)$')

    def __init__(self, id: str) -> None:
        if OmniborId._VALID_OMNIBOR_ID_REGEX.match(id) is None:
            raise InvalidOmniBorIdException(
                f'Supplied value "{id} does not meet format specification.'
            )
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, OmniborId):
            return str(o)
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-OmniBorId: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> 'OmniborId':
        try:
            return OmniborId(id=str(o))
        except ValueError as err:
            raise CycloneDxDeserializationException(
                f'OmniBorId string supplied does not parse: {o!r}'
            ) from err

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, OmniborId):
            return self._id == other._id
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, OmniborId):
            return self._id < other._id
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f'<OmniBorId {self._id}>'

    def __str__(self) -> str:
        return self._id


class Swhid:
    """
    Helper class that allows us to perform validation on data strings that must conform to
    https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html.
    """

    _VALID_SWHID_REGEX = re.compile(r'^swh:1:(cnp|rel|rev|dir|cnt):([0-9a-z]{40})(.*)?$')

    def __init__(self, id: str) -> None:
        if Swhid._VALID_SWHID_REGEX.match(id) is None:
            raise InvalidSwhidException(
                f'Supplied value "{id} does not meet format specification.'
            )
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, Swhid):
            return str(o)
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-Swhid: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> 'Swhid':
        try:
            return Swhid(id=str(o))
        except ValueError as err:
            raise CycloneDxDeserializationException(
                f'Swhid string supplied does not parse: {o!r}'
            ) from err

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Swhid):
            return self._id == other._id
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Swhid):
            return self._id < other._id
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f'<Swhid {self._id}>'

    def __str__(self) -> str:
        return self._id


@attrs.define
class Component(Dependable):
    """
    This is our internal representation of a Component within a Bom.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_component
    """
    name: str = attrs.field(metadata={METADATA_KEY_XML_SEQUENCE: 7})
    type: ComponentType = attrs.field(
        default=ComponentType.LIBRARY,
        metadata={METADATA_KEY_XML_ATTR: True}
    )
    bom_ref: BomRef = attrs.field(
        factory=BomRef,
        converter=_bom_ref_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_1_AND_LATER,
            METADATA_KEY_JSON_NAME: 'bom-ref',
            METADATA_KEY_XML_ATTR: True,
            METADATA_KEY_XML_NAME: 'bom-ref',
        }
    )
    mime_type: Optional[str] = attrs.field(default=None)
    supplier: Optional[OrganizationalEntity] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_2_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 1,
        }
    )
    manufacturer: Optional[OrganizationalEntity] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 2,
        }
    )
    authors: 'SortedSet[OrganizationalContact]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 3,
        }
    )
    author: Optional[str] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_2_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 4,
        }
    )
    publisher: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 5}
    )
    group: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 6}
    )
    version: Optional[str] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_XML_SEQUENCE: 8,
            METADATA_KEY_INCLUDE_NONE: VERSIONS_1_0_THROUGH_1_3,  # Required in older schemas
        }
    )
    description: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 9}
    )
    scope: Optional[ComponentScope] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 10}
    )
    hashes: 'SortedSet[HashType]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 11}
    )
    licenses: LicenseRepository = attrs.field(
        factory=_license_repository_factory,
        converter=_license_repository_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_1_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 12,
        }
    )
    copyright: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 13}
    )
    cpe: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 14}
    )
    purl: Optional[PackageURL] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 15}
    )
    omnibor_ids: 'SortedSet[OmniborId]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_JSON_NAME: 'omniborId',
            METADATA_KEY_XML_SEQUENCE: 16,
        }
    )
    swhids: 'SortedSet[Swhid]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_JSON_NAME: 'swhid',
            METADATA_KEY_XML_SEQUENCE: 17,
        }
    )
    swid: Optional[Swid] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_2_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 18,
        }
    )
    modified: bool = attrs.field(
        default=False,
        metadata={METADATA_KEY_XML_SEQUENCE: 19}
    )
    pedigree: Optional[Pedigree] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_1_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 20,
        }
    )
    external_references: 'SortedSet[ExternalReference]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_1_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 21,
        }
    )
    properties: 'SortedSet[Property]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_3_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 22,
        }
    )
    components: 'SortedSet[Component]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 23}
    )
    evidence: Optional[ComponentEvidence] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_3_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 24,
        }
    )
    release_notes: Optional[ReleaseNotes] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_4_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 25,
        }
    )
    crypto_properties: Optional[CryptoProperties] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 30,
        }
    )
    tags: 'SortedSet[str]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 31,
        }
    )

    @staticmethod
    @deprecated('Deprecated - use cyclonedx.contrib.component.builders.ComponentBuilder().make_for_file() instead')
    def for_file(absolute_file_path: str, path_for_bom: Optional[str]) -> 'Component':
        """Deprecated — Wrapper of :func:`cyclonedx.contrib.component.builders.ComponentBuilder.make_for_file`."""
        from ..contrib.component.builders import ComponentBuilder

        component = ComponentBuilder().make_for_file(absolute_file_path, name=path_for_bom)
        sha1_hash = next((h.content for h in component.hashes if h.alg is HashAlgorithm.SHA_1), None)
        assert sha1_hash is not None
        component.version = f'0.0.0-{sha1_hash[0:12]}'
        component.purl = PackageURL(
            type='generic', name=path_for_bom if path_for_bom else absolute_file_path,
            version=f'0.0.0-{sha1_hash[0:12]}'
        )
        return component

    def get_all_nested_components(self, include_self: bool = False) -> set['Component']:
        components = set()
        if include_self:
            components.add(self)

        for c in self.components:
            components.update(c.get_all_nested_components(include_self=True))

        return components

    def get_pypi_url(self) -> str:
        if self.version:
            return f'https://pypi.org/project/{self.name}/{self.version}'
        else:
            return f'https://pypi.org/project/{self.name}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Component):
            return (
                self.type, self.group, self.name, self.version, self.bom_ref.value,
                None if self.purl is None else str(self.purl),
                self.swid, self.cpe, tuple(self.swhids), self.supplier, self.author,
                self.publisher, self.description, self.mime_type, self.scope,
                tuple(self.hashes), tuple(self.licenses), self.copyright, self.pedigree,
                tuple(self.external_references), tuple(self.properties),
                tuple(self.components), self.evidence, self.release_notes, self.modified,
                tuple(self.authors), tuple(self.omnibor_ids), self.manufacturer,
                self.crypto_properties, tuple(self.tags)
            ) == (
                other.type, other.group, other.name, other.version, other.bom_ref.value,
                None if other.purl is None else str(other.purl),
                other.swid, other.cpe, tuple(other.swhids), other.supplier, other.author,
                other.publisher, other.description, other.mime_type, other.scope,
                tuple(other.hashes), tuple(other.licenses), other.copyright, other.pedigree,
                tuple(other.external_references), tuple(other.properties),
                tuple(other.components), other.evidence, other.release_notes, other.modified,
                tuple(other.authors), tuple(other.omnibor_ids), other.manufacturer,
                other.crypto_properties, tuple(other.tags)
            )
        return NotImplemented

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Component):
            c = self._cmp
            return (
                c(self.type), c(self.group), self.name, c(self.version), c(self.bom_ref.value),
                c(None if self.purl is None else _ComparablePackageURL(self.purl)),
                c(self.swid), c(self.cpe), tuple(self.swhids), c(self.supplier), c(self.author),
                c(self.publisher), c(self.description), c(self.mime_type), c(self.scope),
                tuple(self.hashes), tuple(self.licenses), c(self.copyright), c(self.pedigree),
                tuple(self.external_references), tuple(self.properties),
                tuple(self.components), c(self.evidence), c(self.release_notes), c(self.modified),
                tuple(self.authors), tuple(self.omnibor_ids), c(self.manufacturer),
                c(self.crypto_properties), tuple(self.tags)
            ) < (
                c(other.type), c(other.group), other.name, c(other.version), c(other.bom_ref.value),
                c(None if other.purl is None else _ComparablePackageURL(other.purl)),
                c(other.swid), c(other.cpe), tuple(other.swhids), c(other.supplier), c(other.author),
                c(other.publisher), c(other.description), c(other.mime_type), c(other.scope),
                tuple(other.hashes), tuple(other.licenses), c(other.copyright), c(other.pedigree),
                tuple(other.external_references), tuple(other.properties),
                tuple(other.components), c(other.evidence), c(other.release_notes), c(other.modified),
                tuple(other.authors), tuple(other.omnibor_ids), c(other.manufacturer),
                c(other.crypto_properties), tuple(other.tags)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.type, self.group, self.name, self.version, self.bom_ref.value,
            None if self.purl is None else str(self.purl),
            self.swid, self.cpe, tuple(self.swhids), self.supplier, self.author,
            self.publisher, self.description, self.mime_type, self.scope,
            tuple(self.hashes), tuple(self.licenses), self.copyright, self.pedigree,
            tuple(self.external_references), tuple(self.properties),
            tuple(self.components), self.evidence, self.release_notes, self.modified,
            tuple(self.authors), tuple(self.omnibor_ids), self.manufacturer,
            self.crypto_properties, tuple(self.tags)
        ))

    def __repr__(self) -> str:
        return (f'<Component bom-ref={self.bom_ref!r}, group={self.group}, name={self.name}, '
                f'version={self.version}, type={self.type}>')
