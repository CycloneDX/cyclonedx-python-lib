# CHANGELOG



## v8.2.1 (2024-10-24)

### Fix

* fix: encode quotation mark in URL (#724)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a7c7c97`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a7c7c97c37ee1c7988c028aa779f74893f858c7b))


## v8.2.0 (2024-10-22)

### Feature

* feat: Add Python 3.13 support (#718)

Signed-off-by: gruebel &lt;anton.gruebel@gmail.com&gt; ([`d4be3ba`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d4be3ba6b3ccc65553a7dd10ad559c1eddfbb19b))


## v8.1.0 (2024-10-21)

### Documentation

* docs: fix code examples regarding outputting (#709)



Signed-off-by: Hakan Dilek &lt;hakandilek@gmail.com&gt; ([`c72d5f4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c72d5f483d5c1990fe643c4c25e37373d4d3248f))

### Feature

* feat: add support for Lifecycles in BOM metadata (#698)



---------

Signed-off-by: Johannes Feichtner &lt;johannes@web-wack.at&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: Johannes Feichtner &lt;343448+Churro@users.noreply.github.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`6cfeb71`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6cfeb711f11aec8fa4d7be885f6797cc2eaa7e67))


## v8.0.0 (2024-10-14)

### Breaking

* feat!: v8.0.0 (#665)

### BREAKING Changes

* Removed `cyclonedx.mode.ThisTool`, utilize `cyclonedx.builder.this.this_tool()` instead. 
* Moved `cyclonedx.model.Tool` to `cyclonedx.model.tool.Tool`.
* Property `cyclonedx.mode.bom.BomMetaData.tools` is of type `cyclonedx.model.tool.ToolRepository` now, was `SortedSet[cyclonedx.model.Tool]`.  
  The getter will act accordingly; the setter might act in a backwards-compatible way.
* Property `cyclonedx.mode.vulnerability.Vulnerability.tools` is of type `cyclonedx.model.tool.ToolRepository` now, was `SortedSet[cyclonedx.model.Tool]`.  
  The getter will act accordingly; the setter might act in a backwards-compatible way.
* Constructor `cyclonedx.model.license.LicenseExpression()` accepts optional argument `acknowledgement` only as key-word argument, no longer as positional argument.  
  

### Changes

* Constructor of `cyclonedx.model.bom.BomMetaData` also accepts an instance of `cyclonedx.model.tool.ToolRepository` for argument `tools`.
* Constructor of `cyclonedx.model.bom.BomMetaData` no longer adds this very library as a tool.  
  Downstream users SHOULD add it manually, like `my-bom.metadata.tools.components.add(cyclonedx.builder.this.this_component())`. 

### Fixes

* Deserialization of CycloneDX that do not include tools in the metadata are no longer unexpectedly modified/altered.

### Added

Enabled Metadata Tools representation and serialization in accordance with CycloneDX 1.5 

* New class `cyclonedx.model.tool.ToolRepository`.
* New function `cyclonedx.builder.this.this_component()` -- representation of this very python library as a `Component`.
* New function `cyclonedx.builder.this.this_tool()` -- representation of this very python library as a `Tool`.
* New function `cyclonedx.model.tool.Tool.from_component()`.

### Dependencies

* Raised runtime dependency `py-serializable&gt;=1.1.1,&lt;2`, was `&gt;=1.1.0,&lt;2`.

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: Joshua Kugler &lt;tek30584@adobe.com&gt;
Signed-off-by: semantic-release &lt;semantic-release@bot.local&gt;
Co-authored-by: Joshua Kugler &lt;joshua@azariah.com&gt;
Co-authored-by: semantic-release &lt;semantic-release@bot.local&gt; ([`002f966`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/002f96630ce8fc6f1766ee6cc92a16b35a821c69))

### Documentation

* docs(chaneglog): omit chore/ci/refactor/style/test/build (#703)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a210809`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a210809efb34c2dc895fc0c6d96a3412a9097625))


## v7.6.2 (2024-10-07)

### Documentation

* docs: fix some doc strings

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`4fa8fc1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4fa8fc1b6703ecf6788b72f2d53c6a17e2146cf7))

### Fix

* fix: behavior of and typing for crypto setters with optional values (#694)

fixes #690

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`d8b20bd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d8b20bdc5224ea30cf767f6f3f1a6f8ff2754973))


## v7.6.1 (2024-09-18)

### Fix

* fix: file copyright headers (#676)

utilizes flake8 plugin
&lt;https://pypi.org/project/flake8-copyright-validator/&gt; to assert the
correct headers

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`35e00b4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/35e00b4ee5a9306b9e97b011025409bcbfcef309))


## v7.6.0 (2024-08-14)

### Feature

* feat: `HashType.from_composite_str` for Blake2b, SHA3, Blake3 (#663)

The code mistreated hashes for Blake2b and SHA3.
Code for explicitly handling SHA1 &amp; BLAKE3 was added, as those have no
variants defined in the CycloneDX specification.

fixes #652

---------

Signed-off-by: Michael Schlenker &lt;michael.schlenker@contact-software.com&gt;
Co-authored-by: Michael Schlenker &lt;michael.schlenker@contact-software.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c59036e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c59036e06ddc97284f82efbbc168dc2d89d090d1))


## v7.5.1 (2024-07-08)

### Fix

* fix: XML serialize `normalizedString` and `token` properly (#646)

fixes #638

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b40f739`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b40f739206a44f7dbd94042fb5e1a37c047ea024))


## v7.5.0 (2024-07-04)

### Feature

* feat: add workaround property for v1.5 and v1.6 (#642)

Property `workaround` was missing from the vulnerability model. It was
added in spec v1.5 and was marked as TODO before.

This is my first contribution on this project so if I done something
wrong, just say me :smiley:

Signed-off-by: Louis Maillard &lt;louis.maillard@savoirfairelinux.com&gt;
Signed-off-by: Louis Maillard &lt;louis.maillard@protonmail.com&gt;
Co-authored-by: Louis Maillard &lt;louis.maillard@savoirfairelinux.com&gt; ([`b5ebcf8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b5ebcf8104faf57030cbc5d8190c78524ab86431))


## v7.4.1 (2024-06-12)

### Documentation

* docs: exclude dep bumps from changelog (#627)

fixes #616

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`60361f7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/60361f781a1b356f24a553e133e0f58a2ad37a7d))

### Fix

* fix: `cyclonedx.model.Property.value` value is optional (#631)

`cyclonedx.model.Property.value` value is optional, in accordance with
the spec.

fixes #630

---------

Signed-off-by: Michael Schlenker &lt;michael.schlenker@contact-software.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: Michael Schlenker &lt;michael.schlenker@contact-software.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`ad0f98b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ad0f98b433fd85ba14db6b6288f33d98bc79ee51))


## v7.4.0 (2024-05-23)

### Documentation

* docs: OSSP best practice percentage

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`75f58dc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/75f58dcd41c1495737bff69d354beeeff7660c15))

### Feature

* feat:  updated SPDX license list to `v3.24.0` (#622)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3f9770a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3f9770a95fbe48dfc0cb911a6526690017c2fb37))


## v7.3.4 (2024-05-06)

### Fix

* fix: allow suppliers with empty-string names (#611)

fixes #600

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b331aeb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b331aeb4b7261c7b1359c592b2dcda27bd35e369))


## v7.3.3 (2024-05-06)

### Fix

* fix: json validation allow arbitrary `$schema`  value (#613)

fixes https://github.com/CycloneDX/cyclonedx-python-lib/issues/612

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`08b7c60`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/08b7c607360b65215d9d29d42ae86e60c6efe49b))


## v7.3.2 (2024-04-26)

### Fix

* fix: properly sort components based on all properties (#599)

reverts #587 - as this one introduced errors
fixes #598
fixes #586

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;
Co-authored-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`8df488c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8df488cb422a6363421fee39714df4e8e8e7a593))


## v7.3.1 (2024-04-22)

### Fix

* fix: include all fields of `Component` in `__lt__` function for #586 (#587)

Fixes #586.

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`d784685`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d7846850d1ad33184d1d58b59fdf41a778d05900))


## v7.3.0 (2024-04-19)

### Feature

* feat: license factory set `acknowledgement` (#593)

add a parameter to `LicenseFactory.make_*()` methods, to set the `LicenseAcknowledgement`.

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7ca2455`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7ca2455018d0e191afaaa2fd136a7e4d5b325ec6))


## v7.2.0 (2024-04-19)

### Feature

* feat: disjunctive license acknowledgement (#591)


---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`9bf1839`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9bf1839859a244e790e91c3e1edd82d333598d60))

### Unknown

* doc: poor merge resolved

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`a498faa`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a498faaab248d0512bad9e66afbd8fb1d6c42a66))


## v7.1.0 (2024-04-10)

### Documentation

* docs: missing schema support table &amp; update schema support to reflect version 7.0.0 (#584)

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`d230e67`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d230e67188661a5fb94730e52bf59c11c965c8d7))

### Feature

* feat: support `bom.properties` for CycloneDX v1.5+ (#585)

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`1d1c45a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1d1c45ac82c7927acc388489228a9b5990f68aa7))


## v7.0.0 (2024-04-09)

### Breaking

* feat!: Support for CycloneDX v1.6

* added draft v1.6 schemas and boilerplate for v1.6

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* re-generated test snapshots for v1.6

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* note `bom.metadata.manufacture` as deprecated

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* work on `bom.metadata` for v1.6

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* Deprecated `.component.author`. Added `.component.authors` and `.component.manufacturer`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* work to add `.component.omniborid` - but tests deserialisation tests fail due to schema differences (`.component.author` not in 1.6)

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* work to get deserialization tests passing

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* chore(deps): bump `py-serializable` to &gt;=1.0.3 to resolve issues with deserialization to XML

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* imports tidied

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* properly added `.component.swhid`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* add `.component.cryptoProperties` - with test failures for SchemaVersion &lt; 1.6

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* typing and bandit ignores

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* coding standards

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* test filtering

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* coding standards

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* additional tests to increase code coverage

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* corrected CryptoMode enum

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* coding standards

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* Added `address` to `organizationalEntity`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* Added `address` to `organizationalEntity`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* raise `UserWarning` in `.component.version` has length &gt; 1024

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* coding standards and typing

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* add `acknowledgement` to `LicenseExpression` (#582)


Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* more proper way to filter test cases

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* update schema to published versions

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* fetch schema 1.6 JSON

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* fetch test data for CDX 1.6

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* reformat

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* reformat

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* refactor

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* style

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* refactor

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* docs

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

---------

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8bbdf46`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8bbdf461434ab66673a496a8305c2878bf5c88da))


## v6.4.4 (2024-03-18)

### Fix

* fix: wrong extra name for xml validation (#571)



Signed-off-by: Christoph Reiter &lt;reiter.christoph@gmail.com&gt; ([`10e38e2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/10e38e25095de4b2dafbfcd1fd81dce7a9c0f124))


## v6.4.3 (2024-03-04)

### Fix

* fix: serialization of `model.component.Diff` (#557)

Fixes #556 

---------

Signed-off-by: rcross-lc &lt;151086351+rcross-lc@users.noreply.github.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`22fa873`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/22fa8734bf1a3a8789ad7578bfa0c86cf0a49d4a))


## v6.4.2 (2024-03-01)

### Build

* build: use poetry v1.8.1 (#560)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`6f81dfa`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6f81dfaed32b76f251647f6291791e714ab158a3))

### Documentation

* docs: update architecture description and examples (#550)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a19fd28`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a19fd2828355ae031164ef7a0dda2a8ea2365108))

* docs: exclude internal docs from rendering (#545)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7e55dfe`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7e55dfe213cb2a88b3686f9e8bf93cf4642a2ccd))

### Unknown

* docs

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`63cff7e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/63cff7ee697c9d5fb96da3c8c16f7c9bc7b34e58))

* docs (#546)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b0e5b43`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b0e5b43880e17ec6ce23d5d4e1e7a9a2547c1e79))


## v6.4.1 (2024-01-30)

### Documentation

* docs: ship docs with `sdist` build (#544)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`52ef01c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/52ef01c99319d5aed950e7f6ef6fcfe731ac8b2f))

* docs: refactor example

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c1776b7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c1776b718b81cf72ef0c0251504e0d3631e30b17))

### Fix

* fix: `model.BomRef` no longer equal to unset peers (#543)

  fixes [#539](https://github.com/CycloneDX/cyclonedx-python-lib/issues/539) 


---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`1fd7fee`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1fd7fee9dec888c10087921f2e5a7a60062fb419))


## v6.4.0 (2024-01-22)

### Documentation

* docs: add OpenSSF Best Practices shield (#532)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`59c4381`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/59c43814b07db0aa881d87192939eb93e79b0cc2))

### Feature

* feat: support `py-serializable` v1.0 (#531)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`e1e7277`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e1e72777d8a355c6854f4d9eb26c1e2083c806df))


## v6.3.0 (2024-01-06)

### Documentation

* docs: add `Documentation` url to project meta

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`1080b73`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1080b7387a0bbc49a067cd2efefb1545470947e5))

* docs: add `Documentation` url to project meta

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c4288b3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c4288b35e0e1050f0982f7492cfcd3bea34b445c))

### Feature

* feat: enable dependency `py-serializable 0.17` (#529)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`9f24220`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9f24220029cd18cd191f63876899cd86be52dce1))


## v6.2.0 (2023-12-31)

### Build

* build: allow additional major-version RC branch patterns

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`f8af156`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f8af156c9c38f737b7067722d2a96f8a2a4fcb48))

