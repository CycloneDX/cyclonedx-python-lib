# CycloneDX JavaScript Library

[![shield_npm-version]][link_npm]
[![shield_rtfd]][link_rtfd]
[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_coverage]][link_codacy]
[![shield_ossf-best-practices]][link_ossf-best-practices]
[![shield_license]][license_file]  
[![shield_website]][link_website]
[![shield_slack]][link_slack]
[![shield_groups]][link_discussion]
[![shield_twitter-follow]][link_twitter]

----

Core functionality of [_CycloneDX_][link_website] for _JavaScript_ (_Node.js_ or _WebBrowsers_), written in _TypeScript_ and compiled for the target.

## Responsibilities

* Provide a general purpose _JavaScript_-implementation of [_CycloneDX_][link_website] for _Node.js_ and _WebBrowsers_.
* Provide typing for said implementation, so developers and dev-tools can rely on it.
* Provide data models to work with _CycloneDX_.
* Provide JSON- and XML-normalizers that:
  * Support all shipped data models.
  * Respect any injected [_CycloneDX_ Specification][CycloneDX-spec] and generate valid output according to it.
  * Can be configured to generate reproducible/deterministic output.
  * Can prepare data structures for JSON- and XML-serialization.
* Serialization:
  * Provide a universal JSON-serializer for all target environments.
  * Provide an XML-serializer for all target environments.
  * Support the downstream implementation of custom XML-serializers tailored to specific environments by providing an abstract base class that takes care of normalization and BomRef-discrimination. This is done because there is no universal XML support in _JavaScript_.
* Provide formal JSON- and XML-validators according to [_CycloneDX_ Specification][CycloneDX-spec] (currently for _Node.js_ only).

## Capabilities

* Enums for the following use cases:
  * `AttachmentEncoding`
  * `ComponentScope`
  * `ComponentType`
  * `ExternalReferenceType`
  * `HashAlgorithm`
  * `Vulnerability` related:  
    * `AffectStatus`
    * `AnalysisJustification`
    * `AnalysisResponse`
    * `AnalysisState`
    * `RatingMethod`
    * `Severity`
* Data models for the following use cases:
  * `Attachment`
  * `Bom`
  * `BomLink`, `BomLinkDocument`, `BomLinkElement`
  * `BomRef`, `BomRefRepository`
  * `Component`, `ComponentRepository`, `ComponentEvidence`
  * `ExternalReference`, `ExternalReferenceRepository`
  * `Hash`, `HashContent`,  `HashDictionary`
  * `LicenseExpression`, `NamedLicense`, `SpdxLicense`, `LicenseRepository`
  * `Metadata`
  * `OrganizationalContact`, `OrganizationalContactRepository`
  * `OrganizationalEntity`, `OrganizationalEntityRepository`
  * `Property`, `PropertyRepository`
  * `SWID`
  * `Tool`, `ToolRepository`
  * Vulnerability-related:
    * `Advisory`, `AdvisoryRepository`
    * `Affect`, `AffectRepository`, 
      - AffectedSingleVersion, 
      - AffectedVersionRange, 
      - AffectedVersionRepository
    * Analysis
    * Credits
    * Rating, RatingRepository
    * Reference, ReferenceRepository
    * Source
    * Vulnerability, VulnerabilityRepository
* Utilities for the following use cases:
  * Generate valid random SerialNumbers for Bom.serialNumber.
* Factories for the following use cases:
  * Create data models from any license descriptor string.
  * Create PackageURL from Component data models.
  * Specific to _Node.js_: create data models from PackageJson-like data structures and derived data.
* Builders for the following use cases:
  * Specific to _Node.js_: create deep data models Tool or Component from PackageJson-like data structures.
* Implementation of the [_CycloneDX_ Specification][CycloneDX-spec] for the following versions:
  * `1.6`
  * `1.5`
  * `1.4`
  * `1.3`
  * `1.2`
* Normalizers that convert data models to JSON structures.
* Normalizers that convert data models to XML structures.
* Universal serializer that converts Bom data models to JSON string.
* Specific Serializer that converts Bom data models to XML string:
  - Specific to _WebBrowsers_: implementation utilizes browser-specific document generators and printers.
  - Specific to _Node.js_: implementation utilizes [optional dependencies](#optional-dependencies) as described below.
* Formal validators for JSON string and XML string (currently for _Node.js_ only).  
   Requires [optional dependencies](#optional-dependencies) as described below.

## Installation

This package and the build results are available for _npm_, _pnpm_, and _yarn_: 

```shell
npm i -S @cyclonedx/cyclonedx-library
pnpm add @cyclonedx/cyclonedx-library
yarn add @cyclonedx/cyclonedx-library
