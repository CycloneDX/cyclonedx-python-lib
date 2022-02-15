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
from typing import Iterable, Optional, Set
from uuid import uuid4

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore

from . import AttachedText, Copyright, ExternalReference, HashAlgorithm, HashType, IdentifiableAction, LicenseChoice, \
    OrganizationalEntity, Property, sha1sum, XsUri
from .issue import IssueType
from .release_note import ReleaseNotes
from .vulnerability import Vulnerability
from ..exception.model import NoPropertiesProvidedException


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

    @property
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

    @property
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

    @property
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

    @property
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

    @property
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

    def __hash__(self) -> int:
        return hash((self.uid, self.url, self.author, self.committer, self.message))

    def __repr__(self) -> str:
        return f'<Commit uid={self.uid}, url={self.url}, message={self.message}>'


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

        self.licenses = set(licenses or [])
        self.copyright = set(copyright_ or [])

    @property
    def licenses(self) -> Set[LicenseChoice]:
        """
        Optional list of licenses obtained during analysis.

        Returns:
            Set of `LicenseChoice`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[LicenseChoice]) -> None:
        self._licenses = set(licenses)

    @property
    def copyright(self) -> Set[Copyright]:
        """
        Optional list of copyright statements.

        Returns:
             Set of `Copyright`
        """
        return self._copyright

    @copyright.setter
    def copyright(self, copyright_: Iterable[Copyright]) -> None:
        self._copyright = set(copyright_)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ComponentEvidence):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((tuple(self.licenses), tuple(self.copyright)))

    def __repr__(self) -> str:
        return f'<ComponentEvidence id={id(self)}>'


class ComponentScope(Enum):
    """
    Enum object that defines the permissable 'scopes' for a Component according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_scope
    """
    REQUIRED = 'required'
    OPTIONAL = 'optional'
    EXCLUDED = 'excluded'


class ComponentType(Enum):
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

    def __hash__(self) -> int:
        return hash((self.text, self.url))

    def __repr__(self) -> str:
        return f'<Diff url={self.url}>'


class PatchClassification(Enum):
    """
    Enum object that defines the permissible `patchClassification`s.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_patchClassification
    """
    BACKPORT = 'backport'
    CHERRY_PICK = 'cherry-pick'
    MONKEY = 'monkey'
    UNOFFICIAL = 'unofficial'


class Patch:
    """
    Our internal representation of the `patchType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_patchType
    """

    def __init__(self, *, type_: PatchClassification, diff: Optional[Diff] = None,
                 resolves: Optional[Iterable[IssueType]] = None) -> None:
        self.type = type_
        self.diff = diff
        self.resolves = set(resolves or [])

    @property
    def type(self) -> PatchClassification:
        """
        Specifies the purpose for the patch including the resolution of defects, security issues, or new behavior or
        functionality.

        Returns:
            `PatchClassification`
        """
        return self._type

    @type.setter
    def type(self, type_: PatchClassification) -> None:
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

    @property
    def resolves(self) -> Set[IssueType]:
        """
        Optional list of issues resolved by this patch.

        Returns:
            Set of `IssueType`
        """
        return self._resolves

    @resolves.setter
    def resolves(self, resolves: Iterable[IssueType]) -> None:
        self._resolves = set(resolves)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Patch):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((self.type, self.diff, tuple(self.resolves)))

    def __repr__(self) -> str:
        return f'<Patch type={self.type}, id={id(self)}>'


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

        self.ancestors = set(ancestors or [])
        self.descendants = set(descendants or [])
        self.variants = set(variants or [])
        self.commits = set(commits or [])
        self.patches = set(patches or [])
        self.notes = notes

    @property
    def ancestors(self) -> Set['Component']:
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
        self._ancestors = set(ancestors)

    @property
    def descendants(self) -> Set['Component']:
        """
        Descendants are the exact opposite of ancestors. This provides a way to document all forks (and their forks) of
        an original or root component.

        Returns:
            Set of `Component`
        """
        return self._descendants

    @descendants.setter
    def descendants(self, descendants: Iterable['Component']) -> None:
        self._descendants = set(descendants)

    @property
    def variants(self) -> Set['Component']:
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
        self._variants = set(variants)

    @property
    def commits(self) -> Set[Commit]:
        """
        A list of zero or more commits which provide a trail describing how the component deviates from an ancestor,
        descendant, or variant.

        Returns:
            Set of `Commit`
        """
        return self._commits

    @commits.setter
    def commits(self, commits: Iterable[Commit]) -> None:
        self._commits = set(commits)

    @property
    def patches(self) -> Set[Patch]:
        """
        A list of zero or more patches describing how the component deviates from an ancestor, descendant, or variant.
        Patches may be complimentary to commits or may be used in place of commits.

        Returns:
            Set of `Patch`
        """
        return self._patches

    @patches.setter
    def patches(self, patches: Iterable[Patch]) -> None:
        self._patches = set(patches)

    @property
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
        return f'<Pedigree id={id(self)}>'


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

    @property
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

    @property
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

    @property
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

    @property
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

    @property
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


class Component:
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
                HashType(algorithm=HashAlgorithm.SHA_1, hash_value=sha1_hash)
            ],
            component_type=ComponentType.FILE, purl=PackageURL(
                type='generic', name=path_for_bom if path_for_bom else absolute_file_path,
                version='0.0.0-{}'.format(sha1_hash[0:12])
            )
        )

    def __init__(self, *, name: str, component_type: ComponentType = ComponentType.LIBRARY,
                 mime_type: Optional[str] = None, bom_ref: Optional[str] = None,
                 supplier: Optional[OrganizationalEntity] = None, author: Optional[str] = None,
                 publisher: Optional[str] = None, group: Optional[str] = None, version: Optional[str] = None,
                 description: Optional[str] = None, scope: Optional[ComponentScope] = None,
                 hashes: Optional[Iterable[HashType]] = None, licenses: Optional[Iterable[LicenseChoice]] = None,
                 copyright_: Optional[str] = None, purl: Optional[PackageURL] = None,
                 external_references: Optional[Iterable[ExternalReference]] = None,
                 properties: Optional[Iterable[Property]] = None, release_notes: Optional[ReleaseNotes] = None,
                 cpe: Optional[str] = None, swid: Optional[Swid] = None, pedigree: Optional[Pedigree] = None,
                 components: Optional[Iterable['Component']] = None, evidence: Optional[ComponentEvidence] = None,
                 # Deprecated parameters kept for backwards compatibility
                 namespace: Optional[str] = None, license_str: Optional[str] = None
                 ) -> None:
        self.type = component_type
        self.mime_type = mime_type
        self.bom_ref = bom_ref or str(uuid4())
        self.supplier = supplier
        self.author = author
        self.publisher = publisher
        self.group = group
        self.name = name
        self.version = version
        self.description = description
        self.scope = scope
        self.hashes = set(hashes or [])
        self.licenses = set(licenses or [])
        self.copyright = copyright_
        self.cpe = cpe
        self.purl = purl
        self.swid = swid
        self.pedigree = pedigree
        self.external_references = set(external_references or [])
        self.properties = set(properties or [])
        self.components = set(components or [])
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
                self.licenses = {LicenseChoice(license_expression=license_str)}

        self.__vulnerabilites: Set[Vulnerability] = set()

    @property
    def type(self) -> ComponentType:
        """
        Get the type of this Component.

        Returns:
            Declared type of this Component as `ComponentType`.
        """
        return self._type

    @type.setter
    def type(self, component_type: ComponentType) -> None:
        self._type = component_type

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

    @property
    def bom_ref(self) -> str:
        """
        An optional identifier which can be used to reference the component elsewhere in the BOM. Every bom-ref MUST be
        unique within the BOM.

        If a value was not provided in the constructor, a UUIDv4 will have been assigned.

        Returns:
            `str` as a unique identifiers for this Component
        """
        return self._bom_ref

    @bom_ref.setter
    def bom_ref(self, bom_ref: str) -> None:
        self._bom_ref = bom_ref

    @property
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

    @property
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

    @property
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

    @property
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

    @property
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

    @property
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

    @property
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

    @property
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

    @property
    def hashes(self) -> Set[HashType]:
        """
        Optional list of hashes that help specify the integrity of this Component.

        Returns:
             Set of `HashType`
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes: Iterable[HashType]) -> None:
        self._hashes = set(hashes)

    @property
    def licenses(self) -> Set[LicenseChoice]:
        """
        A optional list of statements about how this Component is licensed.

        Returns:
            Set of `LicenseChoice`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[LicenseChoice]) -> None:
        self._licenses = set(licenses)

    @property
    def copyright(self) -> Optional[str]:
        """
        An optional copyright notice informing users of the underlying claims to copyright ownership in a published
        work.

        Returns:
            `str` or `None`
        """
        return self._copyright

    @copyright.setter
    def copyright(self, copyright_: Optional[str]) -> None:
        self._copyright = copyright_

    @property
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

    @property
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

    @property
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

    @property
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

    @property
    def external_references(self) -> Set[ExternalReference]:
        """
        Provides the ability to document external references related to the component or to the project the component
        describes.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = set(external_references)

    @property
    def properties(self) -> Set[Property]:
        """
        Provides the ability to document properties in a key/value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions.

        Return:
            Set of `Property`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = set(properties)

    @property
    def components(self) -> Set['Component']:
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
        self._components = set(components)

    @property
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

    @property
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

    def add_vulnerability(self, vulnerability: Vulnerability) -> None:
        """
        Add a Vulnerability to this Component.

        Args:
            vulnerability:
                `cyclonedx.model.vulnerability.Vulnerability` instance to add to this Component.

        Returns:
            None
        """
        self.__vulnerabilites.add(vulnerability)

    def get_vulnerabilities(self) -> Set[Vulnerability]:
        """
        Get all the Vulnerabilities for this Component.

        Returns:
             Set of `Vulnerability`
        """
        return self.__vulnerabilites

    def has_vulnerabilities(self) -> bool:
        """
        Does this Component have any vulnerabilities?

        Returns:
             `True` if this Component has 1 or more vulnerabilities, `False` otherwise.
        """
        return bool(self.get_vulnerabilities())

    def get_pypi_url(self) -> str:
        if self.version:
            return f'https://pypi.org/project/{self.name}/{self.version}'
        else:
            return f'https://pypi.org/project/{self.name}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Component):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.type, self.mime_type, self.supplier, self.author, self.publisher, self.group, self.name,
            self.version, self.description, self.scope, tuple(self.hashes), tuple(self.licenses), self.copyright,
            self.cpe, self.purl, self.swid, self.pedigree, tuple(self.external_references), tuple(self.properties),
            tuple(self.components), self.evidence, self.release_notes
        ))

    def __repr__(self) -> str:
        return f'<Component group={self.group}, name={self.name}, version={self.version}>'

    # Deprecated methods
    def get_namespace(self) -> Optional[str]:
        """
        Get the namespace of this Component.

        Returns:
            Declared namespace of this Component as `str` if declared, else `None`.
        """
        warnings.warn('`Component.get_namespace()` is deprecated - use `Component.group`', DeprecationWarning)
        return self._group
