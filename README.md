# Python Library for generating CycloneDX

[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_rtfd]][link_rtfd]
[![shield_pypi-version]][link_pypi]
[![shield_conda-forge-version]][link_conda-forge]
[![shield_license]][license_file]  
[![shield_website]][link_website]
[![shield_slack]][link_slack]
[![shield_groups]][link_discussion]
[![shield_twitter-follow]][link_twitter]

----

This CycloneDX module for Python can generate valid CycloneDX bill-of-material document containing an aggregate of all
project dependencies. CycloneDX is a lightweight BOM specification that is easily created, human-readable, and simple 
to parse.

**This module is not designed for standalone use.**

As of version `3.0.0`, the internal data model was adjusted to allow CycloneDX VEX documents to be produced as per
[official examples](https://cyclonedx.org/capabilities/bomlink/#linking-external-vex-to-bom-inventory) linking a VEX 
documents to a separate BOM document.

If you're looking for a CycloneDX tool to run to generate (SBOM) software bill-of-materials documents, why not checkout 
[CycloneDX Python][cyclonedx-python] or [Jake][jake].

Alternatively, you can use this module yourself in your application to programmatically generate CycloneDX BOMs.

View the documentation [here](https://cyclonedx-python-library.readthedocs.io/).

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

[shield_gh-workflow-test]: https://img.shields.io/github/actions/workflow/status/CycloneDX/cyclonedx-python-lib/poetry.yml?branch=main&logo=GitHub&logoColor=white "build"
[shield_pypi-version]: https://img.shields.io/pypi/v/cyclonedx-python-lib?logo=pypi&logoColor=white&label=PyPI "PyPI"
[shield_conda-forge-version]: https://img.shields.io/conda/vn/conda-forge/cyclonedx-python-lib?logo=anaconda&logoColor=white&label=conda-forge "conda-forge"
[shield_rtfd]: https://img.shields.io/readthedocs/cyclonedx-python-library?logo=readthedocs&logoColor=white "Read the Docs"
[shield_license]: https://img.shields.io/github/license/CycloneDX/cyclonedx-python-lib?logo=open%20source%20initiative&logoColor=white "license"
[shield_website]: https://img.shields.io/badge/https://-cyclonedx.org-blue.svg "homepage"
[shield_slack]: https://img.shields.io/badge/slack-join-blue?logo=Slack&logoColor=white "slack join"
[shield_groups]: https://img.shields.io/badge/discussion-groups.io-blue.svg "groups discussion"
[shield_twitter-follow]: https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white "twitter follow"
[link_gh-workflow-test]: https://github.com/CycloneDX/cyclonedx-python-lib/actions/workflows/poetry.yml?query=branch%3Amain
[link_pypi]: https://pypi.org/project/cyclonedx-python-lib/
[link_conda-forge]: https://anaconda.org/conda-forge/cyclonedx-python-lib
[link_rtfd]: https://cyclonedx-python-library.readthedocs.io/en/latest/?badge=latest
[link_website]: https://cyclonedx.org/
[link_slack]: https://cyclonedx.org/slack/invite
[link_discussion]: https://groups.io/g/CycloneDX
[link_twitter]: https://twitter.com/CycloneDX_Spec

[PEP-508]: https://www.python.org/dev/peps/pep-0508/
