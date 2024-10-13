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
from typing import TYPE_CHECKING, Any, Literal, Optional, Tuple

from ..schema import OutputFormat

if TYPE_CHECKING:  # pragma: no cover
    from ..schema import SchemaVersion

from ..exception import MissingOptionalDependencyException
from ..schema._res import BOM_JSON as _S_BOM, BOM_JSON_STRICT as _S_BOM_STRICT, JSF as _S_JSF, SPDX_JSON as _S_SPDX
from . import BaseSchemabasedValidator, SchemabasedValidator, ValidationError

_missing_deps_error: Optional[Tuple[MissingOptionalDependencyException, ImportError]] = None
try:
    from jsonschema.exceptions import ValidationError as JsonValidationError  # type:ignore[import-untyped]
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
            return self._validata_data(
                json_loads(data))

        def _validata_data(self, data: Any) -> Optional[ValidationError]:
            validator = self._validator  # may throw on error that MUST NOT be caught
            try:
                validator.validate(data)
            except JsonValidationError as error:
                return ValidationError(error)
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
