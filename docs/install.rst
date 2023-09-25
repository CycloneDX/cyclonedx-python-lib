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

Installation
============

Install from `pypi.org`_ as you would any other Python module using your preferred package manager:

.. code-block:: sh

    pip install cyclonedx-python-lib

*CycloneDX-python-lib* is also available from `conda-forge`_.

.. _pypi.org: https://pypi.org/project/cyclonedx-python-lib/
.. _conda-forge: https://anaconda.org/conda-forge/cyclonedx-python-lib

Extras
------

The following extras are available when installing this package:

`json-validation`
    Install the optional dependencies needed for JSON validation.
`xml-validation`
    Install the optional dependencies needed for XML validation.
`validation`
    Install the optional dependencies needed for all supported validations.

They can be used when installing in order to include additional dependencies, e.g.:

.. code-block:: sh

    pip install 'cyclonedx-python-lib[validation]'
