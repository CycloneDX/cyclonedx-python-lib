# encoding: utf-8

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

__all__ = ['JsonValidator', 'JsonStrictValidator']

from abc import ABC
from json import loads as json_loads
from typing import TYPE_CHECKING, Any, Optional, Tuple

if TYPE_CHECKING:
    from ..schema import SchemaVersion

from ..exception import MissingOptionalDependencyException
from ..schema._res import BOM_JSON as _S_BOM, BOM_JSON_STRICT as _S_BOM_STRICT, JSF as _S_JSF, SPDX_JSON as _S_SPDX
from . import ValidationError, _BaseValidator

_missing_deps_error: Optional[Tuple[MissingOptionalDependencyException, ImportError]] = None
try:
    from jsonschema.exceptions import ValidationError as JsonValidationError  # type: ignore[import]
    from jsonschema.validators import Draft7Validator  # type: ignore[import]
    from referencing import Registry
    from referencing.jsonschema import DRAFT7

    if TYPE_CHECKING:
        from jsonschema.protocols import Validator as JsonSchemaValidator  # type: ignore[import]
except ImportError as err:
    _missing_deps_error = MissingOptionalDependencyException(
        'This functionality requires optional dependencies.\n'
        'Please install `cyclonedx-python-lib` with the extra "json-validation".\n'
    ), err


class _BaseJsonValidator(_BaseValidator, ABC):

    def __init__(self, schema_version: 'SchemaVersion') -> None:
        # this is the def that is used for generating the documentation
        super().__init__(schema_version)

    def validate_str(self, data: str) -> Optional[ValidationError]:
        """Validate a string according to the schema version."""
        # this is the def that is used for generating the documentation

    if _missing_deps_error:
        __MDERROR = _missing_deps_error

        def validate_str(self, data: str) -> Optional[ValidationError]:
            raise self.__MDERROR[0]  # from functionality_not_implemented_error[1]

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


class JsonValidator(_BaseJsonValidator):
    """Validator for CycloneDX documents in JSON format."""

    @property
    def _schema_file(self) -> Optional[str]:
        return _S_BOM.get(self.schema_version)


class JsonStrictValidator(_BaseJsonValidator):
    """Strict validator for CycloneDX documents in JSON format.

    In contrast to :class:`~JsonValidator`,
    the document must not have additional or unknown JSON properties.
    """
    @property
    def _schema_file(self) -> Optional[str]:
        return _S_BOM_STRICT.get(self.schema_version)
