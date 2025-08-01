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

from collections.abc import Generator
from glob import iglob
from itertools import chain
from os.path import join
from unittest import TestCase

from ddt import data, ddt, idata, unpack

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation.json import JsonStrictValidator, JsonValidator
from tests import OWN_DATA_DIRECTORY, SCHEMA_TESTDATA_DIRECTORY, DpTuple

UNSUPPORTED_SCHEMA_VERSIONS = {SchemaVersion.V1_0, SchemaVersion.V1_1, }


def _dp_sv_tf(valid: bool) -> Generator:
    prefix = 'valid-' if valid else 'invalid-'
    return (
        DpTuple((sv, tf))
        for sv in SchemaVersion if sv not in UNSUPPORTED_SCHEMA_VERSIONS
        for tf in iglob(join(SCHEMA_TESTDATA_DIRECTORY, sv.to_version(), f'{prefix}*.json'))
    )


def _dp_sv_own(valid: bool) -> Generator:
    return (
        DpTuple((sv, tf))
        for sv in SchemaVersion if sv not in UNSUPPORTED_SCHEMA_VERSIONS
        for tf in iglob(join(OWN_DATA_DIRECTORY, 'json', sv.to_version(), '*.json')) if ('invalid-' in tf) != valid
    )


@ddt
class TestJsonValidator(TestCase):

    @idata(sv for sv in SchemaVersion if sv not in UNSUPPORTED_SCHEMA_VERSIONS)
    def test_validator_as_expected(self, schema_version: SchemaVersion) -> None:
        validator = JsonValidator(schema_version)
        self.assertIs(validator.schema_version, schema_version)
        self.assertIs(validator.output_format, OutputFormat.JSON)

    @idata(UNSUPPORTED_SCHEMA_VERSIONS)
    def test_throws_with_unsupported_schema_version(self, schema_version: SchemaVersion) -> None:
        with self.assertRaisesRegex(ValueError, 'Unsupported schema_version'):
            JsonValidator(schema_version)

    @idata(chain(
        _dp_sv_tf(True),
        _dp_sv_own(True)
    ))
    @unpack
    def test_validate_no_none(self, schema_version: SchemaVersion, test_data_file: str) -> None:
        validator = JsonValidator(schema_version)
        with open(join(test_data_file)) as tdfh:
            test_data = tdfh.read()
        try:
            validation_error = validator.validate_str(test_data)
        except MissingOptionalDependencyException:
            self.skipTest('MissingOptionalDependencyException')
        self.assertIsNone(validation_error)

    @idata(chain(
        _dp_sv_tf(False),
        _dp_sv_own(False)
    ))
    @unpack
    def test_validate_expected_error_one(self, schema_version: SchemaVersion, test_data_file: str) -> None:
        validator = JsonValidator(schema_version)
        with open(join(test_data_file)) as tdfh:
            test_data = tdfh.read()
        try:
            validation_error = validator.validate_str(test_data)
        except MissingOptionalDependencyException:
            self.skipTest('MissingOptionalDependencyException')
        self.assertIsNotNone(validation_error)
        self.assertIsNotNone(validation_error.data)

    @idata(chain(
        _dp_sv_tf(False),
        _dp_sv_own(False)
    ))
    @unpack
    def test_validate_expected_error_iterator(self, schema_version: SchemaVersion, test_data_file: str) -> None:
        validator = JsonValidator(schema_version)
        with open(join(test_data_file)) as tdfh:
            test_data = tdfh.read()
        try:
            validation_errors = validator.validate_str(test_data, all_errors=True)
        except MissingOptionalDependencyException:
            self.skipTest('MissingOptionalDependencyException')
        self.assertIsNotNone(validation_errors)
        validation_errors = tuple(validation_errors)
        self.assertGreater(len(validation_errors), 0)
        for validation_error in validation_errors:
            self.assertIsNotNone(validation_error.data)


@ddt
class TestJsonStrictValidator(TestCase):

    @data(*UNSUPPORTED_SCHEMA_VERSIONS)
    def test_throws_with_unsupported_schema_version(self, schema_version: SchemaVersion) -> None:
        with self.assertRaisesRegex(ValueError, 'Unsupported schema_version'):
            JsonStrictValidator(schema_version)

    @idata(chain(
        _dp_sv_tf(True),
        _dp_sv_own(True)
    ))
    @unpack
    def test_validate_no_none(self, schema_version: SchemaVersion, test_data_file: str) -> None:
        validator = JsonStrictValidator(schema_version)
        with open(join(test_data_file)) as tdfh:
            test_data = tdfh.read()
        try:
            validation_error = validator.validate_str(test_data)
        except MissingOptionalDependencyException:
            self.skipTest('MissingOptionalDependencyException')
        self.assertIsNone(validation_error)

    @idata(chain(
        _dp_sv_tf(False),
        _dp_sv_own(False)
    ))
    @unpack
    def test_validate_expected_error_one(self, schema_version: SchemaVersion, test_data_file: str) -> None:
        validator = JsonStrictValidator(schema_version)
        with open(join(test_data_file)) as tdfh:
            test_data = tdfh.read()
        try:
            validation_error = validator.validate_str(test_data)
        except MissingOptionalDependencyException:
            self.skipTest('MissingOptionalDependencyException')
        self.assertIsNotNone(validation_error)
        self.assertIsNotNone(validation_error.data)

    @idata(chain(
        _dp_sv_tf(False),
        _dp_sv_own(False)
    ))
    @unpack
    def test_validate_expected_error_iterator(self, schema_version: SchemaVersion, test_data_file: str) -> None:
        validator = JsonValidator(schema_version)
        with open(join(test_data_file)) as tdfh:
            test_data = tdfh.read()
        try:
            validation_errors = validator.validate_str(test_data, all_errors=True)
        except MissingOptionalDependencyException:
            self.skipTest('MissingOptionalDependencyException')
        self.assertIsNotNone(validation_errors)
        validation_errors = tuple(validation_errors)
        self.assertGreater(len(validation_errors), 0)
        for validation_error in validation_errors:
            self.assertIsNotNone(validation_error.data)
