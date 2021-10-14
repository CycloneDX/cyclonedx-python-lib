# encoding: utf-8

# This file is part of CycloneDX Python Lib
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
import json

from . import BaseParser
from ..model import ExternalReference, ExternalReferenceType, HashType
from ..model.component import Component


class PipEnvParser(BaseParser):

    def __init__(self, pipenv_contents: str):
        super().__init__()
        pipfile_lock_contents = json.loads(pipenv_contents)

        for package_name in pipfile_lock_contents['default'].keys():
            package_data = pipfile_lock_contents['default'][package_name]
            c = Component(
                name=package_name, version=str(package_data['version']).strip('='),
            )

            if 'index' in package_data.keys() and package_data['index'] == 'pypi':
                # Add download location with hashes stored in Pipfile.lock
                if 'hashes' in package_data.keys():
                    for pip_hash in package_data['hashes']:

                        ext_ref = ExternalReference(
                            reference_type=ExternalReferenceType.DISTRIBUTION,
                            url=c.get_pypi_url(),
                            comment='Distribution available from pypi.org'
                        )
                        ext_ref.add_hash(HashType.from_composite_str(pip_hash))
                        c.add_external_reference(ext_ref)

            self._components.append(c)


class PipEnvFileParser(PipEnvParser):

    def __init__(self, pipenv_lock_filename: str):
        with open(pipenv_lock_filename) as r:
            super(PipEnvFileParser, self).__init__(pipenv_contents=r.read())
        r.close()
