# encoding: utf-8

# This file is part of CycloneDX Python Lib
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

import warnings
from enum import Enum
from os.path import exists
from typing import Any, Iterable, Optional, Set, Union
from uuid import uuid4

# See https://github.com/package-url/packageurl-python/issues/65
import serializable
from packageurl import PackageURL  # type: ignore
from sortedcontainers import SortedSet

from ..exception.model import NoPropertiesProvidedException
from ..schema.schema import (
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
)
from ..serialization import BomRefHelper, PackageUrl
from . import (
    AttachedText,
    ComparableTuple,
    Copyright,
    ExternalReference,
    HashAlgorithm,
    HashType,
    IdentifiableAction,
    LicenseChoice,
    OrganizationalEntity,
    Property,
    XsUri,
    sha1sum,
)
from .bom_ref import BomRef
from .dependency import Dependable
from .issue import IssueType
from .release_note import ReleaseNotes


@serializable.serializable_class
class Commit:
    """
    Our internal representation of the `commitType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_commitType
    """

    def __init__(self, *, uid: Optional[str] = None, url: Optional[XsUri] = None,
                 author: Optional[IdentifiableAction] = None, committer: Optional[IdentifiableAction] = None,
                 message: Optional[str] = None) -> None:
        if not uid and not url and not author and not committer and not message:
            raise NoPropertiesProvidedException(
                'At least one of `uid`, `url`, `author`, `committer` or `message` must be provided for a `Commit`.'
            )

        self.uid = uid
        self.url = url
        self.author = author
        self.committer = committer
        self.message = message

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def uid(self) -> Optional[str]:
        """
        A unique identifier of the commit. This may be version control specific. For example, Subversion uses revision
        numbers whereas git uses commit hashes.

        Returns:
            `str` if set else `None`
        """
        return self._uid

    @uid.setter
    def uid(self, uid: Optional[str]) -> None:
        self._uid = uid

    @property  # type: ignore[misc]
    @serializable.xml_sequence(2)
    def url(self) -> Optional[XsUri]:
        """
        The URL to the commit. This URL will typically point to a commit in a version control system.

        Returns:
             `XsUri` if set else `None`
        """
        return self._url

    @url.setter
    def url(self, url: Optional[XsUri]) -> None:
        self._url = url

    @property  # type: ignore[misc]
    @serializable.xml_sequence(3)
    def author(self) -> Optional[IdentifiableAction]:
        """
        The author who created the changes in the commit.

        Returns:
            `IdentifiableAction` if set else `None`
        """
        return self._author

    @author.setter
    def author(self, author: Optional[IdentifiableAction]) -> None:
        self._author = author

    @property  # type: ignore[misc]
    @serializable.xml_sequence(4)
    def committer(self) -> Optional[IdentifiableAction]:
        """
        The person who committed or pushed the commit

        Returns:
            `IdentifiableAction` if set else `None`
        """
        return self._committer

    @committer.setter
    def committer(self, committer: Optional[IdentifiableAction]) -> None:
        self._committer = committer

    @property  # type: ignore[misc]
    @serializable.xml_sequence(5)
    def message(self) -> Optional[str]:
        """
        The text description of the contents of the commit.

        Returns:
            `str` if set else `None`
        """
        return self._message

    @message.setter
    def message(self, message: Optional[str]) -> None:
        self._message = message

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Commit):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Commit):
            return ComparableTuple((self.uid, self.url, self.author, self.committer, self.message)) < ComparableTuple(
                (other.uid, other.url, other.author, other.committer, other.message))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.uid, self.url, self.author, self.committer, self.message))

    def __repr__(self) -> str:
        return f'<Commit uid={self.uid}, url={self.url}, message={self.message}>'


