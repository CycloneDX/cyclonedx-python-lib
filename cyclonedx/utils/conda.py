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
import sys
from json import JSONDecodeError
from typing import Union

if sys.version_info >= (3, 8, 0):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from urllib.parse import urlparse


class CondaPackage(TypedDict):
    """
    Internal package for unifying Conda package definitions to.
    """
    base_url: str
    build_number: int
    build_string: str
    channel: str
    dist_name: str
    name: str
    platform: str
    version: str
    md5_hash: str


def parse_conda_json_to_conda_package(conda_json_str: str) -> Union[CondaPackage, None]:
    try:
        package_data = json.loads(conda_json_str)
    except JSONDecodeError:
        print(f'Failed to decode JSON: {conda_json_str}')
        raise ValueError(f'Invalid JSON supplied - cannot be parsed: {conda_json_str}')

    if 'md5_hash' not in package_data.keys():
        package_data['md5_hash'] = None

    if isinstance(package_data, dict):
        return CondaPackage(**package_data)

    return None


def parse_conda_list_str_to_conda_package(conda_list_str: str) -> Union[CondaPackage, None]:
    """
    Helper method for parsing a line of output from `conda list --explicit` into our internal `CondaPackage` object.

    Params:
        conda_list_str:
            Line of output from `conda list --explicit`

    Returns:
        Instance of `CondaPackage` else `None`.
    """

    line = conda_list_str.strip()

    if line[0:1] == '#' or line[0:1] == '@' or len(line) == 0:
        # Skip comments, @EXPLICT or empty lines
        return None

    # Remove any hash
    package_hash: str = None
    if '#' in line:
        hash_parts = line.split('#')
        if len(hash_parts) > 1:
            package_hash = hash_parts.pop()
            line = ''.join(hash_parts)

    package_parts = line.split('/')
    package_name_version_build_string = package_parts.pop()
    package_arch = package_parts.pop()
    package_url = urlparse('/'.join(package_parts))

    try:
        package_nvbs_parts = package_name_version_build_string.split('-')
        build_number_with_opt_string = package_nvbs_parts.pop()
        if '.' in build_number_with_opt_string:
            # Remove any .conda at the end if present or other package type eg .tar.gz
            pos = build_number_with_opt_string.find('.')
            build_number_with_opt_string = build_number_with_opt_string[0:pos]

        if '_' in build_number_with_opt_string:
            bnbs_parts = build_number_with_opt_string.split('_')
            if len(bnbs_parts) == 2:
                build_number = int(bnbs_parts.pop())
                build_string = build_number_with_opt_string
            else:
                raise ValueError(f'Unexpected build version string for Conda Package: {conda_list_str}')
        else:
            build_string = None
            build_number = int(build_number_with_opt_string)

        build_version = package_nvbs_parts.pop()
        package_name = '-'.join(package_nvbs_parts)
    except IndexError as e:
        raise ValueError(f'Error parsing {package_nvbs_parts} from {conda_list_str} IndexError: {str(e)}')

    return CondaPackage(
        base_url=package_url.geturl(), build_number=build_number, build_string=build_string,
        channel=package_url.path[1:], dist_name=f'{package_name}-{build_version}-{build_string}',
        name=package_name, platform=package_arch, version=build_version, md5_hash=package_hash
    )
