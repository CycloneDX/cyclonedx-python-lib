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


__all__ = ['ModelValidator', 'ModelValidationError', 'ModelValidationErrorSeverity']

from collections.abc import Iterable
from enum import Enum
from itertools import chain
from typing import TYPE_CHECKING, Any, Union

from ..exception.model import LicenseExpressionAlongWithOthersException, UnknownComponentDependencyException
from . import ValidationError

if TYPE_CHECKING:  # pragma: no cover
    from ..model.bom import Bom, BomMetaData
    from ..model.component import Component
    from ..model.service import Service


class ModelValidationErrorSeverity(str, Enum):
    """Severity level of a :class:`ModelValidationError`."""

    ERROR = 'error'
    """BOM is structurally invalid and cannot be serialized correctly."""

    WARNING = 'warning'
    """BOM may have issues but can still be serialized; attention is recommended."""


class ModelValidationError(ValidationError):
    """Validation failed with this specific error.

    Use :attr:`~data` to access the content.
    Use :attr:`~severity` to determine how critical the issue is.
    """

    def __init__(self, data: Any,
                 severity: ModelValidationErrorSeverity = ModelValidationErrorSeverity.ERROR) -> None:
        super().__init__(data)
        self.severity = severity


class ModelValidator:
    """Perform data-model level validations to make sure we have some known data integrity."""

    def validate(self, bom: 'Bom') -> Iterable[ModelValidationError]:
        """Validate a :class:`~cyclonedx.model.bom.Bom` at the data-model level.

        Yields :class:`ModelValidationError` instances — one per issue found.
        Errors with :attr:`~ModelValidationErrorSeverity.ERROR` severity indicate structural
        invalidity; errors with :attr:`~ModelValidationErrorSeverity.WARNING` severity are
        advisory.

        This method has no side-effects: it does not mutate the ``bom`` passed in.

        :param bom: The :class:`~cyclonedx.model.bom.Bom` to validate.
        :return: An iterable of :class:`ModelValidationError` for each issue found.
        """
        from ..model.license import LicenseExpression

        # Collect all components across the BOM, including nested ones.
        all_components: set['Component'] = set(chain.from_iterable(
            c.get_all_nested_components(include_self=True) for c in bom.components
        ))
        if bom.metadata.component:
            all_components.update(
                bom.metadata.component.get_all_nested_components(include_self=True)
            )

        # 1. Make sure every bom_ref referenced in the dependency graph exists in this BOM.
        all_dependable_bom_refs = {e.bom_ref for e in chain(all_components, bom.services)}
        all_dependency_bom_refs = set(chain(
            (d.ref for d in bom.dependencies),
            chain.from_iterable(d.dependencies_as_bom_refs() for d in bom.dependencies),
        ))
        dependency_diff = all_dependency_bom_refs - all_dependable_bom_refs
        if dependency_diff:
            yield ModelValidationError(UnknownComponentDependencyException(
                'One or more Components have Dependency references to Components/Services that are not known in this '
                f'BOM. They are: {dependency_diff}'
            ))

        # 2. If the root component is set and there are other components, the root should declare
        # at least one dependency — otherwise the Dependency Graph is incomplete.
        # NOTE: guard on the component, not the BomRef — BomRef is falsy when value is None.
        if bom.metadata.component is not None and len(bom.components) > 0 and not any(
            len(d.dependencies) > 0
            for d in bom.dependencies
            if d.ref == bom.metadata.component.bom_ref
        ):
            yield ModelValidationError(
                UserWarning(
                    f'The Component this BOM is describing {bom.metadata.component.purl} has no defined '
                    'dependencies which means the Dependency Graph is incomplete - you should add direct '
                    'dependencies to this "root" Component to complete the Dependency Graph data.'
                ),
                severity=ModelValidationErrorSeverity.WARNING,
            )

        # 3. If a LicenseExpression is set, then there must be no other license.
        # see https://github.com/CycloneDX/specification/pull/205
        elem: Union['BomMetaData', 'Component', 'Service']
        for elem in chain([bom.metadata], all_components, bom.services):  # type: ignore[assignment]
            if len(elem.licenses) > 1 and any(isinstance(li, LicenseExpression) for li in elem.licenses):
                yield ModelValidationError(LicenseExpressionAlongWithOthersException(
                    f'Found LicenseExpression along with others licenses in: {elem!r}'
                ))