### Documentation

* docs: fix typo

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`2563996`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/25639967c93ad464e486f2fe6a148b3be439f43d))

* docs: update intro and description

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`f0bd05d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f0bd05dc854b5b71421b82cfb527fcb8f41a7c4a))

* docs: buld docs on ubuntu22.04 python311

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b3e9ab7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b3e9ab77696f2ee763f1746f8142bdf471477c39))

### Feature

* feat: allow `lxml` requirement in range of `&gt;=4,&lt;6` (#523)

Updates the requirements on [lxml](https://github.com/lxml/lxml) to permit the latest version.
- [Release notes](https://github.com/lxml/lxml/releases)
- [Changelog](https://github.com/lxml/lxml/blob/master/CHANGES.txt)
- [Commits](https://github.com/lxml/lxml/compare/lxml-4.0.0...lxml-5.0.0)

---
updated-dependencies:
- dependency-name: lxml
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`7d12b9a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7d12b9a9f7a2fdc5e6bb12f891c6f4291e20e65e))

### Unknown

* docs

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7dcd166`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7dcd16621002713dcf1ce8e17bc5762320fae4fa))


## v6.1.0 (2023-12-22)

### Feature

* feat: add function to map python `hashlib` algorithms to CycloneDX (#519)

new API: `model.HashType.from_hashlib_alg()`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`81f8cf5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/81f8cf59b1f40ffbd213789a8b1b621a01e3f631))


## v6.0.0 (2023-12-10)

### Breaking

