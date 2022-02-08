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

from datetime import datetime
from decimal import Decimal
from enum import Enum
from json import JSONEncoder
from re import compile
from typing import Any, Dict
from uuid import UUID

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore

from cyclonedx.model import XsUri
from cyclonedx.model.component import Component

HYPHENATED_ATTRIBUTES = [
    'bom_ref', 'mime_type', 'x_trust_boundary'
]
PYTHON_TO_JSON_NAME = compile(r'_([a-z])')


class CycloneDxJSONEncoder(JSONEncoder):

    def default(self, o: Any) -> Any:
        # datetime
        if isinstance(o, datetime):
            return o.isoformat()

        # Decimal
        if isinstance(o, Decimal):
            return float(f'{o:.1f}')

        # Enum
        if isinstance(o, Enum):
            return o.value

        # Set
        if isinstance(o, set):
            return list(o)

        # UUID
        if isinstance(o, UUID):
            return str(o)

        # XsUri
        if isinstance(o, XsUri):
            return str(o)

        # Classes
        if isinstance(o, object):
            d: Dict[Any, Any] = {}
            for k, v in o.__dict__.items():
                # Remove leading _ in key names
                new_key = k[1:]
                if new_key.startswith('_') or '__' in new_key:
                    continue

                # Convert pythonic names to JSON names
                # e.g. 'external_references' to 'externalReferences'
                #
                # Some special cases are hyphenated, not camel case
                if new_key in HYPHENATED_ATTRIBUTES:
                    new_key = new_key.replace('_', '-')
                elif '_' in new_key:
                    new_key = PYTHON_TO_JSON_NAME.sub(lambda x: x.group(1).upper(), new_key)

                # Inject '' for Component.version if it's None
                if isinstance(o, Component) and new_key == 'version' and v is None:
                    d[new_key] = ""
                elif v or v is False:
                    # Skip any None values (exception 'version')
                    if isinstance(v, PackageURL):
                        # Special handling of PackageURL instances which JSON would otherwise automatically encode to
                        # an Array
                        v = str(v.to_string())
                    d[new_key] = v

            return d

        # Fallback to default
        super().default(o=o)
