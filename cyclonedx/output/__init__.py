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

import importlib
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import cast, Optional

from ..model.bom import Bom


class OutputFormat(Enum):
    JSON: str = 'Json'
    XML: str = 'Xml'


class SchemaVersion(Enum):
    V1_0: str = 'V1Dot0'
    V1_1: str = 'V1Dot1'
    V1_2: str = 'V1Dot2'
    V1_3: str = 'V1Dot3'


DEFAULT_SCHEMA_VERSION = SchemaVersion.V1_3


class BaseOutput(ABC):
    _bom: Bom

    def __init__(self, bom: Bom) -> None:
        self._bom = bom

    def get_bom(self) -> Bom:
        return self._bom

    def set_bom(self, bom: Bom) -> None:
        self._bom = bom

    @abstractmethod
    def output_as_string(self) -> str:
        pass

    def output_to_file(self, filename: str, allow_overwrite: bool = False) -> None:
        # Check directory writable
        output_filename = os.path.realpath(filename)
        output_directory = os.path.dirname(output_filename)

        if not os.access(output_directory, os.W_OK):
            raise PermissionError

        if os.path.exists(output_filename) and not allow_overwrite:
            raise FileExistsError

        with open(output_filename, mode='wb') as f_out:
            f_out.write(self.output_as_string().encode('utf-8'))

        f_out.close()


def get_instance(bom: Optional[Bom] = None, output_format: OutputFormat = OutputFormat.XML,
                 schema_version: SchemaVersion = DEFAULT_SCHEMA_VERSION) -> BaseOutput:
    """
    Helper method to quickly get the correct output class/formatter.

    Pass in your BOM and optionally an output format and schema version (defaults to XML and latest schema version).

    :param bom: Bom
    :param output_format: OutputFormat
    :param schema_version: SchemaVersion
    :return:
    """
    try:
        module = importlib.import_module(f"cyclonedx.output.{output_format.value.lower()}")
        output_klass = getattr(module, f"{output_format.value}{schema_version.value}")
    except (ImportError, AttributeError):
        raise ValueError(f"Unknown format {output_format.value.lower()!r}") from None

    return cast(BaseOutput, output_klass(bom=bom))
