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

Examples
========

Complex Serialize
-----------------

.. literalinclude:: ../examples/complex_serialize.py
  :language: python
  :linenos:


Complex Deserialize
-------------------

.. literalinclude:: ../examples/complex_deserialize.py
  :language: python
  :linenos:


Validate SBOMs
--------------

The library ships with strict and non‑strict validators for both JSON and
XML CycloneDX documents.  The example below shows how to validate a
Software Bill of Materials (SBOM) from the command line.  It selects the
appropriate validator based on the file extension and reports any
validation errors found.

.. literalinclude:: ../examples/validate_sbom.py
  :language: python
  :linenos:
