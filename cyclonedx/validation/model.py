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


__all__ = ['ModelValidator', 'ModelValidationError']

import warnings
from collections.abc import Iterable
from itertools import chain
from typing import TYPE_CHECKING, Set, Union

from ..exception.model import LicenseExpressionAlongWithOthersException, UnknownComponentDependencyException
from . import ValidationError

# REMOVED: from ..model.license import LicenseExpression

if TYPE_CHECKING:  # pragma: no cover
    from ..model.bom import Bom, BomMetaData
    from ..model.component import Component
    from ..model.service import Service


class ModelValidationError(ValidationError):
    """Validation failed with this specific error.

    Use :attr:`~data` to access the content.
    """
    pass


class ModelValidator:
    """Perform data-model level validations to make sure we have some known data integrity."""

    def validate(self, bom: 'Bom') -> Iterable[ModelValidationError]:
        """
        Perform data-model level validations to make sure we have some known data integrity
        prior to attempting output of a `Bom`.

        :param bom: The `Bom` to validate.
        :return: An iterable of `ModelValidationError` if any issues are found.
        """
        # 1. Make sure dependencies are all in this Bom.
        all_components: set['Component'] = set(chain.from_iterable(
            c.get_all_nested_components(include_self=True) for c in bom.components))
        if bom.metadata.component:
            all_components.add(bom.metadata.component)

        all_dependable_bom_refs = {e.bom_ref for e in chain(all_components, bom.services)}
        all_dependency_bom_refs = set(chain.from_iterable(d.dependencies_as_bom_refs() for d in bom.dependencies))
        dependency_diff = all_dependency_bom_refs - all_dependable_bom_refs
        if len(dependency_diff) > 0:
            yield ModelValidationError(UnknownComponentDependencyException(
                'One or more Components have Dependency references to Components/Services that are not known in this '
                f'BOM. They are: {dependency_diff}'))

        # 2. if root component is set: dependencies should exist for the Component this BOM is describing
        meta_bom_ref = bom.metadata.component.bom_ref if bom.metadata.component else None
        if meta_bom_ref and len(bom.components) > 0 and not any(
            len(d.dependencies) > 0 for d in bom.dependencies if d.ref == meta_bom_ref
        ):
            warnings.warn(
                f'The Component this BOM is describing {bom.metadata.component.purl} has no defined dependencies '
                'which means the Dependency Graph is incomplete - you should add direct dependencies to this '
                '"root" Component to complete the Dependency Graph data.',
                category=UserWarning, stacklevel=2
            )

        # 3. If a LicenseExpression is set, then there must be no other license.
        # see https://github.com/CycloneDX/specification/pull/205
        from ..model.license import LicenseExpression
        elem: Union['BomMetaData', 'Component', 'Service']
        for elem in chain([bom.metadata], all_components, bom.services):  # type: ignore[assignment]
            if len(elem.licenses) > 1 and any(isinstance(li, LicenseExpression) for li in elem.licenses):
                yield ModelValidationError(LicenseExpressionAlongWithOthersException(
                    f'Found LicenseExpression along with others licenses in: {elem!r}'))
