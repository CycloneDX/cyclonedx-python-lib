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
# Copyright (c) OWASP Foundation. All Rights Reserved.

import warnings
from typing import TYPE_CHECKING, Any, Optional, Union

import serializable
from sortedcontainers import SortedSet

from ..exception.model import MutuallyExclusivePropertiesException
from . import AttachedText, ComparableTuple, XsUri

"""
License related things
"""


@serializable.serializable_class(name='license')
class DisjunctiveLicense:
    """
    This is our internal representation of `licenseType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_licenseType
    """

    def __init__(self, *, id: Optional[str] = None, name: Optional[str] = None,
                 text: Optional[AttachedText] = None, url: Optional[XsUri] = None) -> None:
        if not id and not name:
            raise MutuallyExclusivePropertiesException('Either `id` or `name` MUST be supplied')
        if id and name:
            warnings.warn(
                'Both `id` and `name` have been supplied - `name` will be ignored!',
                category=RuntimeWarning, stacklevel=1
            )
        self._id = id
        self._name = name if not id else None
        self._text = text
        self._url = url

    @property
    @serializable.xml_sequence(1)
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
        if id is not None:
            self._name = None

    @property
    @serializable.xml_sequence(1)
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
        if name is not None:
            self._id = None

    @property
    @serializable.xml_sequence(2)
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
    @serializable.xml_sequence(3)
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DisjunctiveLicense):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DisjunctiveLicense):
            return ComparableTuple((self._id, self._name)) < ComparableTuple((other._id, other._name))
        if isinstance(other, LicenseExpression):
            return False  # self after any LicenseExpression
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._id, self._name, self._text, self._url))

    def __repr__(self) -> str:
        return f'<License id={self._id!r}, name={self._name!r}>'


@serializable.serializable_class(name='expression')
class LicenseExpression:
    """
    This is our internal representation of `licenseType`'s  expression type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_licenseType
    """

    def __init__(self, value: str) -> None:
        self._value = value

    @property
    @serializable.xml_name('.')
    @serializable.json_name('expression')
    def value(self) -> str:
        """
        Value of this LicenseExpression.

        Returns:
             `str`
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    def __hash__(self) -> int:
        return hash(self._value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LicenseExpression):
            return self._value == other._value
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, LicenseExpression):
            return self._value < other._value
        if isinstance(other, DisjunctiveLicense):
            return True  # self before any DisjunctiveLicense
        return NotImplemented

    def __repr__(self) -> str:
        return f'<LicenseExpression value={self._value!r}>'


License = Union[LicenseExpression, DisjunctiveLicense]
"""TypeAlias for a union of supported license models.

- :class:`LicenseExpression`
- :class:`DisjunctiveLicense`
"""

if TYPE_CHECKING:  # pragma: no cover
    # workaround for https://github.com/python/mypy/issues/5264
    # this code path is taken when static code analysis or documentation tools runs through.
    class LicenseRepository(SortedSet[License]):
        """Collection of :class:`License`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        If you wanted a certain order, then you should also express whether the items are concat by `AND` or `OR`.
        If you wanted to do so, you should use :class:`LicenseExpression`.

        As a model, this MUST accept multiple :class:`LicenseExpression` along with
        multiple :class:`DisjunctiveLicense`, as this was an accepted in CycloneDX JSON before v1.5.
        So for modeling purposes, this is supported.
        Denormalizers/deserializers will be thankful.
        The normalization/serialization process SHOULD take care of these facts and do what is needed.
        """
else:
    class LicenseRepository(SortedSet):
        """Collection of :class:`License`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        If you wanted a certain order, then you should also express whether the items are concat by `AND` or `OR`.
        If you wanted to do so, you should use :class:`LicenseExpression`.

        As a model, this MUST accept multiple :class:`LicenseExpression` along with
        multiple :class:`DisjunctiveLicense`, as this was an accepted in CycloneDX JSON before v1.5.
        So for modeling purposes, this is supported.
        Denormalizers/deserializers will be thankful.
        The normalization/serialization process SHOULD take care of these facts and do what is needed.
        """
