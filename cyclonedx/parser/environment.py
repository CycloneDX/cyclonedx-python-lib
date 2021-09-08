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

import sys

if sys.version_info >= (3, 8, 0):
    from importlib.metadata import metadata
else:
    from importlib_metadata import metadata

from . import BaseParser

from ..model.component import Component


class EnvironmentParser(BaseParser):
    """
    This will look at the current Python environment and list out all installed packages.

    Best used when you have virtual Python environments per project.
    """

    def __init__(self):
        import pkg_resources

        i: pkg_resources.DistInfoDistribution
        for i in iter(pkg_resources.working_set):
            c = Component(name=i.project_name, version=i.version)

            i_metadata = self._get_metadata_for_package(i.project_name)
            if 'Author' in i_metadata.keys():
                c.set_author(author=i_metadata.get('Author'))

            if 'License' in i_metadata.keys():
                c.set_license(license_str=i_metadata.get('License'))

            self._components.append(c)

    @staticmethod
    def _get_metadata_for_package(package_name: str):
        if sys.version_info >= (3, 8, 0):
            return metadata(package_name)
        else:
            return metadata(package_name)
