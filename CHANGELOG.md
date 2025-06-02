# CHANGELOG


## v10.0.2 (2025-06-02)

### Bug Fixes

- `model.bommetadata.component` setter typehint
  ([#817](https://github.com/CycloneDX/cyclonedx-python-lib/pull/817),
  [`bfe889a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bfe889a174536303939822404f77158c5c1fb668))

---------

Signed-off-by: dependabot[bot] <support@github.com>

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- `model.bommetadata.component` setter typehint
  ([#817](https://github.com/CycloneDX/cyclonedx-python-lib/pull/817),
  [`bfe889a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bfe889a174536303939822404f77158c5c1fb668))


## v10.0.1 (2025-05-10)

### Bug Fixes

- Add missing comparator for VulnerabilityAnalysis
  ([#812](https://github.com/CycloneDX/cyclonedx-python-lib/pull/812),
  [`0df2982`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0df2982151a99ce6e21336e6904afc0a8058f9af))

When trying to generate a CycloneDX BOM that has two vulnerabilities that only differ in their
  analysis, you get ``` TypeError: '<' not supported between instances of 'VulnerabilityAnalysis'
  and 'VulnerabilityAnalysis' ```

This PR adds the `__lt__` method for the VulnerabilityAnalysis model to fix sorting and also
  includes a test case to verify the fix.

---------

Signed-off-by: Riku Häkli <hakli.riku@gmail.com>

Co-authored-by: Riku Häkli <hakli.riku@gmail.com>

### Documentation

- **fix**: Mdformat
  ([`acf5c45`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/acf5c45874808b831c33344f08ea21df20c727bb))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v10.0.0 (2025-04-23)

### Features

- Drop support for Python <3.9 ([#809](https://github.com/CycloneDX/cyclonedx-python-lib/pull/809),
  [`8b2a07d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8b2a07d01b26cdcb9310fc22de7d4c4b66350a93))

Python 3.8 is end-of-life.

---------

Signed-off-by: Simoh23999 <simocasmina@gmail.com>

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Co-authored-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v9.1.1-rc.1 (2025-03-03)


## v9.1.0 (2025-02-27)

### Bug Fixes

- Improved comparison functionality of `model.VulnerabilityAnalysis`
  ([#795](https://github.com/CycloneDX/cyclonedx-python-lib/pull/795),
  [`7d57c73`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7d57c73ef63bfb016099f4c0312b6702da488efc))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- `model.vulnerabilityanalysis` properties for issued/updated datetime
  ([#794](https://github.com/CycloneDX/cyclonedx-python-lib/pull/794),
  [`4a3955a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4a3955a610bad97550e11c426c61c1295b76f804))

Signed-off-by: Indivar Mishra <indimishra@gmail.com>


## v9.0.2 (2025-02-26)


## v9.0.0 (2025-02-26)

### Features

- 9.0.1 ([#777](https://github.com/CycloneDX/cyclonedx-python-lib/pull/777),
  [`e6f91fa`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e6f91fa98cbb02cda62fd0bc5b1f1b9bf19902ee))

### BREAKING Changes

* Fix: `model.vulnerability.VulnerabilityReference`'s properties are all mandatory
  ([#790](https://github.com/CycloneDX/cyclonedx-python-lib/issues/790) via
  [#792](https://github.com/CycloneDX/cyclonedx-python-lib/pull/792)) * Refactor: Rename
  `spdx.is_compund_expression` -> `spdx.is_expression`
  ([#779](https://github.com/CycloneDX/cyclonedx-python-lib/pull/779)) * Behavior: `BomRef` affects
  comparison/hashing ([#754](https://github.com/CycloneDX/cyclonedx-python-lib/pull/754) &
  [#780](https://github.com/CycloneDX/cyclonedx-python-lib/pull/780)) This is only a breaking change
  if you relied on ordering of elements. * Behavior: streamline comparison/hashing functions
  ([#755](https://github.com/CycloneDX/cyclonedx-python-lib/pull/755)) This is only a breaking
  change if you relied on ordering of elements. * Dependency: bump dependency `py-serializable >=2
  <3`, was `>=1.1.1 <2` ([#775](https://github.com/CycloneDX/cyclonedx-python-lib/pull/775)) This is
  only a breaking change if you have other packages depend on that specific version.

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Signed-off-by: wkoot <3715211+wkoot@users.noreply.github.com>

Signed-off-by: semantic-release <semantic-release@bot.local>

Co-authored-by: wkoot <3715211+wkoot@users.noreply.github.com>

Co-authored-by: semantic-release <semantic-release@bot.local>


## v8.9.0 (2025-02-25)

### Documentation

- Extended instructions for "contributing"
  ([#783](https://github.com/CycloneDX/cyclonedx-python-lib/pull/783),
  [`e2a4ed3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e2a4ed3608253b65a0f902f225fe7b7dd29ab864))

supersedes https://github.com/CycloneDX/cyclonedx-python-lib/pull/773/files#r1954324461

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Avoid raising `NoPropertiesProvidedException` for optional parameters
  ([#786](https://github.com/CycloneDX/cyclonedx-python-lib/pull/786),
  [`845b8d5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/845b8d538d2f0fcadb3a3257a066ad58e3640c97))

the following classes' init no longer raise `NoPropertiesProvidedException`: *
  `cyclonedx.model.IdentifiableAction` * `cyclonedx.model.component.Commit` *
  `cyclonedx.model.component.ComponentEvidence` * `cyclonedx.model.component.Diff` *
  `cyclonedx.model.component.Pedigree` * `cyclonedx.model.issue.IssueTypeSource` *
  `cyclonedx.model.vulnerability.VulnerabilityAnalysis` *
  `cyclonedx.model.vulnerability.VulnerabilityCredits` *
  `cyclonedx.model.vulnerability.VulnerabilityRating` *
  `cyclonedx.model.vulnerability.VulnerabilitySource`

---------

Signed-off-by: Indivar Mishra <indimishra@gmail.com>


## v8.8.0 (2025-02-12)

### Features

- Add `cyclonedx.model.crypto.ProtocolProperties.crypto_refs`
  ([#767](https://github.com/CycloneDX/cyclonedx-python-lib/pull/767),
  [`beb35f5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/beb35f55e3e75d625db45e4ff084dee02e919ef6))

Signed-off-by: Indivar Mishra <indimishra@gmail.com>


## v8.7.0 (2025-02-06)

### Features

- Allow empty `OrganizationalContact` object
  ([#772](https://github.com/CycloneDX/cyclonedx-python-lib/pull/772),
  [`03b35f4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/03b35f4293ab3b4c402c7bb8ff458831e492cb8b))

fixes https://github.com/CycloneDX/cyclonedx-python-lib/issues/771

---------

Signed-off-by: Johannes Feichtner <johannes@web-wack.at>

Signed-off-by: Johannes Feichtner <johannes.feichtner@dynatrace.com>


## v8.6.0 (2025-02-04)

### Features

- Allow empty `OrganizationalEntity` object
  ([#768](https://github.com/CycloneDX/cyclonedx-python-lib/pull/768),
  [`472bded`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/472bded38cd480ba6885d44c798e015b63c89190))

fixes https://github.com/CycloneDX/cyclonedx-python-lib/issues/764

Signed-off-by: Johannes Feichtner <johannes@web-wack.at>

- Expand the capabilities of `models.definition.Standard`
  ([#713](https://github.com/CycloneDX/cyclonedx-python-lib/pull/713),
  [`901dcdc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/901dcdc60a8a46d30878764d7b8bda69c6ba8b80))

---------

Signed-off-by: Hakan Dilek <hakandilek@gmail.com>

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Co-authored-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v8.5.1 (2025-01-28)

### Documentation

- Fix typos in in conda-forge.md and remove unused reference in README
  ([#762](https://github.com/CycloneDX/cyclonedx-python-lib/pull/762),
  [`66ece7a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/66ece7ae0042740a541ceed3048b89c4f2b24145))

- Fix few typos in conda-forge.md - Removed unused PEP-508 ref in README.md

Signed-off-by: Arthit Suriyawongkul <arthit@gmail.com>

- Modernize docstrings for CDX1.6
  ([#759](https://github.com/CycloneDX/cyclonedx-python-lib/pull/759),
  [`fb9a42e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fb9a42ef9bda6407ddf4c49e75d10aa0fc91e46d))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Responsibilities & capabilities
  ([#763](https://github.com/CycloneDX/cyclonedx-python-lib/pull/763),
  [`ab4ae45`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ab4ae4578555f010914d7e904133dd478d7c80c1))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Couple classes and their serializes
  ([#757](https://github.com/CycloneDX/cyclonedx-python-lib/pull/757),
  [`6003feb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6003febaa032969732ee246deb739d1e13bae581))

Deprecates `.serialization.BomRefHelper` and `.serialization.LicenseRepositoryHelper`

fixes #756

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v8.5.0 (2024-11-18)

### Documentation

- Remove invalid docsting note about auto-assigned `bom-ref` values
  ([#733](https://github.com/CycloneDX/cyclonedx-python-lib/pull/733),
  [`5aa5787`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5aa5787767c60dc23fd09f6cf14e54e5b0efceb4))

### Features

- Support CycloneDX 1.6.1 ([#742](https://github.com/CycloneDX/cyclonedx-python-lib/pull/742),
  [`55eafed`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/55eafedf50d395911a697bd9c85eeab5820934ff))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v8.4.0 (2024-10-29)

### Bug Fixes

- No warning for missing dependencies if no component exists
  ([#720](https://github.com/CycloneDX/cyclonedx-python-lib/pull/720),
  [`d9c3ded`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d9c3ded34f443cd04f1f0041f0dd948db3db40e7))

---------

Signed-off-by: weichslgartner <weichslgartner@gmail.com>

### Features

- Add factory method `XsUri.make_bom_link()`
  ([#728](https://github.com/CycloneDX/cyclonedx-python-lib/pull/728),
  [`5ec73d0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5ec73d0668b4f9e087cc11a2e1a0e242ad1b5dd6))

---------

Signed-off-by: Saquib Saifee <saquibsaifee@ibm.com>

Co-authored-by: Saquib Saifee <saquibsaifee@ibm.com>


## v8.3.0 (2024-10-26)

### Documentation

- Revisit examples readme ([#725](https://github.com/CycloneDX/cyclonedx-python-lib/pull/725),
  [`e9020f0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e9020f0b709a5245d1749d2811b8568f892869bb))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Add basic support for Definitions
  ([#701](https://github.com/CycloneDX/cyclonedx-python-lib/pull/701),
  [`a1573e5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a1573e5af12bb54c7328c73971dc2c2f8d820c0a))

---------

Signed-off-by: Hakan Dilek <hakandilek@gmail.com>


## v8.2.1 (2024-10-24)

### Bug Fixes

- Encode quotation mark in URL ([#724](https://github.com/CycloneDX/cyclonedx-python-lib/pull/724),
  [`a7c7c97`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a7c7c97c37ee1c7988c028aa779f74893f858c7b))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v8.2.0 (2024-10-22)

### Features

- Add Python 3.13 support ([#718](https://github.com/CycloneDX/cyclonedx-python-lib/pull/718),
  [`d4be3ba`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d4be3ba6b3ccc65553a7dd10ad559c1eddfbb19b))

Signed-off-by: gruebel <anton.gruebel@gmail.com>


## v8.1.0 (2024-10-21)

### Documentation

- Fix code examples regarding outputting
  ([#709](https://github.com/CycloneDX/cyclonedx-python-lib/pull/709),
  [`c72d5f4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c72d5f483d5c1990fe643c4c25e37373d4d3248f))

Signed-off-by: Hakan Dilek <hakandilek@gmail.com>

### Features

- Add support for Lifecycles in BOM metadata
  ([#698](https://github.com/CycloneDX/cyclonedx-python-lib/pull/698),
  [`6cfeb71`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6cfeb711f11aec8fa4d7be885f6797cc2eaa7e67))

---------

Signed-off-by: Johannes Feichtner <johannes@web-wack.at>

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Signed-off-by: Johannes Feichtner <343448+Churro@users.noreply.github.com>

Co-authored-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v8.0.0 (2024-10-14)

### Documentation

- **chaneglog**: Omit chore/ci/refactor/style/test/build
  ([#703](https://github.com/CycloneDX/cyclonedx-python-lib/pull/703),
  [`a210809`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a210809efb34c2dc895fc0c6d96a3412a9097625))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- V8.0.0 ([#665](https://github.com/CycloneDX/cyclonedx-python-lib/pull/665),
  [`002f966`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/002f96630ce8fc6f1766ee6cc92a16b35a821c69))

### BREAKING Changes

* Removed `cyclonedx.mode.ThisTool`, utilize `cyclonedx.builder.this.this_tool()` instead. * Moved
  `cyclonedx.model.Tool` to `cyclonedx.model.tool.Tool`. * Property
  `cyclonedx.mode.bom.BomMetaData.tools` is of type `cyclonedx.model.tool.ToolRepository` now, was
  `SortedSet[cyclonedx.model.Tool]`. The getter will act accordingly; the setter might act in a
  backwards-compatible way. * Property `cyclonedx.mode.vulnerability.Vulnerability.tools` is of type
  `cyclonedx.model.tool.ToolRepository` now, was `SortedSet[cyclonedx.model.Tool]`. The getter will
  act accordingly; the setter might act in a backwards-compatible way. * Constructor
  `cyclonedx.model.license.LicenseExpression()` accepts optional argument `acknowledgement` only as
  key-word argument, no longer as positional argument.

### Changes

* Constructor of `cyclonedx.model.bom.BomMetaData` also accepts an instance of
  `cyclonedx.model.tool.ToolRepository` for argument `tools`. * Constructor of
  `cyclonedx.model.bom.BomMetaData` no longer adds this very library as a tool. Downstream users
  SHOULD add it manually, like
  `my-bom.metadata.tools.components.add(cyclonedx.builder.this.this_component())`.

### Fixes

* Deserialization of CycloneDX that do not include tools in the metadata are no longer unexpectedly
  modified/altered.

### Added

Enabled Metadata Tools representation and serialization in accordance with CycloneDX 1.5

* New class `cyclonedx.model.tool.ToolRepository`. * New function
  `cyclonedx.builder.this.this_component()` -- representation of this very python library as a
  `Component`. * New function `cyclonedx.builder.this.this_tool()` -- representation of this very
  python library as a `Tool`. * New function `cyclonedx.model.tool.Tool.from_component()`.

### Dependencies

* Raised runtime dependency `py-serializable>=1.1.1,<2`, was `>=1.1.0,<2`.

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Signed-off-by: Joshua Kugler <tek30584@adobe.com>

Signed-off-by: semantic-release <semantic-release@bot.local>

Co-authored-by: Joshua Kugler <joshua@azariah.com>

Co-authored-by: semantic-release <semantic-release@bot.local>


## v7.6.2 (2024-10-07)

### Bug Fixes

- Behavior of and typing for crypto setters with optional values
  ([#694](https://github.com/CycloneDX/cyclonedx-python-lib/pull/694),
  [`d8b20bd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d8b20bdc5224ea30cf767f6f3f1a6f8ff2754973))

fixes #690

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Documentation

- Fix some doc strings
  ([`4fa8fc1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4fa8fc1b6703ecf6788b72f2d53c6a17e2146cf7))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.6.1 (2024-09-18)

### Bug Fixes

- File copyright headers ([#676](https://github.com/CycloneDX/cyclonedx-python-lib/pull/676),
  [`35e00b4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/35e00b4ee5a9306b9e97b011025409bcbfcef309))

utilizes flake8 plugin <https://pypi.org/project/flake8-copyright-validator/> to assert the correct
  headers

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.6.0 (2024-08-14)

### Features

- `hashtype.from_composite_str` for Blake2b, SHA3, Blake3
  ([#663](https://github.com/CycloneDX/cyclonedx-python-lib/pull/663),
  [`c59036e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c59036e06ddc97284f82efbbc168dc2d89d090d1))

The code mistreated hashes for Blake2b and SHA3. Code for explicitly handling SHA1 & BLAKE3 was
  added, as those have no variants defined in the CycloneDX specification.

fixes #652

---------

Signed-off-by: Michael Schlenker <michael.schlenker@contact-software.com>

Co-authored-by: Michael Schlenker <michael.schlenker@contact-software.com>

Co-authored-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.5.1 (2024-07-08)

### Bug Fixes

- Xml serialize `normalizedString` and `token` properly
  ([#646](https://github.com/CycloneDX/cyclonedx-python-lib/pull/646),
  [`b40f739`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b40f739206a44f7dbd94042fb5e1a37c047ea024))

fixes #638

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.5.0 (2024-07-04)

### Features

- Add workaround property for v1.5 and v1.6
  ([#642](https://github.com/CycloneDX/cyclonedx-python-lib/pull/642),
  [`b5ebcf8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b5ebcf8104faf57030cbc5d8190c78524ab86431))

Property `workaround` was missing from the vulnerability model. It was added in spec v1.5 and was
  marked as TODO before.

This is my first contribution on this project so if I done something wrong, just say me :smiley:

Signed-off-by: Louis Maillard <louis.maillard@savoirfairelinux.com>

Signed-off-by: Louis Maillard <louis.maillard@protonmail.com>

Co-authored-by: Louis Maillard <louis.maillard@savoirfairelinux.com>


## v7.4.1 (2024-06-12)

### Bug Fixes

- `cyclonedx.model.property.value` value is optional
  ([#631](https://github.com/CycloneDX/cyclonedx-python-lib/pull/631),
  [`ad0f98b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ad0f98b433fd85ba14db6b6288f33d98bc79ee51))

`cyclonedx.model.Property.value` value is optional, in accordance with the spec.

fixes #630

---------

Signed-off-by: Michael Schlenker <michael.schlenker@contact-software.com>

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Co-authored-by: Michael Schlenker <michael.schlenker@contact-software.com>

Co-authored-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Documentation

- Exclude dep bumps from changelog
  ([#627](https://github.com/CycloneDX/cyclonedx-python-lib/pull/627),
  [`60361f7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/60361f781a1b356f24a553e133e0f58a2ad37a7d))

fixes #616

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.4.0 (2024-05-23)

### Documentation

- Ossp best practice percentage
  ([`75f58dc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/75f58dcd41c1495737bff69d354beeeff7660c15))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Updated SPDX license list to `v3.24.0`
  ([#622](https://github.com/CycloneDX/cyclonedx-python-lib/pull/622),
  [`3f9770a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3f9770a95fbe48dfc0cb911a6526690017c2fb37))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.3.4 (2024-05-06)

### Bug Fixes

- Allow suppliers with empty-string names
  ([#611](https://github.com/CycloneDX/cyclonedx-python-lib/pull/611),
  [`b331aeb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b331aeb4b7261c7b1359c592b2dcda27bd35e369))

fixes #600

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.3.3 (2024-05-06)

### Bug Fixes

- Json validation allow arbitrary `$schema` value
  ([#613](https://github.com/CycloneDX/cyclonedx-python-lib/pull/613),
  [`08b7c60`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/08b7c607360b65215d9d29d42ae86e60c6efe49b))

fixes https://github.com/CycloneDX/cyclonedx-python-lib/issues/612

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.3.2 (2024-04-26)

### Bug Fixes

- Properly sort components based on all properties
  ([#599](https://github.com/CycloneDX/cyclonedx-python-lib/pull/599),
  [`8df488c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8df488cb422a6363421fee39714df4e8e8e7a593))

reverts #587 - as this one introduced errors fixes #598 fixes #586

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Signed-off-by: Paul Horton <paul.horton@owasp.org>

Co-authored-by: Paul Horton <paul.horton@owasp.org>


## v7.3.1 (2024-04-22)

### Bug Fixes

- Include all fields of `Component` in `__lt__` function for #586
  ([#587](https://github.com/CycloneDX/cyclonedx-python-lib/pull/587),
  [`d784685`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d7846850d1ad33184d1d58b59fdf41a778d05900))

Fixes #586.

Signed-off-by: Paul Horton <paul.horton@owasp.org>


## v7.3.0 (2024-04-19)

### Features

- License factory set `acknowledgement`
  ([#593](https://github.com/CycloneDX/cyclonedx-python-lib/pull/593),
  [`7ca2455`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7ca2455018d0e191afaaa2fd136a7e4d5b325ec6))

add a parameter to `LicenseFactory.make_*()` methods, to set the `LicenseAcknowledgement`.

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.2.0 (2024-04-19)

### Features

- Disjunctive license acknowledgement
  ([#591](https://github.com/CycloneDX/cyclonedx-python-lib/pull/591),
  [`9bf1839`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9bf1839859a244e790e91c3e1edd82d333598d60))

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v7.1.0 (2024-04-10)

### Documentation

- Missing schema support table & update schema support to reflect version 7.0.0
  ([#584](https://github.com/CycloneDX/cyclonedx-python-lib/pull/584),
  [`d230e67`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d230e67188661a5fb94730e52bf59c11c965c8d7))

Signed-off-by: Paul Horton <paul.horton@owasp.org>

### Features

- Support `bom.properties` for CycloneDX v1.5+
  ([#585](https://github.com/CycloneDX/cyclonedx-python-lib/pull/585),
  [`1d1c45a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1d1c45ac82c7927acc388489228a9b5990f68aa7))

Signed-off-by: Paul Horton <paul.horton@owasp.org>


## v7.0.0 (2024-04-09)

### Features

- Support for CycloneDX v1.6
  ([`8bbdf46`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8bbdf461434ab66673a496a8305c2878bf5c88da))

* added draft v1.6 schemas and boilerplate for v1.6

Signed-off-by: Paul Horton <paul.horton@owasp.org>

* re-generated test snapshots for v1.6

* note `bom.metadata.manufacture` as deprecated

* work on `bom.metadata` for v1.6

* Deprecated `.component.author`. Added `.component.authors` and `.component.manufacturer`

* work to add `.component.omniborid` - but tests deserialisation tests fail due to schema
  differences (`.component.author` not in 1.6)

* work to get deserialization tests passing


## v6.4.4 (2024-03-18)

### Bug Fixes

- Wrong extra name for xml validation
  ([#571](https://github.com/CycloneDX/cyclonedx-python-lib/pull/571),
  [`10e38e2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/10e38e25095de4b2dafbfcd1fd81dce7a9c0f124))

Signed-off-by: Christoph Reiter <reiter.christoph@gmail.com>


## v6.4.3 (2024-03-04)

### Bug Fixes

- Serialization of `model.component.Diff`
  ([#557](https://github.com/CycloneDX/cyclonedx-python-lib/pull/557),
  [`22fa873`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/22fa8734bf1a3a8789ad7578bfa0c86cf0a49d4a))

Fixes #556

---------

Signed-off-by: rcross-lc <151086351+rcross-lc@users.noreply.github.com>

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Co-authored-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v6.4.2 (2024-03-01)

### Build System

- Use poetry v1.8.1 ([#560](https://github.com/CycloneDX/cyclonedx-python-lib/pull/560),
  [`6f81dfa`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6f81dfaed32b76f251647f6291791e714ab158a3))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Documentation

- Exclude internal docs from rendering
  ([#545](https://github.com/CycloneDX/cyclonedx-python-lib/pull/545),
  [`7e55dfe`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7e55dfe213cb2a88b3686f9e8bf93cf4642a2ccd))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Update architecture description and examples
  ([#550](https://github.com/CycloneDX/cyclonedx-python-lib/pull/550),
  [`a19fd28`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a19fd2828355ae031164ef7a0dda2a8ea2365108))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v6.4.1 (2024-01-30)

### Bug Fixes

- `model.bomref` no longer equal to unset peers
  ([#543](https://github.com/CycloneDX/cyclonedx-python-lib/pull/543),
  [`1fd7fee`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1fd7fee9dec888c10087921f2e5a7a60062fb419))

fixes [#539](https://github.com/CycloneDX/cyclonedx-python-lib/issues/539)

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Documentation

- Refactor example
  ([`c1776b7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c1776b718b81cf72ef0c0251504e0d3631e30b17))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Ship docs with `sdist` build ([#544](https://github.com/CycloneDX/cyclonedx-python-lib/pull/544),
  [`52ef01c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/52ef01c99319d5aed950e7f6ef6fcfe731ac8b2f))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v6.4.0 (2024-01-22)

### Documentation

- Add OpenSSF Best Practices shield
  ([#532](https://github.com/CycloneDX/cyclonedx-python-lib/pull/532),
  [`59c4381`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/59c43814b07db0aa881d87192939eb93e79b0cc2))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Support `py-serializable` v1.0
  ([#531](https://github.com/CycloneDX/cyclonedx-python-lib/pull/531),
  [`e1e7277`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e1e72777d8a355c6854f4d9eb26c1e2083c806df))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v6.3.0 (2024-01-06)

### Documentation

- Add `Documentation` url to project meta
  ([`1080b73`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1080b7387a0bbc49a067cd2efefb1545470947e5))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Add `Documentation` url to project meta
  ([`c4288b3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c4288b35e0e1050f0982f7492cfcd3bea34b445c))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Enable dependency `py-serializable 0.17`
  ([#529](https://github.com/CycloneDX/cyclonedx-python-lib/pull/529),
  [`9f24220`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9f24220029cd18cd191f63876899cd86be52dce1))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v6.2.0 (2023-12-31)

### Build System

- Allow additional major-version RC branch patterns
  ([`f8af156`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f8af156c9c38f737b7067722d2a96f8a2a4fcb48))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Documentation

- Buld docs on ubuntu22.04 python311
  ([`b3e9ab7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b3e9ab77696f2ee763f1746f8142bdf471477c39))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Fix typo
  ([`2563996`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/25639967c93ad464e486f2fe6a148b3be439f43d))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Update intro and description
  ([`f0bd05d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f0bd05dc854b5b71421b82cfb527fcb8f41a7c4a))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Allow `lxml` requirement in range of `>=4,<6`
  ([#523](https://github.com/CycloneDX/cyclonedx-python-lib/pull/523),
  [`7d12b9a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7d12b9a9f7a2fdc5e6bb12f891c6f4291e20e65e))

Updates the requirements on [lxml](https://github.com/lxml/lxml) to permit the latest version. -
  [Release notes](https://github.com/lxml/lxml/releases) -
  [Changelog](https://github.com/lxml/lxml/blob/master/CHANGES.txt) -
  [Commits](https://github.com/lxml/lxml/compare/lxml-4.0.0...lxml-5.0.0)

--- updated-dependencies: - dependency-name: lxml dependency-type: direct:production ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v6.1.0 (2023-12-22)

### Features

- Add function to map python `hashlib` algorithms to CycloneDX
  ([#519](https://github.com/CycloneDX/cyclonedx-python-lib/pull/519),
  [`81f8cf5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/81f8cf59b1f40ffbd213789a8b1b621a01e3f631))

new API: `model.HashType.from_hashlib_alg()`

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v6.0.0 (2023-12-10)

### Features

- V6.0.0 ([#492](https://github.com/CycloneDX/cyclonedx-python-lib/pull/492),
  [`74865f8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/74865f8e498c9723c2ce3556ceecb6a3cfc4c490))

### Breaking Changes

* Removed symbols that were already marked as deprecated (via [#493]) * Removed symbols in
  `parser.*` ([#489] via [#495]) * Removed `output.LATEST_SUPPORTED_SCHEMA_VERSION` ([#491] via
  [#494]) * Serialization of unsupported enum values might downgrade/migrate/omit them ([#490] via
  [#496]) Handling might raise warnings if a data loss occurred due to omitting. The result is a
  guaranteed valid XML/JSON, since no (enum-)invalid values are rendered. * Serialization of any
  `model.component.Component` with unsupported `type` raises
  `exception.serialization.SerializationOfUnsupportedComponentTypeException` ([#490] via [#496]) *
  Object `model.bom_ref.BomRef`'s property `value` defaults to `Null`, was arbitrary `UUID` ([#504]
  via [#505]) This change does not affect serialization. All `bom-ref`s are guaranteed to have
  unique values on rendering. * Removed helpers from public API ([#503] via [#506])

### Added

* Basic support for CycloneDX 1.5 ([#404] via [#488]) * No data models were enhanced nor added, yet.
  Pull requests to add functionality are welcome. * Existing enumerable got new cases, to reflect
  features of CycloneDX 1.5 ([#404] via [#488]) * Outputters were enabled to render CycloneDX 1.5
  ([#404] via [#488])

### Tests

* Created (regression/unit/integration/functional) tests for CycloneDX 1.5 ([#404] via [#488]) *
  Created (regression/functional) tests for Enums' handling and completeness ([#490] via [#496])

### Misc

* Bumped dependency `py-serializable@^0.16`, was `@^0.15` (via [#496])

----

### API Changes — the details for migration

* Added new sub-package `exception.serialization` (via [#496]) * Removed class
  `models.ComparableTuple` ([#503] via [#506]) * Enum `model.ExternalReferenceType` got new cases,
  to reflect features for CycloneDX 1.5 ([#404] via [#488]) * Removed function `models.get_now_utc`
  ([#503] via [#506]) * Removed function `models.sha1sum` ([#503] via [#506]) * Enum
  `model.component.ComponentType` got new cases, to reflect features for CycloneDX 1.5 ([#404] via
  [#488]) * Removed `model.component.Component.__init__()`'s deprecated optional kwarg `namespace`
  (via [#493]) Use kwarg `group` instead. * Removed `model.component.Component.__init__()`'s
  deprecated optional kwarg `license_str` (via [#493]) Use kwarg `licenses` instead. * Removed
  deprecated method `model.component.Component.get_namespace()` (via [#493]) * Removed class
  `models.dependency.DependencyDependencies` ([#503] via [#506]) * Removed
  `model.vulnerability.Vulnerability.__init__()`'s deprecated optional kwarg `source_name` (via
  [#493]) Use kwarg `source` instead. * Removed `model.vulnerability.Vulnerability.__init__()`'s
  deprecated optional kwarg `source_url` (via [#493]) Use kwarg `source` instead. * Removed
  `model.vulnerability.Vulnerability.__init__()`'s deprecated optional kwarg `recommendations` (via
  [#493]) Use kwarg `recommendation` instead. * Removed
  `model.vulnerability.VulnerabilityRating.__init__()`'s deprecated optional kwarg `score_base` (via
  [#493]) Use kwarg `score` instead. * Enum `model.vulnerability.VulnerabilityScoreSource` got new
  cases, to reflect features for CycloneDX 1.5 ([#404] via [#488]) * Removed
  `output.LATEST_SUPPORTED_SCHEMA_VERSION` ([#491] via [#494]) * Removed deprecated function
  `output.get_instance()` (via [#493]) Use function `output.make_outputter()` instead. * Added new
  class `output.json.JsonV1Dot5`, to reflect CycloneDX 1.5 ([#404] via [#488]) * Added new item to
  dict `output.json.BY_SCHEMA_VERSION`, to reflect CycloneDX 1.5 ([#404] via [#488]) * Added new
  class `output.xml.XmlV1Dot5`, to reflect CycloneDX 1.5 ([#404] via [#488]) * Added new item to
  dict `output.xml.BY_SCHEMA_VERSION`, to reflect CycloneDX 1.5 ([#404] via [#488]) * Removed class
  `parser.ParserWarning` ([#489] via [#495]) * Removed class `parser.BaseParser` ([#489] via [#495])
  * Enum `schema.SchemaVersion` got new case `V1_5`, to reflect CycloneDX 1.5 ([#404] via [#488])

[#404]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/404 [#488]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/488 [#489]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/489 [#490]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/490 [#491]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/491 [#493]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/493 [#494]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/494 [#495]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/495 [#496]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/496 [#503]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/503 [#504]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/504 [#505]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/505 [#506]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/506

---------

Signed-off-by: Johannes Feichtner <johannes@web-wack.at>

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Signed-off-by: semantic-release <semantic-release>

Co-authored-by: Johannes Feichtner <343448+Churro@users.noreply.github.com>

Co-authored-by: semantic-release <semantic-release>


## v5.2.0 (2023-12-02)

### Documentation

- Keywaords & funding ([#486](https://github.com/CycloneDX/cyclonedx-python-lib/pull/486),
  [`3189e59`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3189e59ff8e3d3d10f7b949b5a08397ff3d3642b))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- `model.xsuri` migrate control characters according to spec
  ([#498](https://github.com/CycloneDX/cyclonedx-python-lib/pull/498),
  [`e490429`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e49042976f8577af4061c34394db270612488cdf))

fixes https://github.com/CycloneDX/cyclonedx-python-lib/issues/497

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v5.1.1 (2023-11-02)

### Bug Fixes

- Update own `externalReferences`
  ([#480](https://github.com/CycloneDX/cyclonedx-python-lib/pull/480),
  [`edb3dde`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/edb3dde889c06755dd1963ed21dd803db3ea0dcc))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v5.1.0 (2023-10-31)

### Documentation

- Advance license docs
  ([`f61a730`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f61a7303de1d5dacf0917a1d66f5ebe0732ccd75))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Guarantee unique `BomRef`s in serialization result
  ([#479](https://github.com/CycloneDX/cyclonedx-python-lib/pull/479),
  [`a648775`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a648775bb5195621e17fdbae92950ab6d56a665a))

Incorporate `output.BomRefDiscriminator` on serialization

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v5.0.1 (2023-10-24)

### Documentation

- Fix RTFD build ([#476](https://github.com/CycloneDX/cyclonedx-python-lib/pull/476),
  [`b9fcfb4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9fcfb40af366fdee7258ccb720e0fad27994824))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Revisit project meta ([#475](https://github.com/CycloneDX/cyclonedx-python-lib/pull/475),
  [`c3254d0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c3254d055f3cda96d2849222a0bba7be8cf486a3))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v5.0.0 (2023-10-24)

### Features

- V5.0.0 ([#440](https://github.com/CycloneDX/cyclonedx-python-lib/pull/440),
  [`26b151c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/26b151cba7d7d484f23ee7888444f09ad6d016b1))

BREAKING CHANGES ---------------- * Dropped support for python<3.8 ([#436] via [#441]; enable
  [#433]) * Reworked license related models, collections, and factories ([#365] via [#466]) *
  Behavior * Method `model.bom.Bom.validate()` will throw
  `exception.LicenseExpressionAlongWithOthersException`, if detecting invalid license constellation
  ([#453] via [#452]) * Fixed tuple comparison when unequal lengths (via [#461]) * API * Enum
  `schema.SchemaVersion` is no longer string-like ([#442] via [#447]) * Enum `schema.OutputVersion`
  is no longer string-like ([#442] via [#447]) * Abstract class `output.BaseOutput` requires
  implementation of new method `output_format` ([#446] via [#447]) * Abstract method
  `output.BaseOutput.output_as_string()` got new optional parameter `indent` ([#437] via [#458]) *
  Abstract method `output.BaseOutput.output_as_string()` accepts arbitrary kwargs (via [#458],
  [#462]) * Removed class `factory.license.LicenseChoiceFactory` (via [#466]) The old functionality
  was integrated into `factory.license.LicenseFactory`. * Method
  `factory.license.LicenseFactory.make_from_string()`'s parameter `name_or_spdx` was renamed to
  `value` (via [#466]) * Method `factory.license.LicenseFactory.make_from_string()`'s return value
  can also be a `LicenseExpression` ([#365] via [#466]) The behavior imitates the old
  `factory.license.LicenseChoiceFactory.make_from_string()` * Renamed class `module.License` to
  `module.license.DisjunctliveLicense` ([#365] via [#466]) * Removed class `module.LicenseChoice`
  ([#365] via [#466]) Use dedicated classes `module.license.DisjunctliveLicense` and
  `module.license.LicenseExpression` instead * All occurrences of `models.LicenseChoice` were
  replaced by `models.licenses.License` ([#365] via [#466]) * All occurrences of
  `SortedSet[LicenseChoice]` were specialized to `models.license.LicenseRepository` ([#365] via
  [#466])

Fixed ---------------- * Serialization of multy-licenses ([#365] via [#466]) * Detect unused
  "dependent" components in `model.bom.validate()` (via [#464])

Changed ---------------- * Updated latest supported list of supported SPDX license identifiers (via
  [#433]) * Shipped schema files are moved to a protected space (via [#433]) These files were never
  intended for public use. * XML output uses a default namespace, which makes results smaller.
  ([#438] via [#458])

Added ---------------- * Support for Python 3.12 (via [#460]) * JSON- & XML-Validators ([#432],
  [#446] via [#433], [#448]) The functionality might require additional dependencies, that can be
  installed with the extra "validation". See the docs in section "Installation" for details. * JSON
  & XML can be generated in a more human-friendly form ([#437], [#438] via [#458]) * Type hints,
  typings & overloads for better integration downstream (via [#463]) * API * New function
  `output.make_outputter()` (via [#469]) This replaces the deprecated function
  `output.get_instance()`. * New sub-package `validation` ([#432], [#446] via [#433], [#448],
  [#469], [#468], [#469]) * New class `exception.MissingOptionalDependencyException` ([#432] via
  [#433]) * New class `exception.LicenseExpressionAlongWithOthersException` ([#453] via [#452]) *
  New dictionaries `output.{json,xml}.BY_SCHEMA_VERSION` ([#446] via [#447]) * Existing
  implementations of class `output.BaseOutput` now have a new method `output_format` ([#446] via
  [#447]) * Existing implementations of method `output.BaseOutput.output_as_string()` got new
  optional parameter `indent` ([#437] via [#458]) * Existing implementations of method
  `output.BaseOutput.output_to_file()` got new optional parameter `indent` ([#437] via [#458]) * New
  method `factory.license.LicenseFactory.make_with_expression()` (via [#466]) * New class
  `model.license.DisjunctiveLicense` ([#365] via [#466]) * New class
  `model.license.LicenseExpression` ([#365] via [#466]) * New class
  `model.license.LicenseRepository` ([#365] via [#466]) * New class
  `serialization.LicenseRepositoryHelper` ([#365] via [#466])

Deprecated ---------------- * Function `output.get_instance()` might be removed, use
  `output.make_outputter()` instead (via [#469])

Tests ---------------- * Added validation tests with official CycloneDX schema test data ([#432] via
  [#433]) * Use proper snapshots, instead of pseudo comparison ([#437] via [#464]) * Added
  regression test for bug [#365] (via [#466], [#467])

Misc ---------------- * Dependencies: bumped `py-serializable@^0.15.0`, was `@^0.11.1` (via [#458],
  [#463], [#464], [#466]) * Style: streamlined quotes and strings (via [#472]) * Chore: bumped
  internal dev- and QA-tools ([#436] via [#441], [#472]) * Chore: added more QA tools to prevent
  common security issues (via [#473])

[#432]: https://github.com/CycloneDX/cyclonedx-python-lib/issues/432 [#433]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/433 [#436]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/436 [#437]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/437 [#365]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/365 [#438]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/438 [#440]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/440 [#441]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/441 [#442]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/442 [#446]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/446 [#447]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/447 [#448]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/448 [#452]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/452 [#453]:
  https://github.com/CycloneDX/cyclonedx-python-lib/issues/453 [#458]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/458 [#460]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/460 [#461]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/461 [#462]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/462 [#463]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/463 [#464]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/464 [#466]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/466 [#467]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/467 [#468]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/468 [#469]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/469 [#472]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/472 [#473]:
  https://github.com/CycloneDX/cyclonedx-python-lib/pull/473

---------

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

Signed-off-by: Jan Kowalleck <jan.kowalleck@owasp.org>

Signed-off-by: semantic-release <semantic-release>

Co-authored-by: semantic-release <semantic-release>


## v4.2.3 (2023-10-16)

### Bug Fixes

- Spdx-expression-validation internal crashes are cought and handled
  ([#471](https://github.com/CycloneDX/cyclonedx-python-lib/pull/471),
  [`5fa66a0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5fa66a043818eb5747dbd630496c6d31f818c0ab))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v4.2.2 (2023-09-14)

### Bug Fixes

- Ship meta files ([#434](https://github.com/CycloneDX/cyclonedx-python-lib/pull/434),
  [`3a1a8a5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3a1a8a5c1cbe8d8989b4cb335269a02b5c6d4f38))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Documentation

- Fix shield in README
  ([`6a941b1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6a941b1ef5cc0f9e956173cce7e9da57e8c6bf22))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- **example**: Showcase `LicenseChoiceFactory`
  ([#428](https://github.com/CycloneDX/cyclonedx-python-lib/pull/428),
  [`c56ec83`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c56ec8395dd203ac41fa6f4c43970a50c0e80efb))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v4.2.1 (2023-09-06)

### Bug Fixes

- `licensechoicefactory.make_from_string()` prioritize SPDX id over expression
  ([#427](https://github.com/CycloneDX/cyclonedx-python-lib/pull/427),
  [`e1bdfdd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e1bdfddcfab97359fbde9f53dc65f56fc8ec4ba9))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v4.2.0 (2023-09-06)

### Features

- Complete SPDX license expression
  ([#425](https://github.com/CycloneDX/cyclonedx-python-lib/pull/425),
  [`e06f9fd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e06f9fd2c30e8976766f326ff216103d2560cb9a))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v4.1.0 (2023-08-27)

### Documentation

- **examples**: Showcase shorthand dependency management
  ([#403](https://github.com/CycloneDX/cyclonedx-python-lib/pull/403),
  [`8b32efb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8b32efb322a3281d58e9f980bb9001b112aa944a))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Features

- Programmatic access to library's version
  ([#417](https://github.com/CycloneDX/cyclonedx-python-lib/pull/417),
  [`3585ea9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3585ea9911ae521e86793ef18f5891289fb0b604))

adds `cyclonedx.__version__`

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v4.0.1 (2023-06-28)

### Bug Fixes

- Conditional warning if no root dependencies were found
  ([#398](https://github.com/CycloneDX/cyclonedx-python-lib/pull/398),
  [`c8175bb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c8175bb6aebac7f129d42d7a5a0ae928212c20cb))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Build System

- Streamlined ci and builds ([#358](https://github.com/CycloneDX/cyclonedx-python-lib/pull/358),
  [`9779af0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9779af02f5f3cd99fe3e1a088f5547f4991b05b7))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Documentation

- Add exaple how to build and serialize
  ([#397](https://github.com/CycloneDX/cyclonedx-python-lib/pull/397),
  [`65e22bd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/65e22bdc6a1a3fc02a6282146bc8fbc17ddb32fa))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- **examples**: Readme ([#399](https://github.com/CycloneDX/cyclonedx-python-lib/pull/399),
  [`1d262ba`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1d262ba57eab0d61b947fc293fc59c6234f19647))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v4.0.0 (2023-03-20)

### Bug Fixes

- Remove `toml` as dependency as not used and seems to be breaking Python 3.11 CI
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

Signed-off-by: Paul Horton <paul.horton@owasp.org>

- Removed `autopep8` in favour of `flake8` as both have conflicting dependencies now
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

Signed-off-by: Paul Horton <paul.horton@owasp.org>

- Removed `setuptools` as dependency
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

- Removed `types-toml` from dependencies - not used
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

Signed-off-by: Paul Horton <paul.horton@owasp.org>

---------

- Update `serializable` to include XML safety changes
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

Signed-off-by: Paul Horton <paul.horton@owasp.org>

### Features

- Add helper method to get URN for a BOM according to
  https://www.iana.org/assignments/urn-formal/cdx
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

- Allow `serial_number` of BOM to be prescribed
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

- Allow `version` of BOM to be defined
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

- Drop Python 3.6 support
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

Signed-off-by: Hakan Dilek <hakandilek@gmail.com>

Signed-off-by: Paul Horton <paul.horton@owasp.org>

Co-authored-by: Hakan Dilek <hakandilek@gmail.com>

Co-authored-by: Hakan Dilek <hakandilek@users.noreply.github.com>

- Officially test and support Python 3.11
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

Signed-off-by: Paul Horton <paul.horton@owasp.org>

* removed unused imports

* bump `poetry` to `1.1.12` in CI

- Release 4.0.0 #341)
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

Highlights of this release include: * Support for De-serialization from JSON and XML to this
  Pythonic Model * Deprecation of Python 3.6 support * Support for Python 3.11 * Support for
  `BomLink` * Support VEX without needing `Component` in the same `Bom` * Support for `services`
  having `dependencies`

BREAKING CHANGE: Large portions of this library have been re-written for this release and many
  methods and contracts have changed.

Signed-off-by: Paul Horton <paul.horton@owasp.org>

- Support for deserialization from JSON and XML
  ([#290](https://github.com/CycloneDX/cyclonedx-python-lib/pull/290),
  [`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

BREAKING CHANGE:

- Support for Python 3.11 ([#349](https://github.com/CycloneDX/cyclonedx-python-lib/pull/349),
  [`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

- Support VEX without Components in the same BOM
  ([`8fb1b14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8fb1b14f5e04e85f21e654c44fa6b9b774867757))

BREAKING CHANGE: Model classes changed to relocated Vulnerability at Bom, not at Component

Signed-off-by: Paul Horton <paul.horton@owasp.org>

### Breaking Changes

- Large portions of this library have been re-written for this release and many methods and
  contracts have changed.


## v3.1.5 (2023-01-12)

### Bug Fixes

- Mak test's schema paths relative to `cyclonedx` package
  ([#338](https://github.com/CycloneDX/cyclonedx-python-lib/pull/338),
  [`1f0c05f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1f0c05fe2b2a22bc84a1a437dd59390f2ceaf986))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v3.1.4 (2023-01-11)

### Bug Fixes

- **tests**: Include tests in `sdist` builds
  ([#337](https://github.com/CycloneDX/cyclonedx-python-lib/pull/337),
  [`936ad7d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/936ad7d0c26d8f98040203d3234ca8f1afbd73ab))

### Features

- Include `tests` in `sdist` builds for #336
  ([#337](https://github.com/CycloneDX/cyclonedx-python-lib/pull/337),
  [`936ad7d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/936ad7d0c26d8f98040203d3234ca8f1afbd73ab))


## v3.1.3 (2023-01-07)

### Bug Fixes

- Serialize dependency graph for nested components
  ([#329](https://github.com/CycloneDX/cyclonedx-python-lib/pull/329),
  [`fb3f835`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fb3f8351881783281f8b7e796098a4c145b35927))

* tests: regression tests for issue #328 fix: for issue #328

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v3.1.2 (2023-01-06)

### Bug Fixes

- Prevent errors on metadata handling for some specification versions
  ([#330](https://github.com/CycloneDX/cyclonedx-python-lib/pull/330),
  [`f08a656`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f08a65649aee750397edc061eb3b8325a69bb4b4))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

### Documentation

- Fix shields ([#324](https://github.com/CycloneDX/cyclonedx-python-lib/pull/324),
  [`555dad4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/555dad4bc255066036ecca028192eb83df8ba5a0))

caused by https://github.com/badges/shields/issues/8671

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Fix typo ([#318](https://github.com/CycloneDX/cyclonedx-python-lib/pull/318),
  [`63bfb87`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/63bfb8772fe78e9842675d17862c456150dbbc15))

Signed-off-by: Roland Weber <rolweber@de.ibm.com>

- Typo
  ([`539b57a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/539b57a00e4e60e239bb26141f219366121e7bc2))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v3.1.1 (2022-11-28)

### Bug Fixes

- Type hint for `get_component_by_purl` is incorrect
  ([`3f20bf0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3f20bf04a65d5c539230281437255b5f48e17621))


## v3.1.0 (2022-09-15)

### Features

- License factories
  ([`033bad2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/033bad2a50fd2236c712d4621caa57b04fcc2043))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Out-factor SPDX compund detection
  ([`fd4d537`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fd4d537c9dced0e38f14d99dee174cc5bb0bd465))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

- Out-factor SPDX compund detection
  ([`2b69925`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2b699252f8857d97231a689ea9cbfcdff9459626))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v2.7.1 (2022-08-01)

### Bug Fixes

- Pinned `mypy <= 0.961` due to #278
  ([`d6955cb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d6955cb86d8da7a72d0146d0dbeb7c34a794a954))

Signed-off-by: Paul Horton <paul.horton@owasp.org>

- Properly support nested `components` and `services` #275
  ([`6597db7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6597db740f222c68ad90f74fb8fdb58b72642adb))

Signed-off-by: Paul Horton <paul.horton@owasp.org>


## v2.7.0 (2022-07-21)

### Features

- Added updated CycloneDX 1.4.2 schemas
  ([`7fb27ae`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7fb27aed58f7de10f8c6b703699bba315af353e7))

Signed-off-by: Paul Horton <paul.horton@owasp.org>

- Support for CycloneDX schema version `1.4.2`
  ([`db7445c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/db7445cd343fc35c6d6fc9f5af3e28cf97a19732))


## v2.6.0 (2022-06-20)

### Features

- Reduce unnessessarry type casting of `set`/`SortedSet`
  ([#203](https://github.com/CycloneDX/cyclonedx-python-lib/pull/203),
  [`089d971`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/089d9714f8f9f8c70076e48baa18340899cc29fa))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v2.5.2 (2022-06-15)

### Bug Fixes

- Add expected lower-than comparators for `OrganizationalEntity` and `VulnerabilityCredits`
  ([#248](https://github.com/CycloneDX/cyclonedx-python-lib/pull/248),
  [`0046ee1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0046ee19547be8dafe5d73bad886b9c5f725f26e))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v2.5.1 (2022-06-10)

### Bug Fixes

- Add missing `Vulnerability` comparator for sorting
  ([#246](https://github.com/CycloneDX/cyclonedx-python-lib/pull/246),
  [`c3f3d0d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c3f3d0d105f0dcf991175040b6d6c2b6e7e25d8f))

Partial fix for #245.

Signed-off-by: Rodney Richardson <rodney.richardson@cambridgeconsultants.com>


## v2.5.0 (2022-06-10)

### Build System

- Move typing to dev-dependencies
  ([`0e2376b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0e2376baade068ae0490b05550837d104e9abfa4))

Move `types-setuptools` and `types-toml` to dev-dependencies (#226)

Signed-off-by: Adam Johnson <me@adamj.eu>

### Documentation

- Fix typo "This is out" -> "This is our"
  ([`ef0278a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ef0278a2044147e73a281c5a59f95049d4af7641))

Fix typo in comments: "This is out" -> "This is our" (#233)

Signed-off-by: Rodney Richardson <rodney.richardson@cambridgeconsultants.com>

### Features

- Use `SortedSet` in model to improve reproducibility - this will provide predictable ordering of
  various items in generated CycloneDX documents - thanks to @RodneyRichardson
  ([`8a1c404`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8a1c4043f502292b32c4ab36a8618cf3f67ac8df))

Signed-off-by: Paul Horton <paul.horton@owasp.org>


## v2.4.0 (2022-05-17)

### Features

- **deps**: Remove unused `typing-extensions` constraints
  ([`2ce358a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2ce358a37e6ce5f06aa9297aed17f8f5bea38e93))

PullRequest and details via #224

Signed-off-by: gruebel <anton.gruebel@gmail.com>


## v2.3.0 (2022-04-20)

### Features

- Add support for Dependency Graph in Model and output serialisation
  ([`ea34513`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ea34513f8229a909007793288ace2f6f51684333))

Signed-off-by: Paul Horton <paul.horton@owasp.org>


## v2.2.0 (2022-04-12)

### Features

- Bump JSON schemas to latest fix verison for 1.2 and 1.3 - see:
  ([`bd6a088`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd6a088d51c995c0f08271f56aedb456c60c1a2e))

- Bump XML schemas to latest fix version for 1.2-1.4 - see:
  ([`bd2e756`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd2e756de15c37b34d2866e8de521556420bd5d3))


## v2.1.1 (2022-04-05)

### Bug Fixes

- `version` being optional in JSON output can raise error
  ([`ba0c82f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba0c82fbde7ba47502c45caf4fa89e9e4381f482))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Prevent error if `version` not set
  ([`b9a84b5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9a84b5b39fe6cb1560764e86f8bd144f2a901e3))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v2.1.0 (2022-03-28)

### Features

- Output errors are verbose
  ([`bfe8fb1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bfe8fb18825251fd9f146458122aa06137ec27c0))

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v2.0.0 (2022-02-21)

### Bug Fixes

- `component.bom_ref` is not Optional in our model implementation (in the schema it is) - we
  generate a UUID if `bom_ref` is not supplied explicitly
  ([`5c954d1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5c954d1e39ce8509ab36e6de7d521927ad3c997c))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- `expression` not supported in Component Licsnes for version 1.0
  ([`15b081b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/15b081bd1891566dbe00e18a8b21d3be87154f72))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- `license_url` not serialised in XML output #179
  ([#180](https://github.com/CycloneDX/cyclonedx-python-lib/pull/180),
  [`f014d7c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f014d7c4411de9ed5e9cb877878ae416d85b2d92))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Components with no version (optional since 1.4) produce invalid BOM output in XML #150
  ([`70d25c8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/70d25c8c162e05a5992761ccddbad617558346d1))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Further fix for #150
  ([`1f55f3e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1f55f3edfeacfc515ef0b5e493c27dd6e14861d6))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Implemented correct `__hash__` methods in models (#153)
  ([#155](https://github.com/CycloneDX/cyclonedx-python-lib/pull/155),
  [`32c0139`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/32c01396251834c69a5b23c82a5554faf8447f61))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Regression introduced by first fix for #150
  ([`c09e396`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c09e396b98c484d1d3d509a5c41746133fe41276))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Resolved #169 (part of #155) ([#172](https://github.com/CycloneDX/cyclonedx-python-lib/pull/172),
  [`a926b34`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a926b34c7facb8b3709936fe00b62a0b80338f31))

- Temporary fix for `__hash__` of Component with `properties` #153
  ([`a51766d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a51766d202c3774003dd7cd8c115b2d9b3da1f50))

Signed-off-by: Paul Horton <phorton@sonatype.com>

### Features

- `bom-ref` for Component and Vulnerability default to a UUID
  ([#142](https://github.com/CycloneDX/cyclonedx-python-lib/pull/142),
  [`b45ff18`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b45ff187056893c5fb294cbf9de854fd130bb7be))

- `bom-ref` for Component and Vulnerability default to a UUID if not supplied ensuring they have a
  unique value #141
  ([`b45ff18`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b45ff187056893c5fb294cbf9de854fd130bb7be))

Signed-off-by: Paul Horton <phorton@sonatype.com>

* doc: updated documentation to reflect change

* patched other tests to support UUID for bom-ref

* better syntax

* 1.3.0

Automatically generated by python-semantic-release

* WIP but a lil hand up for @madpah

Signed-off-by: Jeffry Hesse <5544326+DarthHater@users.noreply.github.com>

- Bump dependencies
  ([`da3f0ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/da3f0ca3e8b90b37301c03f889eb089bca649b09))

BREAKING CHANGE: Adopt PEP-3102

BREAKING CHANGE: Optional Lists are now non-optional Sets

BREAKING CHANGE: Remove concept of DEFAULT schema version - replaced with LATEST schema version

BREAKING CHANGE: Added `BomRef` data type

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Complete support for `bom.components`
  ([#155](https://github.com/CycloneDX/cyclonedx-python-lib/pull/155),
  [`32c0139`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/32c01396251834c69a5b23c82a5554faf8447f61))

- Completed work on #155 ([#172](https://github.com/CycloneDX/cyclonedx-python-lib/pull/172),
  [`a926b34`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a926b34c7facb8b3709936fe00b62a0b80338f31))

- Support complete model for `bom.metadata`
  ([#162](https://github.com/CycloneDX/cyclonedx-python-lib/pull/162),
  [`2938a6c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2938a6c001a5b0b25477241d4ad6601030c55165))

- Support for `bom.externalReferences` in JSON and XML #124
  ([`1b733d7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1b733d75a78e3757010a8049cab5c7d4656dc2a5))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Support services in XML BOMs
  ([`9edf6c9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9edf6c940d20a44f5b99c557392a9fa4532b332e))

### Breaking Changes

- Adopt PEP-3102

- Optional Lists are now non-optional Sets

- Remove concept of DEFAULT schema version - replaced with LATEST schema version

- Added `BomRef` data type


## v1.3.0 (2022-01-24)

### Features

- `bom-ref` for Component and Vulnerability default to a UUID
  ([#142](https://github.com/CycloneDX/cyclonedx-python-lib/pull/142),
  [`3953bb6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3953bb676f423c325ca4d80f3fcee33ad042ad93))

- `bom-ref` for Component and Vulnerability default to a UUID if not supplied ensuring they have a
  unique value #141 ([#142](https://github.com/CycloneDX/cyclonedx-python-lib/pull/142),
  [`3953bb6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3953bb676f423c325ca4d80f3fcee33ad042ad93))

Signed-off-by: Paul Horton <phorton@sonatype.com>

* doc: updated documentation to reflect change

* patched other tests to support UUID for bom-ref

* better syntax


## v1.2.0 (2022-01-24)

### Features

- Add CPE to component ([#138](https://github.com/CycloneDX/cyclonedx-python-lib/pull/138),
  [`269ee15`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/269ee155f203d5771c56edb92f7279466bf2012f))

* Added CPE to component

Setting CPE was missing for component, now it is possible to set CPE and output CPE for a component.

Signed-off-by: Jens Lucius <jens.lucius@de.bosch.com>

* Fixing problems with CPE addition

- Fixed styling errors - Added reference to CPE Spec - Adding CPE parameter as last parameter to not
  break arguments

* Again fixes for Style and CPE reference

Missing in the last commit

* Added CPE as argument before deprecated arguments

* Added testing for CPE addition and error fixing

- Added output tests for CPE in XML and JSON - Fixes style error in components - Fixes order for CPE
  output in XML (CPE has to come before PURL)

* Fixed output tests

CPE was still in the wrong position in one of the tests - fixed

* Fixed minor test fixtures issues

- cpe was still in wrong position in 1.2 JSON - Indentation fixed in 1.4 JSON

* Fixed missing comma in JSON 1.2 test file


## v1.1.1 (2022-01-19)

### Bug Fixes

- Bump dependencies ([#136](https://github.com/CycloneDX/cyclonedx-python-lib/pull/136),
  [`18ec498`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/18ec4987f6aa4a259d30000a19aa6ee1d49681d1))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v1.1.0 (2022-01-13)

### Features

- Add support for `bom.metadata.component`
  ([#118](https://github.com/CycloneDX/cyclonedx-python-lib/pull/118),
  [`1ac31f4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1ac31f4cb14b6c466e092ff38ee2aa472c883c5d))

* Add support for metadata component

Part of #6

Signed-off-by: Artem Smotrakov <asmotrakov@riotgames.com>

* Better docs and simpler ifs


## v1.0.0 (2022-01-13)


## v0.12.3 (2021-12-15)

### Bug Fixes

- Removed requirements-parser as dependency (temp) as not available for Python 3 as Wheel
  ([#98](https://github.com/CycloneDX/cyclonedx-python-lib/pull/98),
  [`3677d9f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3677d9fd584b7c0eb715954bb7b8adc59c0bc9b1))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.12.2 (2021-12-09)

### Bug Fixes

- Tightened dependency `packageurl-python`
  ([#95](https://github.com/CycloneDX/cyclonedx-python-lib/pull/95),
  [`eb4ae5c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/eb4ae5ca8842877b780a755b6611feef847bdb8c))

fixes #94

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v0.12.1 (2021-12-09)

### Bug Fixes

- Further loosened dependency definitions
  ([`8bef6ec`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8bef6ecad36f51a003b266d776c9520d33e06034))

see #44

updated some locked dependencies to latest versions

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>


## v0.12.0 (2021-12-09)

### Bug Fixes

- Typing definitions to be PY 3.6 compatible
  ([`07ebedc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/07ebedcbab1554970496780bb8bf167f6fe4ad5c))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Typing definitions to be PY 3.6 compatible
  ([`07ebedc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/07ebedcbab1554970496780bb8bf167f6fe4ad5c))

Signed-off-by: Paul Horton <phorton@sonatype.com>

* straigtened up `sys.version_info` constraints/code-branches

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

* removed unused type ignores

* try to fix type variants

* typing for py3.6

* fixed invalid unittest

* mypy silence `warn_unused_ignores`

* mypy in tox for lowest version is pinned

Co-authored-by: Paul Horton <phorton@sonatype.com>

- Update conda package parsing to handle `build` containing underscore
  ([#66](https://github.com/CycloneDX/cyclonedx-python-lib/pull/66),
  [`2c6020a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2c6020a208aa1c0fd13ab337db6343ad1d2d5c43))

Signed-off-by: Paul Horton <phorton@sonatype.com>

* updated some typings

### Features

- Loosed dependency versions to make this library more consumable
  ([`55f10fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/55f10fb5524dafa68112c0836806c27bdd74fcbe))

- Lowering minimum dependency versions
  ([`55f10fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/55f10fb5524dafa68112c0836806c27bdd74fcbe))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Lowering minimum dependency versions - importlib-metadata raising minimum to ensure we get a typed
  library
  ([`55f10fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/55f10fb5524dafa68112c0836806c27bdd74fcbe))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Lowering minimum version for importlib-metadata to 3.4.0 with modified import statement
  ([`55f10fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/55f10fb5524dafa68112c0836806c27bdd74fcbe))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.11.1 (2021-11-10)

### Bug Fixes

- Constructor for `Vulnerability` to correctly define `ratings` as optional
  ([`395a0ec`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/395a0ec14ebcba8e0849a0ced30ec4163c42fa7a))

Signed-off-by: William Woodruff <william@trailofbits.com>

- Tested with Python 3.10 ([#64](https://github.com/CycloneDX/cyclonedx-python-lib/pull/64),
  [`385b835`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/385b835f44fadb0f227b6a8ac992b0c73afc6ef0))

Signed-off-by: Paul Horton <phorton@sonatype.com>

* added trove classifier for Python 3.10

- Upgrade Poetry version to workaround issue between Poetry and Python 3.10 (see:
  https://github.com/python-poetry/poetry/issues/4210)
  ([#64](https://github.com/CycloneDX/cyclonedx-python-lib/pull/64),
  [`385b835`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/385b835f44fadb0f227b6a8ac992b0c73afc6ef0))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.11.0 (2021-11-10)

### Features

- Typing & PEP 561
  ([`9144765`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/91447656c0914ceb2af2e4b7282292ec7b93f5bf))

* adde file for type checkers according to PEP 561

Signed-off-by: Jan Kowalleck <jan.kowalleck@gmail.com>

* added static code analysis as a dev-test

* added the "typed" trove

* added `flake8-annotations` to the tests

* added type hints

* further typing updates

Signed-off-by: Paul Horton <phorton@sonatype.com>

* further typing additions and test updates

* further typing

* further typing - added type stubs for toml and setuptools

* typing work

* coding standards

* fixed tox and mypy running in correct python version

* supressed mypy for `cyclonedx.utils.conda.parse_conda_json_to_conda_package`

* fixed type hints

* fixed some typing related flaws

* added flake8-bugbear for code analysis

Co-authored-by: Paul Horton <phorton@sonatype.com>


## v0.10.2 (2021-10-21)

### Bug Fixes

- Correct way to write utf-8 encoded files
  ([`49f9369`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/49f9369b3eba47a3a8d1bcc505546d7dfaf4c5fe))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.10.1 (2021-10-21)

### Bug Fixes

- Ensure output to file is UTF-8
  ([`a10da20`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a10da20865e90e9a0a5bb1e12fba9cfd23970c39))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Ensure output to file is UTF-8
  ([`193bf64`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/193bf64cdb19bf6fb9662367402dcf7eaab8dd1a))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.10.0 (2021-10-20)

### Features

- Add support for Conda
  ([`bd29c78`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bd29c782d39a4956f482b9e4de20d7f829beefba))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.9.1 (2021-10-19)


## v0.9.0 (2021-10-19)

### Bug Fixes

- Missing check for Classifiers in Environment Parser
  ([`b7fa38e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b7fa38e9740bbc5b4c406410df37c3b34818010c))

Signed-off-by: Paul Horton <phorton@sonatype.com>

### Features

- Add support for parsing package licenses when using the `Environment` Parsers
  ([`c414eaf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c414eafde2abaca1005a2a0af6993fcdc17897d3))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.8.3 (2021-10-14)

### Bug Fixes

- Coding standards violations
  ([`00cd1ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/00cd1ca20899b6861b1b959611a3556ffad36832))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Handle `Pipfile.lock` dependencies without an `index` specified
  ([`26c62fb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/26c62fb996c4b1b2bf719e10c9072cf4fbadab9f))


## v0.8.2 (2021-10-14)

### Bug Fixes

- Add namespace and subpath support to Component to complete PackageURL Spec support
  ([`780adeb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/780adebe3861ef08eb1e8817a5e9e3451c0a2137))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.8.1 (2021-10-12)

### Bug Fixes

- Multiple hashes being created for an externalRefernce which is not as required
  ([`970d192`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/970d19202d13d4becbbf040b3a9fb115dd7a0795))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.8.0 (2021-10-12)

### Features

- Add support for `externalReferneces` for `Components` and associated enhancements to parsers to
  obtain information where possible/known
  ([`a152852`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a152852b361bbb7a69c9f7ab61ae7ea6dcffd214))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.7.0 (2021-10-11)

### Features

- Support for pipenv.lock file parsing
  ([`68a2dff`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/68a2dffc770d40f693b6891a580d1f7d8018f71c))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.6.2 (2021-10-11)


## v0.6.1 (2021-10-11)

### Bug Fixes

- Added ability to add tools in addition to this library when generating CycloneDX + plus fixes
  relating to multiple BOM instances
  ([`e03a25c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e03a25c3d2a1a0b711204bb26c7b898eadacdcb0))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Better methods for checking if a Component is already represented in the BOM, and the ability to
  get the existing instance
  ([`5fee85f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5fee85fc38376478a1a438d228c632a5d14f4740))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.6.0 (2021-10-11)

### Features

- Helper method for representing a File as a Component taking into account versioning for files as
  per https://github.com/CycloneDX/cyclonedx.org/issues/34
  ([`7e0fb3c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7e0fb3c7e32e08cb8667ad11461c7f8208dfdf7f))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Support for non-PyPi Components - PackageURL type is now definable when creating a Component
  ([`fde79e0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fde79e02705bce216e62acd05056b6d2046cde22))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.5.0 (2021-10-11)

### Bug Fixes

- Bumped a dependency version
  ([`efc1053`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/efc1053ec9ed3f57711f78f1eca181f7bff0c3bf))

Signed-off-by: Paul Horton <phorton@sonatype.com>

### Build System

- Updated dependencies, moved pdoc3 to a dev dependency
  ([`6a9947d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6a9947de1036b63804352e45c035d40658d3db01))

Signed-off-by: Paul Horton <phorton@sonatype.com>

### Features

- Add support for tool(s) that generated the SBOM
  ([`7d1e6ef`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7d1e6ef04d473407b9b4eefc2ef18e6723838f94))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.4.1 (2021-09-27)

### Bug Fixes

- Improved handling for `requirements.txt` content without pinned or declared versions
  ([`7f318cb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7f318cb495ac1754029088cae1ef2574c58da2e5))

Signed-off-by: Paul Horton <phorton@sonatype.com>

### Build System

- Dependencies updated
  ([`0411826`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/04118263c2fed1241c4a9f38cc256542ba543d50))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.4.0 (2021-09-16)

### Bug Fixes

- Relaxed typing of parameter to be compatible with Python < 3.9
  ([`f9c7990`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f9c7990695119969c5055bc92a233030db999b84))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Remove unused commented out code
  ([`ba4f285`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba4f285fdbe124c28f7ea60310347cf896540125))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Removed print call
  ([`8806553`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/880655304c082a88d94d6d50c64d33ad931cc974))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Removed print call
  ([`d272d2e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d272d2ea7d3331bde0660bdc87a6ac3331ae0720))

Signed-off-by: Paul Horton <phorton@sonatype.com>

### Features

- Helper methods for deriving Severity and SourceType
  ([`6a86ec2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6a86ec27c13ff5e413c5a5f96d9b7671646f9388))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Support for localising vectors (i.e. stripping out any scheme prefix)
  ([`b9e9e17`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9e9e17ba1e2c1c9dfe551c61ad5152eebd829ab))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.3.0 (2021-09-15)

### Features

- Adding support for extension schema that descriptions vulnerability disclosures
  ([`d496695`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d4966951ab6c0229171cfe97723421bb0302c4fc))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.2.0 (2021-09-14)

### Bug Fixes

- Whitespace on empty line removed
  ([`cfc952e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cfc952eb5f3feb97a41b6c895657058429da3430))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.1.0 (2021-09-13)

### Features

- Add poetry support
  ([`f3ac42f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f3ac42f298b8d093b0ac368993beba43c58c251a))

Signed-off-by: Paul Horton <phorton@sonatype.com>

- Added helper method to return a PackageURL object representing a Component
  ([`367bef1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/367bef11bb1a7ede3100acae39581e33d20fa7f5))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.0.11 (2021-09-10)

### Bug Fixes

- **build**: Removed artefacts associtated with non-poetry build
  ([`f9119d4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f9119d49e462cf1f7ccca9c50af2936f8962fd6d))

Tidied up project to remove items associated with non-Poetry build process. Also aligned a few
  references in README to new home of this project under CycloneDX.

Signed-off-by: Paul Horton <phorton@sonatype.com>

- **build**: Test failure and dependency missing
  ([`9a2cfe9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9a2cfe94386b51acca44ae3bacae319b9b3c8f0d))

Fixed failing tests due to dependency on now removed VERSION file Added flake8 officially as a DEV
  dependency to poetry

Signed-off-by: Paul Horton <phorton@sonatype.com>

- **test**: Test was not updated for revised author statement
  ([`d1c9d37`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d1c9d379a1e92ee49aae8d133e2ad3e117054ec9))

Signed-off-by: Paul Horton <phorton@sonatype.com>


## v0.0.10 (2021-09-08)

### Bug Fixes

- Add in pypi badge
  ([`6098c36`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6098c36715b2459d7b04ced5ba6294437576e481))


## v0.0.9 (2021-09-08)


## v0.0.8 (2021-09-08)

### Bug Fixes

- Additional info to poetry, remove circleci
  ([`2fcfa5a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2fcfa5ac3a7d9d7f372be6d69e1c616b551877df))


## v0.0.7 (2021-09-08)

### Bug Fixes

- Initial release to pypi, tell poetry to include cyclonedx package
  ([`a030177`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a030177cb1a370713c4438b13b7520ef6afd19f6))

- Release with full name
  ([`4c620ed`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4c620ed053aac8c31343b1ca84ca56912b762ab2))


## v0.0.6 (2021-09-08)

### Bug Fixes

- Initial release to pypi
  ([`99687db`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/99687dbec1389bf323bb625bfb707306aa3b8d1a))


## v0.0.5 (2021-09-08)


## v0.0.4 (2021-09-08)


## v0.0.3 (2021-09-08)


## v0.0.2 (2021-09-08)
