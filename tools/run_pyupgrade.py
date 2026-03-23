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

import subprocess  # nosec - subprocess is used to run pyupgrade and not part of published library
import sys
from pathlib import Path

HELP = f"""
Wrapper around pyupgrade to perform a lookup of all *.py/*.pyi files in passed directories
and pass them to pyupgrade in a single invocation.

Usage: {sys.argv[0]} [pyupgrade-args ...] -- <dir ...>
"""

if '--' not in sys.argv:
    print(HELP, file=sys.stderr)
    sys.exit(1)

sep = sys.argv.index('--')
pyupgrade_args = sys.argv[1:sep]
directories = sys.argv[sep + 1:]

if not directories:
    print('Error: at least one directory must be specified after --', '\n', HELP, file=sys.stderr)
    sys.exit(2)

files = sorted({
    str(file)
    for directory in directories
    for pattern in ['*.py', '*.pyi']
    for file in Path(directory).rglob(pattern)
})

result = subprocess.run(  # nosec - shell=False is used to prevent injection, all arg passed as a list
    [sys.executable, '-m', 'pyupgrade', *pyupgrade_args, *files],
    shell=False  # w/o shell all args are passed directly to the process without the need for quotes or escaping
)
sys.exit(result.returncode)
