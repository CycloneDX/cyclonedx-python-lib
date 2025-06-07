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

from decimal import Decimal
from unittest import TestCase

from cyclonedx.exception.model import InvalidConfidenceException
from cyclonedx.model import Copyright
from cyclonedx.model.component_evidence import (
    AnalysisTechnique,
    CallStack,
    CallStackFrame,
    ComponentEvidence,
    Identity,
    IdentityField,
    Method,
    Occurrence,
)


class TestModelComponentEvidence(TestCase):

    def test_no_params(self) -> None:
        ComponentEvidence()  # Does not raise `NoPropertiesProvidedException`

    def test_identity(self) -> None:
        identity = Identity(field=IdentityField.NAME, confidence=Decimal('1'), concluded_value='test')
        ce = ComponentEvidence(identity=[identity])
        self.assertEqual(len(ce.identity), 1)
        self.assertEqual(ce.identity.pop().field, 'name')

    def test_identity_multiple(self) -> None:
        identities = [
            Identity(field=IdentityField.NAME, confidence=Decimal('1'), concluded_value='test'),
            Identity(field=IdentityField.VERSION, confidence=Decimal('0.8'), concluded_value='1.0.0')
        ]
        ce = ComponentEvidence(identity=identities)
        self.assertEqual(len(ce.identity), 2)

    def test_identity_with_methods(self) -> None:
        """Test identity with analysis methods"""
        methods = [
            Method(
                technique=AnalysisTechnique.BINARY_ANALYSIS,  # Changed order to test sorting
                confidence=Decimal('0.9'),
                value='Found in binary'
            ),
            Method(
                technique=AnalysisTechnique.SOURCE_CODE_ANALYSIS,
                confidence=Decimal('0.8'),
                value='Found in source'
            )
        ]
        identity = Identity(field='name', confidence=Decimal('1'), methods=methods)
        self.assertEqual(len(identity.methods), 2)
        sorted_methods = sorted(methods)  # Methods should be sorted by technique name
        self.assertEqual(list(identity.methods), sorted_methods)

        # Verify first method
        method = sorted_methods[0]
        self.assertEqual(method.technique, AnalysisTechnique.BINARY_ANALYSIS)
        self.assertEqual(method.confidence, Decimal('0.9'))
        self.assertEqual(method.value, 'Found in binary')

    def test_method_sorting(self) -> None:
        """Test that methods are properly sorted by technique value"""
        methods = [
            Method(technique=AnalysisTechnique.SOURCE_CODE_ANALYSIS, confidence=Decimal('0.8')),
            Method(technique=AnalysisTechnique.BINARY_ANALYSIS, confidence=Decimal('0.9')),
            Method(technique=AnalysisTechnique.ATTESTATION, confidence=Decimal('1.0'))
        ]

        sorted_methods = sorted(methods)
        self.assertEqual(sorted_methods[0].technique, AnalysisTechnique.ATTESTATION)
        self.assertEqual(sorted_methods[1].technique, AnalysisTechnique.BINARY_ANALYSIS)
        self.assertEqual(sorted_methods[2].technique, AnalysisTechnique.SOURCE_CODE_ANALYSIS)

    def test_invalid_method_confidence(self) -> None:
        """Test that invalid confidence raises ValueError"""
        with self.assertRaises(InvalidConfidenceException):
            Method(technique=AnalysisTechnique.FILENAME, confidence=Decimal('1.5'))

    def test_occurrences(self) -> None:
        occurrence = Occurrence(location='/path/to/file', line=42)
        ce = ComponentEvidence(occurrences=[occurrence])
        self.assertEqual(len(ce.occurrences), 1)
        self.assertEqual(ce.occurrences.pop().line, 42)

    def test_callstack(self) -> None:
        frame = CallStackFrame(
            package='com.example',
            module='app',
            function='main'
        )
        stack = CallStack(frames=[frame])
        ce = ComponentEvidence(callstack=stack)
        self.assertIsNotNone(ce.callstack)
        self.assertEqual(len(ce.callstack.frames), 1)

    def test_licenses(self) -> None:
        from cyclonedx.model.license import DisjunctiveLicense
        license = DisjunctiveLicense(id='MIT')
        ce = ComponentEvidence(licenses=[license])
        self.assertEqual(len(ce.licenses), 1)

    def test_copyright(self) -> None:
        copyright = Copyright(text='(c) 2023')
        ce = ComponentEvidence(copyright=[copyright])
        self.assertEqual(len(ce.copyright), 1)
        self.assertEqual(ce.copyright.pop().text, '(c) 2023')

    def test_full_evidence(self) -> None:
        # Test with all fields populated
        identity = Identity(field=IdentityField.NAME, confidence=Decimal('1'), concluded_value='test')
        occurrence = Occurrence(location='/path/to/file', line=42)
        frame = CallStackFrame(module='app', function='main', line=1)
        stack = CallStack(frames=[frame])
        from cyclonedx.model.license import DisjunctiveLicense
        license = DisjunctiveLicense(id='MIT')
        copyright = Copyright(text='(c) 2023')

        ce = ComponentEvidence(
            identity=[identity],
            occurrences=[occurrence],
            callstack=stack,
            licenses=[license],
            copyright=[copyright]
        )

        self.assertEqual(len(ce.identity), 1)
        self.assertEqual(len(ce.occurrences), 1)
        self.assertIsNotNone(ce.callstack)
        self.assertEqual(len(ce.callstack.frames), 1)
        self.assertEqual(len(ce.licenses), 1)
        self.assertEqual(len(ce.copyright), 1)

    def test_full_evidence_with_complete_stack(self) -> None:
        identity = Identity(field=IdentityField.NAME, confidence=Decimal('1'), concluded_value='test')
        occurrence = Occurrence(location='/path/to/file', line=42)

        frame = CallStackFrame(
            package='com.example',
            module='app',
            function='main',
            parameters=['arg1', 'arg2'],
            line=1,
            column=10,
            full_filename='/path/to/file.py'
        )
        stack = CallStack(frames=[frame])

        from cyclonedx.model.license import DisjunctiveLicense
        license = DisjunctiveLicense(id='MIT')
        copyright = Copyright(text='(c) 2023')

        ce = ComponentEvidence(
            identity=[identity],
            occurrences=[occurrence],
            callstack=stack,
            licenses=[license],
            copyright=[copyright]
        )

        self.assertEqual(len(ce.identity), 1)
        self.assertEqual(len(ce.occurrences), 1)
        self.assertIsNotNone(ce.callstack)
        self.assertEqual(len(ce.callstack.frames), 1)
        self.assertEqual(ce.callstack.frames.pop().package, 'com.example')
        self.assertEqual(len(ce.licenses), 1)
        self.assertEqual(len(ce.copyright), 1)

    def test_same_1(self) -> None:
        ce_1 = ComponentEvidence(copyright=[Copyright(text='Commercial')])
        ce_2 = ComponentEvidence(copyright=[Copyright(text='Commercial')])
        self.assertEqual(hash(ce_1), hash(ce_2))
        self.assertTrue(ce_1 == ce_2)

    def test_same_2(self) -> None:
        ce_1 = ComponentEvidence(copyright=[Copyright(text='Commercial'), Copyright(text='Commercial 2')])
        ce_2 = ComponentEvidence(copyright=[Copyright(text='Commercial 2'), Copyright(text='Commercial')])
        self.assertEqual(hash(ce_1), hash(ce_2))
        self.assertTrue(ce_1 == ce_2)

    def test_not_same_1(self) -> None:
        ce_1 = ComponentEvidence(copyright=[Copyright(text='Commercial')])
        ce_2 = ComponentEvidence(copyright=[Copyright(text='Commercial 2')])
        self.assertNotEqual(hash(ce_1), hash(ce_2))
        self.assertFalse(ce_1 == ce_2)


class TestModelCallStackFrame(TestCase):

    def test_fields(self) -> None:
        # Test CallStackFrame with required fields
        frame = CallStackFrame(
            package='com.example',
            module='app',
            function='main',
            parameters=['arg1', 'arg2'],
            line=1,
            column=10,
            full_filename='/path/to/file.py'
        )
        self.assertEqual(frame.package, 'com.example')
        self.assertEqual(frame.module, 'app')
        self.assertEqual(frame.function, 'main')
        self.assertEqual(len(frame.parameters), 2)
        self.assertEqual(frame.line, 1)
        self.assertEqual(frame.column, 10)
        self.assertEqual(frame.full_filename, '/path/to/file.py')

    def test_module_required(self) -> None:
        """Test that module is the only required field"""
        frame = CallStackFrame(module='app')  # Only mandatory field
        self.assertEqual(frame.module, 'app')
        self.assertIsNone(frame.package)
        self.assertIsNone(frame.function)
        self.assertEqual(len(frame.parameters), 0)
        self.assertIsNone(frame.line)
        self.assertIsNone(frame.column)
        self.assertIsNone(frame.full_filename)
