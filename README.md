# Python Library for generating CycloneDX

[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_pypi-version]][link_pypi]
[![shield_license]][license_file]  
[![shield_website]][link_website]
[![shield_slack]][link_slack]
[![shield_groups]][link_discussion]
[![shield_twitter-follow]][link_twitter]

----

This CycloneDX module for Python can generate valid CycloneDX bill-of-material document containing an aggregate of all
project dependencies.

This module is not designed for standalone use.  
If you're looking for a CycloneDX tool to run to generate (SBOM) software bill-of-materials documents, why not checkout: [CycloneDX Python][cyclonedx-python]

Additionally, the following tool can be used as well (and this library was written to help improve it) [Jake][jake].

Additionally, you can use this module yourself in your application to programmatically generate SBOMs.

CycloneDX is a lightweight BOM specification that is easily created, human-readable, and simple to parse.

## Installation

Install from pypi.org as you would any other Python module:

```shell
pip install cyclonedx-python-lib
```

## Architecture

This module break out into three key areas:

1. **Parser**: Use a parser that suits your needs to automatically gather information about your environment or
   application
2. **Model**: Internal models used to unify data from different parsers
3. **Output**: Choose and configure an output which allows you to define output format as well as the CycloneDX schema
   version

### Parsing

You can use one of the parsers to obtain information about your project or environment. Available parsers:

| Parser | Class / Import | Description |
| ------- | ------ | ------ |
| CondaListJsonParser | `from cyclonedx.parser.conda import CondaListJsonParser` | Parses input provided as a `str` that is output from `conda list --json` |
| CondaListExplicitParser | `from cyclonedx.parser.conda import CondaListExplicitParser` | Parses input provided as a `str` that is output from `conda list --explicit` or `conda list --explicit --md5` |
| Environment | `from cyclonedx.parser.environment import EnvironmentParser` | Looks at the packaged installed in your current Python environment. |
| PipEnvParser | `from cyclonedx.parser.pipenv import PipEnvParser` | Parses `Pipfile.lock` content passed in as a string. |
| PipEnvFileParser | `from cyclonedx.parser.pipenv import PipEnvFileParser` | Parses the `Pipfile.lock` file at the supplied path. |
| PoetryParser | `from cyclonedx.parser.poetry import PoetryParser` | Parses `poetry.lock` content passed in as a string. |
| PoetryFileParser | `from cyclonedx.parser.poetry import PoetryFileParser` | Parses the `poetry.lock` file at the supplied path. |
| RequirementsParser | `from cyclonedx.parser.requirements import RequirementsParser` | Parses a multiline string that you provide that conforms to the `requirements.txt` [PEP-508] standard. |
| RequirementsFileParser | `from cyclonedx.parser.requirements import RequirementsFileParser` | Parses a file that you provide the path to that conforms to the `requirements.txt` [PEP-508] standard. |

#### Example

```py
from cyclonedx.parser.environment import EnvironmentParser

parser = EnvironmentParser()
```

#### Notes on Requirements parsing

CycloneDX software bill-of-materials require pinned versions of requirements. If your `requirements.txt` does not have
pinned versions, warnings will be recorded and the dependencies without pinned versions will be excluded from the
generated CycloneDX. CycloneDX schemas (from version 1.0+) require a component to have a version when included in a
CycloneDX bill of materials (according to schema).

If you need to use a `requirements.txt` in your project that does not have pinned versions an acceptable workaround
might be to:

```shell
pip install -r requirements.txt
pip freeze > requirements-frozen.txt
```

You can then feed in the frozen requirements from `requirements-frozen.txt` _or_ use the `Environment` parser one you
have `pip install`ed your dependencies.

### Modelling

You can create a BOM Model from either a Parser instance or manually using the methods avaialbel directly on the `Bom` class.

