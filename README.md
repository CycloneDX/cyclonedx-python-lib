# CycloneDX Python Library

[![shield_pypi-version]][link_pypi]
[![shield_conda-forge-version]][link_conda-forge]
[![shield_rtfd]][link_rtfd]
[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_coverage]][link_codacy]
[![shield_ossf-best-practices]][link_ossf-best-practices]
[![shield_license]][license_file]  
[![shield_website]][link_website]
[![shield_slack]][link_slack]
[![shield_groups]][link_discussion]
[![shield_twitter-follow]][link_twitter]

----

OWASP [CycloneDX][link_website] is a full-stack Bill of Materials (BOM) standard that provides advanced supply chain capabilities for cyber risk reduction.

This Python package provides data models and tools for working with CycloneDX documents.

> **Note**: This package is a software library not intended for standalone use. For generating Software Bill of Materials (SBOM), check out [CycloneDX Python][cyclonedx-python] or [Jake][jake].

## Installation

**Via pip:**
```shell
pip install cyclonedx-python-lib
```

**Via Conda:**
```shell
conda install -c conda-forge cyclonedx-python-lib
```

## Python Support

We endeavor to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).
However, some features may not be possible/present in older Python versions due to their lack of support.

## VEX Support

As of version `3.0.0`, the library supports CycloneDX VEX documents production with [official example](https://cyclonedx.org/capabilities/bomlink/#linking-external-vex-to-bom-inventory) compatibility for linking VEX to separate CycloneDX documents.

## Documentation

Complete documentation is available on [Read the Docs][link_rtfd]. This includes:
- API Reference
- Usage Examples
- Integration Guides
- Best Practices

## Responsibilities

* Provide a general-purpose Python implementation of [CycloneDX][link_website]
* Provide type hints for implementation support
* Support JSON/XML document parsing and generation
* Validate CycloneDX documents against schema specifications
* Support multiple CycloneDX specification versions
* Maintain comprehensive data models for BOM manipulation
* Enable pip-based installation for downstream usage

## Capabilities

### Enums
* `BomFormat` - BOM format types
* `ComponentType` - Types of components (e.g., APPLICATION, LIBRARY)
* `ComponentScope` - Component scope types
* `DataFlow` - Data flow types
* `Encoding` - Encoding types
* `ExternalReferenceType` - Types of external references
* `HashAlgorithm` - Supported hash algorithms
* `ImpactAnalysisAffectedStatus` - Impact analysis affected status types
* `ImpactAnalysisJustification` - Impact analysis justification types
* `ImpactAnalysisResponse` - Impact analysis response types
* `ImpactAnalysisState` - Impact analysis state types
* `IssueClassification` - Issue classification types
* `LifecyclePhase` - Lifecycle phase types
* `PatchClassification` - Patch classification types
* `VulnerabilityScoreSource` - Vulnerability score source types
* `VulnerabilitySeverity` - Vulnerability severity types

### Data Models

#### Core Models
* `Bom` - Core BOM model
* `BomRef` - BOM reference handling
* `Metadata` - BOM metadata

#### Component & Service Models
* `Component` - Component representation
* `ComponentEvidence` - Component evidence data
* `Service` - Service representation

#### Dependency Models
* `Dependency` - Dependency information
* `DependencyGraph` - Dependency relationships

#### License Models
* `License` - Base license model
* `LicenseExpression` - License expression handling
* `NamedLicense` - Named license representation
* `SpdxLicense` - SPDX license support

#### Analysis Models
* `ImpactAnalysis` - Impact analysis data
* `Issue` - Issue tracking
* `Vulnerability` - Vulnerability information

#### Reference & Organization Models
* `ExternalReference` - External reference data
* `Hash` - Hash information
* `OrganizationalContact` - Contact information
* `OrganizationalEntity` - Organization information

#### Management Models
* `Property` - Property handling
* `Tool` - Tool representation

#### Repository Models
* `BomRefRepository` - BOM reference management
* `ComponentRepository` - Component management
* `ExternalReferenceRepository` - External reference management
* `LicenseRepository` - License management
* `PropertyRepository` - Property management
* `ToolRepository` - Tool management

### Utilities
* Serial number generation for BOMs
* Hash calculation helpers
* License expression parsing
* XML/JSON serialization helpers

### Specification Support
* 1.6
* 1.5
* 1.4
* 1.3
* 1.2
* 1.1

## Contributing

Feel free to open issues, bug reports or pull requests.  
See the [CONTRIBUTING][contributing_file] file for details.

## Copyright & License

CycloneDX Python Lib is Copyright (c) OWASP Foundation. All Rights Reserved.  
Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.  
See the [LICENSE][license_file] file for the full license.

[cyclonedx-python]: https://github.com/CycloneDX/cyclonedx-python
[jake]: https://github.com/sonatype-nexus-community/jake

[license_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/LICENSE
[contributing_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/CONTRIBUTING.md
[changelog_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/CHANGELOG.md
[link_rtfd]: https://cyclonedx-python-library.readthedocs.io/
[CycloneDX-spec]: https://github.com/CycloneDX/specification/tree/master#readme

[shield_pypi-version]: https://img.shields.io/pypi/v/cyclonedx-python-lib?logo=pypi&logoColor=white "PyPI"
[shield_conda-forge-version]: https://img.shields.io/conda/vn/conda-forge/cyclonedx-python-lib?logo=anaconda&logoColor=white "conda-forge"
[shield_rtfd]: https://img.shields.io/readthedocs/cyclonedx-python-library?logo=readthedocs&logoColor=white "Read the Docs"
[shield_gh-workflow-test]: https://img.shields.io/github/actions/workflow/status/CycloneDX/cyclonedx-python-lib/python.yml?branch=main&logo=GitHub&logoColor=white "build"
[shield_coverage]: https://img.shields.io/codacy/coverage/1f9d451e9cdc49ce99c2a1247adab341?logo=Codacy&logoColor=white "test coverage"
[shield_ossf-best-practices]: https://img.shields.io/cii/percentage/7956?label=OpenSSF%20best%20practices "OpenSSF best practices"
[shield_license]: https://img.shields.io/github/license/CycloneDX/cyclonedx-python-lib?logo=open%20source%20initiative&logoColor=white "license"
[shield_website]: https://img.shields.io/badge/https://-cyclonedx.org-blue.svg "homepage"
[shield_slack]: https://img.shields.io/badge/slack-join-blue?logo=Slack&logoColor=white "slack join"
[shield_groups]: https://img.shields.io/badge/discussion-groups.io-blue.svg "groups discussion"
[shield_twitter-follow]: https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white "twitter follow"

[link_pypi]: https://pypi.org/project/cyclonedx-python-lib/
[link_conda-forge]: https://anaconda.org/conda-forge/cyclonedx-python-lib
[link_codacy]: https://app.codacy.com/gh/CycloneDX/cyclonedx-python-lib
[link_ossf-best-practices]: https://www.bestpractices.dev/projects/7956
[link_website]: https://cyclonedx.org/
[link_slack]: https://cyclonedx.org/slack/invite
[link_discussion]: https://groups.io/g/CycloneDX
[link_twitter]: https://twitter.com/CycloneDX_Spec
[link_gh-workflow-test]: https://github.com/CycloneDX/cyclonedx-python-lib/actions/workflows/python.yml?query=branch%3Amain