* feat!: v6.0.0  (#492)

### Breaking Changes

* Removed symbols that were already marked as deprecated (via [#493])
* Removed symbols in `parser.*` ([#489] via [#495])
* Removed `output.LATEST_SUPPORTED_SCHEMA_VERSION` ([#491] via [#494])
* Serialization of unsupported enum values might downgrade/migrate/omit them  ([#490] via [#496])  
  Handling might raise warnings if a data loss occurred due to omitting.  
  The result is a guaranteed valid XML/JSON, since no (enum-)invalid values are rendered.
* Serialization of any `model.component.Component` with unsupported `type` raises `exception.serialization.SerializationOfUnsupportedComponentTypeException` ([#490] via [#496])
* Object `model.bom_ref.BomRef`&#39;s property `value` defaults to `Null`, was arbitrary `UUID` ([#504] via [#505])  
  This change does not affect serialization. All `bom-ref`s are guaranteed to have unique values on rendering.
* Removed helpers from public API ([#503] via [#506])

### Added

* Basic support for CycloneDX 1.5 ([#404] via [#488])
  * No data models were enhanced nor added, yet.  
    Pull requests to add functionality are welcome.
  * Existing enumerable got new cases, to reflect features of CycloneDX 1.5 ([#404] via [#488])
  * Outputters were enabled to render CycloneDX 1.5 ([#404] via [#488])

### Tests

* Created (regression/unit/integration/functional) tests for CycloneDX 1.5 ([#404] via [#488])
* Created (regression/functional) tests for Enums&#39; handling and completeness ([#490] via [#496])

### Misc

* Bumped dependency `py-serializable@^0.16`, was `@^0.15` (via [#496])


----

### API Changes — the details for migration

* Added new sub-package `exception.serialization` (via [#496])
* Removed class `models.ComparableTuple` ([#503] via [#506])
* Enum `model.ExternalReferenceType` got new cases, to reflect features for CycloneDX 1.5 ([#404] via [#488])
* Removed function `models.get_now_utc` ([#503] via [#506])
* Removed function `models.sha1sum` ([#503] via [#506])
* Enum `model.component.ComponentType` got new cases, to reflect features for CycloneDX 1.5 ([#404] via [#488])
* Removed `model.component.Component.__init__()`&#39;s deprecated optional kwarg `namespace` (via [#493])  
  Use kwarg `group` instead.
* Removed `model.component.Component.__init__()`&#39;s deprecated optional kwarg `license_str` (via [#493])  
  Use kwarg `licenses` instead.
* Removed deprecated method `model.component.Component.get_namespace()` (via [#493])
* Removed class `models.dependency.DependencyDependencies` ([#503] via [#506])
* Removed `model.vulnerability.Vulnerability.__init__()`&#39;s deprecated optional kwarg `source_name` (via [#493])  
  Use kwarg `source` instead.
* Removed `model.vulnerability.Vulnerability.__init__()`&#39;s deprecated optional kwarg `source_url` (via [#493])  
  Use kwarg `source` instead.
* Removed `model.vulnerability.Vulnerability.__init__()`&#39;s deprecated optional kwarg `recommendations` (via [#493])  
  Use kwarg `recommendation` instead.
* Removed `model.vulnerability.VulnerabilityRating.__init__()`&#39;s deprecated optional kwarg `score_base` (via [#493])  
  Use kwarg `score` instead.
* Enum `model.vulnerability.VulnerabilityScoreSource` got new cases, to reflect features for CycloneDX 1.5 ([#404] via [#488])
* Removed `output.LATEST_SUPPORTED_SCHEMA_VERSION` ([#491] via [#494])
* Removed deprecated function `output.get_instance()` (via [#493])  
  Use function `output.make_outputter()` instead.
* Added new class `output.json.JsonV1Dot5`, to reflect CycloneDX 1.5 ([#404] via [#488])
* Added new item to dict `output.json.BY_SCHEMA_VERSION`, to reflect CycloneDX 1.5 ([#404] via [#488])
* Added new class `output.xml.XmlV1Dot5`, to reflect CycloneDX 1.5 ([#404] via [#488])
* Added new item to dict `output.xml.BY_SCHEMA_VERSION`, to reflect CycloneDX 1.5 ([#404] via [#488])
* Removed class `parser.ParserWarning` ([#489] via [#495])
* Removed class `parser.BaseParser` ([#489] via [#495])
* Enum `schema.SchemaVersion` got new case `V1_5`, to reflect CycloneDX 1.5 ([#404] via [#488])


[#404]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/404
[#488]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/488
[#489]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/489
[#490]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/490
[#491]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/491
[#493]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/493
[#494]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/494
[#495]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/495
[#496]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/496
[#503]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/503
[#504]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/504
[#505]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/505
[#506]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/506

---------

Signed-off-by: Johannes Feichtner &lt;johannes@web-wack.at&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: semantic-release &lt;semantic-release&gt;
Co-authored-by: Johannes Feichtner &lt;343448+Churro@users.noreply.github.com&gt;
Co-authored-by: semantic-release &lt;semantic-release&gt; ([`74865f8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/74865f8e498c9723c2ce3556ceecb6a3cfc4c490))


## v5.2.0 (2023-12-02)

### Documentation

* docs: keywaords &amp; funding (#486)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3189e59`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3189e59ff8e3d3d10f7b949b5a08397ff3d3642b))

### Feature

* feat: `model.XsUri` migrate control characters according to spec (#498)

fixes https://github.com/CycloneDX/cyclonedx-python-lib/issues/497

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`e490429`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e49042976f8577af4061c34394db270612488cdf))


## v5.1.1 (2023-11-02)

### Fix

* fix: update own `externalReferences` (#480)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`edb3dde`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/edb3dde889c06755dd1963ed21dd803db3ea0dcc))


## v5.1.0 (2023-10-31)

### Documentation

* docs: advance license docs

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`f61a730`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f61a7303de1d5dacf0917a1d66f5ebe0732ccd75))

### Feature

* feat: guarantee unique `BomRef`s in serialization result (#479)

Incorporate `output.BomRefDiscriminator` on serialization

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a648775`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a648775bb5195621e17fdbae92950ab6d56a665a))


## v5.0.1 (2023-10-24)

### Documentation

* docs: revisit project meta (#475)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c3254d0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c3254d055f3cda96d2849222a0bba7be8cf486a3))

* docs: fix RTFD build (#476)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b9fcfb4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9fcfb40af366fdee7258ccb720e0fad27994824))

### Unknown

* &#34;chore(deps): revert bump python-semantic-release/python-semantic-release (#474)&#34;

This reverts commit 9c3ffac34e89610ccc4f9701444127e1e6f5ee07.

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`aae7304`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/aae73048c7aebe5920ec888225bdbde08111601b))


## v5.0.0 (2023-10-24)

### Breaking

* feat!: v5.0.0 (#440)

BREAKING CHANGES
----------------
* Dropped support for python&lt;3.8 ([#436] via [#441]; enable [#433])
* Reworked license related models, collections, and factories ([#365] via [#466])
* Behavior
  * Method `model.bom.Bom.validate()` will throw `exception.LicenseExpressionAlongWithOthersException`, if detecting invalid license constellation ([#453] via [#452])
  * Fixed tuple comparison when unequal lengths (via [#461])
* API
  * Enum `schema.SchemaVersion` is no longer string-like ([#442] via [#447])
  * Enum `schema.OutputVersion` is no longer string-like ([#442] via [#447])
  * Abstract class `output.BaseOutput` requires implementation of new method `output_format` ([#446] via [#447])
  * Abstract method `output.BaseOutput.output_as_string()` got new optional parameter `indent` ([#437] via [#458])
  * Abstract method `output.BaseOutput.output_as_string()` accepts arbitrary kwargs (via [#458], [#462])
  * Removed class `factory.license.LicenseChoiceFactory` (via [#466])  
    The old functionality was integrated into `factory.license.LicenseFactory`.
  * Method `factory.license.LicenseFactory.make_from_string()`&#39;s parameter `name_or_spdx` was renamed to `value` (via [#466])
  * Method `factory.license.LicenseFactory.make_from_string()`&#39;s return value can also be a `LicenseExpression` ([#365] via [#466])  
    The behavior imitates the old `factory.license.LicenseChoiceFactory.make_from_string()`
  * Renamed class `module.License` to `module.license.DisjunctliveLicense` ([#365] via [#466])
  * Removed class `module.LicenseChoice` ([#365] via [#466])  
    Use dedicated classes `module.license.DisjunctliveLicense` and `module.license.LicenseExpression` instead
  * All occurrences of `models.LicenseChoice` were replaced by `models.licenses.License` ([#365] via [#466])
  * All occurrences of `SortedSet[LicenseChoice]` were specialized to `models.license.LicenseRepository` ([#365] via [#466])


Fixed
----------------
* Serialization of multy-licenses ([#365] via [#466])
* Detect unused &#34;dependent&#34; components in `model.bom.validate()` (via [#464])


Changed 
----------------
* Updated latest supported list of supported SPDX license identifiers (via [#433])
* Shipped schema files are moved to a protected space (via [#433])  
  These files were never intended for public use.
* XML output uses a default namespace, which makes results smaller. ([#438] via [#458])


Added
----------------
* Support for Python 3.12 (via [#460])
* JSON- &amp; XML-Validators ([#432], [#446] via [#433], [#448])  
  The functionality might require additional dependencies, that can be installed with the extra &#34;validation&#34;.  
  See the docs in section &#34;Installation&#34; for details.
* JSON &amp; XML can be generated in a more human-friendly form ([#437], [#438] via [#458])
* Type hints, typings &amp; overloads for better integration downstream (via [#463])
* API
  * New function `output.make_outputter()` (via [#469])  
    This replaces the deprecated function `output.get_instance()`.
  * New sub-package `validation` ([#432], [#446] via [#433], [#448], [#469], [#468], [#469])
  * New class `exception.MissingOptionalDependencyException` ([#432] via [#433])
  * New class `exception.LicenseExpressionAlongWithOthersException` ([#453] via [#452])
  * New dictionaries `output.{json,xml}.BY_SCHEMA_VERSION` ([#446] via [#447])
  * Existing implementations of class `output.BaseOutput` now have a new method `output_format` ([#446] via [#447])
  * Existing implementations of method `output.BaseOutput.output_as_string()` got new optional parameter `indent` ([#437] via [#458])
  * Existing implementations of method `output.BaseOutput.output_to_file()` got new optional parameter `indent` ([#437] via [#458])
  * New method `factory.license.LicenseFactory.make_with_expression()` (via [#466])
  * New class `model.license.DisjunctiveLicense` ([#365] via [#466])
  * New class `model.license.LicenseExpression` ([#365] via [#466])
  * New class `model.license.LicenseRepository` ([#365] via [#466])
  * New class `serialization.LicenseRepositoryHelper` ([#365] via [#466])


Deprecated
----------------
* Function `output.get_instance()` might be removed, use `output.make_outputter()` instead (via [#469])


Tests
----------------
* Added validation tests with official CycloneDX schema test data ([#432] via [#433])
* Use proper snapshots, instead of pseudo comparison ([#437] via [#464])
* Added regression test for bug [#365] (via [#466], [#467])


Misc
----------------
* Dependencies: bumped `py-serializable@^0.15.0`, was `@^0.11.1` (via [#458], [#463], [#464], [#466])
* Style: streamlined quotes and strings (via [#472])
* Chore: bumped internal dev- and QA-tools ([#436] via [#441], [#472])
* Chore: added more QA tools to prevent common security issues (via [#473])


[#432]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/432
[#433]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/433
[#436]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/436
[#437]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/437
[#365]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/365
[#438]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/438
[#440]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/440
[#441]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/441
[#442]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/442
[#446]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/446
[#447]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/447
[#448]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/448
[#452]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/452
[#453]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/453
[#458]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/458
[#460]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/460
[#461]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/461
[#462]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/462
[#463]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/463
[#464]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/464
[#466]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/466
[#467]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/467
[#468]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/468
[#469]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/469
[#472]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/472
[#473]: https://github.com/CycloneDX/cyclonedx-python-lib/pull/473

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@owasp.org&gt;
Signed-off-by: semantic-release &lt;semantic-release&gt;
Co-authored-by: semantic-release &lt;semantic-release&gt; ([`26b151c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/26b151cba7d7d484f23ee7888444f09ad6d016b1))


## v4.2.3 (2023-10-16)

### Fix

* fix: SPDX-expression-validation internal crashes are cought and handled (#471)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`5fa66a0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5fa66a043818eb5747dbd630496c6d31f818c0ab))


## v4.2.2 (2023-09-14)

### Documentation

* docs: fix shield in README

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`6a941b1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6a941b1ef5cc0f9e956173cce7e9da57e8c6bf22))

* docs(example): showcase `LicenseChoiceFactory` (#428)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c56ec83`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c56ec8395dd203ac41fa6f4c43970a50c0e80efb))

### Fix

* fix: ship meta files (#434)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3a1a8a5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3a1a8a5c1cbe8d8989b4cb335269a02b5c6d4f38))


## v4.2.1 (2023-09-06)

### Fix

* fix: `LicenseChoiceFactory.make_from_string()` prioritize SPDX id over expression (#427)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`e1bdfdd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e1bdfddcfab97359fbde9f53dc65f56fc8ec4ba9))


## v4.2.0 (2023-09-06)

### Feature

* feat: complete SPDX license expression (#425)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`e06f9fd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e06f9fd2c30e8976766f326ff216103d2560cb9a))


## v4.1.0 (2023-08-27)

### Documentation

* docs(examples): showcase shorthand dependency management (#403)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8b32efb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8b32efb322a3281d58e9f980bb9001b112aa944a))

### Feature

* feat: programmatic access to library&#39;s version (#417)

adds `cyclonedx.__version__`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3585ea9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3585ea9911ae521e86793ef18f5891289fb0b604))


## v4.0.1 (2023-06-28)

### Documentation

* docs(examples): README (#399)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`1d262ba`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1d262ba57eab0d61b947fc293fc59c6234f19647))

* docs: add exaple how to build and serialize (#397)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`65e22bd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/65e22bdc6a1a3fc02a6282146bc8fbc17ddb32fa))

### Fix

* fix: conditional warning if no root dependencies were found (#398)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c8175bb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c8175bb6aebac7f129d42d7a5a0ae928212c20cb))

### Unknown

* 4.0.1

Automatically generated by python-semantic-release ([`4a72f51`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4a72f515ad7b5e46a07f31bea18a94b162e87715))

* Add missing space in warning message. (#364)



Signed-off-by: Michael Schlenker &lt;michael.schlenker@contact-software.com&gt;
Co-authored-by: Michael Schlenker &lt;michael.schlenker@contact-software.com&gt; ([`dad0d28`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/dad0d28ceb7381d1b503e5b29776fc01513f8b04))


## v4.0.0 (2023-03-20)

### Breaking

* feat: Release 4.0.0 #341)

Highlights of this release include:
* Support for De-serialization from JSON and XML to this Pythonic Model
* Deprecation of Python 3.6 support
* Support for Python 3.11
* Support for `BomLink`
* Support VEX without needing `Component` in the same `Bom`
* Support for `services` having `dependencies`

BREAKING CHANGE: Large portions of this library have been re-written for this release and many methods and contracts have changed.

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* feat: support VEX without Components in the same BOM

BREAKING CHANGE: Model classes changed to relocated Vulnerability at Bom, not at Component

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* feat: support VEX without Components in the same BOM

BREAKING CHANGE: Model classes changed to relocated Vulnerability at Bom, not at Component

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

feat: allow `version` of BOM to be defined

feat: allow `serial_number` of BOM to be prescribed

feat: add helper method to get URN for a BOM according to https://www.iana.org/assignments/urn-formal/cdx
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* chore: fix release workflow

* chore: editorconfig

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* feat: support for deserialization from JSON and XML (#290)

BREAKING CHANGE:

* feat: drop Python 3.6 support

Signed-off-by: Hakan Dilek &lt;hakandilek@gmail.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;
Co-authored-by: Hakan Dilek &lt;hakandilek@gmail.com&gt;
Co-authored-by: Hakan Dilek &lt;hakandilek@users.noreply.github.com&gt;

* fix: update `serializable` to include XML safety changes

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* feat: Support for Python 3.11 (#349)

* feat: officially test and support Python 3.11

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* removed unused imports

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* bump `poetry` to `1.1.12` in CI

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* fix: remove `toml` as dependency as not used and seems to be breaking Python 3.11 CI

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* fix: removed `types-toml` from dependencies - not used

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

---------

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* fix: removed `autopep8` in favour of `flake8` as both have conflicting dependencies now

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* chore: bump dev dependencies

fix: removed `setuptools` as dependency
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* tests: compoennt versions optional (#350)

* chore: exclude `venv*` from QA; add typing to QA

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* tests: component versions are optional

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* doc: doc updates for new deserialization feature

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* doc: doc updates for contribution

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

---------

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: Hakan Dilek &lt;hakandilek@gmail.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: Hakan Dilek &lt;hakandilek@gmail.com&gt;
Co-authored-by: Hakan Dilek &lt;hakandilek@users.noreply.github.com&gt; ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

### Unknown

* 4.0.0

Automatically generated by python-semantic-release ([`40fbfda`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/40fbfda428cfa71b16fd6e5e8d5f49cea4b5438b))


## v3.1.5 (2023-01-12)

### Fix

* fix: mak test&#39;s schema paths relative to `cyclonedx` package (#338)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`1f0c05f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1f0c05fe2b2a22bc84a1a437dd59390f2ceaf986))

### Unknown

* 3.1.5

Automatically generated by python-semantic-release ([`ba603cf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba603cf96fad51a85d5159e83c402d613fefbb7c))


## v3.1.4 (2023-01-11)

### Fix

* fix(tests): include tests in `sdist` builds (#337)

* feat: include `tests` in `sdist` builds for #336 
* delete unexpected `DS_Store` file

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`936ad7d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/936ad7d0c26d8f98040203d3234ca8f1afbd73ab))

### Unknown

* 3.1.4

Automatically generated by python-semantic-release ([`0b19294`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0b19294e4820f0da5e81decd4d902ef7789ecb61))


## v3.1.3 (2023-01-07)

### Fix

* fix: serialize dependency graph for nested components (#329)

* tests: regression tests for issue #328
* fix: for issue #328

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`fb3f835`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fb3f8351881783281f8b7e796098a4c145b35927))

### Unknown

* 3.1.3

Automatically generated by python-semantic-release ([`11a420c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/11a420c5fc38bb48d2a91713cc74574acb131184))


## v3.1.2 (2023-01-06)

### Documentation

* docs: typo

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`539b57a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/539b57a00e4e60e239bb26141f219366121e7bc2))

* docs: fix shields (#324)

caused by https://github.com/badges/shields/issues/8671

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`555dad4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/555dad4bc255066036ecca028192eb83df8ba5a0))

* docs: fix typo (#318)


Signed-off-by: Roland Weber &lt;rolweber@de.ibm.com&gt; ([`63bfb87`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/63bfb8772fe78e9842675d17862c456150dbbc15))

### Fix

* fix: prevent errors on metadata handling for some specification versions (#330)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`f08a656`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f08a65649aee750397edc061eb3b8325a69bb4b4))

### Unknown

* 3.1.2

Automatically generated by python-semantic-release ([`0853d14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0853d14780b8e44e9b285bee2ac6b81551640c5f))

* clarify sign-off step (#319)


Signed-off-by: Roland Weber &lt;rolweber@de.ibm.com&gt; ([`007fb96`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/007fb96a1ec23b9516bc383afa85b3efc2707aa8))


## v3.1.1 (2022-11-28)

### Fix

* fix: type hint for `get_component_by_purl` is incorrect

chore: force automated release
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`3f20bf0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3f20bf04a65d5c539230281437255b5f48e17621))

### Unknown

* 3.1.1

Automatically generated by python-semantic-release ([`503955e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/503955ea9e19e1d3ca611df36508dcf1aa93905c))

* Merge pull request #310 from gruebel/fix-method-type-hint

fix: type hint for `get_component_by_purl` is incorrect ([`06037b9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/06037b99e0d6ebc5388d3c5e0799a68233ed92e8))

* move tests to model bom file

Signed-off-by: gruebel &lt;anton.gruebel@gmail.com&gt; ([`4c8a3ab`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4c8a3ab0eef349c007285ff9dfed0c00c6732a96))

* fix type hint for get_component_by_purl

Signed-off-by: gruebel &lt;anton.gruebel@gmail.com&gt; ([`735c05e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/735c05eebb792eed55aeb4d5a7be8043ee1cd9ae))


## v3.1.0 (2022-09-15)

### Feature

* feat: out-factor SPDX compund detection

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`fd4d537`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fd4d537c9dced0e38f14d99dee174cc5bb0bd465))

* feat: out-factor SPDX compund detection

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`2b69925`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2b699252f8857d97231a689ea9cbfcdff9459626))

* feat: license factories

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`033bad2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/033bad2a50fd2236c712d4621caa57b04fcc2043))

### Unknown

* 3.1.0

Automatically generated by python-semantic-release ([`e52c174`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e52c17447b1520103ccb24192ab92560429df595))

* Merge pull request #305 from CycloneDX/license-factories

feat: add license factories to more easily support creation of `License` or `LicenseChoice` from SPDX license strings #304 ([`5ff4494`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5ff4494b0e0d76d04cf8a4245ce0426f0abbd8f9))

* Merge pull request #301 from CycloneDX/fix-poetry-in-tox

chore: fix poetry in tox ([`92aea8d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/92aea8d3413cd2af820cc8160ef48a737951b0ea))

* remove v3 from CHANGELOG #286 (#287)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7029721`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/702972105364a3ab225ea5a586c48cec664601ca))

* 3.0.0

Automatically generated by python-semantic-release ([`69582ff`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/69582ff7a9e3a1cfb2c7193c3d194d69e35899c1))


## v2.7.1 (2022-08-01)

### Fix

* fix: pinned `mypy &lt;= 0.961` due to #278

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`d6955cb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d6955cb86d8da7a72d0146d0dbeb7c34a794a954))

* fix: properly support nested `components` and `services` #275

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`6597db7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6597db740f222c68ad90f74fb8fdb58b72642adb))

### Unknown

* Merge pull request #276 from CycloneDX/fix/bom-validation-nested-components-isue-275

fix: BOM validation fails when Components or Services are nested #275 

fix: updated dependencies #271, #270, #269 and #256 ([`68a0cdd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/68a0cddc0a226947d76b6a275cfceba383797d3b))

* Merge branch &#39;main&#39; into fix/bom-validation-nested-components-isue-275 ([`6caee65`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6caee657260e46f18cade24a73b4f17bc5ad6dd8))

* added tests to cover new `Component.get_all_nested_components()` method

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`75a77ed`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/75a77ed6576f362435d1a3e6e59cbc5d871b9971))

* Revert &#34;chore: re-added `isort` to pre-commit hooks&#34;

This reverts commit f50ee1eb79f3f4e5b9d21824e64192d0af43d3f0.

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`5f7f30e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5f7f30e6a79f7cef6fff296ae0d7e5381f9b5cda))

* removed tests where services are part of dependency tree - see #277

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`f26862b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f26862b0b7f85e3610efbdf17cf304ddc71e5366))

* aded XML output tests for Issue #275

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`ebef5f2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ebef5f212fec13fc8c9bf00553f9bf3f77a0d3f6))

* updated XML output tests

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`356c37e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/356c37ebea85eb10e2505f2b16264d95f292bd55))

* addressed JSON output for #275 including test addiitions

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`692c005`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/692c005c686157134a79e3ffc8ab1e7ce8942de9))


## v2.7.0 (2022-07-21)

### Feature

* feat: support for CycloneDX schema `1.4.2` - adds `vulnerability.properties` to the schema ([`32e7929`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/32e792928bdf37133e966ef72ec01b0bc698482d))

* feat: support for CycloneDX schema version `1.4.2`
- Provides support for `vulnerability.properties`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`db7445c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/db7445cd343fc35c6d6fc9f5af3e28cf97a19732))

* feat: added updated CycloneDX 1.4.2 schemas

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`7fb27ae`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7fb27aed58f7de10f8c6b703699bba315af353e7))

### Unknown

* 2.7.0

Automatically generated by python-semantic-release ([`96d155e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/96d155e864d83482242c22f69af8e7c618d05a1b))


## v2.6.0 (2022-06-20)

### Feature

* feat: reduce unnessessarry type casting of `set`/`SortedSet` (#203)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`089d971`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/089d9714f8f9f8c70076e48baa18340899cc29fa))

### Unknown

* 2.6.0

Automatically generated by python-semantic-release ([`8481e9b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8481e9bd8dc5196c2e703e5cd19974bb22bc270e))


## v2.5.2 (2022-06-15)

### Fix

* fix: add expected lower-than comparators for `OrganizationalEntity` and `VulnerabilityCredits` (#248)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`0046ee1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0046ee19547be8dafe5d73bad886b9c5f725f26e))

### Unknown

* 2.5.2

Automatically generated by python-semantic-release ([`fb9a796`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fb9a796d0b34c2d930503790c74d6d7ed5e3c3d6))


## v2.5.1 (2022-06-10)

### Fix

* fix: add missing `Vulnerability` comparator for sorting (#246)

Partial fix for #245.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`c3f3d0d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c3f3d0d105f0dcf991175040b6d6c2b6e7e25d8f))

### Unknown

* 2.5.1

Automatically generated by python-semantic-release ([`1ea5b20`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1ea5b20f1c93e6e6b3799444c7ea6fd65a2e068c))


## v2.5.0 (2022-06-10)

### Build

* build: move typing to dev-dependencies

Move `types-setuptools` and `types-toml` to dev-dependencies (#226)

Signed-off-by: Adam Johnson &lt;me@adamj.eu&gt; ([`0e2376b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0e2376baade068ae0490b05550837d104e9abfa4))

### Documentation

* docs: fix typo  &#34;This is out&#34; -&gt; &#34;This is our&#34;

Fix typo in comments: &#34;This is out&#34; -&gt; &#34;This is our&#34; (#233)

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`ef0278a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ef0278a2044147e73a281c5a59f95049d4af7641))

### Feature

* feat: use `SortedSet` in model to improve reproducibility - this will provide predictable ordering of various items in generated CycloneDX documents - thanks to @RodneyRichardson

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`8a1c404`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8a1c4043f502292b32c4ab36a8618cf3f67ac8df))

### Unknown

* 2.5.0

Automatically generated by python-semantic-release ([`c820423`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c820423ffffb90ec7a42d8873d99428277f9ae28))

* Merge pull request #235 from RodneyRichardson/use-sorted-set

feat: use `SortedSet` in model to improve reproducibility - this will provide predictable ordering of various items in generated CycloneDX documents - thanks to @RodneyRichardson ([`c43f6d8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c43f6d8ce41a9de91a84cea7a40045cab8121792))

* Merge branch &#39;CycloneDX:main&#39; into use-sorted-set ([`1b8ac25`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1b8ac252a28af1b938d6cad4182e6f2d586b26c0))

* Fix SortedSet type hints for python &lt; 3.8

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`71eeb4a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/71eeb4aeeb9e911df2422c097ebfb671c648242d))

* Fix line length warning.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`e9ee712`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e9ee71291da882a924a9edec7d1f5d6be62797e6))

* Fix more type hints for python &lt; 3.8

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`f042bce`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f042bcef1829a852dd787e226d883f5bbd5c39c3))

* Fix SortedSet type hints for python &lt; 3.8

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`2e283ab`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2e283abed0b67e9e70c825e0d7c6ad7e6691c678))

* Fix type hint on ComparableTuple

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`43ef908`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/43ef908d61fd03e5a4c2ecfabdf22764c8613429))

* Sort usings.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`8f86c12`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8f86c1292d5d0c550a4ec6018b81400255567f93))

* Fix sonatype-lift warnings

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`f1e92e3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f1e92e3cfbe9df2b07b745582608f9f72531684c))

* Fix warnings.

Change tuple -&gt; Tuple
Fix Diff initialization
Add sorting to AttachedText

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`2b47ff6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2b47ff612335b538ceab5e77b60dbe058f739e2e))

* Reduce sortedcontainers.pyi to only the functions used.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`ef0fbe2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ef0fbe2130f763888cb34e8e71a6520d282a0cda))

* Remove flake8 warnings

Remove unused imports and trailing whitespace.
Sort usings in pyi file.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`41d1bee`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/41d1bee824381c25a8c6870abeb1f484c33c78ba))

* Add type hints for SortedSet

Fix use of set/Set.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`df0f554`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/df0f554bff311886705327fd863d573e82123f9e))

* Replace object type hint in __lt__ with Any

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`ec22f68`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ec22f683e1b12843421a23cff15f91628a7dfffe))

* Make reorder() return type explicit List (as flagged by sonatype-lift bot)

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`695ee86`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/695ee862ce9043807a9d825324970cd1b770a46c))

* Use SortedSet in model to improve reproducibility

Added `__lt__()` to all model classes used in SortedSet, with tests
Explicitly declared Enums as (str, Enum) to allow sorting
Added dependency to sortedcollections package

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`368f522`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/368f5221e54a635cd03255efd56d4da2a8d7f56b))


## v2.4.0 (2022-05-17)

### Feature

* feat(deps): remove unused `typing-extensions` constraints

PullRequest and details via #224

Signed-off-by: gruebel &lt;anton.gruebel@gmail.com&gt; ([`2ce358a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2ce358a37e6ce5f06aa9297aed17f8f5bea38e93))

### Unknown

* 2.4.0

Automatically generated by python-semantic-release ([`4874354`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/48743542fd2f3219a4f2295f363ae6e5bcf2a738))

* revert `types-toml` on lowest setup ([`32ece98`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/32ece98b24fd6966722b8cdf698f01b8fb1b8821))


## v2.3.0 (2022-04-20)

### Feature

* feat: add support for Dependency Graph in Model and output serialisation

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`ea34513`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ea34513f8229a909007793288ace2f6f51684333))

### Unknown

* 2.3.0

Automatically generated by python-semantic-release ([`5c1047a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5c1047afc75726cca4130b90b8459418ec6342e8))

* Merge pull request #210 from CycloneDX/feat/support-bom-dependencies

feat: add support for Dependency Graph in Model and output serialisation (JSON and XML) ([`938169c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/938169c05b458967cd1dabc338981d296f5b2842))

* Merge pull request #214 from CycloneDX/feat/support-bom-dependencies-no-cast

no cast ([`2551545`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/25515456f2707964032c1f9642bae3d79ba2b994))

* no cast

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`dec3b70`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/dec3b703f7e69cd2b3fdff34583ee052b1cbb1d2))

* update to use `Set` operators (more Pythonic)

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`f01665e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f01665e96c87b9dd1fdb37d907a8339ba819e2cc))

* missing closing `&gt;` in `BomRef.__repr__`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`2c7c4be`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2c7c4be8210231dcfaf9e8937bd943f3ea6683c3))

* removed unnecessary condition - `self.get_bom().components` is always a `Set`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`5eb5669`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5eb5669bdeb982c9f0b4a72f2264a8559e9a3bc3))

* added additional tests to validate Component in Metadata is properly represented in Dependency Graph

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`b8d526e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b8d526ee52b3923c7755a897e0c042c159fb8d99))

* adjusted unit tests to account for inclusion of Component in Bom Metadata in Dependency Graphy

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`c605f2b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c605f2be90092f09bb0eb89dccb27767d78dcfac))

* updates based on feedback from @jkowalleck

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`04511f3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/04511f3c523bc26b0b434d8334d37eccaaaf1ea4))

* Merge branch &#39;feat/support-bom-dependencies&#39; of github.com:CycloneDX/cyclonedx-python-lib into feat/support-bom-dependencies ([`8fb408c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb408cfe7941efca424777a94084755ee8a50e4))

* doc: updated docs to reflect support for Dependency Graph

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`a680544`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a68054491529631c792e51c764bbf64a5e9b4834))

* updated file hash in test

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`56f3d5d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/56f3d5d432b6c50679cfd733cf2b0ed2ea55400e))

* removed unused import

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`61c3338`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/61c3338e139a8e1a72a659080f2043b352007561))

* doc: updated docs to reflect support for Dependency Graph

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`3df017f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3df017feaaa461bcfa7082f58a5824aa92493b59))

* updated file hash in test

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`449cb1e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/449cb1e56e64e6c144c0d2b6b69649df2d6e5320))

* removed unused import

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`f487c4a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f487c4a44f5604fa3d1da2c0bc57d09e22057973))


## v2.2.0 (2022-04-12)

### Feature

* feat: Bump XML schemas to latest fix version for 1.2-1.4 - see:
https://github.com/CycloneDX/specification/issues/122

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`bd2e756`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd2e756de15c37b34d2866e8de521556420bd5d3))

* feat: bump JSON schemas to latest fix verison for 1.2 and 1.3 - see:
- https://github.com/CycloneDX/specification/issues/123
- https://github.com/CycloneDX/specification/issues/84
- https://github.com/CycloneDX/specification/issues/125

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`bd6a088`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd6a088d51c995c0f08271f56aedb456c60c1a2e))

### Unknown

* 2.2.0

Automatically generated by python-semantic-release ([`67ecfac`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/67ecfacc38817398319ac5d627f2b3a17fb45b3f))

* Merge pull request #207 from CycloneDX/feat/update-schemas

feat: Update CycloneDX Schemas to latest patch versions ([`2c55cb5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2c55cb51042694d48a2eccd8e505833196effb59))

* mark schema files as vendored

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a9c3e77`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a9c3e77998e7c05af5ba097891cd05a8cdb89232))

* Merge pull request #191 from CycloneDX/feat/pre-commit-hooks

[DEV] Add pre-commit hooks ([`91ceeb1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/91ceeb1fdafddf20af546d383a2fb16393977ef5))


## v2.1.1 (2022-04-05)

### Fix

* fix: prevent error if `version` not set

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`b9a84b5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9a84b5b39fe6cb1560764e86f8bd144f2a901e3))

### Unknown

* 2.1.1

Automatically generated by python-semantic-release ([`f78d608`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f78d6081abc1a8adb80ef0c79a07c624ad9e3a5c))

* Merge pull request #194 from CycloneDX/fix/json-output-version-optional-bug-193

fix: `version` being optional in JSON output can raise error ([`6f7e09a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6f7e09aa4d05a4a2dc60569732f6b2ae5582a154))


## v2.1.0 (2022-03-28)

### Feature

* feat: output errors are verbose

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`bfe8fb1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bfe8fb18825251fd9f146458122aa06137ec27c0))

### Fix

* fix: `version` being optional in JSON output can raise error

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`ba0c82f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba0c82fbde7ba47502c45caf4fa89e9e4381f482))

### Unknown

* 2.1.0

Automatically generated by python-semantic-release ([`c58f8f8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c58f8f8456211fbeac79340b480063791c05f404))

* Merge pull request #198 from CycloneDX/verbose_outout_errors

fix: improved output errors - file/directory is now included ([`4618c62`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4618c62da54f90a67d89583d5339ef0532b7813a))

* updated to be more pythonic

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`a1bbf00`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a1bbf001ba9546c998062a0201d4e2562607749e))

* doc: added CONTRIBUTING to public docs
doc: included pre-commit hooks in CONTRIBUTING

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`f38215f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f38215f2b370e14f5629edff1ade97734b3a79cd))

* Merge pull request #182 from CycloneDX/sort-imports

style: sort imports ([`aa37e56`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/aa37e56964b35642e2bf92f336a767fba1914e2b))


## v2.0.0 (2022-02-21)

### Breaking

* feat: bump dependencies

BREAKING CHANGE: Adopt PEP-3102

BREAKING CHANGE: Optional Lists are now non-optional Sets

BREAKING CHANGE: Remove concept of DEFAULT schema version - replaced with LATEST schema version

BREAKING CHANGE: Added `BomRef` data type

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`da3f0ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/da3f0ca3e8b90b37301c03f889eb089bca649b09))

### Feature

* feat: completed work on #155 (#172)

fix: resolved #169 (part of #155)
feat: as part of solving #155, #147 has been implemented

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`a926b34`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a926b34c7facb8b3709936fe00b62a0b80338f31))

* feat: support complete model for `bom.metadata` (#162)

* feat: support complete model for `bom.metadata`
fix: JSON comparison in unit tests was broken
chore: corrected some source license headers

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`2938a6c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2938a6c001a5b0b25477241d4ad6601030c55165))

* feat: support for `bom.externalReferences` in JSON and XML #124

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`1b733d7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1b733d75a78e3757010a8049cab5c7d4656dc2a5))

* feat: Complete support for `bom.components` (#155)

* fix: implemented correct `__hash__` methods in models (#153)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`32c0139`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/32c01396251834c69a5b23c82a5554faf8447f61))

* feat: support services in XML BOMs
feat: support nested services in JSON and XML BOMs

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`9edf6c9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9edf6c940d20a44f5b99c557392a9fa4532b332e))

### Fix

* fix: `license_url` not serialised in XML output #179 (#180)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`f014d7c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f014d7c4411de9ed5e9cb877878ae416d85b2d92))

* fix: `Component.bom_ref` is not Optional in our model implementation (in the schema it is) - we generate a UUID if `bom_ref` is not supplied explicitly

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`5c954d1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5c954d1e39ce8509ab36e6de7d521927ad3c997c))

* fix: temporary fix for `__hash__` of Component with `properties` #153

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`a51766d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a51766d202c3774003dd7cd8c115b2d9b3da1f50))

* fix: further fix for #150

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`1f55f3e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1f55f3edfeacfc515ef0b5e493c27dd6e14861d6))

* fix: regression introduced by first fix for #150

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`c09e396`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c09e396b98c484d1d3d509a5c41746133fe41276))

* fix: Components with no version (optional since 1.4) produce invalid BOM output in XML #150

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`70d25c8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/70d25c8c162e05a5992761ccddbad617558346d1))

* fix: `expression` not supported in Component Licsnes for version 1.0

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`15b081b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/15b081bd1891566dbe00e18a8b21d3be87154f72))

### Unknown

* 2.0.0

Automatically generated by python-semantic-release ([`a4af3dc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a4af3dccbddf4ea91b277746d2305fadf6078ed8))

* Merge pull request #148 from CycloneDX/feat/add-bom-services ([`631e400`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/631e4009340f4466fb45f25bbf3ce7ffa4d8adca))

* Merge branch &#39;main&#39; into feat/add-bom-services ([`9a32351`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9a3235155bd04450c6e520ee6de04b2d6f2c5d0a))

* doc: added RTD badge to README

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`b20d9d1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b20d9d1aceebfa8bae21250e6ae39234caffbb0e))

* implemented `__str__` for `BomRef`

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`670bde4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/670bde47a8a60db764aa706797f1d8ed7cf2c227))

* Continuation of #170 - missed updating Vulnerability to use `BomRef` (#175)

* BREAKING CHANGE: added new model `BomRef` unlocking logic later to ensure uniquness and dependency references

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* updated Vulnerability to also use new `BomRef` model

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`0d82c01`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0d82c019afce3e4aefe56bff9607cfd60186c6b0))

* BREAKING CHANGE: added new model `BomRef` unlocking logic later to ensure uniquness and dependency references (#174)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`d189f2c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d189f2c16870deb683e62cd06a6072b008eab05d))

* BREAKING CHANGE: replaced concept of default schema version with latest supported #171 (#173)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`020fcf0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/020fcf03ef3985dac82a38b8810d6d6cd301809c))

* BREAKING CHANGE: Updated default schema version to 1.4 from 1.3 (#164)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`9b6ce4b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9b6ce4bd7b5a2a332e9f01f93db57b78f65af048))

* BREAKING CHANGE: update models to use `Set` rather than `List` (#160)

* BREAKING CHANGE: update models to use `Set` and `Iterable` rather than `List[..]`
BREAKING CHANGE: update final models to use `@property`
wip

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`142b8bf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/142b8bf4dbb2e61d131b7ca2ec332aac472ef3cd))

* removed unnecessary calls to `hash()` in `__hash__()` methods as pointed out by @jkowalleck

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`0f1fd6d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0f1fd6dfdd41073cbdbb456cf019c7f2ed9e2175))

* BREAKING CHANGE: adopted PEP-3102 for model classes (#158)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`b3c8d9a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b3c8d9a676190f20dfc4ab1b915c1e53c4ac5a82))

* doc: added page to docs to call out which parts of the specification this library supports

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`41a4be0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/41a4be0cedcd26b6645b6e3606cce8e3708c569f))

* attempt to resolve Lift finding

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`2090c08`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2090c0868ca82c4b53c6ffc6f439c0d675147601))

* removed unused imports

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`a35d540`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a35d540c97b898eb152f453003f46ce0e18b7ea6))

* WIP on `bom.services`

* WIP but a lil hand up for @madpah

Signed-off-by: Jeffry Hesse &lt;5544326+DarthHater@users.noreply.github.com&gt;

* chore: added missing license header

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* No default values for required fields

* Add Services to BOM

* Typo fix

* aligned classes with standards, commented out Signature work for now, added first tests for Services

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* addressed standards

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* 1.2.0

Automatically generated by python-semantic-release

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* feat: `bom-ref` for Component and Vulnerability default to a UUID (#142)

* feat: `bom-ref` for Component and Vulnerability default to a UUID if not supplied ensuring they have a unique value #141

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* doc: updated documentation to reflect change

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* patched other tests to support UUID for bom-ref

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* better syntax

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* 1.3.0

Automatically generated by python-semantic-release

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* WIP but a lil hand up for @madpah

Signed-off-by: Jeffry Hesse &lt;5544326+DarthHater@users.noreply.github.com&gt;
Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* chore: added missing license header

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* aligned classes with standards, commented out Signature work for now, added first tests for Services

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* removed signature from this branch

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* Add Services to BOM

* Typo fix

* addressed standards

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* resolved typing issues from merge

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* added a bunch more tests for JSON output

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

Co-authored-by: Paul Horton &lt;phorton@sonatype.com&gt;
Co-authored-by: github-actions &lt;action@github.com&gt; ([`b45ff18`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b45ff187056893c5fb294cbf9de854fd130bb7be))


## v1.3.0 (2022-01-24)

### Feature

* feat: `bom-ref` for Component and Vulnerability default to a UUID (#142)

* feat: `bom-ref` for Component and Vulnerability default to a UUID if not supplied ensuring they have a unique value #141

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* doc: updated documentation to reflect change

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* patched other tests to support UUID for bom-ref

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* better syntax

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`3953bb6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3953bb676f423c325ca4d80f3fcee33ad042ad93))

### Unknown

* 1.3.0

Automatically generated by python-semantic-release ([`4178181`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/41781819e2de8f650271e7de11d395fa43939f22))


## v1.2.0 (2022-01-24)

### Feature

* feat: add CPE to component (#138)

* Added CPE to component

Setting CPE was missing for component, now it is possible to set CPE and output CPE for a component.

Signed-off-by: Jens Lucius &lt;jens.lucius@de.bosch.com&gt;

* Fixing problems with CPE addition

- Fixed styling errors
- Added reference to CPE Spec
- Adding CPE parameter as last parameter to not break arguments

Signed-off-by: Jens Lucius &lt;jens.lucius@de.bosch.com&gt;

* Again fixes for Style and CPE reference

Missing in the last commit

Signed-off-by: Jens Lucius &lt;jens.lucius@de.bosch.com&gt;

* Added CPE as argument before deprecated arguments

Signed-off-by: Jens Lucius &lt;jens.lucius@de.bosch.com&gt;

* Added testing for CPE addition and error fixing

- Added output tests for CPE in XML and JSON
- Fixes style error in components
- Fixes order for CPE output in XML (CPE has to come before PURL)

Signed-off-by: Jens Lucius &lt;jens.lucius@de.bosch.com&gt;

* Fixed output tests

CPE was still in the wrong position in one of the tests - fixed

Signed-off-by: Jens Lucius &lt;jens.lucius@de.bosch.com&gt;

* Fixed minor test fixtures issues

- cpe was still in wrong position in 1.2 JSON
- Indentation fixed in 1.4 JSON

Signed-off-by: Jens Lucius &lt;jens.lucius@de.bosch.com&gt;

* Fixed missing comma in JSON 1.2 test file

Signed-off-by: Jens Lucius &lt;jens.lucius@de.bosch.com&gt; ([`269ee15`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/269ee155f203d5771c56edb92f7279466bf2012f))

### Unknown

* 1.2.0

Automatically generated by python-semantic-release ([`97c215c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/97c215cf0c4e8c315ed84cbcb92b22c6b7bcd8c2))


## v1.1.1 (2022-01-19)

### Fix

* fix: bump dependencies (#136)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`18ec498`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/18ec4987f6aa4a259d30000a19aa6ee1d49681d1))

### Unknown

* 1.1.1

Automatically generated by python-semantic-release ([`dec63de`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/dec63de950e0ad81cbb51373b0e647bce551297e))


## v1.1.0 (2022-01-13)

### Feature

* feat: add support for `bom.metadata.component` (#118)

* Add support for metadata component

Part of #6

Signed-off-by: Artem Smotrakov &lt;asmotrakov@riotgames.com&gt;

* Better docs and simpler ifs

Signed-off-by: Artem Smotrakov &lt;asmotrakov@riotgames.com&gt; ([`1ac31f4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1ac31f4cb14b6c466e092ff38ee2aa472c883c5d))

### Unknown

* 1.1.0

Automatically generated by python-semantic-release ([`d4007bd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d4007bd5986173eb2645eebcdd2c6405150f1456))


## v1.0.0 (2022-01-13)

### Unknown

* Manually generated release ([`3509fb6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3509fb643af12cc4393309a006c6bbe63b1bd674))

* Support for CycloneDX schema version 1.4 (#108)

BREAKING CHANGE: Support for CycloneDX 1.4. This includes:
- Support for `tools` having `externalReferences`
- Allowing `version` for a `Component` to be optional in 1.4
- Support for `releaseNotes` per `Component`
- Support for the core schema implementation of Vulnerabilities (VEX)

Other changes included in this PR:
- Unit tests now include schema validation (we&#39;ve left schema validation out of the core library due to dependency bloat)
- Fixes to ensure schema is adhered to in 1.0
- URI&#39;s are now used throughout the library through a new `XsUri` class to provide URI validation
- Documentation is now hosted on readthedocs.org (https://cyclonedx-python-library.readthedocs.io/)
- `$schema` is now included in JSON BOMs
- Concrete Parsers how now been moved into downstream projects to keep this libraries focus on modelling and outputting CycloneDX - see https://github.com/CycloneDX/cyclonedx-python
- Added reference to release of this library on Anaconda

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Co-authored-by: Paul Horton &lt;phorton@sonatype.com&gt;

Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7fb6da9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7fb6da9166050333ae5db7e35ab792b9bdee48d4))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib ([`d26970b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d26970bcc52568645c303f060d71cbc25edbfe78))

* Update CONTRIBUTING.md ([`4448d9b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4448d9b4846a7dfb9eeee355d41fbb100a48d388))


## v0.12.3 (2021-12-15)

### Fix

* fix: removed requirements-parser as dependency (temp) as not available for Python 3 as Wheel (#98)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`3677d9f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3677d9fd584b7c0eb715954bb7b8adc59c0bc9b1))

### Unknown

* 0.12.3

Automatically generated by python-semantic-release ([`cfc9d38`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cfc9d382aea3f69f79d50a4fbb8607346f86ce03))


## v0.12.2 (2021-12-09)

### Fix

* fix: tightened dependency `packageurl-python` (#95)

fixes #94

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`eb4ae5c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/eb4ae5ca8842877b780a755b6611feef847bdb8c))

### Unknown

* 0.12.2

Automatically generated by python-semantic-release ([`54b9f74`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/54b9f744be28b53795bd03e78576eed15b70c10a))


## v0.12.1 (2021-12-09)

### Fix

* fix: further loosened dependency definitions

see #44

updated some locked dependencies to latest versions

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8bef6ec`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8bef6ecad36f51a003b266d776c9520d33e06034))

### Unknown

* 0.12.1

Automatically generated by python-semantic-release ([`43fc36e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/43fc36ebc966ac511e5b7dbff9b0bef6f88d5d2c))


## v0.12.0 (2021-12-09)

### Feature

* feat: loosed dependency versions to make this library more consumable

* feat: lowering minimum dependency versions

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* feat: lowering minimum dependency versions

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* feat: lowering minimum dependency versions - importlib-metadata raising minimum to ensure we get a typed library

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* feat: lowering minimum dependency versions - importlib-metadata raising minimum to ensure we get a typed library

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* feat: lowering minimum version for importlib-metadata to 3.4.0 with modified import statement

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`55f10fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/55f10fb5524dafa68112c0836806c27bdd74fcbe))

### Unknown

* 0.12.0

Automatically generated by python-semantic-release ([`1a907ea`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1a907eae0a3436844ffc2782b990c4b502f409e6))

* Merge pull request #88 from CycloneDX/contributing-file

initial CONTRIBUTING file ([`20035bb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/20035bb5dde8dd3b619b200aec7037c338b18c74))

* initial CONTRIBUTING file

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`6ffe14d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6ffe14d4d51d246cda66ce99ee20893ede8d017f))

* CHORE: poetry(deps): bump filelock from 3.3.2 to 3.4.0

poetry(deps): bump filelock from 3.3.2 to 3.4.0 ([`e144aa2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e144aa29a0fd61483f4940da08ff542c9c3c3332))

* CHORE: poetry(deps): bump types-setuptools from 57.4.2 to 57.4.4

poetry(deps): bump types-setuptools from 57.4.2 to 57.4.4 ([`5fcdcb7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5fcdcb701a9da5c9a786e0fe690bfd0a8d5d4e0c))

* poetry(deps): bump filelock from 3.3.2 to 3.4.0

Bumps [filelock](https://github.com/tox-dev/py-filelock) from 3.3.2 to 3.4.0.
- [Release notes](https://github.com/tox-dev/py-filelock/releases)
- [Changelog](https://github.com/tox-dev/py-filelock/blob/main/docs/changelog.rst)
- [Commits](https://github.com/tox-dev/py-filelock/compare/3.3.2...3.4.0)

---
updated-dependencies:
- dependency-name: filelock
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`8d4520e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8d4520ee3ee781a3a2f4db879e79e38b40fe4829))

* CHORE: poetry(deps-dev): bump flake8-bugbear from 21.9.2 to 21.11.29

poetry(deps-dev): bump flake8-bugbear from 21.9.2 to 21.11.29 ([`fc6e3ac`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fc6e3acd5a1875a27e3b8037ad3b9a794598c894))

* poetry(deps): bump types-setuptools from 57.4.2 to 57.4.4

Bumps [types-setuptools](https://github.com/python/typeshed) from 57.4.2 to 57.4.4.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-setuptools
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`00dcbb8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/00dcbb80d25c00b2b9bd4f6b765275cd956b33fa))

* CHORE: poetry(deps): bump importlib-metadata from 4.8.1 to 4.8.2

poetry(deps): bump importlib-metadata from 4.8.1 to 4.8.2 ([`28f9676`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/28f96769e653c3b7c76cb07ba1a4ecbbc43ab46c))

* poetry(deps-dev): bump flake8-bugbear from 21.9.2 to 21.11.29

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 21.9.2 to 21.11.29.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/21.9.2...21.11.29)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`1eec2e8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1eec2e8aab5f31f3070be34eccfd8791ef2edcca))

* CHORE: poetry(deps-dev): bump coverage from 6.1.2 to 6.2

poetry(deps-dev): bump coverage from 6.1.2 to 6.2 ([`bdd9365`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bdd93650a64ce2385f4f29bc1f20df6530e9012c))

* CHORE: poetry(deps): bump mako from 1.1.5 to 1.1.6

poetry(deps): bump mako from 1.1.5 to 1.1.6 ([`33d3ecc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/33d3ecc80f47c947d2fc2b13743471dd6dc941ab))

* poetry(deps-dev): bump coverage from 6.1.2 to 6.2

Bumps [coverage](https://github.com/nedbat/coveragepy) from 6.1.2 to 6.2.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/6.1.2...6.2)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`be1af9b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/be1af9b9955a31b6c1a8627010bfd4d932c9f9f1))

* DOCS: fix README shields &amp; links ([`43b1121`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/43b112128acd9e28a47e46d8691ead46e39b288e))

* doc: readme maintenance - shields &amp; links (#72)

* README: restructure links

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: add lan to fenced code blocks

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: fix some formatting

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: modernized shields

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: harmonize links

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: add language to code fences

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: markdown fixes

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: removed py version shield

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3d0ea2f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3d0ea2f4c6ee5c2dedf1abb779f46543896fff4a))

* poetry(deps): bump mako from 1.1.5 to 1.1.6

Bumps [mako](https://github.com/sqlalchemy/mako) from 1.1.5 to 1.1.6.
- [Release notes](https://github.com/sqlalchemy/mako/releases)
- [Changelog](https://github.com/sqlalchemy/mako/blob/main/CHANGES)
- [Commits](https://github.com/sqlalchemy/mako/commits)

---
updated-dependencies:
- dependency-name: mako
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`3344b86`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3344b862490ecb419c9b1f74bd7548ddcf392329))

* Merge pull request #47 from CycloneDX/dependabot/pip/filelock-3.3.2

poetry(deps): bump filelock from 3.3.1 to 3.3.2 ([`3f967b3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3f967b3d0ec47ba5bcc1cdd8fb29970ba69d7aed))

* FIX: update Conda package parsing to handle `build` containing underscore (#66)

* fix: update conda package parsing to handle `build` containing underscore

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* updated some typings

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`2c6020a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2c6020a208aa1c0fd13ab337db6343ad1d2d5c43))

* poetry(deps): bump importlib-metadata from 4.8.1 to 4.8.2

Bumps [importlib-metadata](https://github.com/python/importlib_metadata) from 4.8.1 to 4.8.2.
- [Release notes](https://github.com/python/importlib_metadata/releases)
- [Changelog](https://github.com/python/importlib_metadata/blob/main/CHANGES.rst)
- [Commits](https://github.com/python/importlib_metadata/compare/v4.8.1...v4.8.2)

---
updated-dependencies:
- dependency-name: importlib-metadata
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`003f6b4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/003f6b410e0e32e8c454ad157999b031471baf6f))

* poetry(deps): bump filelock from 3.3.1 to 3.3.2

Bumps [filelock](https://github.com/tox-dev/py-filelock) from 3.3.1 to 3.3.2.
- [Release notes](https://github.com/tox-dev/py-filelock/releases)
- [Changelog](https://github.com/tox-dev/py-filelock/blob/main/docs/changelog.rst)
- [Commits](https://github.com/tox-dev/py-filelock/compare/3.3.1...3.3.2)

---
updated-dependencies:
- dependency-name: filelock
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`55022b7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/55022b7a63763436d193cefda6d6a4e0ad36fb40))

* Merge pull request #45 from CycloneDX/dependabot/pip/importlib-resources-5.4.0

poetry(deps): bump importlib-resources from 5.3.0 to 5.4.0 ([`b8acf9f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b8acf9f3e087f37c2f9afded2d8555c053f09a43))

* Merge pull request #70 from CycloneDX/dependabot/pip/pyparsing-3.0.6

poetry(deps): bump pyparsing from 3.0.5 to 3.0.6 ([`faa8628`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/faa862813e27bb4b828f6116c95961b156cd7547))

* Merge pull request #69 from CycloneDX/dependabot/pip/coverage-6.1.2

poetry(deps-dev): bump coverage from 6.1.1 to 6.1.2 ([`eba56dc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/eba56dc6512304e2956563d173bdb363b785fa50))

* poetry(deps): bump pyparsing from 3.0.5 to 3.0.6

Bumps [pyparsing](https://github.com/pyparsing/pyparsing) from 3.0.5 to 3.0.6.
- [Release notes](https://github.com/pyparsing/pyparsing/releases)
- [Changelog](https://github.com/pyparsing/pyparsing/blob/master/CHANGES)
- [Commits](https://github.com/pyparsing/pyparsing/compare/pyparsing_3.0.5...pyparsing_3.0.6)

---
updated-dependencies:
- dependency-name: pyparsing
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`4f2b2d8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4f2b2d89291b1c20385ce6431959586acfeab1cd))

* poetry(deps-dev): bump coverage from 6.1.1 to 6.1.2

Bumps [coverage](https://github.com/nedbat/coveragepy) from 6.1.1 to 6.1.2.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/6.1.1...6.1.2)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`1d0f5ea`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1d0f5ea2ed5dfb38ce1d1d8170773cb880f228dc))


## v0.11.1 (2021-11-10)

### Fix

* fix: constructor for `Vulnerability` to correctly define `ratings` as optional

Signed-off-by: William Woodruff &lt;william@trailofbits.com&gt; ([`395a0ec`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/395a0ec14ebcba8e0849a0ced30ec4163c42fa7a))

### Unknown

* 0.11.1

Automatically generated by python-semantic-release ([`a80f87a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a80f87a588f8b52bfd8e9c5b12edf0fdde56c510))

* FEAT: Support Python 3.10 (#64)

* fix: tested with Python 3.10

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* added trove classifier for Python 3.10

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* fix: upgrade Poetry version to workaround issue between Poetry and Python 3.10 (see: https://github.com/python-poetry/poetry/issues/4210)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`385b835`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/385b835f44fadb0f227b6a8ac992b0c73afc6ef0))

* poetry(deps): bump importlib-resources from 5.3.0 to 5.4.0

Bumps [importlib-resources](https://github.com/python/importlib_resources) from 5.3.0 to 5.4.0.
- [Release notes](https://github.com/python/importlib_resources/releases)
- [Changelog](https://github.com/python/importlib_resources/blob/main/CHANGES.rst)
- [Commits](https://github.com/python/importlib_resources/compare/v5.3.0...v5.4.0)

---
updated-dependencies:
- dependency-name: importlib-resources
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`a1dd775`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a1dd7752459b70b432784ec2b7d8a1cb24a916a9))


## v0.11.0 (2021-11-10)

### Feature

* feat: Typing &amp; PEP 561

* adde file for type checkers according to PEP 561

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* added static code analysis as a dev-test

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* added the &#34;typed&#34; trove

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* added `flake8-annotations` to the tests

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* added type hints

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* further typing updates

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* further typing additions and test updates

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* further typing

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* further typing - added type stubs for toml and setuptools

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* further typing

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* typing work

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* coding standards

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* fixed tox and mypy running in correct python version

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* supressed mypy for `cyclonedx.utils.conda.parse_conda_json_to_conda_package`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* fixed type hints

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* fixed some typing related flaws

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* added flake8-bugbear for code analysis

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Co-authored-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`9144765`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/91447656c0914ceb2af2e4b7282292ec7b93f5bf))

### Unknown

* 0.11.0

Automatically generated by python-semantic-release ([`7262783`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7262783dbcf5823065670f3f7cbba0ce25b3a4ea))

* Merge pull request #41 from jkowalleck/improv-abstract

fixed some abstract definitions ([`f34e2c2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f34e2c2bc7aed20968a5ac69337ed484d097af3b))

* Merge pull request #42 from jkowalleck/improv-pipenv

slacked pipenv parser ([`08bc4ab`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/08bc4ab2b01c76d7472a558cae02deab0485c61c))

* Merge pull request #43 from jkowalleck/improv-conda-typehints

fixed typehints/docs in `_BaseCondaParser` ([`931016d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/931016d9b700280692903db5aa653d390a80bd63))

* Merge pull request #54 from jkowalleck/create-CODEOWNERS

created CODEOWNERS ([`7f28bef`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7f28bef15ed0b9ed6af88286d5f6dcc0726b6feb))

* Merge pull request #56 from CycloneDX/dependabot/pip/py-1.11.0

poetry(deps): bump py from 1.10.0 to 1.11.0 ([`f1cda3c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f1cda3c3ba859336d70da36d4966bc7c247af97a))

* Merge pull request #58 from CycloneDX/dependabot/pip/pyparsing-3.0.5

poetry(deps): bump pyparsing from 2.4.7 to 3.0.5 ([`0525439`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0525439d2237684ce531449d19e60456fc46d26b))

* Merge pull request #19 from CycloneDX/dependabot/pip/zipp-3.6.0

poetry(deps): bump zipp from 3.5.0 to 3.6.0 ([`c54c968`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c54c96853e3325571dee26038e965279d5b9cfe2))

* poetry(deps): bump py from 1.10.0 to 1.11.0

Bumps [py](https://github.com/pytest-dev/py) from 1.10.0 to 1.11.0.
- [Release notes](https://github.com/pytest-dev/py/releases)
- [Changelog](https://github.com/pytest-dev/py/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pytest-dev/py/compare/1.10.0...1.11.0)

---
updated-dependencies:
- dependency-name: py
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`330711f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/330711fe911739ac9119a0721f7f7bde6e1389e4))

* Merge pull request #57 from CycloneDX/dependabot/pip/coverage-6.1.1

poetry(deps-dev): bump coverage from 5.5 to 6.1.1 ([`fa55e5c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fa55e5ceef65749ccbf6bd0303db649346c79019))

* poetry(deps): bump pyparsing from 2.4.7 to 3.0.5

Bumps [pyparsing](https://github.com/pyparsing/pyparsing) from 2.4.7 to 3.0.5.
- [Release notes](https://github.com/pyparsing/pyparsing/releases)
- [Changelog](https://github.com/pyparsing/pyparsing/blob/master/CHANGES)
- [Commits](https://github.com/pyparsing/pyparsing/compare/pyparsing_2.4.7...pyparsing_3.0.5)

---
updated-dependencies:
- dependency-name: pyparsing
  dependency-type: indirect
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`3bedaff`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3bedaffc7f52026348cc6e2a38ba193ba71d4f29))

* Merge pull request #55 from CycloneDX/dependabot/pip/virtualenv-20.10.0

poetry(deps): bump virtualenv from 20.8.1 to 20.10.0 ([`4c3df85`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4c3df857eba656f1ccb51ba9ad6af2cb49226747))

* CI/CT runs on main &amp; master branch ([`2d0df7b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2d0df7bacf4ead54eee7378ede8626cc93fce3df))

* poetry(deps-dev): bump coverage from 5.5 to 6.1.1

Bumps [coverage](https://github.com/nedbat/coveragepy) from 5.5 to 6.1.1.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/coverage-5.5...6.1.1)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`e322d74`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e322d7476b4a17b012d27c26683809bd1dee86b1))

* poetry(deps): bump virtualenv from 20.8.1 to 20.10.0

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.8.1 to 20.10.0.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.8.1...20.10.0)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`3927cdc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3927cdcd2c37af23543832dbfae2d087cb09787c))

* created CODEOWNERS

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`e8e499c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e8e499cb2b74f9d7e7afe4d0f00e1725eabb655e))

* fixed typehints/docs in `_BaseCondaParser`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`af6ddfd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/af6ddfdc8c7cbdd1bade5ea0c89896ca9791eb3d))

* slacked pipenv parser

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a3572ba`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a3572ba61ca537de8efd0855c774819a963cd212))

* fixed some abstract definitions

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`9e67998`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9e67998e53558363b2c76c75f13bb2772fb5a22d))


## v0.10.2 (2021-10-21)

### Fix

* fix: correct way to write utf-8 encoded files

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`49f9369`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/49f9369b3eba47a3a8d1bcc505546d7dfaf4c5fe))

### Unknown

* 0.10.2

Automatically generated by python-semantic-release ([`79538e9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/79538e92834e548a3f9697388a47efa3b27da678))


## v0.10.1 (2021-10-21)

### Fix

* fix: ensure output to file is UTF-8

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`a10da20`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a10da20865e90e9a0a5bb1e12fba9cfd23970c39))

* fix: ensure output to file is UTF-8

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`193bf64`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/193bf64cdb19bf6fb9662367402dcf7eaab8dd1a))

### Unknown

* 0.10.1

Automatically generated by python-semantic-release ([`e6451a3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e6451a39ee18fcf49287a8f685df730846e965b7))

* Merge pull request #40 from CycloneDX/fix/issue-39-windows-UnicodeEncodeError

FIX: Resolve file encoding issues on Windows ([`48329e0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/48329e033e499f4b9a2c204b2fe5c7c512689605))

* remove memoryview from sha1 file hashing

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`a56be0f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a56be0f2044c1c867c383a7ed26f5fce4097d21a))

* added debug to CI to aid understanding of miss matching SHA1 hashes on Windows

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`10c6b51`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/10c6b51ec1fb8fc816002fda96e551ff0e430941))


## v0.10.0 (2021-10-20)

### Feature

* feat: add support for Conda

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`bd29c78`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd29c782d39a4956f482b9e4de20d7f829beefba))

### Unknown

* 0.10.0

Automatically generated by python-semantic-release ([`eea3598`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/eea35980ab121899d46178ec10e90058d0e1be45))

* Merge pull request #38 from CycloneDX/feat/conda-support

feat: add support for Conda ([`ee5d36d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ee5d36dd677abfb1ba5600b44abf45cb2612b792))

* add support pre Python 3.8

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`2d01116`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2d011165e36d03c8d82c7b92b56f1aeec9c18cd6))

* doc: updated documentation with Conda support (and missed updates for externalReferences)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`57e9dc7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/57e9dc7b2adcfa2bac60a854c91bf77947e8e9cf))


## v0.9.1 (2021-10-19)

### Fix

* fix: missing check for Classifiers in Environment Parser

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`b7fa38e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b7fa38e9740bbc5b4c406410df37c3b34818010c))

### Unknown

* 0.9.1

Automatically generated by python-semantic-release ([`f132c92`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f132c92bf38f1c173b381f18817f0f86b6ddde85))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib ([`51a1e50`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/51a1e50aad27c1f862812031be74281e839815df))


## v0.9.0 (2021-10-19)

### Feature

* feat: add support for parsing package licenses when using the `Environment` Parsers

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`c414eaf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c414eafde2abaca1005a2a0af6993fcdc17897d3))

### Unknown

* 0.9.0

Automatically generated by python-semantic-release ([`ad65564`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ad6556462d92381dcd8494ca93496ea796282565))

* Merge pull request #36 from CycloneDX/feat/add-license-support

Add support for parsing package licenses from installed packages ([`d45f75b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d45f75b88611ab97f39bde672cbdd9e8ff71dd3e))


## v0.8.3 (2021-10-14)

### Fix

* fix: coding standards violations

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`00cd1ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/00cd1ca20899b6861b1b959611a3556ffad36832))

* fix: handle `Pipfile.lock` dependencies without an `index` specified
fix: multiple fixes in variable scoping to prevent accidental data sharing

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`26c62fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/26c62fb996c4b1b2bf719e10c9072cf4fbadab9f))

### Unknown

* 0.8.3

Automatically generated by python-semantic-release ([`91f9a8b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/91f9a8bb60fe8faddd86268c0ede89cd0caa5a76))

