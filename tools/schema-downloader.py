# encoding: utf-8
import re
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

from os.path import dirname, join
from urllib.request import urlretrieve
import re

SOURCE_ROOT = 'https://raw.githubusercontent.com/CycloneDX/specification/1.4/schema/'
TARGET_ROOT = join(dirname(__file__), '..', 'cyclonedx', 'schema', '_res')

bom_xsd = {
    'versions': ['1.4', '1.3', '1.2', '1.1', '1.0'],
    'sourcePattern': f'{SOURCE_ROOT}bom-%s.xsd',
    'targetPattern': join(TARGET_ROOT, 'bom-%s.SNAPSHOT.xsd'),
    'replace': [],
    'replaceRE': [
        (re.compile(r'schemaLocation="https?://cyclonedx.org/schema/spdx"'), 'schemaLocation="spdx.SNAPSHOT.xsd"')
    ]
}

# "version" is not required but optional with a default value!
#   this is wrong in schema<1.5
_bomSchemaEnumMatch = re.compile(
    r'("\$id": "(http://cyclonedx\.org/schema/bom.+?\.schema\.json)".*"enum": \[\s+")http://cyclonedx\.org/schema/bom.+?\.schema\.json"',
    re.DOTALL)
_bomSchemaEnumReplace = r'\1\2"'


# "version" is not required but optional with a default value!
# this is wrong in schema<1.5
_bomRequired = """
  "required": [
    "bomFormat",
    "specVersion",
    "version"
  ],"""
_bomRequiredReplace = """
  "required": [
    "bomFormat",
    "specVersion"
  ],"""


# there was a case where the default value did not match the own pattern ...
# this is wrong in schema<1.5
_defaultWithPatternMatch = re.compile(r'\s+"default": "",(?![^}]*?"pattern": "\^\(\.\*\)\$")', re.MULTILINE)
_defaultWithPatternReplace = r''

bom_json_lax = {
    'versions': ['1.4', '1.3', '1.2'],
    'sourcePattern': f'{SOURCE_ROOT}bom-%s.schema.json',
    'targetPattern': join(TARGET_ROOT, 'bom-%s.SNAPSHOT.schema.json'),
    'replace': [
        ('spdx.schema.json', 'spdx.SNAPSHOT.schema.json'),
        ('jsf-0.82.schema.json', 'jsf-0.82.SNAPSHOT.schema.json'),
        (_bomRequired, _bomRequiredReplace),
    ],
    'replaceRE': [
        (_bomSchemaEnumMatch, _bomSchemaEnumReplace),
        # there was a case where the default value did not match the own pattern ...
        # this is wrong in schema<1.5
        # with current SchemaValidator this is no longer required, as defaults are not applied
        # (re.compile(r'\s+"default": "",(?![^}]*?"pattern": "\^\(\.\*\)\$")', re.MULTILINE), '')
    ]
}

bom_json_strict = {
    'versions': ['1.3', '1.2'],
    'sourcePattern': f'{SOURCE_ROOT}bom-%s-strict.schema.json',
    'targetPattern': join(TARGET_ROOT, 'bom-%s-strict.SNAPSHOT.schema.json'),
    'replace': bom_json_lax['replace'],
    'replaceRE': bom_json_lax['replaceRE']
}

other_downloadables = [
    (f'{SOURCE_ROOT}spdx.schema.json', join(TARGET_ROOT, 'spdx.SNAPSHOT.schema.json')),
    (f'{SOURCE_ROOT}spdx.xsd', join(TARGET_ROOT, 'spdx.SNAPSHOT.xsd')),
    (f'{SOURCE_ROOT}jsf-0.82.schema.json', join(TARGET_ROOT, 'jsf-0.82.SNAPSHOT.schema.json')),
]

for dspec in (bom_xsd, bom_json_lax, bom_json_strict):
    for version in dspec['versions']:
        source = dspec['sourcePattern'].replace('%s', version)
        target = dspec['targetPattern'].replace('%s', version)
        tempfile, _ = urlretrieve(source)
        with open(tempfile, 'r') as tmpf:
            with open(target, 'w') as tarf:
                text = tmpf.read()
                for search, replace in dspec['replace']:
                    text = text.replace(search, replace)
                for search, replace in dspec['replaceRE']:
                    text = search.sub(replace, text)
                tarf.write(text)

for source, target in other_downloadables:
    urlretrieve(source, target)