The model also supports definition of vulnerabilities for output using the CycloneDX schema extension for
[Vulnerability Disclosures](https://cyclonedx.org/use-cases/#vulnerability-disclosure) as of version 0.3.0.

**Note:** Known vulnerabilities associated with Components can be sourced from various data sources, but this library
will not source them for you. Perhaps look at [Jake][jake] if you're interested in this.

#### Example from a Parser

```py
from cyclonedx.model.bom import Bom
from cyclonedx.parser.environment import EnvironmentParser

parser = EnvironmentParser()
bom = Bom.from_parser(parser=parser)
```

### Generating Output

Once you have an instance of a `Bom` you can produce output in either `JSON` or `XML` against any of the supporting CycloneDX schema versions as you require.

We provide two helper methods:

* Output to string (for you to do with as you require)
* Output directly to a filename you provide

#### Example as JSON

```py
from cyclonedx.output import get_instance, OutputFormat

outputter = get_instance(bom=bom, output_format=OutputFormat.JSON)
outputter.output_as_string()
```

#### Example as XML

```py
from cyclonedx.output import get_instance, SchemaVersion

outputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_2)
outputter.output_to_file(filename='/tmp/sbom-v1.2.xml')
```

## Library API Documentation

The Library API Documentation is available online at [https://cyclonedx.github.io/cyclonedx-python-lib/](https://cyclonedx.github.io/cyclonedx-python-lib/).

## Schema Support

This library is a work in progress and complete support for all parts of the CycloneDX schema will come in future releases.

Here is a summary of the parts of the schema supported by this library:

_Note: We refer throughout using XPath, but the same is true for both XML and JSON output formats._

<table width="100%">
   <thead>
      <tr>
         <th>XPath</th>
         <th>Support v1.3</th>
         <th>Support v1.2</th>
         <th>Support v1.1</th>
         <th>Support v1.0</th>
         <th>Notes</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td><code>/bom</code></td>
         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>
         <td>
            This is the root element and is supported with all it's defined attributes.
         </td>
      </tr>
      <tr>
         <td><code>/bom/metadata</code></td>
         <td>Y</td><td>Y</td><td>N/A</td><td>N/A</td>
         <td>
            <code>timestamp</code> and <code>tools</code> are currently supported 
         </td>
      </tr>
      <tr>
         <td><code>/bom/components</code></td>
         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>
         <td>&nbsp;</td>
      </tr>
      <tr>
         <th colspan="6"><strong><code>/bom/components/component</code></strong></th>
      </tr>
      <tr>
         <td><code>./author</code></td>
         <td>Y</td><td>Y</td><td>N/A</td><td>N/A</td>
         <td>&nbsp;</td>
      </tr>
      <tr>
         <td><code>./name</code></td>
         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>
         <td>&nbsp;</td>
      </tr>
      <tr>
         <td><code>./version</code></td>
         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>
         <td>&nbsp;</td>
      </tr>
      <tr>
         <td><code>./purl</code></td>
         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>
         <td>&nbsp;</td>
      </tr>
      <tr>
         <td><code>./externalReferences</code></td>
         <td>Y</td><td>Y</td><td>Y</td><td>N/A</td>
         <td>Not all Parsers have this information. It will be populated where there is information available.</td>
      </tr>
      <tr>
         <td><code>./hashes</code></td>
         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>
         <td>
            These are supported when programmatically creating a <code>Bom</code> - these will not currently be 
            automatically populated when using a <code>Parser</code>.
         </td>
      </tr>
   </tbody>
</table>

### Notes on Schema Support

* N/A is where the CycloneDX standard does not include this
* If the table above does not refer to an element, it is not currently supported

## Python Support

We endeavour to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).
However, some features may not be possible/present in older Python versions due to their lack of support.

## Changelog

See our [CHANGELOG][chaneglog_file].

## Contributing

Feel free to open issues, bugreports or pull requests.  
See the [CONTRIBUTING][contributing_file] file for details.

## Copyright & License

CycloneDX Python Lib is Copyright (c) OWASP Foundation. All Rights Reserved.  
Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.  
See the [LICENSE][license_file] file for the full license.

[cyclonedx-python]: https://github.com/CycloneDX/cyclonedx-python
[jake]: https://github.com/sonatype-nexus-community/jake

[license_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/LICENSE
[chaneglog_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/CHANGELOG.md
[contributing_file]: https://github.com/CycloneDX/cyclonedx-python-lib/blob/master/CONTRIBUTING.md

[shield_gh-workflow-test]: https://img.shields.io/github/workflow/status/CycloneDX/cyclonedx-python-lib/Python%20CI/main?logo=GitHub&logoColor=white "build"
[shield_pypi-version]: https://img.shields.io/pypi/v/cyclonedx-python-lib?logo=Python&logoColor=white&label=PyPI "PyPI"
[shield_license]: https://img.shields.io/github/license/CycloneDX/cyclonedx-python-lib "license"
[shield_website]: https://img.shields.io/badge/https://-cyclonedx.org-blue.svg "homepage"
[shield_slack]: https://img.shields.io/badge/slack-join-blue?logo=Slack&logoColor=white "slack join"
[shield_groups]: https://img.shields.io/badge/discussion-groups.io-blue.svg "groups discussion"
[shield_twitter-follow]: https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white "twitter follow"
[link_gh-workflow-test]: https://github.com/CycloneDX/cyclonedx-python-lib/actions/workflows/poetry.yml?query=branch%3Amain
[link_pypi]: https://pypi.org/project/cyclonedx-python-lib/
[link_website]: https://cyclonedx.org/
[link_slack]: https://cyclonedx.org/slack/invite
[link_discussion]: https://groups.io/g/CycloneDX
[link_twitter]: https://twitter.com/CycloneDX_Spec

[PEP-508]: https://www.python.org/dev/peps/pep-0508/