* Merge pull request #34 from CycloneDX/fix/issue-33-pipfile-lock-parse-failure

BUG: Fixe for `Pipfile.lock` parsing + accidental data sharing issues identified during testing ([`4079323`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4079323617263886319ddcf80ee1d77909a40b69))


## v0.8.2 (2021-10-14)

### Fix

* fix: add namespace and subpath support to Component to complete PackageURL Spec support

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`780adeb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/780adebe3861ef08eb1e8817a5e9e3451c0a2137))

### Unknown

* 0.8.2

Automatically generated by python-semantic-release ([`298318f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/298318fdbf252115f874eb544c2d1f24abb6ab5a))

* Merge pull request #32 from CycloneDX/feat/full-packageurl-support

Add `namespace` and `subpath` support to `Component` ([`bb3af91`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bb3af916f1ff0e224d9c197596570bca98ea4525))


## v0.8.1 (2021-10-12)

### Fix

* fix: multiple hashes being created for an externalRefernce which is not as required

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`970d192`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/970d19202d13d4becbbf040b3a9fb115dd7a0795))

### Unknown

* 0.8.1

Automatically generated by python-semantic-release ([`70689a2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/70689a21edfd5f17cd2aabc09d4579646a4f1633))


## v0.8.0 (2021-10-12)

### Feature

* feat: add support for `externalReferneces` for `Components` and associated enhancements to parsers to obtain information where possible/known

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`a152852`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a152852b361bbb7a69c9f7ab61ae7ea6dcffd214))

### Unknown

* 0.8.0

Automatically generated by python-semantic-release ([`7a49f9d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7a49f9d8cd791e9b1a7e1a8587e589e3b8319ec7))

