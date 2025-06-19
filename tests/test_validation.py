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


import unittest
from itertools import product

from ddt import data, ddt, named_data, unpack

from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator, squeeze

UNDEFINED_FORMAT_VERSION = {
    (OutputFormat.JSON, SchemaVersion.V1_1),
    (OutputFormat.JSON, SchemaVersion.V1_0),
}


@ddt
class TestGetSchemabasedValidator(unittest.TestCase):

    @named_data(*([f'{f.name} {v.name}', f, v]
                  for f, v
                  in product(OutputFormat, SchemaVersion)
                  if (f, v) not in UNDEFINED_FORMAT_VERSION))
    @unpack
    def test_as_expected(self, of: OutputFormat, sv: SchemaVersion) -> None:
        validator = make_schemabased_validator(of, sv)
        self.assertIs(validator.output_format, of)
        self.assertIs(validator.schema_version, sv)

    @data(
        *(('foo', sv, (ValueError, 'Unexpected output_format')) for sv in SchemaVersion),
        *((f, v, (ValueError, 'Unsupported schema_version')) for f, v in UNDEFINED_FORMAT_VERSION)
    )
    @unpack
    def test_fails_on_wrong_args(self, of: OutputFormat, sv: SchemaVersion, raises_regex: tuple) -> None:
        with self.assertRaisesRegex(*raises_regex):
            make_schemabased_validator(of, sv)


class TestSqueeze(unittest.TestCase):

    def test_squeeze_size_minus_one_returns_original_text(self) -> None:
        """Test that size=-1 returns original text unchanged."""
        self.assertEqual(squeeze('hello world', -1), 'hello world')
        self.assertEqual(squeeze('', -1), '')
        self.assertEqual(squeeze('a', -1), 'a')
        self.assertEqual(squeeze('very long text that would normally be squeezed', -1),
                         'very long text that would normally be squeezed')

    def test_squeeze_size_zero_returns_empty_text(self) -> None:
        """Test that size=-1 returns original text unchanged."""
        self.assertEqual(squeeze('hello world', 0, ''), '')
        self.assertEqual(squeeze('', 0, ''), '')

    def test_squeeze_text_shorter_than_or_equal_size_returns_original(self) -> None:
        """Test that text shorter than or equal to size returns original text."""
        self.assertEqual(squeeze('hello', 10), 'hello')
        self.assertEqual(squeeze('hello', 5), 'hello')
        self.assertEqual(squeeze('', 5), '')
        self.assertEqual(squeeze('a', 5), 'a')
        self.assertEqual(squeeze('ab', 10), 'ab')

    def test_squeeze_with_default_replacement(self) -> None:
        """Test squeezing with default ' ... ' replacement."""
        self.assertEqual(squeeze('hello world', 8), 'h ... ld')
        self.assertEqual(squeeze('hello world', 7), 'h ... d')
        self.assertEqual(squeeze('hello world', 9), 'he ... ld')
        self.assertEqual(squeeze('hello world', 10), 'he ... rld')
        self.assertEqual(squeeze('hello world', 11), 'hello world')

    def test_squeeze_with_custom_replacement(self) -> None:
        """Test squeezing with custom replacement strings."""
        self.assertEqual(squeeze('hello world', 8, '..'), 'hel..rld')
        self.assertEqual(squeeze('hello world', 7, '..'), 'he..rld')
        self.assertEqual(squeeze('hello world', 9, '---'), 'hel---rld')
        self.assertEqual(squeeze('hello world', 10, 'XX'), 'hellXXorld')

    def test_squeeze_with_single_character_replacement(self) -> None:
        """Test squeezing with single character replacement."""
        self.assertEqual(squeeze('hello world', 5, '*'), 'he*ld')
        self.assertEqual(squeeze('hello world', 6, '*'), 'he*rld')
        self.assertEqual(squeeze('hello world', 7, '*'), 'hel*rld')

    def test_squeeze_with_empty_replacement(self) -> None:
        """Test squeezing with empty replacement string."""
        self.assertEqual(squeeze('hello world', 5, ''), 'herld')
        self.assertEqual(squeeze('hello world', 6, ''), 'helrld')
        self.assertEqual(squeeze('hello world', 7, ''), 'helorld')

    def test_squeeze_replacement_equals_target_size(self) -> None:
        """Test when replacement string equals the target size."""
        self.assertEqual(squeeze('hello world', 4, '....'), '....')
        self.assertEqual(squeeze('hello world', 3, '***'), '***')

    def test_squeeze_very_short_target_sizes(self) -> None:
        """Test edge cases with very short target sizes."""
        self.assertEqual(squeeze('hello world', 5, '.'), 'he.ld')
        self.assertEqual(squeeze('hello world', 6, '.'), 'he.rld')
        self.assertEqual(squeeze('hello world', 1, 'X'), 'X')

    def test_squeeze_with_long_text(self) -> None:
        """Test squeezing with very long text."""
        long_text = 'a' * 100
        result = squeeze(long_text, 10, '...')
        self.assertEqual(len(result), 10)
        self.assertEqual(result, 'aaa...aaaa')

        # Test with different replacement
        result2 = squeeze(long_text, 8, '--')
        self.assertEqual(len(result2), 8)
        self.assertEqual(result2, 'aaa--aaa')

    def test_squeeze_size_distribution_even(self) -> None:
        """Test size distribution when remaining space is even."""
        # size=8, replacement="--" (len=2), remaining=6, left=3, right=3
        self.assertEqual(squeeze('abcdefghijk', 8, '--'), 'abc--ijk')
        # size=10, replacement="...." (len=4), remaining=6, left=3, right=3
        self.assertEqual(squeeze('abcdefghijk', 10, '....'), 'abc....ijk')

    def test_squeeze_size_distribution_odd(self) -> None:
        """Test size distribution when remaining space is odd."""
        # size=9, replacement="--" (len=2), remaining=7, left=3, right=4
        self.assertEqual(squeeze('abcdefghijk', 9, '--'), 'abc--hijk')
        # size=11, replacement="..." (len=3), remaining=8, left=4, right=4
        self.assertEqual(squeeze('abcdefghijk', 11, '...'), 'abcdefghijk')

    def test_squeeze_raises_error_when_replacement_too_long(self) -> None:
        """Test that ValueError is raised when replacement is longer than target size."""
        with self.assertRaises(ValueError) as context:
            squeeze('hello world', 3, ' ... ')
        self.assertIn('size = 3 < len(replacement) = 5', str(context.exception))

        with self.assertRaises(ValueError) as context:
            squeeze('hello world', 2, 'abc')
        self.assertIn('size = 2 < len(replacement) = 3', str(context.exception))

        with self.assertRaises(ValueError) as context:
            squeeze('hello world', 1, 'ab')
        self.assertIn('size = 1 < len(replacement) = 2', str(context.exception))

    def test_squeeze_error_when_replacement_long_but_no_squeeze_needed(self) -> None:
        """Test that no error is raised when replacement is long but text doesn't need squeezing."""
        # Text is shorter than size, so no squeezing would occur,
        # yet, the replacement is longer than the requested size, so error is raised
        with self.assertRaises(ValueError) as context:
            self.assertEqual(squeeze('abc', 10, 'very long replacement'), 'abc')
        self.assertIn('size = 10 < len(replacement) = 21', str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.assertEqual(squeeze('', 3, 'abcd'), '')
        self.assertIn('size = 3 < len(replacement) = 4', str(context.exception))


if __name__ == '__main__':
    unittest.main()
