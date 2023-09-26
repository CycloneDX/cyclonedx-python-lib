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

__all__ = ['ModelValidator']

import warnings
from itertools import chain
from typing import TYPE_CHECKING, Union, Set

from exception.model import UnknownComponentDependencyException, LicenseExpressionAlongWithOthersException

if TYPE_CHECKING:
    from ..model.bom import Bom, BomMetaData
    from ..model.component import Component
    from ..model.service import Service


class ModelValidator:
    """Perform data-model level validations to make sure we have some known data integrity. """

    def validate_bom(self, bom: 'Bom') -> bool:
        # 0. Make sure all Dependable have a Dependency entry
        if bom.metadata.component:
            bom.register_dependency(target=bom.metadata.component)
        for _c in bom.components:
            bom.register_dependency(target=_c)
        for _s in bom.services:
            bom.register_dependency(target=_s)

        all_components: Set['Component'] = set(chain.from_iterable(
            c.get_all_nested_components(include_self=True) for c in bom.components))
        if bom.metadata.component:
            all_components.add(bom.metadata.component)

        # 1. Make sure dependencies are all in this Bom.
        all_dependable_bom_refs = set(e.bom_ref for e in chain(all_components, bom.services))
        all_dependency_bom_refs = set(chain.from_iterable(d.dependencies_as_bom_refs() for d in bom.dependencies))
        dependency_diff = all_dependency_bom_refs - all_dependable_bom_refs
        if len(dependency_diff) > 0:
            raise UnknownComponentDependencyException(
                f'One or more Components have Dependency references to Components/Services that are not known in this '
                f'BOM. They are: {dependency_diff}')

        # 2. if root component is set: dependencies should exist for the Component this BOM is describing
        meta_bom_ref = bom.metadata.component.bom_ref if bom.metadata.component else None
        if meta_bom_ref and not any(len(d.dependencies) for d in bom.dependencies if d.ref == meta_bom_ref):
            warnings.warn(
                f'The Component this BOM is describing {bom.metadata.component.purl} has no defined dependencies '
                f'which means the Dependency Graph is incomplete - you should add direct dependencies to this '
                f'"root" Component to complete the Dependency Graph data.',
                UserWarning)

        # 3. If a LicenseExpression is set, then there must be no other license.
        # see https://github.com/CycloneDX/specification/pull/205
        elem: Union['BomMetaData', 'Component', 'Service']
        for elem in chain([bom.metadata], all_components, bom.services):  # type: ignore[assignment]
            if len(elem.licenses) > 1 and any(li.expression for li in elem.licenses):
                raise LicenseExpressionAlongWithOthersException(
                    f'Found LicenseExpression along with others licenses in: {elem!r}')

        return True