* Merge pull request #29 from CycloneDX/feat/component-external-references

FEATURE: Add support for `externalReferences` against `Component`s ([`bdee0ea`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bdee0ea277d9f378b3a5e225c2ac3d8e20e2c53c))

* doc: notable improvements to API documentation generation (added search, branding, a little styling)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`e7a5b5a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e7a5b5a2c5b5681a75a24e9739d13ead01f362e3))


## v0.7.0 (2021-10-11)

### Feature

* feat: support for pipenv.lock file parsing

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`68a2dff`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/68a2dffc770d40f693b6891a580d1f7d8018f71c))

### Unknown

* 0.7.0

Automatically generated by python-semantic-release ([`827bd1c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/827bd1cf2db6cfcffdae98dbd6d24efac63d0cb6))

* Merge pull request #27 from CycloneDX/feat/add-pipenv-support

FEATURE: Add `Pipfile.lock` (pipenv) support ([`2c42e2a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2c42e2a616c07eec1f844b4fbc4e1e3b4a0815d8))

* doc: updated README.md to include Pipfile.lock parsing

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`2c66834`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2c66834ee6aac75b3e810d13b5a3b41967043252))


## v0.6.2 (2021-10-11)

### Fix

* fix: added ability to add tools in addition to this library when generating CycloneDX + plus fixes relating to multiple BOM instances

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`e03a25c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e03a25c3d2a1a0b711204bb26c7b898eadacdcb0))

