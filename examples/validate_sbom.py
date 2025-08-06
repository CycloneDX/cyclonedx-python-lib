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

"""Simple command‑line example for validating CycloneDX SBOMs.

This script demonstrates how to validate a CycloneDX SBOM against the
official JSON and XML schemas using the :mod:`cyclonedx.validation`
subsystem.  It accepts the path to a JSON or XML SBOM as its first
command–line argument, selects the appropriate validator based on the
file extension and schema version and reports any validation errors.

Validation requires optional dependencies.  Install the
``cyclonedx-python-lib`` package with the ``json-validation`` or
``xml-validation`` extras depending on the SBOM format you wish to
validate::

    pip install "cyclonedx-python-lib[json-validation]"
    pip install "cyclonedx-python-lib[xml-validation]"

If these dependencies are missing the validation will be skipped and
an explanatory message will be printed instead.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Optional

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator
from cyclonedx.validation import ValidationError


def _detect_format(path: Path) -> OutputFormat:
    """Detect the SBOM format based on the file suffix.

    Parameters
    ----------
    path:
        The path to the SBOM file.

    Returns
    -------
    cyclonedx.schema.OutputFormat
        The detected output format.

    Raises
    ------
    ValueError
        If the file suffix is neither ``.json`` nor ``.xml``.
    """
    suffix = path.suffix.lower()
    if suffix == ".json":
        return OutputFormat.JSON
    if suffix == ".xml":
        return OutputFormat.XML
    raise ValueError(f"Unsupported SBOM file format: {suffix}. Only .json and .xml are supported.")


def validate_sbom(path: Path, schema_version: SchemaVersion = SchemaVersion.V1_6) -> Optional[Iterable[ValidationError]]:
    """Validate the SBOM at ``path`` for the given schema version.

    Parameters
    ----------
    path:
        Path to the SBOM file to validate.
    schema_version:
        The CycloneDX schema version the SBOM is expected to conform to.  Defaults to
        :class:`~cyclonedx.schema.SchemaVersion.V1_6`.

    Returns
    -------
    Optional[Iterable[ValidationError]]
        ``None`` if the SBOM is valid, otherwise an iterable of validation errors.

    Notes
    -----
    ``None`` is returned when the validation passes or when the optional validation
    dependencies are not installed and validation is skipped.  In the latter case
    an explanatory message is printed to ``stderr``.
    """
    fmt = _detect_format(path)
    data = path.read_text(encoding="utf-8")
    validator = make_schemabased_validator(output_format=fmt, schema_version=schema_version)
    try:
        # Request all errors so the caller can iterate over them if present.
        return validator.validate_str(data, all_errors=True)  # type: ignore[return-value]
    except MissingOptionalDependencyException as exc:
        # Inform the user that validation is skipped due to missing optional dependencies.
        print(f"Validation skipped for {path.name}: {exc}", file=sys.stderr)
        return None


def main(argv: list[str] | None = None) -> int:
    """Entry point for command‑line usage.

    Expects a single positional argument – the path to the SBOM file.  If
    validation errors are found they are written to ``stderr`` and the
    process exits with a non‑zero status code.  Otherwise a success message
    is printed and a zero exit status is returned.
    """
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <path-to-sbom.json|sbom.xml>", file=sys.stderr)
        return 1
    sbom_path = Path(argv[1])
    try:
        result = validate_sbom(sbom_path)
    except ValueError as ve:
        print(str(ve), file=sys.stderr)
        return 1
    if result is None:
        # Either valid or skipped due to missing deps.
        return 0
    # If the SBOM is valid validate_str returns ``None``.  Otherwise it returns an iterable of errors.
    if isinstance(result, Iterable):
        errors: list[ValidationError] = list(result)
        if not errors:
            print("SBOM valid")
            return 0
        print(f"SBOM invalid – {len(errors)} error(s) found:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 2
    # Unexpected type (should not occur); treat as generic failure.
    print("Unexpected result from validator", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