@serializable.serializable_class
class ComponentEvidence:
    """
    Our internal representation of the `componentEvidenceType` complex type.

    Provides the ability to document evidence collected through various forms of extraction or analysis.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_componentEvidenceType
    """

    def __init__(self, *, licenses: Optional[Iterable[LicenseChoice]] = None,
                 copyright_: Optional[Iterable[Copyright]] = None) -> None:
        if not licenses and not copyright_:
            raise NoPropertiesProvidedException(
                'At least one of `licenses` or `copyright_` must be supplied for a `ComponentEvidence`.'
            )

        self.licenses = licenses or []  # type: ignore
        self.copyright_ = copyright_ or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'license')
    def licenses(self) -> "SortedSet[LicenseChoice]":
        """
        Optional list of licenses obtained during analysis.

        Returns:
            Set of `LicenseChoice`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[LicenseChoice]) -> None:
        self._licenses = SortedSet(licenses)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'text')
    def copyright_(self) -> "SortedSet[Copyright]":
        """
        Optional list of copyright statements.

        Returns:
             Set of `Copyright`
        """
        return self._copyright

    @copyright_.setter
    def copyright_(self, copyright_: Iterable[Copyright]) -> None:
        self._copyright = SortedSet(copyright_)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ComponentEvidence):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((tuple(self.licenses), tuple(self.copyright_)))

    def __repr__(self) -> str:
        return f'<ComponentEvidence id={id(self)}>'


class ComponentScope(str, Enum):
    """
    Enum object that defines the permissable 'scopes' for a Component according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_scope
    """
    REQUIRED = 'required'
    OPTIONAL = 'optional'
    EXCLUDED = 'excluded'


class ComponentType(str, Enum):
    """
    Enum object that defines the permissible 'types' for a Component according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_classification
    """
    APPLICATION = 'application'
    CONTAINER = 'container'
    DEVICE = 'device'
    FILE = 'file'
    FIRMWARE = 'firmware'
    FRAMEWORK = 'framework'
    LIBRARY = 'library'
    OPERATING_SYSTEM = 'operating-system'


class Diff:
    """
    Our internal representation of the `diffType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_diffType
    """

    def __init__(self, *, text: Optional[AttachedText] = None, url: Optional[XsUri] = None) -> None:
        if not text and not url:
            raise NoPropertiesProvidedException(
                'At least one of `text` or `url` must be provided for a `Diff`.'
            )

        self.text = text
        self.url = url

    @property
    def text(self) -> Optional[AttachedText]:
        """
        Specifies the optional text of the diff.

        Returns:
            `AttachedText` if set else `None`
        """
        return self._text

    @text.setter
    def text(self, text: Optional[AttachedText]) -> None:
        self._text = text

    @property
    def url(self) -> Optional[XsUri]:
        """
        Specifies the URL to the diff.

        Returns:
            `XsUri` if set else `None`
        """
        return self._url

    @url.setter
    def url(self, url: Optional[XsUri]) -> None:
        self._url = url

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Diff):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Diff):
            return ComparableTuple((self.url, self.text)) < ComparableTuple((other.url, other.text))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.text, self.url))

    def __repr__(self) -> str:
        return f'<Diff url={self.url}>'


class PatchClassification(str, Enum):
    """
    Enum object that defines the permissible `patchClassification`s.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_patchClassification
    """
    BACKPORT = 'backport'
    CHERRY_PICK = 'cherry-pick'
    MONKEY = 'monkey'
    UNOFFICIAL = 'unofficial'


@serializable.serializable_class
class Patch:
    """
    Our internal representation of the `patchType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_patchType
    """

    def __init__(self, *, type_: PatchClassification, diff: Optional[Diff] = None,
                 resolves: Optional[Iterable[IssueType]] = None) -> None:
        self.type_ = type_
        self.diff = diff
        self.resolves = resolves or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def type_(self) -> PatchClassification:
        """
        Specifies the purpose for the patch including the resolution of defects, security issues, or new behavior or
        functionality.

        Returns:
            `PatchClassification`
        """
        return self._type

    @type_.setter
    def type_(self, type_: PatchClassification) -> None:
        self._type = type_

    @property
    def diff(self) -> Optional[Diff]:
        """
        The patch file (or diff) that show changes.

        .. note::
            Refer to https://en.wikipedia.org/wiki/Diff.

        Returns:
            `Diff` if set else `None`
        """
        return self._diff

    @diff.setter
    def diff(self, diff: Optional[Diff]) -> None:
        self._diff = diff

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'issue')
    def resolves(self) -> "SortedSet[IssueType]":
        """
        Optional list of issues resolved by this patch.

        Returns:
            Set of `IssueType`
        """
        return self._resolves

    @resolves.setter
    def resolves(self, resolves: Iterable[IssueType]) -> None:
        self._resolves = SortedSet(resolves)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Patch):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Patch):
            return ComparableTuple((self.type_, self.diff, ComparableTuple(self.resolves))) < ComparableTuple(
                (other.type_, other.diff, ComparableTuple(other.resolves)))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.type_, self.diff, tuple(self.resolves)))

    def __repr__(self) -> str:
        return f'<Patch type={self.type_}, id={id(self)}>'


@serializable.serializable_class
class Pedigree:
    """
    Our internal representation of the `pedigreeType` complex type.

    Component pedigree is a way to document complex supply chain scenarios where components are created, distributed,
    modified, redistributed, combined with other components, etc. Pedigree supports viewing this complex chain from the
    beginning, the end, or anywhere in the middle. It also provides a way to document variants where the exact relation
    may not be known.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_pedigreeType
    """

    def __init__(self, *, ancestors: Optional[Iterable['Component']] = None,
                 descendants: Optional[Iterable['Component']] = None, variants: Optional[Iterable['Component']] = None,
                 commits: Optional[Iterable[Commit]] = None, patches: Optional[Iterable[Patch]] = None,
                 notes: Optional[str] = None) -> None:
        if not ancestors and not descendants and not variants and not commits and not patches and not notes:
            raise NoPropertiesProvidedException(
                'At least one of `ancestors`, `descendants`, `variants`, `commits`, `patches` or `notes` must be '
                'provided for `Pedigree`'
            )

        self.ancestors = ancestors or []  # type: ignore
        self.descendants = descendants or []  # type: ignore
        self.variants = variants or []  # type: ignore
        self.commits = commits or []  # type: ignore
        self.patches = patches or []  # type: ignore
        self.notes = notes

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'component')
    @serializable.xml_sequence(1)
    def ancestors(self) -> "SortedSet['Component']":
        """
        Describes zero or more components in which a component is derived from. This is commonly used to describe forks
        from existing projects where the forked version contains a ancestor node containing the original component it
        was forked from.

        For example, Component A is the original component. Component B is the component being used and documented in
        the BOM. However, Component B contains a pedigree node with a single ancestor documenting Component A - the
        original component from which Component B is derived from.

        Returns:
            Set of `Component`
        """
        return self._ancestors

    @ancestors.setter
    def ancestors(self, ancestors: Iterable['Component']) -> None:
        self._ancestors = SortedSet(ancestors)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'component')
    @serializable.xml_sequence(2)
    def descendants(self) -> "SortedSet['Component']":
        """
        Descendants are the exact opposite of ancestors. This provides a way to document all forks (and their forks) of
        an original or root component.

        Returns:
            Set of `Component`
        """
        return self._descendants

    @descendants.setter
    def descendants(self, descendants: Iterable['Component']) -> None:
        self._descendants = SortedSet(descendants)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'component')
    @serializable.xml_sequence(3)
    def variants(self) -> "SortedSet['Component']":
        """
        Variants describe relations where the relationship between the components are not known. For example, if
        Component A contains nearly identical code to Component B. They are both related, but it is unclear if one is
        derived from the other, or if they share a common ancestor.

        Returns:
            Set of `Component`
        """
        return self._variants

    @variants.setter
    def variants(self, variants: Iterable['Component']) -> None:
        self._variants = SortedSet(variants)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'commit')
    @serializable.xml_sequence(4)
    def commits(self) -> "SortedSet[Commit]":
        """
        A list of zero or more commits which provide a trail describing how the component deviates from an ancestor,
        descendant, or variant.

        Returns:
            Set of `Commit`
        """
        return self._commits

    @commits.setter
    def commits(self, commits: Iterable[Commit]) -> None:
        self._commits = SortedSet(commits)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'patch')
    @serializable.xml_sequence(5)
    def patches(self) -> "SortedSet[Patch]":
        """
        A list of zero or more patches describing how the component deviates from an ancestor, descendant, or variant.
        Patches may be complimentary to commits or may be used in place of commits.

        Returns:
            Set of `Patch`
        """
        return self._patches

    @patches.setter
    def patches(self, patches: Iterable[Patch]) -> None:
        self._patches = SortedSet(patches)

    @property  # type: ignore[misc]
    @serializable.xml_sequence(6)
    def notes(self) -> Optional[str]:
        """
        Notes, observations, and other non-structured commentary describing the components pedigree.

        Returns:
            `str` if set else `None`
        """
        return self._notes

    @notes.setter
    def notes(self, notes: Optional[str]) -> None:
        self._notes = notes

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pedigree):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            tuple(self.ancestors), tuple(self.descendants), tuple(self.variants), tuple(self.commits),
            tuple(self.patches), self.notes
        ))

    def __repr__(self) -> str:
        return f'<Pedigree id={id(self)}, hash={hash(self)}>'


@serializable.serializable_class
class Swid:
    """
    Our internal representation of the `swidType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_swidType
    """

    def __init__(self, *, tag_id: str, name: str, version: Optional[str] = None,
                 tag_version: Optional[int] = None, patch: Optional[bool] = None,
                 text: Optional[AttachedText] = None, url: Optional[XsUri] = None) -> None:
        self.tag_id = tag_id
        self.name = name
        self.version = version
        self.tag_version = tag_version
        self.patch = patch
        self.text = text
        self.url = url

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def tag_id(self) -> str:
        """
        Maps to the tagId of a SoftwareIdentity.

        Returns:
            `str`
        """
        return self._tag_id

    @tag_id.setter
    def tag_id(self, tag_id: str) -> None:
        self._tag_id = tag_id

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def name(self) -> str:
        """
        Maps to the name of a SoftwareIdentity.

        Returns:
             `str`
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def version(self) -> Optional[str]:
        """
        Maps to the version of a SoftwareIdentity.

        Returns:
             `str` if set else `None`.
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def tag_version(self) -> Optional[int]:
        """
        Maps to the tagVersion of a SoftwareIdentity.

        Returns:
            `int` if set else `None`
        """
        return self._tag_version

    @tag_version.setter
    def tag_version(self, tag_version: Optional[int]) -> None:
        self._tag_version = tag_version

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def patch(self) -> Optional[bool]:
        """
        Maps to the patch of a SoftwareIdentity.

        Returns:
             `bool` if set else `None`
        """
        return self._patch

    @patch.setter
    def patch(self, patch: Optional[bool]) -> None:
        self._patch = patch

    @property
    def text(self) -> Optional[AttachedText]:
        """
        Specifies the full content of the SWID tag.

        Returns:
            `AttachedText` if set else `None`
        """
        return self._text

    @text.setter
    def text(self, text: Optional[AttachedText]) -> None:
        self._text = text

    @property
    def url(self) -> Optional[XsUri]:
        """
        The URL to the SWID file.

        Returns:
            `XsUri` if set else `None`
        """
        return self._url

    @url.setter
    def url(self, url: Optional[XsUri]) -> None:
        self._url = url

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Swid):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((self.tag_id, self.name, self.version, self.tag_version, self.patch, self.text, self.url))

    def __repr__(self) -> str:
        return f'<Swid tagId={self.tag_id}, name={self.name}, version={self.version}>'


@serializable.serializable_class
class Component(Dependable):
    """
    This is our internal representation of a Component within a Bom.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_component
    """

    @staticmethod
    def for_file(absolute_file_path: str, path_for_bom: Optional[str]) -> 'Component':
        """
        Helper method to create a Component that represents the provided local file as a Component.

        Args:
            absolute_file_path:
                Absolute path to the file you wish to represent
            path_for_bom:
                Optionally, if supplied this is the path that will be used to identify the file in the BOM

        Returns:
            `Component` representing the supplied file
        """
        if not exists(absolute_file_path):
            raise FileExistsError('Supplied file path \'{}\' does not exist'.format(absolute_file_path))

        sha1_hash: str = sha1sum(filename=absolute_file_path)
        return Component(
            name=path_for_bom if path_for_bom else absolute_file_path,
            version='0.0.0-{}'.format(sha1_hash[0:12]),
            hashes=[
                HashType(alg=HashAlgorithm.SHA_1, content=sha1_hash)
            ],
            type_=ComponentType.FILE, purl=PackageURL(
                type='generic', name=path_for_bom if path_for_bom else absolute_file_path,
                version='0.0.0-{}'.format(sha1_hash[0:12])
            )
        )

    def __init__(self, *, name: str, type_: ComponentType = ComponentType.LIBRARY,
                 mime_type: Optional[str] = None, bom_ref: Optional[Union[str, BomRef]] = None,
                 supplier: Optional[OrganizationalEntity] = None, author: Optional[str] = None,
                 publisher: Optional[str] = None, group: Optional[str] = None, version: Optional[str] = None,
                 description: Optional[str] = None, scope: Optional[ComponentScope] = None,
                 hashes: Optional[Iterable[HashType]] = None, licenses: Optional[Iterable[LicenseChoice]] = None,
                 copyright_: Optional[str] = None, purl: Optional[PackageURL] = None,
                 external_references: Optional[Iterable[ExternalReference]] = None,
                 properties: Optional[Iterable[Property]] = None, release_notes: Optional[ReleaseNotes] = None,
                 cpe: Optional[str] = None, swid: Optional[Swid] = None, pedigree: Optional[Pedigree] = None,
                 components: Optional[Iterable['Component']] = None, evidence: Optional[ComponentEvidence] = None,
                 modified: bool = False,
                 # Deprecated parameters kept for backwards compatibility
                 namespace: Optional[str] = None, license_str: Optional[str] = None
                 ) -> None:
        self.type_ = type_
        self.mime_type = mime_type
        if type(bom_ref) == BomRef:
            self._bom_ref = bom_ref
        else:
            self._bom_ref = BomRef(value=str(bom_ref) if bom_ref else str(uuid4()))
        self.supplier = supplier
        self.author = author
        self.publisher = publisher
        self.group = group
        self.name = name
        self.version = version
        self.description = description
        self.scope = scope
        self.hashes = hashes or []  # type: ignore
        self.licenses = licenses or []  # type: ignore
        self.copyright_ = copyright_
        self.cpe = cpe
        self.purl = purl
        self.swid = swid
        self.modified = modified
        self.pedigree = pedigree
        self.external_references = external_references or []  # type: ignore
        self.properties = properties or []  # type: ignore
        self.components = components or []  # type: ignore
        self.evidence = evidence
        self.release_notes = release_notes

        # Deprecated for 1.4, but kept for some backwards compatibility
        if namespace:
            warnings.warn(
                '`namespace` is deprecated and has been replaced with `group` to align with the CycloneDX standard',
                DeprecationWarning
            )
            if not group:
                self.group = namespace

        if license_str:
            warnings.warn(
                '`license_str` is deprecated and has been replaced with `licenses` to align with the CycloneDX '
                'standard', DeprecationWarning
            )
            if not licenses:
                self.licenses = [LicenseChoice(expression=license_str)]  # type: ignore

        self.__dependencies: "SortedSet[BomRef]" = SortedSet()

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def type_(self) -> ComponentType:
        """
        Get the type of this Component.

        Returns:
            Declared type of this Component as `ComponentType`.
        """
        return self._type_

    @type_.setter
    def type_(self, component_type: ComponentType) -> None:
        self._type_ = component_type

    @property
    def mime_type(self) -> Optional[str]:
        """
        Get any declared mime-type for this Component.

        When used on file components, the mime-type can provide additional context about the kind of file being
        represented such as an image, font, or executable. Some library or framework components may also have an
        associated mime-type.

        Returns:
            `str` if set else `None`
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type: Optional[str]) -> None:
        self._mime_type = mime_type

    @property  # type: ignore[misc]
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRefHelper)
    @serializable.view(SchemaVersion1Dot1)
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> BomRef:
        """
        An optional identifier which can be used to reference the component elsewhere in the BOM. Every bom-ref MUST be
        unique within the BOM.

        If a value was not provided in the constructor, a UUIDv4 will have been assigned.

        Returns:
            `BomRef`
        """
        return self._bom_ref

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_sequence(1)
    def supplier(self) -> Optional[OrganizationalEntity]:
        """
        The organization that supplied the component. The supplier may often be the manufacture, but may also be a
        distributor or repackager.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._supplier

    @supplier.setter
    def supplier(self, supplier: Optional[OrganizationalEntity]) -> None:
        self._supplier = supplier

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_sequence(2)
    def author(self) -> Optional[str]:
        """
        The person(s) or organization(s) that authored the component.

        Returns:
            `str` if set else `None`
        """
        return self._author

    @author.setter
    def author(self, author: Optional[str]) -> None:
        self._author = author

    @property  # type: ignore[misc]
    @serializable.xml_sequence(3)
    def publisher(self) -> Optional[str]:
        """
        The person(s) or organization(s) that published the component

        Returns:
            `str` if set else `None`
        """
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: Optional[str]) -> None:
        self._publisher = publisher

    @property  # type: ignore[misc]
    @serializable.xml_sequence(4)
    def group(self) -> Optional[str]:
        """
        The grouping name or identifier. This will often be a shortened, single name of the company or project that
        produced the component, or the source package or domain name. Whitespace and special characters should be
        avoided.

        Examples include: `apache`, `org.apache.commons`, and `apache.org`.

        Returns:
            `str` if set else `None`
        """
        return self._group

    @group.setter
    def group(self, group: Optional[str]) -> None:
        self._group = group

    @property  # type: ignore[misc]
    @serializable.xml_sequence(5)
    def name(self) -> str:
        """
        The name of the component.

        This will often be a shortened, single name of the component.

        Examples: `commons-lang3` and `jquery`.

        Returns:
            `str`
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property  # type: ignore[misc]
    @serializable.include_none(SchemaVersion1Dot0, "")
    @serializable.include_none(SchemaVersion1Dot1, "")
    @serializable.include_none(SchemaVersion1Dot2, "")
    @serializable.include_none(SchemaVersion1Dot3, "")
    @serializable.xml_sequence(6)
    def version(self) -> Optional[str]:
        """
        The component version. The version should ideally comply with semantic versioning but is not enforced.

        This is NOT optional for CycloneDX Schema Version < 1.4 but was agreed to default to an empty string where a
        version was not supplied for schema versions < 1.4

        Returns:
            Declared version of this Component as `str` or `None`
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property  # type: ignore[misc]
    @serializable.xml_sequence(7)
    def description(self) -> Optional[str]:
        """
        Get the description of this Component.

        Returns:
            `str` if set, else `None`.
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property  # type: ignore[misc]
    @serializable.xml_sequence(8)
    def scope(self) -> Optional[ComponentScope]:
        """
        Specifies the scope of the component.

        If scope is not specified, 'required' scope should be assumed by the consumer of the BOM.

        Returns:
            `ComponentScope` or `None`
        """
        return self._scope

    @scope.setter
    def scope(self, scope: Optional[ComponentScope]) -> None:
        self._scope = scope

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'hash')
    @serializable.xml_sequence(9)
    def hashes(self) -> "SortedSet[HashType]":
        """
        Optional list of hashes that help specify the integrity of this Component.

        Returns:
             Set of `HashType`
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes: Iterable[HashType]) -> None:
        self._hashes = SortedSet(hashes)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot1)
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'licenses')
    @serializable.xml_sequence(10)
    def licenses(self) -> "SortedSet[LicenseChoice]":
        """
        A optional list of statements about how this Component is licensed.

        Returns:
            Set of `LicenseChoice`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[LicenseChoice]) -> None:
        self._licenses = SortedSet(licenses)

    @property  # type: ignore[misc]
    @serializable.xml_sequence(11)
    def copyright_(self) -> Optional[str]:
        """
        An optional copyright notice informing users of the underlying claims to copyright ownership in a published
        work.

        Returns:
            `str` or `None`
        """
        return self._copyright_

    @copyright_.setter
    def copyright_(self, copyright_: Optional[str]) -> None:
        self._copyright_ = copyright_

    @property  # type: ignore[misc]
    @serializable.xml_sequence(12)
    def cpe(self) -> Optional[str]:
        """
        Specifies a well-formed CPE name that conforms to the CPE 2.2 or 2.3 specification.
        See https://nvd.nist.gov/products/cpe

        Returns:
            `str` if set else `None`
        """
        return self._cpe

    @cpe.setter
    def cpe(self, cpe: Optional[str]) -> None:
        self._cpe = cpe

    @property  # type: ignore[misc]
    @serializable.type_mapping(PackageUrl)
    @serializable.xml_sequence(13)
    def purl(self) -> Optional[PackageURL]:
        """
        Specifies the package-url (PURL).

        The purl, if specified, must be valid and conform to the specification defined at:
        https://github.com/package-url/purl-spec

        Returns:
            `PackageURL` or `None`
        """
        return self._purl

    @purl.setter
    def purl(self, purl: Optional[PackageURL]) -> None:
        self._purl = purl

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_sequence(14)
    def swid(self) -> Optional[Swid]:
        """
        Specifies metadata and content for ISO-IEC 19770-2 Software Identification (SWID) Tags.

        Returns:
            `Swid` if set else `None`
        """
        return self._swid

    @swid.setter
    def swid(self, swid: Optional[Swid]) -> None:
        self._swid = swid

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot0)
    @serializable.xml_sequence(18)
    def modified(self) -> bool:
        return self._modified

    @modified.setter
    def modified(self, modified: bool) -> None:
        self._modified = modified

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot1)
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_sequence(16)
    def pedigree(self) -> Optional[Pedigree]:
        """
        Component pedigree is a way to document complex supply chain scenarios where components are created,
        distributed, modified, redistributed, combined with other components, etc.

        Returns:
            `Pedigree` if set else `None`
        """
        return self._pedigree

    @pedigree.setter
    def pedigree(self, pedigree: Optional[Pedigree]) -> None:
        self._pedigree = pedigree

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot1)
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    @serializable.xml_sequence(17)
    def external_references(self) -> "SortedSet[ExternalReference]":
        """
        Provides the ability to document external references related to the component or to the project the component
        describes.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'property')
    @serializable.xml_sequence(18)
    def properties(self) -> "SortedSet[Property]":
        """
        Provides the ability to document properties in a key/value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions.

        Return:
            Set of `Property`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'component')
    @serializable.xml_sequence(19)
    def components(self) -> "SortedSet['Component']":
        """
        A list of software and hardware components included in the parent component. This is not a dependency tree. It
        provides a way to specify a hierarchical representation of component assemblies, similar to system -> subsystem
        -> parts assembly in physical supply chains.

        Returns:
            Set of `Component`
        """
        return self._components

    @components.setter
    def components(self, components: Iterable['Component']) -> None:
        self._components = SortedSet(components)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_sequence(20)
    def evidence(self) -> Optional[ComponentEvidence]:
        """
        Provides the ability to document evidence collected through various forms of extraction or analysis.

        Returns:
            `ComponentEvidence` if set else `None`
        """
        return self._evidence

    @evidence.setter
    def evidence(self, evidence: Optional[ComponentEvidence]) -> None:
        self._evidence = evidence

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_sequence(21)
    def release_notes(self) -> Optional[ReleaseNotes]:
        """
        Specifies optional release notes.

        Returns:
            `ReleaseNotes` or `None`
        """
        return self._release_notes

    @release_notes.setter
    def release_notes(self, release_notes: Optional[ReleaseNotes]) -> None:
        self._release_notes = release_notes

    def get_all_nested_components(self, include_self: bool = False) -> Set["Component"]:
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
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Component):
            return ComparableTuple((self.type_, self.group, self.name, self.version)) < ComparableTuple(
                (other.type_, other.group, other.name, other.version))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.type_, self.mime_type, self.supplier, self.author, self.publisher, self.group, self.name,
            self.version, self.description, self.scope, tuple(self.hashes), tuple(self.licenses), self.copyright_,
            self.cpe, self.purl, self.swid, self.pedigree, tuple(self.external_references), tuple(self.properties),
            tuple(self.components), self.evidence, self.release_notes, self.modified
        ))

    def __repr__(self) -> str:
        return f'<Component bom-ref={self.bom_ref}, group={self.group}, name={self.name}, ' \
               f'version={self.version}, type={self.type_}>'

    # Deprecated methods
    def get_namespace(self) -> Optional[str]:
        """
        Get the namespace of this Component.

        Returns:
            Declared namespace of this Component as `str` if declared, else `None`.
        """
        warnings.warn('`Component.get_namespace()` is deprecated - use `Component.group`', DeprecationWarning)
        return self._group
