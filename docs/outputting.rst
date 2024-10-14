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

Outputting
==========

Once you have an instance of a :py:mod:`cyclonedx.model.bom.Bom` you can produce output in either **JSON** or **XML**
against any of the supported CycloneDX schema versions.

We provide two helper methods:

* Output to string (for you to do with as you require)
* Output directly to a filename you provide

By default output will be in XML at latest supported schema version - see :py:mod:`cyclonedx.output.LATEST_SUPPORTED_SCHEMA_VERSION`.

Supported CycloneDX Schema Versions
-----------------------------------

This library supports the following schema versions:

* 1.0 (XML) - `(note, 1.1 schema version has no support for JSON)`
* 1.1 (XML) - `(note, 1.1 schema version has no support for JSON)`
* 1.2 (XML, JSON)
* 1.3 (XML, JSON)
* 1.4 (XML, JSON) - the latest supported schema version

Outputting to JSON
------------------

The below example relies on the latest schema version, but sets the output format to JSON. Output is returned
as a ``str``.

.. code-block:: python

    from cyclonedx.output import make_outputter, BaseOutput, OutputFormat, SchemaVersion

    outputter: BaseOutput = make_outputter(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_6)
    bom_json: str = outputter.output_as_string()

Alternatively, if the output format and schema version are constants, you can use the predefined format+schema combined outputs:

.. code-block:: python

    from cyclonedx.output.json import JsonV1Dot6

    outputter = JsonV1Dot6(bom=bom)
    bom_json: str = outputter.output_as_string()


Outputting to XML
------------------

The below example relies on the default output format being XML, but overrides the schema version to 1.2. Output is
written to the supplied filename.

.. code-block:: python

    from cyclonedx.output import make_outputter, BaseOutput, OutputFormat, SchemaVersion

    outputter: BaseOutput = make_outputter(bom=bom, output_format=OutputFormat.XML, schema_version=SchemaVersion.V1_2)
    outputter.output_to_file(filename='/tmp/sbom-v1.2.xml')

Alternatively, if the output format and schema version are constants, you can use the predefined format+schema combined outputs:

.. code-block:: python

    from cyclonedx.output.xml import XmlV1Dot2

    outputter = XmlV1Dot2(bom=bom)
    outputter.output_to_file(filename='/tmp/sbom-v1.2.xml')
