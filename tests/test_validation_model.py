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

from unittest import TestCase

from cyclonedx.exception.model import LicenseExpressionAlongWithOthersException, UnknownComponentDependencyException
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.model.dependency import Dependency
from cyclonedx.model.license import DisjunctiveLicense, LicenseExpression
from cyclonedx.validation.model import ModelValidationErrorSeverity, ModelValidator


class TestModelValidator(TestCase):

    def test_validate_clean_bom(self) -> None:
        bom = Bom()
        bom.metadata.component = Component(name='root', version='1.0', bom_ref='root')
        errors = list(ModelValidator().validate(bom))
        self.assertEqual(0, len(errors))

    def test_validate_multiple_errors_have_error_severity(self) -> None:
        bom = Bom()
        comp = Component(name='test', version='1.0', bom_ref='test-comp')
        comp.licenses.update([
            DisjunctiveLicense(id='MIT'),
            LicenseExpression(value='Apache-2.0 OR MIT'),
        ])
        bom.components.add(comp)
        bom.dependencies.add(Dependency('test-comp', dependencies=[Dependency('non-existent-ref')]))

        errors = list(ModelValidator().validate(bom))

        self.assertEqual(2, len(errors))
        error_types = [type(e.data) for e in errors]
        self.assertIn(UnknownComponentDependencyException, error_types)
        self.assertIn(LicenseExpressionAlongWithOthersException, error_types)
        for error in errors:
            self.assertEqual(ModelValidationErrorSeverity.ERROR, error.severity)

    def test_validate_unknown_toplevel_dependency_ref_detected(self) -> None:
        """Regression: top-level d.ref values must also be validated against known BOM components."""
        bom = Bom()
        comp = Component(name='real', version='1.0', bom_ref='real-comp')
        bom.components.add(comp)
        # 'ghost-ref' is not in the BOM at all
        bom.dependencies.add(Dependency('ghost-ref'))

        errors = list(ModelValidator().validate(bom))

        error_types = [type(e.data) for e in errors]
        self.assertIn(UnknownComponentDependencyException, error_types)

    def test_validate_incomplete_dependency_graph_yields_warning(self) -> None:
        """Check #2 must yield a WARNING-severity error, not a Python UserWarning."""
        import warnings as _warnings
        bom = Bom()
        bom.metadata.component = Component(name='root', version='1.0', bom_ref='root')
        bom.components.add(Component(name='dep', version='1.0', bom_ref='dep'))

        with _warnings.catch_warnings():
            _warnings.simplefilter('error')  # turn any Python warning into an error
            errors = list(ModelValidator().validate(bom))  # must not raise

        warning_errors = [e for e in errors if e.severity == ModelValidationErrorSeverity.WARNING]
        self.assertEqual(1, len(warning_errors))
        self.assertIsInstance(warning_errors[0].data, UserWarning)

    def test_validate_nested_root_component_license_invalid(self) -> None:
        """Regression: nested components under metadata.component must be license-checked."""
        bom = Bom()
        root = Component(name='root', version='1.0', bom_ref='root')
        nested = Component(name='nested', version='1.0', bom_ref='nested')
        nested.licenses.update([
            DisjunctiveLicense(id='MIT'),
            LicenseExpression(value='Apache-2.0 OR MIT'),
        ])
        root.components.add(nested)
        bom.metadata.component = root

        errors = list(ModelValidator().validate(bom))

        error_types = [type(e.data) for e in errors]
        self.assertIn(LicenseExpressionAlongWithOthersException, error_types)

    def test_validate_no_side_effects(self) -> None:
        bom = Bom()
        bom.metadata.component = Component(name='root', version='1.0', bom_ref='root')
        self.assertEqual(0, len(bom.dependencies))
        list(ModelValidator().validate(bom))
        self.assertEqual(0, len(bom.dependencies))
