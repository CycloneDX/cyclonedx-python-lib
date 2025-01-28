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

Responsibilities
================

* Provide a general purpose Python-implementation of `CycloneDX`_.
* Provide type hints for said implementation, so developers and dev-tools can rely on it.
* Provide data models to work with CycloneDX.
* Provide data model-validators according to `CycloneDX Specification`_.
* Provide JSON- and XML-serializers, that...
   * support all shipped data models.
   * respect any supported `CycloneDX Specification`_ and generates valid output according to it.
   * generate reproducible/deterministic results.
* Provide formal JSON- and XML-validators according to `CycloneDX Specification`_.
* Pre-populate `bom-ref`, so linkage is possible. (affects only some data models)

Capabilities
============

* Enums for the following use cases:
* Data models for the following use cases:
* Factories for the following use cases:
* Builders for the following use cases:
   * Build a :class:`Component <cyclonedx.model.component.Component>` data model that represents this library
   * Build a :class:`Tool <cyclonedx.model.tool.Tool>` data model that represents this library
* Implementation of the `CycloneDX Specification`_ for the following versions:
   * ``1.6``
   * ``1.5``
   * ``1.4``
   * ``1.3``
   * ``1.2``
   * ``1.1``
   * ``1.0``
* Serializer that converts :class:`BOM <cyclonedx.model.bom.Bom>` data models to XML string
* Serializer that converts :class:`BOM <cyclonedx.model.bom.Bom>` data models to JSON string
* Formal validators for JSON string and XML string.
  Requires optional dependencies as described in :ref:`install instructions <install extras>`


.. _CycloneDX: https://cyclonedx.org/
.. _CycloneDX Specification: https://github.com/CycloneDX/specification/#readme
