# encoding: utf-8

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
#

import hashlib
import re
import sys
import warnings
from enum import Enum
from typing import List, Optional, Union

from ..exception.model import InvalidLocaleTypeException, InvalidUriException, NoPropertiesProvidedException, \
    MutuallyExclusivePropertiesException, UnknownHashTypeException

"""
Uniform set of models to represent objects within a CycloneDX software bill-of-materials.

You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
from a `cyclonedx.parser.BaseParser` implementation.
"""


def sha1sum(filename: str) -> str:
    """
    Generate a SHA1 hash of the provided file.

    Args:
        filename:
            Absolute path to file to hash as `str`

    Returns:
        SHA-1 hash
    """
    h = hashlib.sha1()
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            h.update(byte_block)
    return h.hexdigest()


class Encoding(Enum):
    """
    This is out internal representation of the encoding simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.4/#type_encoding
    """
    BASE_64 = 'base64'


class AttachedText:
    """
    This is our internal representation of the `attachedTextType` complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.3/#type_attachedTextType
    """

    DEFAULT_CONTENT_TYPE = 'text/plain'

    def __init__(self, content: str, content_type: str = DEFAULT_CONTENT_TYPE,
                 encoding: Optional[Encoding] = None) -> None:
        self.content_type = content_type
        self.encoding = encoding
        self.content = content

    @property
    def content_type(self) -> str:
        """
        Specifies the content type of the text. Defaults to text/plain if not specified.

        Returns:
            `str`
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type: str) -> None:
        self._content_type = content_type

    @property
    def encoding(self) -> Optional[Encoding]:
        """
        Specifies the optional encoding the text is represented in.

        Returns:
            `Encoding` if set else `None`
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: Optional[Encoding]) -> None:
        self._encoding = encoding

    @property
    def content(self) -> str:
        """
        The attachment data.

        Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment
        text.

        Returns:
            `str`
        """
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        self._content = content


class HashAlgorithm(Enum):
    """
    This is out internal representation of the hashAlg simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.3/#type_hashAlg
    """

    BLAKE2B_256 = 'BLAKE2b-256'
    BLAKE2B_384 = 'BLAKE2b-384'
    BLAKE2B_512 = 'BLAKE2b-512'
    BLAKE3 = 'BLAKE3'
    MD5 = 'MD5'
    SHA_1 = 'SHA-1'
    SHA_256 = 'SHA-256'
    SHA_384 = 'SHA-384'
    SHA_512 = 'SHA-512'
    SHA3_256 = 'SHA3-256'
    SHA3_384 = 'SHA3-384'
    SHA3_512 = 'SHA3-512'


class HashType:
    """
    This is our internal representation of the hashType complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.3/#type_hashType
    """

    @staticmethod
    def from_composite_str(composite_hash: str) -> 'HashType':
        """
        Attempts to convert a string which includes both the Hash Algorithm and Hash Value and represent using our
        internal model classes.

        Args:
             composite_hash:
                Composite Hash string of the format `HASH_ALGORITHM`:`HASH_VALUE`.
                Example: `sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b`.

        Raises:
            `UnknownHashTypeException` if the type of hash cannot be determined.

        Returns:
            An instance of `HashType`.
        """
        parts = composite_hash.split(':')

        algorithm_prefix = parts[0].lower()
        if algorithm_prefix == 'md5':
            return HashType(
                algorithm=HashAlgorithm.MD5,
                hash_value=parts[1].lower()
            )
        elif algorithm_prefix[0:3] == 'sha':
            return HashType(
                algorithm=getattr(HashAlgorithm, 'SHA_{}'.format(algorithm_prefix[3:])),
                hash_value=parts[1].lower()
            )
        elif algorithm_prefix[0:6] == 'blake2':
            return HashType(
                algorithm=getattr(HashAlgorithm, 'BLAKE2b_{}'.format(algorithm_prefix[6:])),
                hash_value=parts[1].lower()
            )

        raise UnknownHashTypeException(f"Unable to determine hash type from '{composite_hash}'")

    def __init__(self, algorithm: HashAlgorithm, hash_value: str) -> None:
        self._alg = algorithm
        self._content = hash_value

    def get_algorithm(self) -> HashAlgorithm:
        return self._alg

    def get_hash_value(self) -> str:
        return self._content

    def __repr__(self) -> str:
        return f'<Hash {self._alg.value}:{self._content}>'


