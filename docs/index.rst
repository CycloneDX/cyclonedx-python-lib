.. # Licensed under the Apache License, Version 2.0 (the "License");
   # you may not use this file except in compliance with the License.
   # You may obtain a copy of the License at
   #
   #     http://www.apache.org/licenses/LICENSE-2.0
   #
   # Unless required by applicable law or agreed to in writing, software
   # distributed under the License is distributed on an "AS IS" BASIS,
   # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   # See the License for the specific language governing permissions and
   # limitations under the License.
   #
   # SPDX-License-Identifier: Apache-2.0

CycloneDX’s Python Library documentation
====================================================

CycloneDX is a lightweight BOM specification that is easily created, human-readable, and simple to parse.

This CycloneDX module for Python can generate valid CycloneDX bill-of-material document containing an aggregate of all
project dependencies.

As of version ``3.0.0``, the internal data model was adjusted to allow CycloneDX VEX documents to be produced as per
`official examples`_ linking VEX to a separate BOM.

This module is not designed for standalone use (i.e. it is not executable on it’s own). If you’re looking for a
CycloneDX tool to run to generate (SBOM) software bill-of-materials documents, why not checkout:

* `CycloneDX Python`_
* `Jake`_
* `CycloneDX Tool Center`_

This library was designed to be used by developers - you can use this module yourself in your application to
programmatically generate SBOMs.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   architecture
   examples
   contributing
   support
   changelog


.. _CycloneDX Python: https://pypi.org/project/cyclonedx-bom/
.. _Jake: https://pypi.org/project/jake
.. _CycloneDX Tool Center: https://cyclonedx.org/tool-center/
.. _official examples: https://cyclonedx.org/capabilities/bomlink/#linking-external-vex-to-bom-inventory