### Unknown

* 0.6.2

Automatically generated by python-semantic-release ([`e68fbc2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e68fbc2ff5576fc1f5c0444f601c58f40f3cd917))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib ([`2bf2711`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2bf27119e7a1a3716706c28c3fb259496d0de6f1))


## v0.6.1 (2021-10-11)

### Fix

* fix: better methods for checking if a Component is already represented in the BOM, and the ability to get the existing instance

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`5fee85f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5fee85fc38376478a1a438d228c632a5d14f4740))

### Unknown

* 0.6.1

Automatically generated by python-semantic-release ([`c530460`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c530460f504939d34e8c73066bfdd252dd95f090))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib ([`eb3a46b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/eb3a46b4365818dec08ea079f47e4abd75ebbd64))


## v0.6.0 (2021-10-11)

### Feature

* feat: helper method for representing a File as a Component taking into account versioning for files as per https://github.com/CycloneDX/cyclonedx.org/issues/34

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`7e0fb3c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7e0fb3c7e32e08cb8667ad11461c7f8208dfdf7f))

* feat: support for non-PyPi Components - PackageURL type is now definable when creating a Component

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`fde79e0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fde79e02705bce216e62acd05056b6d2046cde22))

### Unknown

* 0.6.0

Automatically generated by python-semantic-release ([`907cd2d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/907cd2d317f3cfd28febb450959938d09815b9c2))

