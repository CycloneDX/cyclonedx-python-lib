#!/usr/bin/env python3

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

import re
from os.path import dirname, join, realpath
from urllib.request import urlretrieve

SOURCE_ROOT = 'https://raw.githubusercontent.com/CycloneDX/specification/refs/tags/1.6.1/schema/'
SOURCE_ROOT_LATEST = 'https://raw.githubusercontent.com/CycloneDX/specification/refs/heads/master/schema/'
TARGET_ROOT = realpath(join(dirname(__file__), '..', 'cyclonedx', 'schema', '_res'))

BOM_XSD = {
    'versions': ['1.6', '1.5', '1.4', '1.3', '1.2', '1.1', '1.0'],
    'sourcePattern': f'{SOURCE_ROOT}bom-%s.xsd',
    'targetPattern': join(TARGET_ROOT, 'bom-%s.SNAPSHOT.xsd'),
    'replace': [],
    'replaceRE': [
        (re.compile(r'schemaLocation="https?://cyclonedx.org/schema/spdx"'), 'schemaLocation="spdx.SNAPSHOT.xsd"')
    ]
}

# "$schema" is not required but optional.
#  that enum constraint value there is complicated -> remove it.
#  See https://github.com/CycloneDX/specification/issues/402
#  See https://github.com/CycloneDX/specification/pull/403
_BOM_SCHEMA_ENUM_RE = re.compile(
    r',?\s*"enum":\s*\[\s*"http://cyclonedx\.org/schema/.+?\.schema\.json"\s*\]',
    re.DOTALL)
_BOM_SCHEMA_ENUM_REPL = r''


# "version" is not required but optional with a default value!
# this is wrong in schema<1.5
_BOM_REQUIRED_S = """
  "required": [
    "bomFormat",
    "specVersion",
    "version"
  ],"""
_BOM_REQUIRED_R = """
  "required": [
    "bomFormat",
    "specVersion"
  ],"""


# there was a case where the default value did not match the own pattern ...
# this is wrong in schema<1.5
_DEFAULTS_WITH_PATTERN_RE = re.compile(r'\s+"default": "",(?![^}]*?"pattern": "\^\(\.\*\)\$")', re.MULTILINE)
_DEFAULTS_WITH_PATERN_REPL = r''

BOM_JSON_LAX = {
    'versions': ['1.6', '1.5', '1.4', '1.3', '1.2'],
    'sourcePattern': f'{SOURCE_ROOT}bom-%s.schema.json',
    'targetPattern': join(TARGET_ROOT, 'bom-%s.SNAPSHOT.schema.json'),
    'replace': [
        ('spdx.schema.json', 'spdx.SNAPSHOT.schema.json'),
        ('jsf-0.82.schema.json', 'jsf-0.82.SNAPSHOT.schema.json'),
        (_BOM_REQUIRED_S, _BOM_REQUIRED_R),
    ],
    'replaceRE': [
        (_BOM_SCHEMA_ENUM_RE, _BOM_SCHEMA_ENUM_REPL),
        # there was a case where the default value did not match the own pattern ...
        # this is wrong in schema<1.5
        # with current SchemaValidator this is no longer required, as defaults are not applied
        # (re.compile(r'\s+"default": "",(?![^}]*?"pattern": "\^\(\.\*\)\$")', re.MULTILINE), '')
    ]
}

BOM_JSON_STRICT = {
    'versions': ['1.3', '1.2'],
    'sourcePattern': f'{SOURCE_ROOT}bom-%s-strict.schema.json',
    'targetPattern': join(TARGET_ROOT, 'bom-%s-strict.SNAPSHOT.schema.json'),
    'replace': BOM_JSON_LAX['replace'],
    'replaceRE': BOM_JSON_LAX['replaceRE']
}

OTHER_DOWNLOADABLES = [
    (f'{SOURCE_ROOT_LATEST}spdx.schema.json', join(TARGET_ROOT, 'spdx.SNAPSHOT.schema.json')),
    (f'{SOURCE_ROOT_LATEST}spdx.xsd', join(TARGET_ROOT, 'spdx.SNAPSHOT.xsd')),
    (f'{SOURCE_ROOT_LATEST}jsf-0.82.schema.json', join(TARGET_ROOT, 'jsf-0.82.SNAPSHOT.schema.json')),
]

for dspec in (BOM_XSD, BOM_JSON_LAX, BOM_JSON_STRICT):
    for version in dspec['versions']:
        source = dspec['sourcePattern'].replace('%s', version)
        target = dspec['targetPattern'].replace('%s', version)
        tempfile, _ = urlretrieve(source)  # nosec B310
        print(source, '->', target)
        with open(tempfile) as tmpf:
            text = tmpf.read()
        with open(target, 'w', newline='\n') as tarf:
            for search, replace in dspec['replace']:
                text = text.replace(search, replace)
            for search, replace in dspec['replaceRE']:
                text = search.sub(replace, text)
            tarf.write(text)

for source, target in OTHER_DOWNLOADABLES:
    print(source, '->', target)
    urlretrieve(source, target)  # nosec B310