class ExternalReferenceType(Enum):
    """
    Enum object that defines the permissible 'types' for an External Reference according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_externalReferenceType
    """
    ADVISORIES = 'advisories'
    BOM = 'bom'
    BUILD_META = 'build-meta'
    BUILD_SYSTEM = 'build-system'
    CHAT = 'chat'
    DISTRIBUTION = 'distribution'
    DOCUMENTATION = 'documentation'
    ISSUE_TRACKER = 'issue-tracker'
    LICENSE = 'license'
    MAILING_LIST = 'mailing-list'
    OTHER = 'other'
    RELEASE_NOTES = 'release-notes'  # Only supported in >= 1.4
    SOCIAL = 'social'
    SCM = 'vcs'
    SUPPORT = 'support'
    VCS = 'vcs'
    WEBSITE = 'website'


class XsUri:
    """
    Helper class that allows us to perform validation on data strings that are defined as xs:anyURI
    in CycloneDX schema.

    Developers can just use this via `str(XsUri('https://www.google.com'))`.

    .. note::
        See XSD definition for xsd:anyURI: http://www.datypic.com/sc/xsd/t-xsd_anyURI.html
    """

    _INVALID_URI_REGEX = re.compile(r'%(?![0-9A-F]{2})|#.*#', re.IGNORECASE + re.MULTILINE)

    def __init__(self, uri: str) -> None:
        if re.search(XsUri._INVALID_URI_REGEX, uri):
            raise InvalidUriException(
                f"Supplied value '{uri}' does not appear to be a valid URI."
            )
        self._uri = uri

    def __eq__(self, other: object) -> bool:
        if isinstance(other, XsUri):
            return str(self) == str(other)
        return False

    def __repr__(self) -> str:
        return self._uri


class ExternalReference:
    """
    This is out internal representation of an ExternalReference complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_externalReference
    """

    def __init__(self, reference_type: ExternalReferenceType, url: Union[str, XsUri], comment: str = '',
                 hashes: Optional[List[HashType]] = None) -> None:
        self._type: ExternalReferenceType = reference_type
        self._url = str(url)
        self._comment = comment
        self._hashes: List[HashType] = hashes if hashes else []

    def add_hash(self, our_hash: HashType) -> None:
        """
        Adds a hash that pins/identifies this External Reference.

        Args:
            our_hash:
                `HashType` instance
        """
        self._hashes.append(our_hash)

    def get_comment(self) -> Union[str, None]:
        """
        Get the comment for this External Reference.

        Returns:
            Any comment as a `str` else `None`.
        """
        return self._comment

    def get_hashes(self) -> List[HashType]:
        """
        List of cryptographic hashes that identify this External Reference.

        Returns:
            `List` of `HashType` objects where there are any hashes, else an empty `List`.
        """
        return self._hashes

    def get_reference_type(self) -> ExternalReferenceType:
        """
        Get the type of this External Reference.

        Returns:
            `ExternalReferenceType` that represents the type of this External Reference.
        """
        return self._type

    def get_url(self) -> str:
        """
        Get the URL/URI for this External Reference.

        Returns:
            URI as a `str`.
        """
        return self._url

    def __repr__(self) -> str:
        return f'<ExternalReference {self._type.name}, {self._url}> {self._hashes}'


