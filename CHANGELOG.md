# Changelog

<!--next-version-placeholder-->

## v2.5.1 (2022-06-10)
### Fix
* Add missing `Vulnerability` comparator for sorting ([#246](https://github.com/CycloneDX/cyclonedx-python-lib/issues/246)) ([`c3f3d0d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c3f3d0d105f0dcf991175040b6d6c2b6e7e25d8f))

## v2.5.0 (2022-06-10)
### Feature
* Use `SortedSet` in model to improve reproducibility - this will provide predictable ordering of various items in generated CycloneDX documents - thanks to @RodneyRichardson ([`8a1c404`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8a1c4043f502292b32c4ab36a8618cf3f67ac8df))

### Documentation
* Fix typo  "This is out" -> "This is our" ([`ef0278a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ef0278a2044147e73a281c5a59f95049d4af7641))

## v2.4.0 (2022-05-17)
### Feature
* **deps:** Remove unused `typing-extensions` constraints ([`2ce358a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2ce358a37e6ce5f06aa9297aed17f8f5bea38e93))

## v2.3.0 (2022-04-20)
### Feature
* Add support for Dependency Graph in Model and output serialisation ([`ea34513`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ea34513f8229a909007793288ace2f6f51684333))

## v2.2.0 (2022-04-12)
### Feature
* Bump XML schemas to latest fix version for 1.2-1.4 - see: ([`bd2e756`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd2e756de15c37b34d2866e8de521556420bd5d3))
* Bump JSON schemas to latest fix verison for 1.2 and 1.3 - see: ([`bd6a088`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd6a088d51c995c0f08271f56aedb456c60c1a2e))

## v2.1.1 (2022-04-05)
### Fix
* Prevent error if `version` not set ([`b9a84b5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9a84b5b39fe6cb1560764e86f8bd144f2a901e3))
* `version` being optional in JSON output can raise error ([`ba0c82f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba0c82fbde7ba47502c45caf4fa89e9e4381f482))

## v2.1.0 (2022-03-28)
### Feature
* Output errors are verbose ([`bfe8fb1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bfe8fb18825251fd9f146458122aa06137ec27c0))

## v2.0.0 (2022-02-21)
### Feature
* Bump dependencies ([`da3f0ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/da3f0ca3e8b90b37301c03f889eb089bca649b09))
* Completed work on #155 ([#172](https://github.com/CycloneDX/cyclonedx-python-lib/issues/172)) ([`a926b34`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a926b34c7facb8b3709936fe00b62a0b80338f31))
* Support complete model for `bom.metadata` ([#162](https://github.com/CycloneDX/cyclonedx-python-lib/issues/162)) ([`2938a6c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2938a6c001a5b0b25477241d4ad6601030c55165))
* Support for `bom.externalReferences` in JSON and XML #124 ([`1b733d7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1b733d75a78e3757010a8049cab5c7d4656dc2a5))
* Complete support for `bom.components` ([#155](https://github.com/CycloneDX/cyclonedx-python-lib/issues/155)) ([`32c0139`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/32c01396251834c69a5b23c82a5554faf8447f61))
* Support services in XML BOMs ([`9edf6c9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9edf6c940d20a44f5b99c557392a9fa4532b332e))

### Fix
* `license_url` not serialised in XML output #179 ([#180](https://github.com/CycloneDX/cyclonedx-python-lib/issues/180)) ([`f014d7c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f014d7c4411de9ed5e9cb877878ae416d85b2d92))
* `Component.bom_ref` is not Optional in our model implementation (in the schema it is) - we generate a UUID if `bom_ref` is not supplied explicitly ([`5c954d1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5c954d1e39ce8509ab36e6de7d521927ad3c997c))
* Temporary fix for `__hash__` of Component with `properties` #153 ([`a51766d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a51766d202c3774003dd7cd8c115b2d9b3da1f50))
* Further fix for #150 ([`1f55f3e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1f55f3edfeacfc515ef0b5e493c27dd6e14861d6))
* Regression introduced by first fix for #150 ([`c09e396`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c09e396b98c484d1d3d509a5c41746133fe41276))
* Components with no version (optional since 1.4) produce invalid BOM output in XML #150 ([`70d25c8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/70d25c8c162e05a5992761ccddbad617558346d1))
* `expression` not supported in Component Licsnes for version 1.0 ([`15b081b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/15b081bd1891566dbe00e18a8b21d3be87154f72))

### Breaking
* Adopt PEP-3102 ([`da3f0ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/da3f0ca3e8b90b37301c03f889eb089bca649b09))
* Optional Lists are now non-optional Sets ([`da3f0ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/da3f0ca3e8b90b37301c03f889eb089bca649b09))
* Remove concept of DEFAULT schema version - replaced with LATEST schema version ([`da3f0ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/da3f0ca3e8b90b37301c03f889eb089bca649b09))
* Added `BomRef` data type ([`da3f0ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/da3f0ca3e8b90b37301c03f889eb089bca649b09))

## v1.3.0 (2022-01-24)
### Feature
* `bom-ref` for Component and Vulnerability default to a UUID ([#142](https://github.com/CycloneDX/cyclonedx-python-lib/issues/142)) ([`3953bb6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3953bb676f423c325ca4d80f3fcee33ad042ad93))

## v1.2.0 (2022-01-24)
### Feature
* Add CPE to component ([#138](https://github.com/CycloneDX/cyclonedx-python-lib/issues/138)) ([`269ee15`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/269ee155f203d5771c56edb92f7279466bf2012f))

## v1.1.1 (2022-01-19)
### Fix
* Bump dependencies ([#136](https://github.com/CycloneDX/cyclonedx-python-lib/issues/136)) ([`18ec498`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/18ec4987f6aa4a259d30000a19aa6ee1d49681d1))

## v1.1.0 (2022-01-13)
### Feature
* Add support for `bom.metadata.component` ([#118](https://github.com/CycloneDX/cyclonedx-python-lib/issues/118)) ([`1ac31f4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1ac31f4cb14b6c466e092ff38ee2aa472c883c5d))

## v1.0.0 (2022-01-13)

Support for CycloneDX schema version 1.4 (#108)

### Breaking Changes
Support for CycloneDX 1.4. This includes:
* Support for `tools` having `externalReferences`
* Allowing `version` for a `Component` to be optional in 1.4
* Support for `releaseNotes` per `Component`
* Support for the core schema implementation of Vulnerabilities (VEX)

### Features
* `$schema` is now included in JSON BOMs
* Concrete Parsers how now been moved into downstream projects to keep this libraries focus on modelling and outputting CycloneDX - see https://github.com/CycloneDX/cyclonedx-python

### Fixes
* Unit tests now include schema validation (we've left schema validation out of the core library due to dependency bloat)
* Ensure schema is adhered to in 1.0
* URIs are now used throughout the library through a new `XsUri` class to provide URI validation

### Other
* Documentation is now hosted on readthedocs.org (https://cyclonedx-python-library.readthedocs.io/)
* Added reference to release of this library on Anaconda

## v0.12.3 (2021-12-15)
### Fix
* Removed requirements-parser as dependency (temp) as not available for Python 3 as Wheel ([#98](https://github.com/CycloneDX/cyclonedx-python-lib/issues/98)) ([`3677d9f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3677d9fd584b7c0eb715954bb7b8adc59c0bc9b1))

## v0.12.2 (2021-12-09)
### Fix
* Tightened dependency `packageurl-python` ([#95](https://github.com/CycloneDX/cyclonedx-python-lib/issues/95)) ([`eb4ae5c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/eb4ae5ca8842877b780a755b6611feef847bdb8c))

## v0.12.1 (2021-12-09)
### Fix
* Further loosened dependency definitions ([`8bef6ec`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8bef6ecad36f51a003b266d776c9520d33e06034))

## v0.12.0 (2021-12-09)
### Feature
* Loosed dependency versions to make this library more consumable ([`55f10fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/55f10fb5524dafa68112c0836806c27bdd74fcbe))

## v0.11.1 (2021-11-10)
### Fix
* Constructor for `Vulnerability` to correctly define `ratings` as optional ([`395a0ec`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/395a0ec14ebcba8e0849a0ced30ec4163c42fa7a))

## v0.11.0 (2021-11-10)
### Feature
* Typing & PEP 561 ([`9144765`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/91447656c0914ceb2af2e4b7282292ec7b93f5bf))

## v0.10.2 (2021-10-21)
### Fix
* Correct way to write utf-8 encoded files ([`49f9369`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/49f9369b3eba47a3a8d1bcc505546d7dfaf4c5fe))

## v0.10.1 (2021-10-21)
### Fix
* Ensure output to file is UTF-8 ([`a10da20`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a10da20865e90e9a0a5bb1e12fba9cfd23970c39))
* Ensure output to file is UTF-8 ([`193bf64`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/193bf64cdb19bf6fb9662367402dcf7eaab8dd1a))

## v0.10.0 (2021-10-20)
### Feature
* Add support for Conda ([`bd29c78`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd29c782d39a4956f482b9e4de20d7f829beefba))

## v0.9.1 (2021-10-19)
### Fix
* Missing check for Classifiers in Environment Parser ([`b7fa38e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b7fa38e9740bbc5b4c406410df37c3b34818010c))

## v0.9.0 (2021-10-19)
### Feature
* Add support for parsing package licenses when using the `Environment` Parsers ([`c414eaf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c414eafde2abaca1005a2a0af6993fcdc17897d3))

## v0.8.3 (2021-10-14)
### Fix
* Coding standards violations ([`00cd1ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/00cd1ca20899b6861b1b959611a3556ffad36832))
* Handle `Pipfile.lock` dependencies without an `index` specified ([`26c62fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/26c62fb996c4b1b2bf719e10c9072cf4fbadab9f))

## v0.8.2 (2021-10-14)
### Fix
* Add namespace and subpath support to Component to complete PackageURL Spec support ([`780adeb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/780adebe3861ef08eb1e8817a5e9e3451c0a2137))

## v0.8.1 (2021-10-12)
### Fix
* Multiple hashes being created for an externalRefernce which is not as required ([`970d192`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/970d19202d13d4becbbf040b3a9fb115dd7a0795))

## v0.8.0 (2021-10-12)
### Feature
* Add support for `externalReferneces` for `Components` and associated enhancements to parsers to obtain information where possible/known ([`a152852`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a152852b361bbb7a69c9f7ab61ae7ea6dcffd214))

## v0.7.0 (2021-10-11)
### Feature
* Support for pipenv.lock file parsing ([`68a2dff`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/68a2dffc770d40f693b6891a580d1f7d8018f71c))

## v0.6.2 (2021-10-11)
### Fix
* Added ability to add tools in addition to this library when generating CycloneDX + plus fixes relating to multiple BOM instances ([`e03a25c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e03a25c3d2a1a0b711204bb26c7b898eadacdcb0))

## v0.6.1 (2021-10-11)
### Fix
* Better methods for checking if a Component is already represented in the BOM, and the ability to get the existing instance ([`5fee85f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5fee85fc38376478a1a438d228c632a5d14f4740))

## v0.6.0 (2021-10-11)
### Feature
* Helper method for representing a File as a Component taking into account versioning for files as per https://github.com/CycloneDX/cyclonedx.org/issues/34 ([`7e0fb3c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7e0fb3c7e32e08cb8667ad11461c7f8208dfdf7f))
* Support for non-PyPi Components - PackageURL type is now definable when creating a Component ([`fde79e0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fde79e02705bce216e62acd05056b6d2046cde22))

## v0.5.0 (2021-10-11)
### Feature
* Add support for tool(s) that generated the SBOM ([`7d1e6ef`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7d1e6ef04d473407b9b4eefc2ef18e6723838f94))

### Fix
* Bumped a dependency version ([`efc1053`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/efc1053ec9ed3f57711f78f1eca181f7bff0c3bf))

## v0.4.1 (2021-09-27)
### Fix
* Improved handling for `requirements.txt` content without pinned or declared versions ([`7f318cb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7f318cb495ac1754029088cae1ef2574c58da2e5))

## v0.4.0 (2021-09-16)
### Feature
* Support for localising vectors (i.e. stripping out any scheme prefix) ([`b9e9e17`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9e9e17ba1e2c1c9dfe551c61ad5152eebd829ab))
* Helper methods for deriving Severity and SourceType ([`6a86ec2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6a86ec27c13ff5e413c5a5f96d9b7671646f9388))

### Fix
* Removed print call ([`8806553`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/880655304c082a88d94d6d50c64d33ad931cc974))
* Relaxed typing of parameter to be compatible with Python < 3.9 ([`f9c7990`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f9c7990695119969c5055bc92a233030db999b84))
* Removed print call ([`d272d2e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d272d2ea7d3331bde0660bdc87a6ac3331ae0720))
* Remove unused commented out code ([`ba4f285`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba4f285fdbe124c28f7ea60310347cf896540125))

## v0.3.0 (2021-09-15)
### Feature
* Adding support for extension schema that descriptions vulnerability disclosures ([`d496695`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d4966951ab6c0229171cfe97723421bb0302c4fc))

## v0.2.0 (2021-09-14)
### Feature
* Added helper method to return a PackageURL object representing a Component ([`367bef1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/367bef11bb1a7ede3100acae39581e33d20fa7f5))

### Fix
* Whitespace on empty line removed ([`cfc952e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cfc952eb5f3feb97a41b6c895657058429da3430))

## v0.1.0 (2021-09-13)
### Feature
* Add poetry support ([`f3ac42f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f3ac42f298b8d093b0ac368993beba43c58c251a))

## v0.0.11 (2021-09-10)
### Fix
* **test:** Test was not updated for revised author statement ([`d1c9d37`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d1c9d379a1e92ee49aae8d133e2ad3e117054ec9))
* **build:** Test failure and dependency missing ([`9a2cfe9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9a2cfe94386b51acca44ae3bacae319b9b3c8f0d))
* **build:** Removed artefacts associtated with non-poetry build ([`f9119d4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f9119d49e462cf1f7ccca9c50af2936f8962fd6d))

## v0.0.10 (2021-09-08)
### Fix
* Add in pypi badge ([`6098c36`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6098c36715b2459d7b04ced5ba6294437576e481))

## v0.0.9 (2021-09-08)
### Fix
* Additional info to poetry, remove circleci ([`2fcfa5a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2fcfa5ac3a7d9d7f372be6d69e1c616b551877df))

## v0.0.8 (2021-09-08)
### Fix
* Initial release to pypi, tell poetry to include cyclonedx package ([`a030177`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a030177cb1a370713c4438b13b7520ef6afd19f6))

## v0.0.7 (2021-09-08)
### Fix
* Release with full name ([`4c620ed`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4c620ed053aac8c31343b1ca84ca56912b762ab2))

## v0.0.6 (2021-09-08)
### Fix
* Initial release to pypi ([`99687db`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/99687dbec1389bf323bb625bfb707306aa3b8d1a))

## v0.0.5 (2021-09-08)


## v0.0.4 (2021-09-08)


## v0.0.3 (2021-09-08)


## v0.0.2 (2021-09-08)