* Merge pull request #25 from CycloneDX/feat/additions-to-enable-integration-into-checkov

Support for representing File as Component ([`63a86b0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/63a86b05aa722078d57f143f35c1f5600396ec7a))


## v0.5.0 (2021-10-11)

### Build

* build: updated dependencies, moved pdoc3 to a dev dependency

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`6a9947d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6a9947de1036b63804352e45c035d40658d3db01))

### Feature

* feat: add support for tool(s) that generated the SBOM

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`7d1e6ef`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7d1e6ef04d473407b9b4eefc2ef18e6723838f94))

### Fix

* fix: bumped a dependency version

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`efc1053`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/efc1053ec9ed3f57711f78f1eca181f7bff0c3bf))

### Unknown

* 0.5.0

Automatically generated by python-semantic-release ([`a655d29`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a655d29ae9a93bdd72fee481d6a0ec8b71f6cce0))

* Merge pull request #20 from CycloneDX/feat/additional-metadata

feat: add support for tool(s) that generated the SBOM ([`b33cbf4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b33cbf4cb40179e5710729b89d3c120e69448777))

* fix for Pytho&lt; 3.8 support in tests

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`c9b6019`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c9b6019609ae206ba965d0c4f7c06ffcf8835e1d))

* ensure support for Python &lt; 3.8

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`53a82cf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/53a82cfbe7e828380c31b2441113f318d2a2c99e))

* ensure support for Python &lt; 3.8

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`2a9e56a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2a9e56a7e1e0235a06aa70f7750f1656f9305a8a))

* doc: added documentation

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`cf13c68`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cf13c6817552c0a6549ecd7131fdcd437ccc7210))

* poetry(deps): bump zipp from 3.5.0 to 3.6.0

Bumps [zipp](https://github.com/jaraco/zipp) from 3.5.0 to 3.6.0.
- [Release notes](https://github.com/jaraco/zipp/releases)
- [Changelog](https://github.com/jaraco/zipp/blob/main/CHANGES.rst)
- [Commits](https://github.com/jaraco/zipp/compare/v3.5.0...v3.6.0)

---
updated-dependencies:
- dependency-name: zipp
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`30f2547`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/30f254724b49c7596c58f11ef8f5a182706ef03a))

* doc: bumped gh-action for publishing docs

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`ac70eee`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ac70eeed9325892ef9ae44b162d8a3ae43a435cc))

* doc: added documentation to model/bom

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`fe98ada`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fe98ada121279f6119f3045abd737cc5b775a30f))

* doc: formatting

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`1ad7fb1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1ad7fb117acbec87def897f4dc549dc398decce6))

* doc: added missing docstrings to allow documentation to generate

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`ed743d9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ed743d9b90904a6719309de85078657f9e4a48cd))

* Merge pull request #10 from coderpatros/docs

Add initial doc generation and publishing ([`7873ad9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7873ad9d3fed8c04b94999c21345ae4ca198e091))


## v0.4.1 (2021-09-27)

### Build

* build: dependencies updated

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`0411826`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/04118263c2fed1241c4a9f38cc256542ba543d50))

### Fix

* fix: improved handling for `requirements.txt` content without pinned or declared versions

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`7f318cb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7f318cb495ac1754029088cae1ef2574c58da2e5))

### Unknown

* 0.4.1

Automatically generated by python-semantic-release ([`d5b7a2f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d5b7a2fc731b29fd7a3f29fe3c94f14a98a82e69))

* Merge pull request #15 from CycloneDX/fix/issue-14-requirements-unpinned-versions

fix: improved handling for `requirements.txt` content without pinned … ([`f248015`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f248015ff9719dd0029f6267067356672f16f8c3))

* Add initial doc generation and publishing

Signed-off-by: Patrick Dwyer &lt;patrick.dwyer@owasp.org&gt; ([`cd1b558`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cd1b558fe472895f9332d9844f99e652c14ec41e))


## v0.4.0 (2021-09-16)

### Feature

* feat: support for localising vectors (i.e. stripping out any scheme prefix)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`b9e9e17`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9e9e17ba1e2c1c9dfe551c61ad5152eebd829ab))

* feat: helper methods for deriving Severity and SourceType

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`6a86ec2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6a86ec27c13ff5e413c5a5f96d9b7671646f9388))

### Fix

* fix: removed print call

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`8806553`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/880655304c082a88d94d6d50c64d33ad931cc974))

* fix: relaxed typing of parameter to be compatible with Python &lt; 3.9

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`f9c7990`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f9c7990695119969c5055bc92a233030db999b84))

* fix: removed print call

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`d272d2e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d272d2ea7d3331bde0660bdc87a6ac3331ae0720))

* fix: remove unused commented out code

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`ba4f285`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba4f285fdbe124c28f7ea60310347cf896540125))

### Unknown

* 0.4.0

Automatically generated by python-semantic-release ([`f441413`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f441413668676c0435b173c01d612e9040d6f6db))


## v0.3.0 (2021-09-15)

### Feature

* feat: adding support for extension schema that descriptions vulnerability disclosures

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`d496695`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d4966951ab6c0229171cfe97723421bb0302c4fc))

### Unknown

* 0.3.0

Automatically generated by python-semantic-release ([`a5c3dab`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a5c3dab5818c183bd88385c7ad88e11eb34a0417))

* Merge pull request #5 from CycloneDX/feat/support-schema-extension-vulnerability-1.0

FEATURE: add support for Vulnerability Disclosures ([`6914272`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/69142723935199409f6bf91b68ecf1e91107f165))

* doc: updated README to explain support for Vulnerability Disclosures

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`f477bf0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f477bf03fc78cc2652e97cd77a3e7ab66306a39b))


## v0.2.0 (2021-09-14)

### Feature

* feat: added helper method to return a PackageURL object representing a Component

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`367bef1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/367bef11bb1a7ede3100acae39581e33d20fa7f5))

### Fix

* fix: whitespace on empty line removed

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`cfc952e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cfc952eb5f3feb97a41b6c895657058429da3430))

### Unknown

* 0.2.0

Automatically generated by python-semantic-release ([`866eda7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/866eda764d01ee85778bea662c7556113121137e))

* Merge pull request #4 from CycloneDX/feat/component-as-packageurl

fix: whitespace on empty line removed ([`ddc37f3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ddc37f395a1dbace39280a4f7b1074d954414f2d))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib ([`6142d2e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6142d2e3b9b655ebf95b59c93525ce8008851b34))


## v0.1.0 (2021-09-13)

### Feature

