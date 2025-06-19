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


__all__ = ['JsonValidator', 'JsonStrictValidator']

from abc import ABC
from json import loads as json_loads
from typing import TYPE_CHECKING, Any, Literal, Optional

from ..schema import OutputFormat

if TYPE_CHECKING:  # pragma: no cover
    from ..schema import SchemaVersion

from ..exception import MissingOptionalDependencyException
from ..schema._res import BOM_JSON as _S_BOM, BOM_JSON_STRICT as _S_BOM_STRICT, JSF as _S_JSF, SPDX_JSON as _S_SPDX
from . import BaseSchemabasedValidator, SchemabasedValidator, ValidationError, squeeze

_missing_deps_error: Optional[tuple[MissingOptionalDependencyException, ImportError]] = None
try:
    from jsonschema.exceptions import ValidationError as JsonSchemaValidationError  # type:ignore[import-untyped]
    from jsonschema.validators import Draft7Validator  # type:ignore[import-untyped]
    from referencing import Registry
    from referencing.jsonschema import DRAFT7

    if TYPE_CHECKING:  # pragma: no cover
        from jsonschema.protocols import Validator as JsonSchemaValidator  # type:ignore[import-untyped]
except ImportError as err:
    _missing_deps_error = MissingOptionalDependencyException(
        'This functionality requires optional dependencies.\n'
        'Please install `cyclonedx-python-lib` with the extra "json-validation".\n'
    ), err


def _get_message_with_squeezed_context(error: 'JsonSchemaValidationError', context_limit: int, replacement: str) -> str:
    # The below code depends on jsonschema internals, that messages are created
    # like `yield ValidationError(f"{instance!r} has non-unique elements")`
    # and tries to replace `{instance!r}` with a shortened version, if needed
    message: str = error.message
    if context_limit <= 0 or len(message) <= context_limit:
        return message

    repr_context = repr(error.instance)
    if len(repr_context) <= context_limit:
        return message

    return message.replace(repr_context, squeeze(repr_context, context_limit, replacement))


class _JsonValidationError(ValidationError):
    def get_squeezed_message(self, *, context_limit: int = -1, max_size: int = -1, replacement: str = ' ... ') -> str:
        """Extracts, and sanitizes the error message.

        Messages can be quite big from underlying libraries, as they sometimes
        add context to the error message..

        This is amended both in a generic and library specific ways here.

        :param max_size: squeeze message to this size.
        :param context_limit: jsonschema messages most of the time include the
                              instance repr as context, which can be very big
                              (in the megabytes range), so an attempt is made to
                              shorten context to this size.
        :param replacement: to mark place of dropped text bit[s]

        With the defaults, no squeezing happens.
        """
        message = _get_message_with_squeezed_context(self.data, context_limit, replacement)
        return squeeze(message, max_size, replacement)

    @property
    def path(self) -> str:
        """Path to the location of the problem in the document.

        An XPath/JSONPath string.
        """
        return str(getattr(self.data, 'json_path', ''))


class _BaseJsonValidator(BaseSchemabasedValidator, ABC):
    @property
    def output_format(self) -> Literal[OutputFormat.JSON]:
        return OutputFormat.JSON

    def __init__(self, schema_version: 'SchemaVersion') -> None:
        # this is the def that is used for generating the documentation
        super().__init__(schema_version)

    if _missing_deps_error:  # noqa:C901
        __MDERROR = _missing_deps_error

        def validate_str(self, data: str) -> Optional[ValidationError]:
            raise self.__MDERROR[0] from self.__MDERROR[1]

    else:
        def validate_str(self, data: str) -> Optional[ValidationError]:
            return self._validate_data(
                json_loads(data))

        def _validate_data(self, data: Any) -> Optional[ValidationError]:
            validator = self._validator  # may throw on error that MUST NOT be caught
            try:
                validator.validate(data)
            except JsonSchemaValidationError as error:
                return _JsonValidationError(error)
            return None

        __validator: Optional['JsonSchemaValidator'] = None

        @property
        def _validator(self) -> 'JsonSchemaValidator':
            if not self.__validator:
                schema_file = self._schema_file
                if schema_file is None:
                    raise NotImplementedError('missing schema file')
                with open(schema_file) as sf:
                    self.__validator = Draft7Validator(
                        json_loads(sf.read()),
                        registry=self.__make_validator_registry(),
                        format_checker=Draft7Validator.FORMAT_CHECKER)
            return self.__validator

        @staticmethod
        def __make_validator_registry() -> Registry[Any]:
            schema_prefix = 'http://cyclonedx.org/schema/'
            with open(_S_SPDX) as spdx, open(_S_JSF) as jsf:
                return Registry().with_resources([
                    (f'{schema_prefix}spdx.SNAPSHOT.schema.json', DRAFT7.create_resource(json_loads(spdx.read()))),
                    (f'{schema_prefix}jsf-0.82.SNAPSHOT.schema.json', DRAFT7.create_resource(json_loads(jsf.read()))),
                ])


class JsonValidator(_BaseJsonValidator, BaseSchemabasedValidator, SchemabasedValidator):
    """Validator for CycloneDX documents in JSON format."""

    @property
    def _schema_file(self) -> Optional[str]:
        return _S_BOM.get(self.schema_version)


class JsonStrictValidator(_BaseJsonValidator, BaseSchemabasedValidator, SchemabasedValidator):
    """Strict validator for CycloneDX documents in JSON format.

    In contrast to :class:`~JsonValidator`,
    the document must not have additional or unknown JSON properties.
    """
    @property
    def _schema_file(self) -> Optional[str]:
        return _S_BOM_STRICT.get(self.schema_version)
