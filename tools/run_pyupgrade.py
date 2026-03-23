#!/usr/bin/env python3

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
