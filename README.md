# Python Library for generating CycloneDX

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/sonatype-nexus-community/cyclonedx-python-lib/Python%20CI)
![Python Version Support](https://img.shields.io/badge/python-3.6+-blue)
![PyPI Version](https://img.shields.io/pypi/v/cyclonedx-python-lib?label=PyPI&logo=pypi)
[![GitHub license](https://img.shields.io/github/license/sonatype-nexus-community/cyclonedx-python-lib)](https://github.com/sonatype-nexus-community/cyclonedx-python-lib/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/sonatype-nexus-community/cyclonedx-python-lib)](https://github.com/sonatype-nexus-community/cyclonedx-python-lib/issues)
[![GitHub forks](https://img.shields.io/github/forks/sonatype-nexus-community/cyclonedx-python-lib)](https://github.com/sonatype-nexus-community/cyclonedx-python-lib/network)
[![GitHub stars](https://img.shields.io/github/stars/sonatype-nexus-community/cyclonedx-python-lib)](https://github.com/sonatype-nexus-community/cyclonedx-python-lib/stargazers)

----

This CycloneDX module for Python can generate valid CycloneDX bill-of-material document containing an aggregate of all
project dependencies.

This module is not designed for standalone use. If you're looking for a CycloneDX tool to run to generate (SBOM) software
bill-of-materials documents, why not checkout:

- [cyclonedx-python](https://github.com/CycloneDX/cyclonedx-python)

Additionally, the following tool can be used as well (and this library was written to help improve it)
- [Jake](https://github.com/sonatype-nexus-community/jake)

Additionally, you can use this module yourself in your application to programmatically generate SBOMs.

CycloneDX is a lightweight BOM specification that is easily created, human-readable, and simple to parse.

## Installation

Install from pypi.org as you would any other Python module:

```
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
| Environment | `from cyclonedx.parser.environment import EnvironmentParser` | Looks at the packaged installed in your current Python environment. |
| RequirementsParser | `from cyclonedx.parser.requirements import RequirementsParser` | Parses a multiline string that you provide that conforms to the `requirements.txt` [PEP-508](https://www.python.org/dev/peps/pep-0508/) standard. |
| RequirementsFileParser | `from cyclonedx.parser.requirements import RequirementsFileParser` | Parses a file that you provide the path to that conforms to the `requirements.txt` [PEP-508](https://www.python.org/dev/peps/pep-0508/) standard. |

#### Example

```
from cyclonedx.parser.environment import EnvironmentParser

parser = EnvironmentParser()
```

### Modelling

You can create a BOM Model from either an Parser instance or manually using the methods avaialbel directly on the `Bom` class.

#### Example from a Parser

```
from cyclonedx.model.bom import Bom
from cyclonedx.parser.environment import EnvironmentParser

parser = EnvironmentParser()
bom = Bom.from_parser(parser=parser)
```

### Generating Output

Once you have an instance of a `Bom` you can produce output in either `JSON` or `XML` against any of the supporting CycloneDX schema versions as you require.

We provide two helper methods:
1. Output to string (for you to do with as you require)
2. Output directly to a filename you provide

##### Example as JSON

```
from cyclonedx.output import get_instance, OutputFormat

outputter = get_instance(bom=bom, output_format=OutputFormat.JSON)
outputter.output_as_string()
```

##### Example as XML
```
from cyclonedx.output import get_instance, SchemaVersion

outputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_2)
outputter.output_to_file(filename='/tmp/sbom-v1.2.xml')
```

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
            Only <code>timestamp</code> is currently supported 
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
   </tbody>
</table>

### Notes on Schema Support

1. N/A is where the CycloneDX standard does not include this
2. If the table above does not refer to an element, it is not currently supported

## Python Support

We endeavour to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).
However, some features may not be possible/present in older Python versions due to their lack of support.

## Copyright & License
CycloneDX Python Lib is Copyright (c) OWASP Foundation. All Rights Reserved.

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.
