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

OWASP `CycloneDX`_ is a full-stack Bill of Materials (BOM) standard
that provides advanced supply chain capabilities for cyber risk reduction.

This Python package provides data models, validators and more,
to help you create/render/read CycloneDX documents.

**This package is not designed for standalone use. It is a software library.**

As of version ``3.0.0`` of this library, the internal data model was adjusted to allow CycloneDX VEX documents to be produced as per
`official examples`_ linking VEX to a separate CycloneDX document.

If you're looking for a CycloneDX tool to run to generate (SBOM) software bill-of-materials documents, why not checkout
`CycloneDX Python`_ or `Jake`_.


.. _CycloneDX: https://cyclonedx.org/
.. _official examples: https://cyclonedx.org/capabilities/bomlink/#linking-external-vex-to-bom-inventory
.. _CycloneDX Python: https://pypi.org/project/cyclonedx-bom/
.. _Jake: https://pypi.org/project/jake
.. _CycloneDX Tool Center: https://cyclonedx.org/tool-center/


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   architecture
   examples
   contributing
   support
   changelog
   upgrading
