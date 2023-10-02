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

"""
Set of classes and methods for outputting our libraries internal Bom model to CycloneDX documents in varying formats
and according to different versions of the CycloneDX schema standard.
"""

import os
from abc import ABC, abstractmethod
from importlib import import_module
from typing import Iterable, Optional, Type, Union

from ..model.bom import Bom
from ..model.component import Component
from ..schema import OutputFormat, SchemaVersion

LATEST_SUPPORTED_SCHEMA_VERSION = SchemaVersion.V1_4


class BaseOutput(ABC):

    def __init__(self, bom: Bom, **kwargs: int) -> None:
        super().__init__(**kwargs)
        self._bom = bom
        self._generated: bool = False

    def _chained_components(self, container: Union[Bom, Component]) -> Iterable[Component]:
        for component in container.components:
            yield component
            yield from self._chained_components(component)

    @property
    @abstractmethod
    def schema_version(self) -> SchemaVersion:
        ...

    @property
    @abstractmethod
    def output_format(self) -> OutputFormat:
        ...

    @property
    def generated(self) -> bool:
        return self._generated

    @generated.setter
    def generated(self, generated: bool) -> None:
        self._generated = generated

    def get_bom(self) -> Bom:
        return self._bom

    def set_bom(self, bom: Bom) -> None:
        self._bom = bom

    @abstractmethod
    def generate(self, force_regeneration: bool = False) -> None:
        ...

    @abstractmethod
    def output_as_string(self, *,
                         indent: Optional[Union[int, str]] = None) -> str:
        ...

    def output_to_file(self, filename: str, allow_overwrite: bool = False, *,
                       indent: Optional[Union[int, str]] = None) -> None:
        # Check directory writable
        output_filename = os.path.realpath(filename)
        output_directory = os.path.dirname(output_filename)
        if not os.access(output_directory, os.W_OK):
            raise PermissionError(output_directory)
        if os.path.exists(output_filename) and not allow_overwrite:
            raise FileExistsError(output_filename)
        with open(output_filename, mode='wb') as f_out:
            f_out.write(self.output_as_string(indent=indent).encode('utf-8'))


def get_instance(bom: Bom, output_format: OutputFormat = OutputFormat.XML,
                 schema_version: SchemaVersion = LATEST_SUPPORTED_SCHEMA_VERSION) -> BaseOutput:
    """
    Helper method to quickly get the correct output class/formatter.

    Pass in your BOM and optionally an output format and schema version (defaults to XML and latest schema version).

    :param bom: Bom
    :param output_format: OutputFormat
    :param schema_version: SchemaVersion
    :return:
    """
    # all exceptions are undocumented, as they are pure functional, and should be prevented by correct typing...
    if not isinstance(output_format, OutputFormat):
        raise TypeError(f"unexpected output_format: {output_format!r}")
    if not isinstance(schema_version, SchemaVersion):
        raise TypeError(f"unexpected schema_version: {schema_version!r}")
    try:
        module = import_module(f'.{output_format.name.lower()}', __package__)
    except ImportError as error:  # pragma: no cover
        raise ValueError(f'Unknown output_format: {output_format.name}') from error
    klass: Optional[Type[BaseOutput]] = module.BY_SCHEMA_VERSION.get(schema_version, None)
    if klass is None:  # pragma: no cover
        raise ValueError(f'Unknown {output_format.name}/schema_version: {schema_version.name}')
    return klass(bom=bom)
