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

Work with [CycloneDX] documents.  
OWASP CycloneDX is a full-stack Bill of Materials (BOM) standard that provides advanced supply chain capabilities for cyber risk reduction.

## Responsibilities

* Provide a general purpose _Python_-implementation of [_CycloneDX_][CycloneDX].
* Provide type hints and documentation for all implementations to support developers and development tools.
* Provide data models to work with _CycloneDX_.
* Provide JSON and XML normalizers that:
  * Support all shipped data models
  * Respect any injected [_CycloneDX_ Specification][CycloneDX-spec] and generate valid output
  * Can prepare data structures for JSON and XML serialization
* Serialization:
  * Provide JSON serialization
  * Provide XML serialization
* Validation against _CycloneDX_ Specification:
  * Provide JSON validation
  * Provide XML validation

## Capabilities

* Data models for:
  * `Bom`
  * Components and Component repositories
  * Dependencies
  * External references
  * License expressions and repositories
  * Metadata
  * Properties
  * Tools
  * VEX (Vulnerability Exploitability eXchange)
* Support for multiple BOM types:
  * SBOM (Software Bill of Materials)
  * VEX (Vulnerability Exchange)
  * VDR (Vulnerability Disclosure Report)
  * OBOM (Operations BOM)
  * MBOM (Manufacturing BOM)
  * SaaSBOM (Software as a Service BOM)
* Implementation of [_CycloneDX_ Specification][CycloneDX-spec] versions:
  * 1.0 through 1.5
* Utilities for:
  * Generating valid BOM serial numbers
  * Managing BOM references
  * Handling dependencies
* Validation capabilities for both JSON and XML formats

## Installation

Install via pip:
```shell
pip install cyclonedx-python-lib
```

Or via conda:
```shell
conda install -c conda-forge cyclonedx-python-lib
```

Optional validation support:
```shell
# For complete validation support
pip install cyclonedx-python-lib[validation]

# For JSON-only validation
pip install cyclonedx-python-lib[json-validation]

# For XML-only validation
pip install cyclonedx-python-lib[xml-validation]
```

## Usage

Basic example of creating a BOM:

```python
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component

# Create a new BOM
bom = Bom()

# Add a component
component = Component(
    name="my-component",
    version="1.0.0"
)
bom.components.add(component)

# Serialize to JSON or XML
json_output = outputter.output_json(bom)
xml_output = outputter.output_xml(bom)
```

See the [documentation][link_rtfd] for more detailed examples and API reference.

## Python Support

We support all [current actively supported Python versions](https://www.python.org/downloads/):
* Python 3.8
* Python 3.9
* Python 3.10
* Python 3.11
* Python 3.12
* Python 3.13

## Documentation

* API documentation is available on [Read the Docs][link_rtfd]
* Type hints are provided for IDE and tool support
* Examples are included in the repository

## Contributing

Feel free to open issues, bug reports, or pull requests.  
See the [CONTRIBUTING][contributing_file] file for details.

## License

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.  
See the [LICENSE][license_file] file for the full license.

[CycloneDX]: https://cyclonedx.org/
[CycloneDX-spec]: https://github.com/CycloneDX/specification/tree/master#readme

[license_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/LICENSE
[contributing_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/CONTRIBUTING.md

[shield_pypi-version]: https://img.shields.io/pypi/v/cyclonedx-python-lib?logo=pypi&logoColor=white&label=PyPI "PyPI"
[shield_conda-forge-version]: https://img.shields.io/conda/vn/conda-forge/cyclonedx-python-lib?logo=anaconda&logoColor=white&label=conda-forge "conda-forge"
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
[link_rtfd]: https://cyclonedx-python-library.readthedocs.io/
[link_gh-workflow-test]: https://github.com/CycloneDX/cyclonedx-python-lib/actions/workflows/python.yml?query=branch%3Amain
[link_codacy]: https://app.codacy.com/gh/CycloneDX/cyclonedx-python-lib
[link_ossf-best-practices]: https://www.bestpractices.dev/projects/7956
[link_website]: https://cyclonedx.org/
[link_slack]: https://cyclonedx.org/slack/invite
[link_discussion]: https://groups.io/g/CycloneDX
[link_twitter]: https://twitter.com/CycloneDX_Spec
