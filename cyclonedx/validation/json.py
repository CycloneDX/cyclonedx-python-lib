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
from os.path import join
from typing import TYPE_CHECKING, Any, Never, Optional, Tuple

from ..schema import _RES_DIR as _SCHEMA_RES_DIR
from . import ValidationError, _BaseValidator

functionality_not_implemented_error: Optional[Tuple[NotImplementedError, Any]] = None
try:
    from jsonschema import FormatChecker
    from jsonschema.exceptions import ValidationError as JsonValidationError
    from jsonschema.protocols import Validator
    from jsonschema.validators import Draft7Validator
    from referencing import Registry, Resource
    from referencing.exceptions import NoSuchResource
    from referencing.jsonschema import DRAFT7

    if TYPE_CHECKING:
        from jsonschema.protocols import Validator as JsonSchemaValidator
except ImportError as err:
    functionality_not_implemented_error = NotImplementedError(
        'This functionality requires optional dependencies.\n'
        'Please install `cyclonedx-python-lib` with the extra "json-validation".\n'
    ), err

if functionality_not_implemented_error:
    class _BaseJsonValidator(_BaseValidator, ABC):
        def validate_str(self, data: str) -> Optional[ValidationError]:
            raise functionality_not_implemented_error[0]  # from functionality_not_implemented_error[1]

        def validata_data(self, data: Any) -> Optional[ValidationError]:
            raise functionality_not_implemented_error[0]  # from functionality_not_implemented_error[1]

else:
    class _BaseJsonValidator(_BaseValidator, ABC):
        __validator: Optional['JsonSchemaValidator'] = None

        @staticmethod
        def __make_validator_registry() -> Registry:
            def _prevent_retrieve(uri: str) -> Never:
                raise NoSuchResource(ref=uri)

            schema_prefix = 'http://cyclonedx.org/schema/'
            spdx = open(join(_SCHEMA_RES_DIR, 'spdx.SNAPSHOT.schema.json'))
            jsf = open(join(_SCHEMA_RES_DIR, 'jsf-0.82.SNAPSHOT.schema.json'))
            with spdx, jsf:
                return Registry(
                    retrieve=_prevent_retrieve  # prevent unexpected outbound access
                ).with_resources([
                    (f'{schema_prefix}spdx.SNAPSHOT.schema.json', DRAFT7.create_resource(json_loads(spdx.read()))),
                    (f'{schema_prefix}jsf-0.82.SNAPSHOT.schema.json', DRAFT7.create_resource(json_loads(jsf.read()))),
                ])

        @property
        def _validator(self) -> 'JsonSchemaValidator':
            if not self.__validator:
                with open(self._schema_file) as sf:
                    schema = json_loads(sf.read())
                self.__validator = Draft7Validator(schema,
                                                   registry=self.__make_validator_registry(),
                                                   format_checker=Draft7Validator.FORMAT_CHECKER)
            return self.__validator

        def validate_str(self, data: str) -> Optional[ValidationError]:
            return self.validata_data(json_loads(data))

        def validata_data(self, data: Any) -> Optional[ValidationError]:
            validator = self._validator  # may throw on error that MUST NOT be caught
            try:
                validator.validate(data)
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
