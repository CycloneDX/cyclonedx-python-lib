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

## Overview

CycloneDX Python Library provides a comprehensive implementation for working with CycloneDX documents in Python. It supports creating, parsing, and validating Software Bill of Materials (SBOM) in both JSON and XML formats.

## Key Features

* **Full CycloneDX Support**: Implements [CycloneDX Specification][CycloneDX-spec] versions 1.0 through 1.5
* **Multiple BOM Types**:
  - SBOM (Software Bill of Materials)
  - VEX (Vulnerability Exchange)
  - VDR (Vulnerability Disclosure Report)
  - OBOM (Operations BOM)
  - MBOM (Manufacturing BOM)
  - SaaSBOM (Software as a Service BOM)
* **Rich Data Models**:
  - Components and Component repositories
  - Dependencies management
  - License expressions and repositories
  - External references
  - VEX (Vulnerability Exploitability eXchange)
* **Format Support**:
  - JSON serialization and validation
  - XML serialization and validation
* **Developer-Friendly**:
  - Complete type hints
  - Comprehensive documentation
  - IDE integration support

## Installation

Choose your preferred installation method:

```shell
# Via pip
pip install cyclonedx-python-lib

# Via conda
conda install -c conda-forge cyclonedx-python-lib

# With validation support
pip install cyclonedx-python-lib[validation]     # Complete validation
pip install cyclonedx-python-lib[json-validation] # JSON-only validation
pip install cyclonedx-python-lib[xml-validation]  # XML-only validation
```

## Quick Start

### Basic BOM Creation

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

### Complex Example: Working with JSON and XML

```python
from cyclonedx.model.bom import Bom
from cyclonedx.schema import SchemaVersion
from cyclonedx.validation import JsonStrictValidator
from defusedxml import ElementTree as SafeElementTree

# Create and validate JSON BOM
json_validator = JsonStrictValidator(SchemaVersion.V1_6)
validation_errors = json_validator.validate_str(json_data)
if not validation_errors:
    bom_from_json = Bom.from_json(json_data)

# Create and validate XML BOM
xml_validator = make_schemabased_validator(OutputFormat.XML, SchemaVersion.V1_6)
validation_errors = xml_validator.validate_str(xml_data)
if not validation_errors:
    bom_from_xml = Bom.from_xml(SafeElementTree.fromstring(xml_data))
```

## Advanced Usage

### Component with Dependencies

```python
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component

# Create main component
app = Component(
    name="myApp",
    version="1.0.0",
    component_type="application"
)

# Create dependency
library = Component(
    name="some-library",
    version="2.1.0",
    component_type="library"
)

# Add to BOM with dependency relationship
bom = Bom()
bom.components.add(app)
bom.components.add(library)
bom.dependencies.add(app, [library])
```

## Python Support

Supports all current Python versions:
* Python 3.8
* Python 3.9
* Python 3.10
* Python 3.11
* Python 3.12
* Python 3.13

## Documentation & Resources

* [Full API Documentation][link_rtfd]
* [GitHub Repository](https://github.com/CycloneDX/cyclonedx-python-lib)
* [CycloneDX Specification][CycloneDX-spec]
* Join the community:
  * [Slack Channel][link_slack]
  * [Discussion Group][link_discussion]
  * [Twitter][link_twitter]

## Contributing

We welcome contributions! Please see our [CONTRIBUTING][contributing_file] guide for details.

## License

Licensed under the Apache License, Version 2.0. See the [LICENSE][license_file] file for details.

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
