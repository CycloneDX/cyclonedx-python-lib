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

Core functionality of [_CycloneDX_][link_website] for _Python_,
providing a full-stack Bill of Materials (BOM) standard that enables advanced supply chain capabilities for cyber risk reduction.

**This package is not designed for standalone use. It is a software library.**

As of version `3.0.0`, the internal data model was adjusted to allow CycloneDX VEX documents to be produced as per [official examples](https://cyclonedx.org/capabilities/bomlink/#linking-external-vex-to-bom-inventory) linking VEX to a separate CycloneDX document.

If you're looking for a CycloneDX tool to run to generate (SBOM) software bill-of-materials documents, why not check out [CycloneDX Python][cyclonedx-python] or [Jake][jake].

## Responsibilities

* Provide a general purpose _Python_-implementation of [_CycloneDX_][CycloneDX].
* Provide typing and comprehensive documentation for developers and dev-tools to rely on.
* Provide data models to work with _CycloneDX_.
* Provide JSON- and XML-normalizers, that...
  * Support all shipped data models.
  * Respect any injected [_CycloneDX_ Specification][CycloneDX-spec] and generate valid output according to it.
  * Can prepare data structures for JSON- and XML-serialization.
* Serialization:
  * Provide a JSON serializer.
  * Provide an XML serializer.
* Validation against _CycloneDX_ Specification:
  * Provide a JSON validator.
  * Provide an XML validator.
* Support [_pip_-based installation](https://pip.pypa.io/en/stable/) for downstream usage.

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
* Implementation of the [_CycloneDX_ Specification][CycloneDX-spec] for the following versions:
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
* Formal validators for JSON string and XML string according to _CycloneDX_ Specification

## Installation

Install via pip:

```shell
pip install cyclonedx-python-lib
```

The package is also available via conda-forge:

```shell
conda install -c conda-forge cyclonedx-python-lib
```

## Usage

See extended [examples].

```python
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component

# Create a new BOM
bom = Bom()

# Add metadata component
bom.metadata.component = Component(
    name="my-application",
    version="1.0.0"
)

# Add a dependency component
component_a = Component(
    name="my-component-a",
    version="1.0.0"
)
bom.components.add(component_a)
bom.metadata.component.dependencies.add(component_a.bom_ref)
```

## API Documentation

We ship code annotations, so that your IDE and tools may pick up the documentation when you use this library downstream.

There are also pre-rendered documentations hosted on [readthedocs][link_rtfd].

Additionally, there is a prepared config for [_Sphinx_](https://www.sphinx-doc.org/en/master/) that you can use to generate the docs for yourself.

## Schema Support

This library has partial support for the CycloneDX specification. Here's what's currently supported:

### Root Level Schema Support

| Data Path                  | Supported? | Notes                                             |
|----------------------------|------------|---------------------------------------------------|
| `bom[@version]`           | Yes        |                                                   |
| `bom[@serialNumber]`      | Yes        |                                                   |
| `bom.metadata`            | Yes        | Not supported: `lifecycles`                       |
| `bom.components`          | Yes        | Not supported: `modified`, `modelCard`, `data`, `signature` |
| `bom.externalReferences`  | Yes        |                                                   |
| `bom.dependencies`        | Yes        | Since version `2.3.0`                            |

### Internal Model Schema Support

| Internal Model             | Supported? | Notes                                             |
|----------------------------|------------|---------------------------------------------------|
| `ComponentEvidence`        | Yes        | Not currently supported: `callstack`, `identity`, `occurrences` |
| `DisjunctiveLicense`      | Yes        | Not currently supported: `@bom-ref`, `licensing`, `properties` |

## Contributing

Feel free to open issues, bug reports, or pull requests.  
See the [CONTRIBUTING][contributing_file] file for details.

## License

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.  
See the [LICENSE][license_file] file for the full license.

[CycloneDX]: https://cyclonedx.org/
[CycloneDX-spec]: https://github.com/CycloneDX/specification/tree/master#readme
[cyclonedx-python]: https://github.com/CycloneDX/cyclonedx-python
[jake]: https://github.com/sonatype-nexus-community/jake

[license_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/LICENSE
[contributing_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/CONTRIBUTING.md
[examples]: https://github.com/CycloneDX/cyclonedx-python-lib/tree/master/examples
[link_rtfd]: https://cyclonedx-python-library.readthedocs.io/

[shield_pypi-version]: https://img.shields.io/pypi/v/cyclonedx-python-lib?logo=pypi&logoColor=white "PyPI"
[shield_conda-forge-version]: https://img.shields.io/conda/vn/conda-forge/cyclonedx-python-lib?logo=anaconda&logoColor=white "conda-forge"
[shield_rtfd]: https://img.shields.io/readthedocs/cyclonedx-python-library?logo=readthedocs&logoColor=white "Read the Docs"
[shield_gh-workflow-test]: https://img.shields.io/github/actions/workflow/status/CycloneDX/cyclonedx-python-lib/python.yml?branch=master&logo=GitHub&logoColor=white "build"
[shield_coverage]: https://img.shields.io/codacy/coverage/TBD?logo=Codacy&logoColor=white "test coverage"
[shield_ossf-best-practices]: https://img.shields.io/cii/percentage/7956?label=OpenSSF%20best%20practices "OpenSSF best practices"
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
