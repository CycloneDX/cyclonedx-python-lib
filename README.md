# CycloneDX Python Library

[![shield_pypi-version]][link_pypi]
[![shield_conda-forge-version]][link_conda_forge]
[![shield_rtfd]][link_rtfd]
[![shield_gh-workflow-test]][link_gh_workflow_test]
[![shield_coverage]][link_codacy]
[![shield_ossf-best-practices]][link_ossf_best_practices]
[![shield_license]][license_file]  
[![shield_website]][link_website]
[![shield_slack]][link_slack]
[![shield_groups]][link_discussion]
[![shield_twitter-follow]][link_twitter]

----

OWASP [CycloneDX][link_website] is a full-stack Bill of Materials (BOM) standard that provides advanced supply chain capabilities for cyber risk reduction.

This Python package provides data models, validators, and tools for creating, rendering, and reading CycloneDX documents.

> **Note**: This package is a software library not intended for standalone use. For generating Software Bill of Materials (SBOM), check out [CycloneDX Python][cyclonedx-python] or [Jake][jake].

As of version `3.0.0`, the library supports CycloneDX VEX documents production with [official example](https://cyclonedx.org/capabilities/bomlink/#linking-external-vex-to-bom-inventory) compatibility for linking VEX to separate CycloneDX documents.

## Responsibilities

* Provide a general-purpose *Python*-implementation of [*CycloneDX*][link_website]
* Provide type hints for said implementation, so developers and dev-tools can rely on it
* Provide data models to work with *CycloneDX*
* Provide JSON and XML normalizers that:
   * Support all shipped data models
   * Respect any injected [*CycloneDX* Specification][CycloneDX-spec] and generate valid output according to it
   * Can prepare data structures for JSON and XML serialization
* Serialization:
   * Provide a JSON serializer
   * Provide an XML serializer
* Validation against *CycloneDX* Specification:
   * Provide a JSON validator
   * Provide an XML validator
* Support *pip*-based installation for downstream usage

## Capabilities

* Enums for the following use cases:
   * `ComponentType`
   * `ExternalReferenceType`
   * `HashAlgorithm`
   * `LicenseAcknowledgement`
* Data models for the following use cases:
   * `Bom`
   * `BomRef`, `BomRefRepository`
   * `Component`, `ComponentRepository`, `ComponentEvidence`
   * `ExternalReference`, `ExternalReferenceRepository`
   * `LicenseExpression`, `NamedLicense`, `SpdxLicense`, `LicenseRepository`
   * `Metadata`
   * `Property`, `PropertyRepository`
   * `Tool`, `ToolRepository`
* Utilities for the following use cases:
   * Generate valid random SerialNumbers for `Bom.serialNumber`
* Factories for the following use cases:
   * Create data models from any license descriptor string
* Implementation of the [*CycloneDX* Specification][CycloneDX-spec] for the following versions:
   * `1.6`
   * `1.5`
   * `1.4`
   * `1.3`
   * `1.2`
   * `1.1`
* Normalizers that convert data models to JSON structures
* Normalizers that convert data models to XML structures
* Serializer that converts `Bom` data models to JSON string
* Serializer that converts `Bom` data models to XML string
* Validator that checks JSON against *CycloneDX* Specification
* Validator that checks XML against *CycloneDX* Specification

## Installation

**Via pip:**
```shell
pip install cyclonedx-python-lib
```

**Via Conda:**
```shell
conda install -c conda-forge cyclonedx-python-lib
```

## Quick Start

```python
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.model.component_type import ComponentType

# Create a new BOM
bom = Bom()

# Set metadata component
bom.metadata.component = Component(
    type=ComponentType.APPLICATION,
    name="MyProject"
)

# Add a dependency component
component_a = Component(
    type=ComponentType.LIBRARY,
    name="my-component-a"
)
bom.components.add(component_a)
bom.metadata.component.dependencies.add(component_a.bom_ref)
```

## Schema Support

### Root Level Elements

| Element                    | Status     | Notes                                    |
|---------------------------|------------|------------------------------------------|
| `bom[@version]`           | ✅         |                                          |
| `bom[@serialNumber]`      | ✅         |                                          |
| `bom.metadata`            | ✅         | Excluding: `lifecycles`                  |
| `bom.components`          | ✅         | Excluding: `modified`, `modelCard`, `data`, `signature` |
| `bom.externalReferences`  | ✅         |                                          |
| `bom.dependencies`        | ✅         | Added in v2.3.0                         |

### Internal Models

| Model                     | Status     | Notes                                    |
|--------------------------|------------|------------------------------------------|
| `ComponentEvidence`      | ✅         | Excluding: `callstack`, `identity`, `occurrences` |
| `DisjunctiveLicense`     | ✅         | Excluding: `@bom-ref`, `licensing`, `properties` |

## Documentation

- IDE-compatible code annotations
- Complete documentation on [Read the Docs][link_rtfd]
- Sphinx configuration for local documentation generation

## Contributing

We welcome contributions! See the [CONTRIBUTING][contributing_file] file for guidelines.

## License

Licensed under Apache 2.0 - see the [LICENSE][license_file] file for details.

[CycloneDX]: https://cyclonedx.org/
[CycloneDX-spec]: https://github.com/CycloneDX/specification/tree/master#readme

[license_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/LICENSE
[contributing_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/CONTRIBUTING.md
[link_rtfd]: https://cyclonedx-python-library.readthedocs.io/

[shield_pypi-version]: https://img.shields.io/pypi/v/cyclonedx-python-lib?logo=pypi&logoColor=white "PyPI"
[shield_conda_forge-version]: https://img.shields.io/conda/vn/conda-forge/cyclonedx-python-lib?logo=anaconda&logoColor=white "conda-forge"
[shield_rtfd]: https://img.shields.io/readthedocs/cyclonedx-python-library?logo=readthedocs&logoColor=white "Read the Docs"
[shield_gh_workflow_test]: https://img.shields.io/github/actions/workflow/status/CycloneDX/cyclonedx-python-lib/python.yml?branch=main&logo=GitHub&logoColor=white "build"
[shield_coverage]: https://img.shields.io/codacy/coverage/1f9d451e9cdc49ce99c2a1247adab341?logo=Codacy&logoColor=white "test coverage"
[shield_ossf_best_practices]: https://img.shields.io/cii/percentage/7956?label=OpenSSF%20best%20practices "OpenSSF best practices"
[shield_license]: https://img.shields.io/github/license/CycloneDX/cyclonedx-python-lib?logo=open%20source%20initiative&logoColor=white "license"
[shield_website]: https://img.shields.io/badge/https://-cyclonedx.org-blue.svg "homepage"
[shield_slack]: https://img.shields.io/badge/slack-join-blue?logo=Slack&logoColor=white "slack join"
[shield_groups]: https://img.shields.io/badge/discussion-groups.io-blue.svg "groups discussion"
[shield_twitter-follow]: https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white "twitter follow"

[link_pypi]: https://pypi.org/project/cyclonedx-python-lib/
[link_conda_forge]: https://anaconda.org/conda-forge/cyclonedx-python-lib
[link_codacy]: https://app.codacy.com/gh/CycloneDX/cyclonedx-python-lib
[link_ossf_best_practices]: https://www.bestpractices.dev/projects/7956
[link_website]: https://cyclonedx.org/
[link_slack]: https://cyclonedx.org/slack/invite
[link_discussion]: https://groups.io/g/CycloneDX
[link_twitter]: https://twitter.com/CycloneDX_Spec
