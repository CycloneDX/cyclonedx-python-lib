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

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore


class Dependency:
    def __init__(self, purl: PackageURL = None) -> None:
        self.purl = purl

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Dependency):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.purl.name, self.purl.version, self.purl
        ))

    def __repr__(self) -> str:
        return f'<Dependency name={self.purl.name}, version={self.purl.version}>'
