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

"""
Set of classes and methods which allow for quick creation of a Bom instance from your environment or Python project.

Use a Parser instead of programmatically creating a Bom as a developer.

Different parsers support population of different information about your dependencies due to how information is
obtained and limitations of what information is available to each Parser. The table below explains coverage as to what
information is obtained by each set of Parsers. It does NOT guarantee the information is output in the resulting
CycloneDX BOM document.

| Data Path | Environment | Pipenv | Poetry | Requirements |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| `component.supplier` | N (if in package METADATA) | N/A | | |
| `component.author` | Y (if in package METADATA) | N/A | | |
| `component.publisher` | N (if in package METADATA) | N/A | | |
| `component.group` | - | - | - | - |
| `component.name` | Y | Y | Y | Y |
| `component.version` | Y | Y | Y | Y |
| `component.description` | N | N/A | N | N/A |
| `component.scope` | N | N/A | N | N/A |
| `component.hashes` | N/A | Y - see below (1) | Y - see below (1) | N/A |
| `component.licenses` | Y (if in package METADATA) | N/A | N/A | N/A |
| `component.copyright` | N (if in package METADATA) | N/A | N/A | N/A |
| `component.cpe` | _Deprecated_ | _Deprecated_ | _Deprecated_ | _Deprecated_ |
| `component.purl` | Y | Y | Y | Y |
| `component.swid` | N/A | N/A | N/A | N/A |
| `component.modified` | _Deprecated_ | _Deprecated_ | _Deprecated_ | _Deprecated_ |
| `component.pedigree` | N/A | N/A | N/A | N/A |
| `component.externalReferences` | N/A | Y - see below (1) | Y - see below (1) | N/A |
| `component.properties` | N/A | N/A | N/A | N/A |
| `component.components` | N/A | N/A | N/A | N/A |
| `component.evidence` | N/A | N/A | N/A | N/A |

**Legend:**

* `Y`: YES with any caveat states.
* `N`: Not currently supported, but support believed to be possible.
* `N/A`: Not supported and not deemed possible (i.e. the Parser would never be able to reliably determine this info).
* `-`: Deemed not applicable to the Python ecosystem.

**Notes:**

1. Python packages are regularly available as both `.whl` and `.tar.gz` packages. This means for that for a given
    package and version multiple artefacts are possible - which would mean multiple hashes are possible. CycloneDX
    supports only a single set of hashes identifying a single artefact at `component.hashes`. To cater for this
    situation in Python, we add the hashes to `component.externalReferences`, as we cannot determine which package was
    actually obtained and installed to meet a given dependency.

"""

from abc import ABC
from typing import List

from ..model.component import Component


class ParserWarning:
    _item: str
    _warning: str

    def __init__(self, item: str, warning: str):
        self._item = item
        self._warning = warning

    def get_item(self) -> str:
        return self._item

    def get_warning_message(self) -> str:
        return self._warning

    def __repr__(self):
        return '<ParserWarning item=\'{}\'>'.format(self._item)


class BaseParser(ABC):
    _components: List[Component] = []
    _warnings: List[ParserWarning] = []

    def __init__(self):
        self._components.clear()
        self._warnings.clear()

    def component_count(self) -> int:
        return len(self._components)

    def get_components(self) -> List[Component]:
        return self._components

    def get_warnings(self) -> List[ParserWarning]:
        return self._warnings

    def has_warnings(self) -> bool:
        return len(self._warnings) > 0
