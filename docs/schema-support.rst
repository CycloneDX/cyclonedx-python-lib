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

Schema Support
==============

This library has partial support for the CycloneDX specification (we continue to grow support).

The following sub-sections aim to explain what support this library provides and any known gaps in support. We do this
by calling out support for data as defined in the latest CycloneDX standard specification, regardless of whether it is
supported in prior versions of the CycloneDX schema.

+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| Data Path                  | Supported?    | Notes                                                                                             |
+============================+===============+===================================================================================================+
| ``bom[@version]``          | Yes           |                                                                                                   |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom[@serialNumber]``     | Yes           |                                                                                                   |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.metadata``           | Yes           |                                                                                                   |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.components``         | Yes           | Not supported: ``modified`` (as it is deprecated), ``signature``.                                 |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.services``           | Yes           | Not supported: ``signature``.                                                                     |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.externalReferences`` | Yes           |                                                                                                   |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.dependencies``       | Yes           | Since ``2.3.0``                                                                                   |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.compositions``       | No            |                                                                                                   |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.properties``         | No            | See `schema specification bug 130`_                                                               |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.vulnerabilities``    | Yes           | Note: Prior to CycloneDX 1.4, these were present under ``bom.components`` via a schema extension. |
|                            |               | Note: As of ``cyclonedx-python-lib`` ``>3.0.0``, Vulnerability are modelled differently                 |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+
| ``bom.signature``          | No            |                                                                                                   |
+----------------------------+---------------+---------------------------------------------------------------------------------------------------+


.. _schema specification bug 130: https://github.com/CycloneDX/specification/issues/130