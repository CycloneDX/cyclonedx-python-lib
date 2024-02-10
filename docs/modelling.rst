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

Modelling
=========

You can create a BOM Model from either manually using the methods available
directly on the :py:class:`cyclonedx.model.bom.Bom` class,
or deserialize a JSON/XML via :py:meth:`cyclonedx.model.bom.Bom.from_json`/:py:meth:`cyclonedx.model.bom.Bom.from_xml`

Vulnerabilities are supported by the Model as of version 0.3.0.

    **Note:** Known vulnerabilities associated with Components can be sourced from various data sources, but this library
    will not source them for you. Perhaps look at `Jake`_ if you're interested in this.

Example BOM created programmatically
------------------------------------

.. note::

    It is recommended that you have a good understanding of the `CycloneDX Schema`_ before attempting to create a BOM
    programmatically with this library.


For the most up-to-date in-depth examples, look at our `Unit Tests`_.

Example BOM created from existing CycloneDX BOM
------------------------------------

.. note::

    Supported from version 4.0.0 of this library.

Deserializing from a CycloneDX JSON BOM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each model class in this library that is serializable provides a magic ``from_json()`` method.

See the example below to read and deserialize a JSON CycloneDX document. Note that reading the file and loading as JSON
is the programmers responsibility.

.. code-block:: python

    import json
    from cyclonedx.model.bom import Bom

    with open('/path/to/my/cyclonedx.json') as input_json:
        deserialized_bom = Bom.from_json(data=json.loads(input_json.read()))


Deserializing from a CycloneDX XML BOM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each model class in this library that is serializable provides a magic ``from_xml()`` method.

See the example below to read and deserialize a XML CycloneDX document. Note that reading the file and loading as XML
is the programmers responsibility. Be careful to avoid XML vulnerabilities as documented `here`_. It is recommended that
you use a library such as `defusedxml` instead of the native `xml.etree.ElementTree`.

.. code-block:: python

    from xml.etree import ElementTree
    from cyclonedx.model.bom import Bom

    with open('/path/to/my/cyclonedx.xml') as input_xml:
        deserialized_bom = cast(Bom, Bom.from_xml(data=ElementTree.fromstring(input_xml.read())))




.. _CycloneDX Python: https://github.com/CycloneDX/cyclonedx-python
.. _Jake: https://pypi.org/project/jake
.. _CycloneDX Schema: https://cyclonedx.org/docs/latest
.. _Unit Tests: https://github.com/CycloneDX/cyclonedx-python-lib/tree/main/tests
.. _here: https://docs.python.org/3/library/xml.html#xml-vulnerabilities