* feat: add poetry support

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`f3ac42f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f3ac42f298b8d093b0ac368993beba43c58c251a))

### Unknown

* 0.1.0

Automatically generated by python-semantic-release ([`0da668f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0da668f398bef2baee63b0d342063b6dc0eea71a))

* Merge pull request #3 from CycloneDX/feat/poetry-lock-support

FEATURE: Adde poetry.lock parser support ([`37ba7c6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/37ba7c61a17881fc02119dcfd7b6e0a7cab48cbf))

* feat(parser) - added support for parsing dependencies from poetry.lock files.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`15bc553`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/15bc5539e2339581f80048a571ca632f17988530))

* fix(parser) parsers were able to share state unexpectedly

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`dc59914`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/dc59914e961104d9fcd37822b172d798e68b6ebd))


## v0.0.11 (2021-09-10)

### Fix

* fix(test): test was not updated for revised author statement

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`d1c9d37`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d1c9d379a1e92ee49aae8d133e2ad3e117054ec9))

* fix(build): test failure and dependency missing

Fixed failing tests due to dependency on now removed VERSION file
Added flake8 officially as a DEV dependency to poetry

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`9a2cfe9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9a2cfe94386b51acca44ae3bacae319b9b3c8f0d))

* fix(build): removed artefacts associtated with non-poetry build

Tidied up project to remove items associated with non-Poetry build process. Also aligned a few references in README to new home of this project under CycloneDX.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`f9119d4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f9119d49e462cf1f7ccca9c50af2936f8962fd6d))

### Unknown

* 0.0.11

Automatically generated by python-semantic-release ([`1c0aa71`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1c0aa716b36e1305b7a3a2b9e2dfd6e5c6ac0011))

* Merge pull request #2 from CycloneDX/fix/tidy-up-build-remove-pip

fix(build): removed artefacts associated with non-poetry build ([`b7de7b3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b7de7b3c9ba2c8c824d898ee994169b66b78b07a))


## v0.0.10 (2021-09-08)

### Fix

* fix: add in pypi badge ([`6098c36`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6098c36715b2459d7b04ced5ba6294437576e481))

### Unknown

* 0.0.10

Automatically generated by python-semantic-release ([`245d809`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/245d809c3918d023ae58af2fb352f14912be091c))


## v0.0.9 (2021-09-08)

### Fix

* fix: additional info to poetry, remove circleci ([`2fcfa5a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2fcfa5ac3a7d9d7f372be6d69e1c616b551877df))

### Unknown

* 0.0.9

Automatically generated by python-semantic-release ([`e4a90cf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e4a90cfc46db3284e1f3e53f6555405fc14dc654))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib into main ([`69aaba5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/69aaba5f941cbffc40b47d18c6f9dd9dd754b57b))


## v0.0.8 (2021-09-08)

### Fix

* fix: initial release to pypi, tell poetry to include cyclonedx package ([`a030177`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a030177cb1a370713c4438b13b7520ef6afd19f6))

### Unknown

* 0.0.8

Automatically generated by python-semantic-release ([`fc3f24c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fc3f24c13938948c4786ecf8ace3fc241c0f458e))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib into main ([`da2d18c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/da2d18cd60a781bf097e563466bda0d3e51b9e8f))


## v0.0.7 (2021-09-08)

### Fix

* fix: release with full name ([`4c620ed`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4c620ed053aac8c31343b1ca84ca56912b762ab2))

### Unknown

* 0.0.7

Automatically generated by python-semantic-release ([`19943e8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/19943e8287bbe67031cada6f5377d438f2b033c1))


## v0.0.6 (2021-09-08)

### Fix

* fix: initial release to pypi ([`99687db`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/99687dbec1389bf323bb625bfb707306aa3b8d1a))

### Unknown

* 0.0.6

Automatically generated by python-semantic-release ([`98ad249`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/98ad24950dbb5f5b08db41e1bb4e359f8f0b8b49))

* Switch to using action ([`cce468a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cce468a7004d848ddbaab4affa392bd2f74414dd))


## v0.0.5 (2021-09-08)

### Unknown

* 0.0.5

Automatically generated by python-semantic-release ([`9bf4b9a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9bf4b9a29cc4b0bbdf5771ffc22b918a6081a0a1))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib into main ([`eeec0bb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/eeec0bba7d0a615f8384caa50ed95c2240b5a951))

* Try this on for size ([`aa93310`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/aa93310830a86aa441337be34081c46d9475384c))


## v0.0.4 (2021-09-08)

### Unknown

* 0.0.4

Automatically generated by python-semantic-release ([`b16d6c5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b16d6c59495de396c73dfe1ffabcbfd325dfa619))

* Use python3 to install ([`4c810e1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4c810e16b1a93afb923652f66e77ee08ff0ffd49))


## v0.0.3 (2021-09-08)

### Unknown

* 0.0.3

Automatically generated by python-semantic-release ([`05306ee`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/05306ee235df1d7aa662c9323e6186cc3d1129dc))

* Merge branch &#39;main&#39; of github.com:CycloneDX/cyclonedx-python-lib into main ([`f1d120c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f1d120c5dca530424dd79b3303458cc0adbc28de))

* Bump up version of poetry ([`89db268`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/89db2689bbdb94f2f290abe1bf721b163d75001e))


## v0.0.2 (2021-09-08)

### Unknown

* 0.0.2

Automatically generated by python-semantic-release ([`e15dec6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e15dec696bd88d00f5f5fdce74cb407bc65a42e2))

* Remove check for push ([`71b1270`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/71b12709f0fb55852cbb030669a80a5ebd2f2e92))

* Manual deploy workflow ([`9b4ac33`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9b4ac335becf7e7b83cd3fa619c8975b6335f5eb))

* License headers, OWASP etc... ([`559b8d2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/559b8d227e52b6798a71149c87f4090ea1244c85))

* Fixed unit tests pinned to a VERISON. ([`5d907d5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5d907d58e57f2eb7731047a51a88104cb07c1796))

* Bump to version 0.0.2 ([`1050839`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/105083951dc93f28a4816c0c699af7db7f2789d9))

* Implemented writing SBOM to a file. ([`74f4153`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/74f4153d84c3bbdb875eac679fe933b777f90f18))

* Updated badge in README to include Python 3.6+ support. ([`0a5903c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0a5903c56971a19172fe904f02836c5c5e2262db))

* Removed print() statement accidentally left in. ([`22965a7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/22965a707de6db7bb08721809035562be72c69d5))

* Merge pull request #1 from sonatype-nexus-community/features/initial-port-of-v1.1-generation-from-jake

Initial port of library code to new library ([`2f2634b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2f2634b86612b4f0d2142b09f3aece588937fcaa))

* Added license headers to all source files. Added classifiers for Python version to setup.py. ([`bb6bb24`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bb6bb24440996257ce609b0f399f930153b65e8e))

* Renamed model file to not reference CycloneDX as the models are agnostic on purpose. ([`03d03ed`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/03d03edfca7bed56d21733120cb5b002a32bb466))

* Forgot to add updated poetry.lock file relfecting Python 3.6+ support ([`5d3d491`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5d3d49184039a2f41411cd96d5dfcf1544fab05f))

* Updated project to state support from Python v3.6+ ([`619ee1d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/619ee1dfc23f7220a1941c3fa5068761346c84cb))

* Adding Python 3.6 support for test &amp; CI. ([`daa12ba`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/daa12ba8925128da040cf836bc3f16a2126e9091))

* Fixing CircleCI config. ([`a446f4c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a446f4cb197fd40a3065a372108c1719cde91136))

* Fixes to GitHub actions. ([`d2aa277`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d2aa277bce954100adad42e33c095bc1f9ce23cd))

* Disabled Py3.6 checks and added flake8. ([`8c01da3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8c01da3d8f6038fb24df07ab3fb0945c79893e9f))

* Attempt to fix CI&#39;s for multiple Python environments. ([`affb6b2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/affb6b2dc7afeaff5b5cd0a1d4f65678394a2ff7))

* Added support for Python versions 3.7+ ([`ae24ba9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ae24ba9c26ddf4ef91937e8489b1894a986724de))

* Added missing ENV var for GH actions. ([`c750ec6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c750ec62411c6d4473d3cc0a33dc96f90a443cef))

* Missed wrapping a coverage command with poetry. ([`3c74c82`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3c74c822445e5aeaaa387c8e5522ca8cd841cfd8))

* Added poetry virtualenv caching + wrapped tox and coverage with poetry to ensure they run in the poetry venv. ([`780e3df`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/780e3dfa043957174e1f79cf450d1ee69d6530d3))

* Fixed typo in Github action. ([`3953675`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/395367531e7a00c086e723a78d059e6016fb242e))

* Correction: Supported Python version in setup.py ([`2f4917b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2f4917ba81f8ddba994a2c5012303bccb307a419))

* Updated poetry dependencies and configuration. ([`75041e5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/75041e51ff684853d7c2b94e5a722a4ec14043fc))

* Initial draft GitHub actions being added. ([`e2403e8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e2403e8c4194be6bee70a58ef86d9acec6de5dbb))

* Added Poetry supprot. ([`e9a67f8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e9a67f8a405b6c664d2b91bd4966a8ade9902d40))

* Addressing issues reported by flake8. ([`3ad394c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3ad394c14d9cbf3e706f4fe47b6f83938576a2ac))

* Refactored output classes to use multiple inheritance allowing a single place to define which schema version support various attributes and elements. ([`95c5b38`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/95c5b389bb5c8c358420aaf5c62694dcabe663ce))

* Updated README to reflect support for author. ([`bff5954`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bff5954f70967f3605fa6226a223590b89e07313))

* Skeleton support for &#39;author&#39; + v1.1 and v1.0 for JSON added (along with tests). ([`e987f35`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e987f357314199442ed2c5823575833915dfccb1))

* Corrected typo in README ([`0d2c355`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0d2c35519374b4efddf399dd519e5a1443a56692))

* Updated README to include a summary of the support this library provides across the different schema versions. ([`34f421f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/34f421f4076d16c30ddf291f5c1866c1b623258a))

* Initial support for V1.0 and V1.1 in XML output format. ([`37f6b00`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/37f6b00b7e354b76a9f8f72ed2c1004a0e728319))

* Added &#39;serialNumber&#39; to SBOMs (JSON and XML). ([`50e3c75`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/50e3c7546b92e3241feefa6dea0fbfa9c1145843))

* Added a bunch more content to the README to explain how the library can be used. ([`bb41dc6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bb41dc6d333f59025aae97c602cbe41343645b20))

* Added metadata initial support to JSON output format. ([`8c5590f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8c5590fd3c5c59de9a5b6cf49005f4c6e444265d))

* Addition of simple &#39;metadata&#39; element for XML SBOM&#39;s. ([`f9e9773`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f9e97733b0cc57bbb71341b4ced4ccc8f09b7f28))

* Added initial JSON outputter and associated tests. ([`3e1f5ec`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3e1f5ec9354a779adf44129656a1ccdcffadee6d))

* Fix to generate HTML coverage reports and stash in CircleCI builds. ([`dd88603`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/dd886032b92d491f462d62f269f3df7ed823d436))

* Added HTML coverage report. ([`ce700e5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ce700e5bdff7ce4a8bd5614239b129e59afe2908))

* Missed coverage as a dependency for testing. ([`01643d6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/01643d67f73ec8ee35884d0bcc15c892649f6b72))

* Added coverage reporting for tests ([`c34b1a6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c34b1a63fd7958d2b1060ba51054a55b57228549))

* Added first tests for XML SBOM generation (v1.3 and v1.2). ([`cb4337a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cb4337a1cb14ee62471140add8954dd7c5b6b314))

* WIP: Starting to generate XML output for BOMs ([`35bdfca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/35bdfca4fc01cdb3fa7ab6fb37b1c05eaa7189ec))

* Updated CircleCI config to run tox. Fixed fomratting in tests. ([`9a56230`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9a5623098ff712df0cefbd2327e8058f9ac74e17))

* Rebasing from main. ([`822ab8b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/822ab8b43a06bf1712d134d44acb136e70134c05))

* Initial skeleton tests for output genereation. ([`a614f3e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a614f3e9cc6210a25daff79e4ec428f15221cc1e))

* pretty badge ([`60e975c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/60e975c12cdf6c15c9e38585becaf53850609d67))

* initial CI for discussion ([`7e88cd5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7e88cd5920480cd6bde4e72b8b85314242964013))

* Added a little more information to the README. ([`460c624`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/460c62487e66df750a99e10a62bf19bf0baf2e76))

* Fixed issue reported by Flake8. Ensuring tests run on PY 3.9. ([`cce130f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cce130f53a7c73554015ce672cbe8799e863e64b))

* Basic structure without any output generation available (very basic Component definition). ([`6ac5dc2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6ac5dc29fb4bc52f66698966e0b570588621be72))

* Added tox config with flake8 and py3.9 support. ([`1def201`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1def2015d3aad4b58980d9b86cca840f19ac4ee6))

* Initially added skeleton packaging structure and official CycloneDX schemas. ([`ac519c9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ac519c9a21bc8e4a75927868f32f29febc648509))

* Added inital blank README prior to branching for initial work. ([`b175f6a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b175f6a9178c510cfa14b5d2788feecfd65d8e94))

* Added inital blank README prior to branching for initial work. ([`e8b5d48`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e8b5d4802079f92da106b8e0a68f9311c328a656))

* Initial commit ([`62353b0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/62353b0ce57f797bcb9dfd97871e886db8269478))
