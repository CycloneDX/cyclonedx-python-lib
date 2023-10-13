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


from typing import TYPE_CHECKING, Literal, Union, overload

from ..schema import OutputFormat

if TYPE_CHECKING:  # pragma: no cover
    from ..schema import SchemaVersion
    from . import BaseSchemaBasedValidator
    from .json import JsonValidator
    from .xml import XmlValidator


@overload
def get_instance(output_format: Literal[OutputFormat.JSON], schema_version: 'SchemaVersion'
                 ) -> 'JsonValidator':
    ...


@overload
def get_instance(output_format: Literal[OutputFormat.XML], schema_version: 'SchemaVersion'
                 ) -> 'XmlValidator':
    ...


@overload
def get_instance(output_format: OutputFormat, schema_version: 'SchemaVersion'
                 ) -> Union['JsonValidator', 'XmlValidator']:
    ...


def get_instance(output_format: OutputFormat, schema_version: 'SchemaVersion') -> 'BaseSchemaBasedValidator':
    """get the default schema-based validator for a certain `OutputFormat`

    Raises error when no instance could be built.
    """
    # all exceptions are undocumented, as they are pure functional, and should be prevented by correct typing...
    if TYPE_CHECKING:
        from typing import Type
        Validator: Type[BaseSchemaBasedValidator]
    if OutputFormat.JSON is output_format:
        from .json import JsonValidator as Validator
    elif OutputFormat.XML is output_format:
        from .xml import XmlValidator as Validator
    else:
        raise ValueError(f'Unexpected output_format: {output_format!r}')
    return Validator(schema_version)
