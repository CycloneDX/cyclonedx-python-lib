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
written in Python with complete type hints.

**This package is not designed for standalone use. It is a software library.**

As of version `3.0.0`, the internal data model was adjusted to allow CycloneDX VEX documents to be produced as per [official examples](https://cyclonedx.org/capabilities/bomlink/#linking-external-vex-to-bom-inventory) linking VEX to a separate CycloneDX document.

If you're looking for a CycloneDX tool to run to generate (SBOM) software bill-of-materials documents, check out [CycloneDX Python][cyclonedx-python] or [Jake][jake].

## Responsibilities

* Provide a general-purpose _Python_-implementation of [_CycloneDX_][link_website].
* Provide type hints for said implementation, so developers and dev-tools can rely on it.
* Provide data models to work with _CycloneDX_.
* Provide JSON and XML normalizers that:
  * Support all shipped data models.
  * Respect any injected [_CycloneDX_ Specification][CycloneDX-spec] and generate valid output according to it.
  * Can prepare data structures for JSON and XML serialization.
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
* Validator that checks JSON against _CycloneDX_ Specification
* Validator that checks XML against _CycloneDX_ Specification

## Installation

# CycloneDX Python Library

[![PyPI](https://img.shields.io/pypi/v/cyclonedx-python-lib?logo=pypi&logoColor=white)](https://pypi.org/project/cyclonedx-python-lib/)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/cyclonedx-python-lib?logo=anaconda&logoColor=white)](https://anaconda.org/conda-forge/cyclonedx-python-lib)
[![Documentation](https://img.shields.io/readthedocs/cyclonedx-python-library?logo=readthedocs&logoColor=white)](https://cyclonedx-python-library.readthedocs.io/)
[![Build](https://img.shields.io/github/actions/workflow/status/CycloneDX/cyclonedx-python-lib/python.yml?branch=main&logo=GitHub&logoColor=white)](https://github.com/CycloneDX/cyclonedx-python-lib/actions)
[![Coverage](https://img.shields.io/codacy/coverage/1f9d451e9cdc49ce99c2a1247adab341?logo=Codacy&logoColor=white)](https://app.codacy.com/gh/CycloneDX/cyclonedx-python-lib)
[![OpenSSF Best Practices](https://img.shields.io/cii/percentage/7956?label=OpenSSF%20best%20practices)](https://www.bestpractices.dev/projects/7956)
[![License](https://img.shields.io/github/license/CycloneDX/cyclonedx-python-lib?logo=open%20source%20initiative&logoColor=white)](LICENSE)
[![Website](https://img.shields.io/badge/https://-cyclonedx.org-blue.svg)](https://cyclonedx.org/)
[![Slack](https://img.shields.io/badge/slack-join-blue?logo=Slack&logoColor=white)](https://cyclonedx.org/slack/invite)
[![Discussion](https://img.shields.io/badge/discussion-groups.io-blue.svg)](https://groups.io/g/CycloneDX)
[![Twitter](https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white)](https://twitter.com/CycloneDX_Spec)

---

OWASP [CycloneDX](https://cyclonedx.org/) is a full-stack Bill of Materials (BOM) standard that provides advanced supply chain capabilities for cyber risk reduction.

This Python package provides data models, validators, and more to help you create, render, and read CycloneDX documents.

**This package is not designed for standalone use. It is a software library.**

As of version `3.0.0`, the internal data model was adjusted to allow CycloneDX VEX documents to be produced as per [official examples](https://cyclonedx.org/capabilities/bomlink/#linking-external-vex-to-bom-inventory) linking VEX to a separate CycloneDX document.

If you're looking for a CycloneDX tool to generate (SBOM) software bill-of-materials documents, check out [CycloneDX Python](https://github.com/CycloneDX/cyclonedx-python) or [Jake](https://github.com/CycloneDX/jake).

## Responsibilities

* Provide a general-purpose **Python** implementation of [CycloneDX](https://cyclonedx.org/).
* Offer type hints and comprehensive documentation for developers.
* Provide data models to work with **CycloneDX**.
* Implement JSON and XML normalizers that:
  * Support all shipped data models.
  * Respect any injected [CycloneDX Specification](https://github.com/CycloneDX/specification) and generate valid output according to it.
  * Can prepare data structures for JSON and XML serialization.
* Serialization:
  * Provide a JSON serializer.
  * Provide an XML serializer.
* Validation against **CycloneDX** Specification:
  * Provide a JSON validator.
  * Provide an XML validator.
* Support [pip-based installation](https://pip.pypa.io/en/stable/) for downstream usage.

## Capabilities

* **Schema Support**: 
  - Implements the [CycloneDX Specification](https://github.com/CycloneDX/specification) for versions:
    * `1.6`
    * `1.5`
    * `1.4`
    * `1.3`
    * `1.2`
    * `1.1`
* **Enums for Use Cases**:
  - `ComponentType`
  - `ExternalReferenceType`
  - `HashAlgorithm`
  - `LicenseAcknowledgement`
* **Data Models**:
  - `Bom`, `BomRef`, `BomRefRepository`
  - `Component`, `ComponentRepository`, `ComponentEvidence`
  - `ExternalReference`, `ExternalReferenceRepository`
  - `LicenseExpression`, `NamedLicense`, `SpdxLicense`, `LicenseRepository`
  - Other relevant models as defined in the specification.
* **Utilities**:
  - Generate valid random SerialNumbers for `Bom.serialNumber`.
* **Factories**:
  - Create data models from any license descriptor string.
* **Validation**:
  - Formal validators for JSON and XML strings according to the CycloneDX specification.

## Installation

Install via pip:

```shell
pip install cyclonedx-python-lib
```

## Usage

Here's a quick example of how to use the library:

```python
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component

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

## API Documentation

We ship code annotations so that your IDE and tools may pick up the documentation when you use this library downstream.

There are also pre-rendered documentations hosted on [Read the Docs](https://cyclonedx-python-library.readthedocs.io/).

Additionally, there is a prepared config for [Sphinx](https://www.sphinx-doc.org/en/master/) that you can use to generate the docs for yourself.

## Schema Support

This library has partial support for the CycloneDX specification (we continue to grow support). The following sub-sections aim to explain what support this library provides and any known gaps in support.

### Root Level Schema Support

| Data Path | Supported? | Notes |
|-----------|------------|-------|
| `bom[@version]` | Yes | |
| `bom[@serialNumber]` | Yes | |
| `bom.metadata` | Yes | Not supported: `lifecycles` |
| `bom.components` | Yes | Not supported: `modified`, `modelCard`, `data`, `signature` |
| `bom.externalReferences` | Yes | |
| `bom.dependencies` | Yes | Since version `2.3.0` |

### Internal Model Schema Support

| Internal Model | Supported? | Notes |
|---------------|------------|-------|
| `ComponentEvidence` | Yes | Not currently supported: `callstack`, `identity`, `occurrences` |
| `DisjunctiveLicense` | Yes | Not currently supported: `@bom-ref`, `licensing`, `properties` |

For detailed schema support, refer to the [CycloneDX Specification](https://github.com/CycloneDX/specification).

## Contributing

Feel free to open issues, bug reports, or pull requests.  
See the [CONTRIBUTING](CONTRIBUTING.md) file for details.

## License

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.  
See the [LICENSE](LICENSE) file for the full license.
