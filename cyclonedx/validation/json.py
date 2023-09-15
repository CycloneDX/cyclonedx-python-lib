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

from . import _BaseValidator, ValidationError
from typing import Optional, TYPE_CHECKING
from ..schema import _RES_DIR as _SCHEMA_RES_DIR
from os.path import join
from json import loads as json_loads
from abc import ABC

functionality_not_implemented_error: Optional[NotImplementedError] = None
try:
    from jsonschema.validators import validator_for
    from jsonschema.exceptions import ValidationError as JsonValidationError
    from referencing import Registry, Resource
    from referencing.exceptions import NoSuchResource

    if TYPE_CHECKING:
        from jsonschema.protocols import Validator as JsonSchemaValidator
except ImportError as err:
    functionality_not_implemented_error = NotImplementedError(
        'this functionality requires optional dependencies.\n'
        'please install the extra "json-validation"\n'
        f'---\nprevious: {err}'
    )


class _BaseJsonValidator(_BaseValidator, ABC):
    __validator: Optional['JsonSchemaValidator']

    @staticmethod
    def __fetch_schema_file(uri: str) -> 'Resource':
        if not uri.startswith("http://cyclonedx.org/schema/"):
            raise NoSuchResource(ref=uri)

        file = join(_SCHEMA_RES_DIR, uri.removeprefix("http://cyclonedx.org/schema/"))
        with open(file, 'r') as fh:
            return Resource.from_contents(json_loads(fh.read()))

    @property
    def _validator(self) -> 'JsonSchemaValidator':
        if not self.__validator:
            if functionality_not_implemented_error:
                raise functionality_not_implemented_error

            schema_registry = Registry(retrieve=self.__fetch_schema_file)
            with open(self._schema_file, 'r') as sf:
                schema = json_loads(sf.read())
            self.__validator = validator_for(schema)(schema, registry=schema_registry)
        return self.__validator

    def validate(self, data: str) -> Optional[ValidationError]:
        if functionality_not_implemented_error:
            raise functionality_not_implemented_error

        structure = json_loads(data)
        validator = self._validator  # may throw on error that MUST NOT be caught
        try:
            validator.validate(structure)
        except JsonValidationError as error:
            return ValidationError(error)


class JsonValidator(_BaseJsonValidator):

    @property
    def _schema_file(self) -> str:
        return join(_SCHEMA_RES_DIR, f'bom-{self.schema_version.to_version()}.SNAPSHOT.schema.json')


class JsonStrictValidator(_BaseJsonValidator):

    @property
    def _schema_file(self) -> str:
        return join(_SCHEMA_RES_DIR, f'bom-{self.schema_version.to_version()}-strict.SNAPSHOT.schema.json')
