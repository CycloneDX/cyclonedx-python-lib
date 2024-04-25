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
!!! ALL SYMBOLS IN HERE ARE INTERNAL.
Everything might change without any notice.
"""

from itertools import zip_longest
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

if TYPE_CHECKING:  # pragma: no cover
    from packageurl import PackageURL


class ComparableTuple(Tuple[Optional[Any], ...]):
    """
    Allows comparison of tuples, allowing for None values.
    """

    def __lt__(self, other: Any) -> bool:
        for s, o in zip_longest(self, other):
            if s == o:
                continue
            # the idea is to have any consistent order, not necessarily "natural" order.
            if s is None:
                return False
            if o is None:
                return True
            return True if s < o else False
        return False

    def __gt__(self, other: Any) -> bool:
        for s, o in zip_longest(self, other):
            if s == o:
                continue
            # the idea is to have any consistent order, not necessarily "natural" order.
            if s is None:
                return True
            if o is None:
                return False
            return True if s > o else False
        return False


class ComparableDict:
    """
    Allows comparison of dictionaries, allowing for missing/None values.
    """

    def __init__(self, dict_: Dict[Any, Any]) -> None:
        self._dict = dict_

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, ComparableDict):
            return True
        keys = sorted(self._dict.keys() | other._dict.keys())
        return ComparableTuple(self._dict.get(k) for k in keys) \
            < ComparableTuple(other._dict.get(k) for k in keys)

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, ComparableDict):
            return False
        keys = sorted(self._dict.keys() | other._dict.keys())
        return ComparableTuple(self._dict.get(k) for k in keys) \
            > ComparableTuple(other._dict.get(k) for k in keys)


class ComparablePackageURL(ComparableTuple):
    """
    Allows comparison of PackageURL, allowing for qualifiers.
    """

    def __new__(cls, purl: 'PackageURL') -> 'ComparablePackageURL':
        return super().__new__(
            ComparablePackageURL, (
                purl.type,
                purl.namespace,
                purl.version,
                ComparableDict(purl.qualifiers) if isinstance(purl.qualifiers, dict) else purl.qualifiers,
                purl.subpath
            ))
