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

Architecture
============

This library broadly is separated into three key functional areas:

1. **Parser**: Downstream tools may provide concrete implementation of the :py:mod:`cyclonedx.parser.BaseParser` which
   can easily help you build a Model from your project or ecosystem.
   For Python specific parser implementations see `cyclonedx-python`_
2. **Model**: Internal models used to unify data from different parsers

    **Note:** As of version 4.0.0 of this library we support deserialization from JSON and XML as well as
    serialization to JSON and XML.

3. **Output**: Choose and configure an output which allows you to define output format as well as the CycloneDX schema
   version

When wishing to generate a BOM, the process is as follows:

1. Generate a Model by either:
    1. Programmatically using this library
    2. By deserializing from an existing CycloneDX BOM document
    3. From a :py:mod:`cyclonedx.parser`
2. Output the Model using an :py:mod:`cyclonedx.output` instance that reflects the schema version and format you require

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modelling
   schema-support
   outputting

.. _cyclonedx-python: https://pypi.org/project/cyclonedx-bom/
