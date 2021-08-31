# Python Library for generating CycloneDX

This CycloneDX module for Python can generate valid CycloneDX bill-of-material document containing an aggregate of all 
project dependencies.

This module is not designed for standalone use. If you're looking for a tool to run to generate CycloneDX
software bill-of-materials documents, why not checkout:
- [Jake](https://github.com/sonatype-nexus-community/jake)

Or you can use this module yourself in your application to generate SBOMs.

CycloneDX is a lightweight BOM specification that is easily created, human-readable, and simple to parse.

## Installation

Install from pypi.org as you would any other Python module:

```
pip install cyclonedx-python-lib
```

## Architecture

This module break out into three key areas:
1. **Parser**: Use a parser that suits your needs to automatically gather information
   about your environment or application
2. **Model**: Internal models used to unify data from different parsers
3. **Output**: Choose and configure an output which allows you to define output format as well
   as the CycloneDX schema version

## The Fine Print

Remember:

It is worth noting that this is **NOT SUPPORTED** by Sonatype, and is a contribution of ours
to the open source community (read: you!)

* Use this contribution at the risk tolerance that you have
* Do NOT file Sonatype support tickets related to `cyclonedx-python-lib` support in regard to this project
* DO file issues here on GitHub, so that the community can pitch in

Phew, that was easier than I thought. Last but not least of all - have fun!

