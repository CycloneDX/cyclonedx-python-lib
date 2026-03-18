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
from cyclonedx.validation.model import ModelValidator


class TestModelValidator(TestCase):
    def test_validate_multiple_errors(self) -> None:
        bom = Bom()
        # Error 1: Component with multiple licenses including expression
        comp = Component(name='test', version='1.0', bom_ref='test-comp')
        comp.licenses.update([
            DisjunctiveLicense(id='MIT'),
            LicenseExpression(value='Apache-2.0 OR MIT')
        ])
        bom.components.add(comp)

        # Error 2: Unknown dependency reference
        bom.dependencies.add(Dependency('test-comp', dependencies=[Dependency('non-existent-ref')]))

        validator = ModelValidator()
        errors = list(validator.validate(bom))

        self.assertEqual(len(errors), 2)
        error_types = [type(e.data) for e in errors]
        self.assertIn(UnknownComponentDependencyException, error_types)
        self.assertIn(LicenseExpressionAlongWithOthersException, error_types)

    def test_validate_clean_bom(self) -> None:
        bom = Bom()
        bom.metadata.component = Component(name='root', version='1.0', bom_ref='root')
        validator = ModelValidator()
        errors = list(validator.validate(bom))
        self.assertEqual(len(errors), 0)

    def test_bom_validate_deprecated_behavior(self) -> None:
        bom = Bom()
        bom.metadata.component = Component(name='root', version='1.0', bom_ref='root')

        # Verify side effect: register_dependency is called by Bom.validate
        self.assertEqual(len(bom.dependencies), 0)
        with self.assertWarns(DeprecationWarning):
            bom.validate()
        self.assertEqual(len(bom.dependencies), 1)
        self.assertEqual(next(iter(bom.dependencies)).ref.value, 'root')

    def test_model_validator_no_side_effects(self) -> None:
        bom = Bom()
        bom.metadata.component = Component(name='root', version='1.0', bom_ref='root')

        # Verify NO side effect: ModelValidator should not call register_dependency
        self.assertEqual(len(bom.dependencies), 0)
        validator = ModelValidator()
        list(validator.validate(bom))
        self.assertEqual(len(bom.dependencies), 0)