class License:
    """
    This is out internal representation of `licenseType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_licenseType
    """

    def __init__(self, spxd_license_id: Optional[str] = None, license_name: Optional[str] = None,
                 license_text: Optional[AttachedText] = None, license_url: Optional[XsUri] = None) -> None:
        if not spxd_license_id and not license_name:
            raise MutuallyExclusivePropertiesException('Either `spxd_license_id` or `license_name` MUST be supplied')
        if spxd_license_id and license_name:
            warnings.warn(
                'Both `spxd_license_id` and `license_name` have been supplied - `license_name` will be ignored!',
                RuntimeWarning
            )
        self.id = spxd_license_id
        if not spxd_license_id:
            self.name = license_name
        else:
            self.name = None
        self.text = license_text
        self.url = license_url

    @property
    def id(self) -> Optional[str]:
        """
        A valid SPDX license ID

        Returns:
            `str` or `None`
        """
        return self._id

    @id.setter
    def id(self, id: Optional[str]) -> None:
        self._id = id

    @property
    def name(self) -> Optional[str]:
        """
        If SPDX does not define the license used, this field may be used to provide the license name.

        Returns:
            `str` or `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    def text(self) -> Optional[AttachedText]:
        """
        Specifies the optional full text of the attachment

        Returns:
            `AttachedText` else `None`
        """
        return self._text

    @text.setter
    def text(self, text: Optional[AttachedText]) -> None:
        self._text = text

    @property
    def url(self) -> Optional[XsUri]:
        """
        The URL to the attachment file. If the attachment is a license or BOM, an externalReference should also be
        specified for completeness.

        Returns:
            `XsUri` or `None`
        """
        return self._url

    @url.setter
    def url(self, url: Optional[XsUri]) -> None:
        self._url = url


class LicenseChoice:
    """
    This is out internal representation of `licenseChoiceType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_licenseChoiceType
    """

    def __init__(self, license: Optional[License] = None, license_expression: Optional[str] = None) -> None:
        if not license and not license_expression:
            raise NoPropertiesProvidedException(
                'One of `license` or `license_expression` must be supplied - neither supplied'
            )
        if license and license_expression:
            warnings.warn(
                'Both `license` and `license_expression` have been supplied - `license` will take precedence',
                RuntimeWarning
            )
        self.license = license
        if not license:
            self.expression = license_expression
        else:
            self.expression = None

    @property
    def license(self) -> Optional[License]:
        """
        License definition

        Returns:
            `License` or `None`
        """
        return self._license

    @license.setter
    def license(self, license: Optional[License]) -> None:
        self._license = license

    @property
    def expression(self) -> Optional[str]:
        """
        A valid SPDX license expression (not enforced).

        Refer to https://spdx.org/specifications for syntax requirements.

        Returns:
            `str` or `None`
        """
        return self._expression

    @expression.setter
    def expression(self, expression: Optional[str]) -> None:
        self._expression = expression


class Property:
    """
    This is out internal representation of `propertyType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_propertyType

    Specifies an individual property with a name and value.
    """

    def __init__(self, name: str, value: str) -> None:
        self._name = name
        self._value = value

    def get_name(self) -> str:
        """
        Get the name of this Property.

        Returns:
            Name of this Property as `str`.
        """
        return self._name

    def get_value(self) -> str:
        """
        Get the value of this Property.

        Returns:
            Value of this Property as `str`.
        """
        return self._value


class NoteText:
    """
    This is out internal representation of the Note.text complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_releaseNotesType
    """

    DEFAULT_CONTENT_TYPE: str = 'text/plain'

    def __init__(self, content: str, content_type: Optional[str] = None,
                 content_encoding: Optional[Encoding] = None) -> None:
        self.content = content
        self.content_type = content_type or NoteText.DEFAULT_CONTENT_TYPE
        self.encoding = content_encoding

    @property
    def content(self) -> str:
        """
        Get the text content of this Note.

        Returns:
            `str` note content
        """
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        self._content = content

    @property
    def content_type(self) -> Optional[str]:
        """
        Get the content-type of this Note.

        Defaults to 'text/plain' if one was not explicitly specified.

        Returns:
            `str` content-type
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type: str) -> None:
        self._content_type = content_type

    @property
    def encoding(self) -> Optional[Encoding]:
        """
        Get the encoding method used for the note's content.

        Returns:
            `Encoding` if set else `None`
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: Optional[Encoding]) -> None:
        self._encoding = encoding


class Note:
    """
    This is out internal representation of the Note complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_releaseNotesType
    """

    _LOCALE_TYPE_REGEX = re.compile(r'^[a-z]{2}(?:\-[A-Z]{2})?$')

    def __init__(self, text: NoteText, locale: Optional[str] = None) -> None:
        self.text = text
        self.locale = locale

    @property
    def text(self) -> NoteText:
        """
        Specifies the full content of the release note.

        Returns:
            `NoteText`
        """
        return self._text

    @text.setter
    def text(self, text: NoteText) -> None:
        self._text = text

    @property
    def locale(self) -> Optional[str]:
        """
        Get the ISO locale of this Note.

        The ISO-639 (or higher) language code and optional ISO-3166 (or higher) country code.

        Examples include: "en", "en-US", "fr" and "fr-CA".

        Returns:
            `str` locale if set else `None`
        """
        return self._locale

    @locale.setter
    def locale(self, locale: Optional[str]) -> None:
        self._locale = locale
        if isinstance(locale, str):
            if not re.search(Note._LOCALE_TYPE_REGEX, locale):
                self._locale = None
                raise InvalidLocaleTypeException(
                    f"Supplied locale '{locale}' is not a valid locale. "
                    f"Locale string should be formatted as the ISO-639 (or higher) language code and optional "
                    f"ISO-3166 (or higher) country code. according to ISO-639 format. Examples include: 'en', 'en-US'."
                )


class OrganizationalContact:
    """
    This is out internal representation of the `organizationalContact` complex type that can be used in multiple places
    within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_organizationalContact
    """

    def __init__(self, name: Optional[str] = None, phone: Optional[str] = None, email: Optional[str] = None) -> None:
        if not name and not phone and not email:
            raise NoPropertiesProvidedException(
                'One of name, email or phone must be supplied for an OrganizationalContact - none supplied.'
            )
        self._name: Optional[str] = name
        self._email: Optional[str] = email
        self._phone: Optional[str] = phone

    @property
    def name(self) -> Optional[str]:
        """
        Get the name of the contact.

        Returns:
            `str` if set else `None`
        """
        return self._name

    @property
    def email(self) -> Optional[str]:
        """
        Get the email of the contact.

        Returns:
            `str` if set else `None`
        """
        return self._email

    @property
    def phone(self) -> Optional[str]:
        """
        Get the phone of the contact.

        Returns:
            `str` if set else `None`
        """
        return self._phone


class OrganizationalEntity:
    """
    This is out internal representation of the `organizationalEntity` complex type that can be used in multiple places
    within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_organizationalEntity
    """

    def __init__(self, name: Optional[str] = None, urls: Optional[List[XsUri]] = None,
                 contacts: Optional[List[OrganizationalContact]] = None) -> None:
        if not name and not urls and not contacts:
            raise NoPropertiesProvidedException(
                'One of name, urls or contacts must be supplied for an OrganizationalEntity - none supplied.'
            )
        self._name: Optional[str] = name
        self._url: Optional[List[XsUri]] = urls
        self._contact: Optional[List[OrganizationalContact]] = contacts

    @property
    def name(self) -> Optional[str]:
        """
        Get the name of the organization.

        Returns:
            `str` if set else `None`
        """
        return self._name

    @property
    def urls(self) -> Optional[List[XsUri]]:
        """
        Get a list of URLs of the organization. Multiple URLs are allowed.

        Returns:
            `List[XsUri]` if set else `None`
        """
        return self._url

    @property
    def contacts(self) -> Optional[List[OrganizationalContact]]:
        """
        Get a list of contact person at the organization. Multiple contacts are allowed.

        Returns:
            `List[OrganizationalContact]` if set else `None`
        """
        return self._contact


class Tool:
    """
    This is out internal representation of the `toolType` complex type within the CycloneDX standard.

    Tool(s) are the things used in the creation of the BOM.

    .. note::
        See the CycloneDX Schema for toolType: https://cyclonedx.org/docs/1.3/#type_toolType
    """

    def __init__(self, vendor: Optional[str] = None, name: Optional[str] = None, version: Optional[str] = None,
                 hashes: Optional[List[HashType]] = None,
                 external_references: Optional[List[ExternalReference]] = None) -> None:
        self._vendor = vendor
        self._name = name
        self._version = version
        self._hashes: List[HashType] = hashes or []
        self._external_references: List[ExternalReference] = external_references or []

    def add_external_reference(self, reference: ExternalReference) -> None:
        """
        Add an external reference to this Tool.

        Args:
            reference:
                `ExternalReference` to add to this Tool.

        Returns:
            None
        """
        self._external_references.append(reference)

    def add_external_references(self, references: List[ExternalReference]) -> None:
        """
        Add a list of external reference to this Tool.

        Args:
            references:
                List of `ExternalReference` to add to this Tool.

        Returns:
            None
        """
        self._external_references = self._external_references + references

    def get_external_references(self) -> List[ExternalReference]:
        """
        List of External References that relate to this Tool.

        Returns:
            `List` of `ExternalReference` objects where there are, else an empty `List`.
        """
        return self._external_references

    def get_hashes(self) -> List[HashType]:
        """
        List of cryptographic hashes that identify this version of this Tool.

        Returns:
            `List` of `HashType` objects where there are any hashes, else an empty `List`.
        """
        return self._hashes

    def get_name(self) -> Optional[str]:
        """
        The name of this Tool.

        Returns:
            `str` representing the name of the Tool
        """
        return self._name

    def get_vendor(self) -> Optional[str]:
        """
        The vendor of this Tool.

        Returns:
            `str` representing the vendor of the Tool
        """
        return self._vendor

    def get_version(self) -> Optional[str]:
        """
        The version of this Tool.

        Returns:
            `str` representing the version of the Tool
        """
        return self._version

    def __repr__(self) -> str:
        return '<Tool {}:{}:{}>'.format(self._vendor, self._name, self._version)


if sys.version_info >= (3, 8):
    from importlib.metadata import version as meta_version
else:
    from importlib_metadata import version as meta_version

try:
    __ThisToolVersion: Optional[str] = str(meta_version('cyclonedx-python-lib'))  # type: ignore[no-untyped-call]
except Exception:
    __ThisToolVersion = None
ThisTool = Tool(vendor='CycloneDX', name='cyclonedx-python-lib', version=__ThisToolVersion or 'UNKNOWN')
ThisTool.add_external_references(references=[
    ExternalReference(
        reference_type=ExternalReferenceType.BUILD_SYSTEM,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/actions')
    ),
    ExternalReference(
        reference_type=ExternalReferenceType.DISTRIBUTION,
        url=XsUri('https://pypi.org/project/cyclonedx-python-lib/')
    ),
    ExternalReference(
        reference_type=ExternalReferenceType.DOCUMENTATION,
        url=XsUri('https://cyclonedx.github.io/cyclonedx-python-lib/')
    ),
    ExternalReference(
        reference_type=ExternalReferenceType.ISSUE_TRACKER,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/issues')
    ),
    ExternalReference(
        reference_type=ExternalReferenceType.LICENSE,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/LICENSE')
    ),
    ExternalReference(
        reference_type=ExternalReferenceType.RELEASE_NOTES,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md')
    ),
    ExternalReference(
        reference_type=ExternalReferenceType.VCS,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib')
    ),
    ExternalReference(
        reference_type=ExternalReferenceType.WEBSITE,
        url=XsUri('https://cyclonedx.org')
    )
])
