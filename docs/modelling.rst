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

You can create a BOM Model from either a :py:mod:`cyclonedx.parser` instance or manually using the methods available
directly on the :py:mod:`cyclonedx.model.bom.Bom` class.

Vulnerabilities are supported by the Model as of version 0.3.0.

    **Note:** Known vulnerabilities associated with Components can be sourced from various data sources, but this library
    will not source them for you. Perhaps look at `Jake`_ if you're interested in this.

Example BOM using a Parser
--------------------------

    **Note:** Concreate parser implementations were moved out of this library and into `CycloneDX Python`_ as of version
    ``1.0.0``.

.. code-block:: python

    from cyclonedx.model.bom import Bom
    from cyclonedx_py.parser.environment import EnvironmentParser

    parser = EnvironmentParser()
    bom = Bom.from_parser(parser=parser)

Example BOM created programmatically
------------------------------------

.. note::

    It is recommended that you have a good understanding of the `CycloneDX Schema`_ before attempting to create a BOM
    programmatically with this library.


For the most up-to-date in-depth examples, look at our `Unit Tests`_.


.. _CycloneDX Python: https://github.com/CycloneDX/cyclonedx-python
.. _Jake: https://pypi.org/project/jake
.. _CycloneDX Schema: https://cyclonedx.org/docs/latest
.. _Unit Tests: https://github.com/CycloneDX/cyclonedx-python-lib/tree/main/tests