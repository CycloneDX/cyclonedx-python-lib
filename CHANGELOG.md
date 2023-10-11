# CHANGELOG



## v4.2.2 (2023-09-14)

### Chore

* chore: dont lock poetry (#431)

fixes #430

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`49b144b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/49b144be519705b03adc510ddcc6b9e4504b7a40))

* chore(deps): bump actions/checkout from 3 to 4 (#429)

Bumps [actions/checkout](https://github.com/actions/checkout) from 3 to 4.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/v3...v4)

---
updated-dependencies:
- dependency-name: actions/checkout
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`a70754d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a70754d602e109538c06e06e59f563953c21ab1b))

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

### Chore

* chore(deps): bump python-semantic-release/python-semantic-release (#423)

Bumps [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) from 8.0.7 to 8.0.8.
- [Release notes](https://github.com/python-semantic-release/python-semantic-release/releases)
- [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.md)
- [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v8.0.7...v8.0.8)

---
updated-dependencies:
- dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`13e441d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/13e441d581e2c419b46719148078155d44786e52))

### Feature

* feat: complete SPDX license expression (#425)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`e06f9fd`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e06f9fd2c30e8976766f326ff216103d2560cb9a))


## v4.1.0 (2023-08-27)

### Chore

* chore: migrate to python-semantic-release8 (#421)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`14c501c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/14c501c1133c747e1a7dad6df8cad01a03f71a20))

* chore: migrate to python-semantic-release8 (#420)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`0e35d88`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0e35d88b329bebe05f19748a23a31abf6295c933))

* chore: migrate to python-semantic-release8 (#419)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`adf5a36`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/adf5a3668c7c9aa3e0478fd1eabf3b3163fae691))

* chore(deps-dev): bump distlib from 0.3.6 to 0.3.7 (#412)

Bumps [distlib](https://github.com/pypa/distlib) from 0.3.6 to 0.3.7.
- [Release notes](https://github.com/pypa/distlib/releases)
- [Changelog](https://github.com/pypa/distlib/blob/master/CHANGES.rst)
- [Commits](https://github.com/pypa/distlib/compare/0.3.6...0.3.7)

---
updated-dependencies:
- dependency-name: distlib
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`bc9f01d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bc9f01dd90688ef57f755d1b8ca5c5f7739d9d5d))

* chore(deps-dev): bump pluggy from 1.0.0 to 1.2.0 (#413)

Bumps [pluggy](https://github.com/pytest-dev/pluggy) from 1.0.0 to 1.2.0.
- [Changelog](https://github.com/pytest-dev/pluggy/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pytest-dev/pluggy/compare/1.0.0...1.2.0)

---
updated-dependencies:
- dependency-name: pluggy
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`be8af3e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/be8af3e950d3908179e0f194132222bd04310c36))

* chore(deps-dev): bump typed-ast from 1.5.4 to 1.5.5 (#411)

Bumps [typed-ast](https://github.com/python/typed_ast) from 1.5.4 to 1.5.5.
- [Changelog](https://github.com/python/typed_ast/blob/master/release_process.md)
- [Commits](https://github.com/python/typed_ast/compare/1.5.4...1.5.5)

---
updated-dependencies:
- dependency-name: typed-ast
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`75302b1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/75302b1de9ad9245327fa3b09181c7ff381fefe8))

* chore(deps-dev): bump lxml from 4.9.2 to 4.9.3 (#405)

Bumps [lxml](https://github.com/lxml/lxml) from 4.9.2 to 4.9.3.
- [Release notes](https://github.com/lxml/lxml/releases)
- [Changelog](https://github.com/lxml/lxml/blob/master/CHANGES.txt)
- [Commits](https://github.com/lxml/lxml/compare/lxml-4.9.2...lxml-4.9.3)

---
updated-dependencies:
- dependency-name: lxml
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`6aa057b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6aa057bb2f0e3804e57b799fd9c3f969fb328fb7))

* chore(deps-dev): bump mypy from 1.4.0 to 1.4.1 (#400)

Bumps [mypy](https://github.com/python/mypy) from 1.4.0 to 1.4.1.
- [Commits](https://github.com/python/mypy/compare/v1.4.0...v1.4.1)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`54d6a1a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/54d6a1a676d0d9715acd0d9275410b95bd9b82cf))

### Ci

* ci: streamline concurrency for deploy (#406)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`6a7ddfa`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6a7ddfa635995f5dbb849ba5141dcb19a70db0ea))

* ci: run examples on prod-deps only (#402)

* ci: run examples on prod-deps only

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* ci: simplify ci

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`cf40048`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cf40048f00d4d9a70306ee414ebf5a1f970c6a70))

* ci: run examples (#401)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`058f386`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/058f38609453ec738d9cdaa01cbed1b22066cc77))

### Documentation

* docs(examples): showcase shorthand dependency management (#403)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8b32efb`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8b32efb322a3281d58e9f980bb9001b112aa944a))

### Feature

* feat: programmatic access to library&#39;s version (#417)

adds `cyclonedx.__version__`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3585ea9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3585ea9911ae521e86793ef18f5891289fb0b604))


## v4.0.1 (2023-06-28)

### Chore

* chore(deps): bump python-semantic-release/python-semantic-release (#393)

Bumps [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) from 7.33.2 to 7.34.6.
- [Release notes](https://github.com/python-semantic-release/python-semantic-release/releases)
- [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.md)
- [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v7.33.2...v7.34.6)

---
updated-dependencies:
- dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`2180d31`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2180d31e21736f535745878d2459ba6603b2b0d3))

* chore(deps-dev): bump mypy from 1.3.0 to 1.4.0 (#395)

* chore(deps-dev): bump mypy from 1.3.0 to 1.4.0

Bumps [mypy](https://github.com/python/mypy) from 1.3.0 to 1.4.0.
- [Commits](https://github.com/python/mypy/compare/v1.3.0...v1.4.0)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

* style: ignore type confusion

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

---------

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`ab36db4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ab36db4a77e4a343f8699726c438e5b5233badbe))

* chore(deps): bump filelock from 3.10.7 to 3.12.2 (#394)

Bumps [filelock](https://github.com/tox-dev/py-filelock) from 3.10.7 to 3.12.2.
- [Release notes](https://github.com/tox-dev/py-filelock/releases)
- [Changelog](https://github.com/tox-dev/py-filelock/blob/main/docs/changelog.rst)
- [Commits](https://github.com/tox-dev/py-filelock/compare/3.10.7...3.12.2)

---
updated-dependencies:
- dependency-name: filelock
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`90b339b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/90b339b34c3afeb11d1044d9dd3fcb3feea47327))

* chore(deps-dev): bump coverage from 7.2.6 to 7.2.7 (#390)

Bumps [coverage](https://github.com/nedbat/coveragepy) from 7.2.6 to 7.2.7.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/7.2.6...7.2.7)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`638d472`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/638d472d474f286c3adff6e35b5ea354ef140153))

* chore(deps-dev): bump xmldiff from 2.6.1 to 2.6.3 (#388)

Bumps [xmldiff](https://github.com/Shoobx/xmldiff) from 2.6.1 to 2.6.3.
- [Release notes](https://github.com/Shoobx/xmldiff/releases)
- [Changelog](https://github.com/Shoobx/xmldiff/blob/master/CHANGES.rst)
- [Commits](https://github.com/Shoobx/xmldiff/compare/2.6.1...2.6.3)

---
updated-dependencies:
- dependency-name: xmldiff
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`b5fa67c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b5fa67c50216029af16d0643d6032e4a8bcde5e4))

* chore(deps-dev): bump coverage from 7.2.5 to 7.2.6 (#387)

Bumps [coverage](https://github.com/nedbat/coveragepy) from 7.2.5 to 7.2.6.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/7.2.5...7.2.6)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`c49c320`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c49c3203b3afc41e44355b403c2b495a322e4d8a))

* chore(deps-dev): bump mypy from 1.2.0 to 1.3.0 (#385)

Bumps [mypy](https://github.com/python/mypy) from 1.2.0 to 1.3.0.
- [Commits](https://github.com/python/mypy/compare/v1.2.0...v1.3.0)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`bb6d8bc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bb6d8bcdec1c10ca143396818d7605cc2f3277a6))

* chore(deps-dev): bump xmldiff from 2.5 to 2.6.1 (#375)

Bumps [xmldiff](https://github.com/Shoobx/xmldiff) from 2.5 to 2.6.1.
- [Release notes](https://github.com/Shoobx/xmldiff/releases)
- [Changelog](https://github.com/Shoobx/xmldiff/blob/master/CHANGES.rst)
- [Commits](https://github.com/Shoobx/xmldiff/compare/2.5...2.6.1)

---
updated-dependencies:
- dependency-name: xmldiff
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`27b9ec5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/27b9ec57a48bcb0c29499df8e915b956c7b06b50))

* chore(deps-dev): bump mypy from 1.1.1 to 1.2.0 (#372)

Bumps [mypy](https://github.com/python/mypy) from 1.1.1 to 1.2.0.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v1.1.1...v1.2.0)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`5e5a8c2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5e5a8c25979dc0769048d36abba5b1623b797f2e))

* chore(deps-dev): bump coverage from 7.2.2 to 7.2.5 (#383)

Bumps [coverage](https://github.com/nedbat/coveragepy) from 7.2.2 to 7.2.5.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/7.2.2...7.2.5)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`b288d94`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b288d9406ff592c1f12be82746ccf7fd527413d7))

* chore(deps): update poetry and other dependency versions (#369)

* update packageurl type hints

Signed-off-by: gruebel &lt;anton.gruebel@gmail.com&gt;

* lower bound packageurl-python dependency

Signed-off-by: gruebel &lt;anton.gruebel@gmail.com&gt;

* update deps.lowest.r

Signed-off-by: gruebel &lt;anton.gruebel@gmail.com&gt;

---------

Signed-off-by: gruebel &lt;anton.gruebel@gmail.com&gt; ([`aa5b936`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/aa5b936f17c5a9840a0f436b8d4540439cf4c0a5))

* chore: CI/QA/Build meintenance (#358)

* build: streamlined ci and builds

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* chore: upgrade lockfile with poetry1.4

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* removed extra brace

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* fixed long line

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;
Co-authored-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`9779af0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9779af02f5f3cd99fe3e1a088f5547f4991b05b7))

* chore: followup of #340 (#360)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`723ae8e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/723ae8e4ddbffc4851c10f64692e7265973ef730))

* chore: prevent dev-lowest-lockfile from dependency bumps (#359)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`16870f4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/16870f4119865b549172cc76588ca1aa7ce00357))

* chore: manually craft more accurate CHANGELOG for `4.0.0`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`32ce3a2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/32ce3a2ca018b8afcfcb101cad8fac80c547ddc5))

### Ci

* ci: cannot use variables in `uses`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`2371a1b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2371a1bdc39c85ee65e43ac8bb22cae1b199385e))

* ci: cannot use variables in `uses`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`aa0eab1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/aa0eab134c85e7501134f8a417c34e430abc7101))

* ci: add concurrency rules (#361)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`f65d646`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f65d64699a48bd6fe540c7503491ce29b1ce38d1))

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

### Chore

* chore(deps): bump relekang/python-semantic-release from 7.31.2 to 7.33.1 (#345)

Bumps [relekang/python-semantic-release](https://github.com/relekang/python-semantic-release) from 7.31.2 to 7.33.1.
- [Release notes](https://github.com/relekang/python-semantic-release/releases)
- [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.md)
- [Commits](https://github.com/relekang/python-semantic-release/compare/v7.31.2...v7.33.1)

---
updated-dependencies:
- dependency-name: relekang/python-semantic-release
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`a011d89`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a011d89ce6cee9e56bcfcc9a9338fa1e559721f7))

* chore: package manifest fix link to homepage and documentation (#291)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`f2350b4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f2350b4e2b0fb7668ca987e523c53acb6ac6fefb))

### Feature

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

### Chore

* chore: do not ship exra LICENSE file (#339)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b7f1028`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b7f1028156de8d1e14a391d84d24aa697814902a))

### Fix

* fix: mak test&#39;s schema paths relative to `cyclonedx` package (#338)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`1f0c05f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1f0c05fe2b2a22bc84a1a437dd59390f2ceaf986))

### Unknown

* 3.1.5

Automatically generated by python-semantic-release ([`ba603cf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba603cf96fad51a85d5159e83c402d613fefbb7c))


## v3.1.4 (2023-01-11)

### Chore

* chore: add Jan Kowalleck as a maintainer

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7aae26d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7aae26d09c8c0d6976f10d94c2bfbd4cb8f11a0b))

### Fix

* fix(tests): include tests in `sdist` builds (#337)

* feat: include `tests` in `sdist` builds for #336 
* delete unexpected `DS_Store` file

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`936ad7d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/936ad7d0c26d8f98040203d3234ca8f1afbd73ab))

### Test

* test: mock `ThisTool.version` for constisten results (#335)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`57a9e5e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/57a9e5e4f5b1eb785984be9d5a35aac60315232d))

### Unknown

* 3.1.4

Automatically generated by python-semantic-release ([`0b19294`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0b19294e4820f0da5e81decd4d902ef7789ecb61))


## v3.1.3 (2023-01-07)

### Fix

* fix: serialize dependency graph for nested components (#329)

* tests: regression tests for issue #328
* fix: for issue #328

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`fb3f835`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fb3f8351881783281f8b7e796098a4c145b35927))

### Test

* test: tidy up test beds (#333)

* test: consolidate imports
* test: recreate all fixtures
* test: docs

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`ab862e7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ab862e79b72b808693e2ec7f6fe1fa3e99cae011))

### Unknown

* 3.1.3

Automatically generated by python-semantic-release ([`11a420c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/11a420c5fc38bb48d2a91713cc74574acb131184))


## v3.1.2 (2023-01-06)

### Chore

* chore(deps): bump Gr1N/setup-poetry from 7 to 8 (#326)

Bumps [Gr1N/setup-poetry](https://github.com/Gr1N/setup-poetry) from 7 to 8.
- [Release notes](https://github.com/Gr1N/setup-poetry/releases)
- [Commits](https://github.com/Gr1N/setup-poetry/compare/v7...v8)

---
updated-dependencies:
- dependency-name: Gr1N/setup-poetry
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`f3af229`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f3af22979978f0c38c4c8f48b4271ee6a6c1e1bd))

* chore: editorconfig

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8c75b1b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8c75b1ba63c10929c005ea27ebb6f63afa8b9719))

### Ci

* ci: fix py36 (#320)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`cf9f790`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/cf9f790e30f5b430ea1ece8916b54323e1cdb5ee))

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

### Style

* style: split joined path segments (#331)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`493104c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/493104c1bccc669ee55b89a2c360268d36f3f1b7))

### Unknown

* 3.1.2

Automatically generated by python-semantic-release ([`0853d14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0853d14780b8e44e9b285bee2ac6b81551640c5f))

* clarify sign-off step (#319)


Signed-off-by: Roland Weber &lt;rolweber@de.ibm.com&gt; ([`007fb96`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/007fb96a1ec23b9516bc383afa85b3efc2707aa8))


## v3.1.1 (2022-11-28)

### Chore

* chore: CHANGELOG typos ([`6c0c174`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6c0c1742d2ea19dfc0284785cf9597b43ef05979))

* chore: update CHANGELOG to explain jump from `2.7.1` to `3.1.0`. ([`1b8cd12`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1b8cd12b03adb03451ed8ee4562161bd82a18972))

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

### Chore

* chore: fix release workflow ([`5863622`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/586362272af3f5fd7a11c1c65502bca31d8813eb))

* chore: fix poetry in tox

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7f8c668`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7f8c668cf152af554dbc5183f275723cd3d472b2))

### Feature

* feat: out-factor SPDX compund detection

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`fd4d537`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fd4d537c9dced0e38f14d99dee174cc5bb0bd465))

* feat: out-factor SPDX compund detection

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`2b69925`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/2b699252f8857d97231a689ea9cbfcdff9459626))

* feat: license factories

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`033bad2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/033bad2a50fd2236c712d4621caa57b04fcc2043))

### Test

* test: license factories

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`baf83f9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/baf83f9aebe4cdf38341c2432bf8a97e74db5105))

### Unknown

* 3.1.0

Automatically generated by python-semantic-release ([`e52c174`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e52c17447b1520103ccb24192ab92560429df595))

* Merge pull request #305 from CycloneDX/license-factories

feat: add license factories to more easily support creation of `License` or `LicenseChoice` from SPDX license strings #304 ([`5ff4494`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5ff4494b0e0d76d04cf8a4245ce0426f0abbd8f9))

* tests: refactor tests

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3644f13`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3644f1357ae6b0e1f84e442cd6d9a045fc26fbce))

* tests: rebase/fixup poetry lock

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`26817c0`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/26817c0089bfd4083ecfb5ce85039c8d75b84606))

* Merge pull request #301 from CycloneDX/fix-poetry-in-tox

chore: fix poetry in tox ([`92aea8d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/92aea8d3413cd2af820cc8160ef48a737951b0ea))

* remove v3 from CHANGELOG #286 (#287)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7029721`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/702972105364a3ab225ea5a586c48cec664601ca))

* 3.0.0

Automatically generated by python-semantic-release ([`69582ff`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/69582ff7a9e3a1cfb2c7193c3d194d69e35899c1))


## v2.7.1 (2022-08-01)

### Chore

* chore: manual fix release publication `2.7.1`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`b569548`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b56954840ada89c0ba63b4be16e099cd74cc001d))

* chore(deps-dev): bump flake8-isort from 4.1.1 to 4.1.2.post0 (#280)

Bumps [flake8-isort](https://github.com/gforcada/flake8-isort) from 4.1.1 to 4.1.2.post0.
- [Release notes](https://github.com/gforcada/flake8-isort/releases)
- [Changelog](https://github.com/gforcada/flake8-isort/blob/master/CHANGES.rst)
- [Commits](https://github.com/gforcada/flake8-isort/compare/4.1.1...4.1.2.post0)

---
updated-dependencies:
- dependency-name: flake8-isort
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`01cb53b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/01cb53b9a29f0dfa35b57d4ac0ac56f2d8778f0a))

* chore: resolve hang issue with running isort as pre-commit hook

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`fb25b70`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fb25b70c0a3b5a5855332e1c5371219b97beb181))

* chore: re-added `isort` to pre-commit hooks
ran isort

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`051e543`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/051e5436fc5d317286d0d25c8987cf236d20af08))

### Ci

* ci: change pinned version of python-semantic-release as preventing automated releases

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`6e12be7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6e12be70fb2a71de60428155b4d0ae82fa43ef2d))

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

### Chore

* chore(deps): bump virtualenv from 20.15.0 to 20.15.1 (#255)

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.15.0 to 20.15.1.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.15.0...20.15.1)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`d720a5f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d720a5fed662eaf19657d5a2d3f46a9b386d13de))

* chore(deps-dev): bump flake8-bugbear from 22.6.22 to 22.7.1 (#259)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.6.22 to 22.7.1.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.6.22...22.7.1)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`1175f60`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1175f603f863bbcdb3d49dd84c66a25a5826c6ea))

* chore(deps-dev): bump jsonschema from 4.6.0 to 4.6.1 (#258)

Bumps [jsonschema](https://github.com/python-jsonschema/jsonschema) from 4.6.0 to 4.6.1.
- [Release notes](https://github.com/python-jsonschema/jsonschema/releases)
- [Changelog](https://github.com/python-jsonschema/jsonschema/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/python-jsonschema/jsonschema/compare/v4.6.0...v4.6.1)

---
updated-dependencies:
- dependency-name: jsonschema
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`ddbfabc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ddbfabce2487f21ef204674dc5bd8de70c8fd204))

* chore(deps-dev): bump lxml from 4.9.0 to 4.9.1 (#257)

Bumps [lxml](https://github.com/lxml/lxml) from 4.9.0 to 4.9.1.
- [Release notes](https://github.com/lxml/lxml/releases)
- [Changelog](https://github.com/lxml/lxml/blob/master/CHANGES.txt)
- [Commits](https://github.com/lxml/lxml/compare/lxml-4.9.0...lxml-4.9.1)

---
updated-dependencies:
- dependency-name: lxml
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`f045b7f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f045b7ffcf318652dd8a13b7fe5c61f3b4d81a7b))

* chore(deps): bump virtualenv from 20.14.1 to 20.15.0 (#251)

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.14.1 to 20.15.0.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.14.1...20.15.0)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`70270a9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/70270a97b481d976eea82bd3c35bbb5055104234))

* chore(deps-dev): bump flake8-bugbear from 22.4.25 to 22.6.22 (#252)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.4.25 to 22.6.22.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.4.25...22.6.22)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`c957226`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c957226543b43631d247f3417621668cc824232a))

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

### Chore

* chore(deps): bump colorama from 0.4.4 to 0.4.5 (#249)

Bumps [colorama](https://github.com/tartley/colorama) from 0.4.4 to 0.4.5.
- [Release notes](https://github.com/tartley/colorama/releases)
- [Changelog](https://github.com/tartley/colorama/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/tartley/colorama/compare/0.4.4...0.4.5)

---
updated-dependencies:
- dependency-name: colorama
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`39637ad`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/39637ade2668003c3bf7c22cf40c72bae324d8c1))

### Feature

* feat: reduce unnessessarry type casting of `set`/`SortedSet` (#203)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`089d971`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/089d9714f8f9f8c70076e48baa18340899cc29fa))

### Unknown

* 2.6.0

Automatically generated by python-semantic-release ([`8481e9b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8481e9bd8dc5196c2e703e5cd19974bb22bc270e))


## v2.5.2 (2022-06-15)

### Chore

* chore(deps): bump actions/setup-python from 3 to 4 (#247)

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 3 to 4.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v3...v4)

---
updated-dependencies:
- dependency-name: actions/setup-python
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`ddd0144`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ddd01446e5fe201bfb0cebeee3c4afb25f54223b))

### Fix

* fix: add expected lower-than comparators for `OrganizationalEntity` and `VulnerabilityCredits` (#248)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`0046ee1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0046ee19547be8dafe5d73bad886b9c5f725f26e))

### Unknown

* 2.5.2

Automatically generated by python-semantic-release ([`fb9a796`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fb9a796d0b34c2d930503790c74d6d7ed5e3c3d6))


## v2.5.1 (2022-06-10)

### Chore

* chore(deps-dev): bump mypy from 0.960 to 0.961 (#244)

Bumps [mypy](https://github.com/python/mypy) from 0.960 to 0.961.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.960...v0.961)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`48ea951`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/48ea951c92f0b944e5aae2cd1cfd299b02fb4322))

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

### Chore

* chore(deps-dev): bump jsonschema from 4.5.1 to 4.6.0 (#242)

Bumps [jsonschema](https://github.com/python-jsonschema/jsonschema) from 4.5.1 to 4.6.0.
- [Release notes](https://github.com/python-jsonschema/jsonschema/releases)
- [Changelog](https://github.com/python-jsonschema/jsonschema/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/python-jsonschema/jsonschema/compare/v4.5.1...v4.6.0)

---
updated-dependencies:
- dependency-name: jsonschema
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`32af991`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/32af991c8f69c7f9f2f06b68c014bc7af0498d5d))

* chore(deps-dev): bump lxml from 4.8.0 to 4.9.0 (#241)

Bumps [lxml](https://github.com/lxml/lxml) from 4.8.0 to 4.9.0.
- [Release notes](https://github.com/lxml/lxml/releases)
- [Changelog](https://github.com/lxml/lxml/blob/master/CHANGES.txt)
- [Commits](https://github.com/lxml/lxml/compare/lxml-4.8.0...lxml-4.9.0)

---
updated-dependencies:
- dependency-name: lxml
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`6d5189e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6d5189e4612126a2fcc72ffe77857ab6fbea25bc))

* chore(deps-dev): bump mypy from 0.942 to 0.960 (#230)

Bumps [mypy](https://github.com/python/mypy) from 0.942 to 0.960.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.942...v0.960)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`88d9d8b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/88d9d8b7ff18f495a0767e3ed9f37783030ca45d))

* chore(deps): bump types-setuptools from 57.4.12 to 57.4.17 (#238)

Bumps [types-setuptools](https://github.com/python/typeshed) from 57.4.12 to 57.4.17.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-setuptools
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`3d011ab`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3d011ab8f46a3486e1f0dc2a4bb099f7e68f31dd))

* chore(deps): bump types-setuptools from 57.4.12 to 57.4.17 (#237)

Bumps [types-setuptools](https://github.com/python/typeshed) from 57.4.12 to 57.4.17.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-setuptools
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`a1d1bae`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a1d1bae1e5a1e3fdabba3082b3f1a94e3265312d))

* chore(deps): bump typed-ast from 1.5.2 to 1.5.4 (#232)

Bumps [typed-ast](https://github.com/python/typed_ast) from 1.5.2 to 1.5.4.
- [Release notes](https://github.com/python/typed_ast/releases)
- [Changelog](https://github.com/python/typed_ast/blob/master/release_process.md)
- [Commits](https://github.com/python/typed_ast/compare/1.5.2...1.5.4)

---
updated-dependencies:
- dependency-name: typed-ast
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`866f9ac`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/866f9ac4e4f270fd24b04766aa0082dac6116359))

* chore(deps-dev): bump jsonschema from 4.4.0 to 4.5.1 (#221)

Bumps [jsonschema](https://github.com/python-jsonschema/jsonschema) from 4.4.0 to 4.5.1.
- [Release notes](https://github.com/python-jsonschema/jsonschema/releases)
- [Changelog](https://github.com/python-jsonschema/jsonschema/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/python-jsonschema/jsonschema/compare/v4.4.0...v4.5.1)

---
updated-dependencies:
- dependency-name: jsonschema
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`c65ce28`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c65ce284d602b9218464cc8b2cfbcff6b13aa910))

### Ci

* ci: fix run with lowest compat dependencies (#240)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a4596c8`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a4596c8023553a15e33b45e84142e4ef27591b6a))

* ci: pin GH-action `semantic-release` to v7.28.1 (#234)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`91e1297`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/91e12971bf90fffb5b440b2acc74a3f8614932bd))

### Documentation

* docs: fix typo  &#34;This is out&#34; -&gt; &#34;This is our&#34;

Fix typo in comments: &#34;This is out&#34; -&gt; &#34;This is our&#34; (#233)

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`ef0278a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ef0278a2044147e73a281c5a59f95049d4af7641))

### Feature

* feat: use `SortedSet` in model to improve reproducibility - this will provide predictable ordering of various items in generated CycloneDX documents - thanks to @RodneyRichardson

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`8a1c404`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8a1c4043f502292b32c4ab36a8618cf3f67ac8df))

### Test

* test: tests calculate versions if needed 

Don&#39;t hardcode component version in test (#229)

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`7b3ce65`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/7b3ce65f92ff6009a1e29d4938eac5ea664b2538))

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

### Chore

* chore(deps): bump virtualenv from 20.14.0 to 20.14.1 (#208)

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.14.0 to 20.14.1.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.14.0...20.14.1)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`04f3671`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/04f3671de036b340faf18170603fad32095771cb))

* chore(deps-dev): bump tox from 3.24.5 to 3.25.0 (#209)

Bumps [tox](https://github.com/tox-dev/tox) from 3.24.5 to 3.25.0.
- [Release notes](https://github.com/tox-dev/tox/releases)
- [Changelog](https://github.com/tox-dev/tox/blob/master/docs/changelog.rst)
- [Commits](https://github.com/tox-dev/tox/compare/3.24.5...3.25.0)

---
updated-dependencies:
- dependency-name: tox
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`8eee5d3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8eee5d354c3ee640bbc773d315f1c17e1a8334fd))

* chore(deps): bump types-toml from 0.10.4 to 0.10.7 (#222)

Bumps [types-toml](https://github.com/python/typeshed) from 0.10.4 to 0.10.7.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-toml
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`5d19805`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5d19805c4e0568d4fc0894ed0b9d7cb3b99e219b))

* chore(deps-dev): bump flake8-bugbear from 22.3.23 to 22.4.25 (#220)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.3.23 to 22.4.25.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.3.23...22.4.25)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`de7f4aa`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/de7f4aae0378c6475d65ac9ec2303155d4062591))

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

### Chore

* chore(deps): bump actions/upload-artifact from 2 to 3 (#204)

Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 2 to 3.
- [Release notes](https://github.com/actions/upload-artifact/releases)
- [Commits](https://github.com/actions/upload-artifact/compare/v2...v3)

---
updated-dependencies:
- dependency-name: actions/upload-artifact
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`dad8538`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/dad8538797352e1f2d0bb322b2df007370da19be))

* chore(deps): bump types-setuptools from 57.4.11 to 57.4.12 (#205)

Bumps [types-setuptools](https://github.com/python/typeshed) from 57.4.11 to 57.4.12.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-setuptools
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`eae598a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/eae598adca14eaa7125ab8bc6a2af4b213cdbd5c))

### Ci

* ci: introduce `timeout-minutes` and drop `dependabot` branches for CI #206

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`e5b426f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e5b426f0287e75f8c9c2b0937cebaab13dc069a5))

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

### Chore

* chore: shield icons in README ([`87c490e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/87c490e883f1c68a96233ca6d83e641481fb83a4))

### Fix

* fix: prevent error if `version` not set

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`b9a84b5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b9a84b5b39fe6cb1560764e86f8bd144f2a901e3))

### Unknown

* 2.1.1

Automatically generated by python-semantic-release ([`f78d608`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f78d6081abc1a8adb80ef0c79a07c624ad9e3a5c))

* Merge pull request #194 from CycloneDX/fix/json-output-version-optional-bug-193

fix: `version` being optional in JSON output can raise error ([`6f7e09a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6f7e09aa4d05a4a2dc60569732f6b2ae5582a154))


## v2.1.0 (2022-03-28)

### Chore

* chore(deps): bump virtualenv from 20.13.4 to 20.14.0 (#200)

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.13.4 to 20.14.0.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.13.4...20.14.0)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`6ccb637`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6ccb63789fdc49c2b0b7f1349f4a4f168951ed73))

* chore(deps-dev): bump mypy from 0.941 to 0.942 (#199)

Bumps [mypy](https://github.com/python/mypy) from 0.941 to 0.942.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.941...v0.942)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`51dadb9`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/51dadb9ded4a49a9ad6e22dd689cbfbbe04547aa))

* chore(deps-dev): bump flake8-bugbear from 22.1.11 to 22.3.23 (#201)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.1.11 to 22.3.23.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.1.11...22.3.23)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`4f9f169`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4f9f1693950caecdd6b01c25c2b47c7940f703b5))

* chore(deps): bump types-setuptools from 57.4.10 to 57.4.11 (#197)

Bumps [types-setuptools](https://github.com/python/typeshed) from 57.4.10 to 57.4.11.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-setuptools
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`8f4db6b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8f4db6b99b1213949c69605019e468ca9598a8e0))

* chore(deps-dev): bump mypy from 0.940 to 0.941 (#195)

Bumps [mypy](https://github.com/python/mypy) from 0.940 to 0.941.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.940...v0.941)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`8012c29`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8012c299634537340a061e9b1b3ad60071fd7c13))

* chore(deps): bump virtualenv from 20.13.3 to 20.13.4 (#196)

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.13.3 to 20.13.4.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/20.13.4/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.13.3...20.13.4)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`f94bb64`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f94bb64f5216eb8de8f032368e3c73f914e0b737))

* chore(deps): bump testfixtures from 6.18.4 to 6.18.5 (#187)

Bumps [testfixtures](https://github.com/Simplistix/testfixtures) from 6.18.4 to 6.18.5.
- [Release notes](https://github.com/Simplistix/testfixtures/releases)
- [Changelog](https://github.com/simplistix/testfixtures/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/Simplistix/testfixtures/compare/6.18.4...6.18.5)

---
updated-dependencies:
- dependency-name: testfixtures
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`3b92776`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3b92776d75ea0e75f5b41bdfb69b78851e0ffc52))

* chore(deps): bump types-setuptools from 57.4.9 to 57.4.10 (#188)

Bumps [types-setuptools](https://github.com/python/typeshed) from 57.4.9 to 57.4.10.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-setuptools
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`dcfaf21`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/dcfaf21f27fd490277de01eb0eb9b59a522d5353))

* chore(deps): bump virtualenv from 20.13.2 to 20.13.3 (#189)

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.13.2 to 20.13.3.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.13.2...20.13.3)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`e71e5b3`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/e71e5b3a46cb6c5c915d9b31eb8e0e815c511a3d))

* chore(deps-dev): bump mypy from 0.931 to 0.940 (#192)

Bumps [mypy](https://github.com/python/mypy) from 0.931 to 0.940.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.931...v0.940)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`9fce6bf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9fce6bf853032de9b2eec1f2b20341c8fbe6f639))

* chore: added autopep8 to pre-commit and clarified command in CONTRIBUTING for performance

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`5dafb1c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/5dafb1c88208caccaf82fc5abea41df0d295d5a4))

* chore: first pass pre-commit config

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`fd6ab7a`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fd6ab7ab2136c4afd8169fc97e0ee6ecbbef56a7))

* chore: added documentation to CONTRIBUTING guidelines

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`67cefe1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/67cefe1e5f9eb3bdb1d07c29e1ea351937c15bc0))

* chore(deps): bump actions/checkout from 2 to 3 (#184)

Bumps [actions/checkout](https://github.com/actions/checkout) from 2 to 3.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/v2...v3)

---
updated-dependencies:
- dependency-name: actions/checkout
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`a3ed3c7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/a3ed3c712a8a85361a59522efc356ab5194b0999))

* chore(deps): bump actions/setup-python from 2 to 3 (#183)

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 2 to 3.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v2...v3)

---
updated-dependencies:
- dependency-name: actions/setup-python
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`ee79ffa`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ee79ffaaa6155f6890379a847b49a805c1ee7202))

* chore: dependabot prefix `chore`, not eco-system ([`c96cea4`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/c96cea47f855add5edf2707305ef7b671da7db39))

* chore: make isort and flake8-isort available

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b211de5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/b211de50b92393e653b9a9f907c66a81b016d870))

* chore: poetry(deps): bump pyparsing from 3.0.6 to 3.0.7 (#140)

Bumps [pyparsing](https://github.com/pyparsing/pyparsing) from 3.0.6 to 3.0.7.
- [Release notes](https://github.com/pyparsing/pyparsing/releases)
- [Changelog](https://github.com/pyparsing/pyparsing/blob/master/CHANGES)
- [Commits](https://github.com/pyparsing/pyparsing/compare/pyparsing_3.0.6...pyparsing_3.0.7)

---
updated-dependencies:
- dependency-name: pyparsing
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`1bdb798`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/1bdb7987a86af967d5a883626346f217a243bfda))

* chore: poetry(deps): bump types-setuptools from 57.4.7 to 57.4.9 (#168)

Bumps [types-setuptools](https://github.com/python/typeshed) from 57.4.7 to 57.4.9.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-setuptools
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`48c3f99`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/48c3f997abf2560b648d85b907c001879e063551))

* chore: poetry(deps): bump filelock from 3.4.0 to 3.4.1 (#116)

Bumps [filelock](https://github.com/tox-dev/py-filelock) from 3.4.0 to 3.4.1.
- [Release notes](https://github.com/tox-dev/py-filelock/releases)
- [Changelog](https://github.com/tox-dev/py-filelock/blob/main/docs/changelog.rst)
- [Commits](https://github.com/tox-dev/py-filelock/compare/3.4.0...3.4.1)

---
updated-dependencies:
- dependency-name: filelock
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`17f1a5f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/17f1a5f8555675913ea09318848dd28ce96d1c3c))

* chore: poetry(deps): bump attrs from 21.2.0 to 21.4.0 (#113)

Bumps [attrs](https://github.com/python-attrs/attrs) from 21.2.0 to 21.4.0.
- [Release notes](https://github.com/python-attrs/attrs/releases)
- [Changelog](https://github.com/python-attrs/attrs/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/python-attrs/attrs/compare/21.2.0...21.4.0)

---
updated-dependencies:
- dependency-name: attrs
  dependency-type: indirect
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`3c39ae5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3c39ae5f7435b4e0240e674e47283ac3beb9f2b8))

* chore: poetry(deps): bump typed-ast from 1.5.1 to 1.5.2 (#144)

Bumps [typed-ast](https://github.com/python/typed_ast) from 1.5.1 to 1.5.2.
- [Release notes](https://github.com/python/typed_ast/releases)
- [Changelog](https://github.com/python/typed_ast/blob/master/release_process.md)
- [Commits](https://github.com/python/typed_ast/compare/1.5.1...1.5.2)

---
updated-dependencies:
- dependency-name: typed-ast
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`ac5809e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ac5809e93a3a5c54b04c75bd959216a4b21095ff))

* chore: poetry(deps): bump packageurl-python from 0.9.6 to 0.9.9 (#177)

Bumps [packageurl-python](https://github.com/package-url/packageurl-python) from 0.9.6 to 0.9.9.
- [Release notes](https://github.com/package-url/packageurl-python/releases)
- [Changelog](https://github.com/package-url/packageurl-python/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/package-url/packageurl-python/compare/v0.9.6...v0.9.9)

---
updated-dependencies:
- dependency-name: packageurl-python
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`4bfba14`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4bfba14bfacca773fd2e949e327f94b794fdef0b))

* chore: poetry(deps): bump virtualenv from 20.13.1 to 20.13.2 (#181)

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.13.1 to 20.13.2.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.13.1...20.13.2)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`20e3368`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/20e3368f35e28187f41ac0652384ea2104d45e35))

### Feature

* feat: output errors are verbose

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`bfe8fb1`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bfe8fb18825251fd9f146458122aa06137ec27c0))

### Fix

* fix: `version` being optional in JSON output can raise error

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`ba0c82f`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/ba0c82fbde7ba47502c45caf4fa89e9e4381f482))

### Style

* style: sorted all imports

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`4780a84`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/4780a84979d213d6ce6d9527945d532cbd6a8ceb))

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

### Chore

* chore: poetry(deps): bump virtualenv from 20.13.0 to 20.13.1 (#167)

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.13.0 to 20.13.1.
- [Release notes](https://github.com/pypa/virtualenv/releases)
- [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst)
- [Commits](https://github.com/pypa/virtualenv/compare/20.13.0...20.13.1)

---
updated-dependencies:
- dependency-name: virtualenv
  dependency-type: indirect
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`9e80258`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/9e802582bd9b9bdd0e1e91a0af551d3f2190fb5e))

* chore:  poetry(deps): bump types-toml from 0.10.3 to 0.10.4 (#166)

Bumps [types-toml](https://github.com/python/typeshed) from 0.10.3 to 0.10.4.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-toml
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`02449f6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/02449f6102e49f9e2425ab4e5b050f38832e6ba9))

* chore: bump dependencies

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`6c280e7`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6c280e7794466ad9b6f1ce5eb985035bea21eaaa))

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

### Test

* test: refactor to work on PY &lt; 3.10

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`0ce5de6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/0ce5de6a223e10161a8b864d0115e95d849d5e87))

* test: refactored fixtures for tests which has uncovered #150, #151 and #152

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`df43a9b`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/df43a9bff4b8360234bf50058ded82e44e2df082))

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

### Chore

* chore: attempt to produce manual GitHub action to release a RC version

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`3058afc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3058afc42fa632be6a0efb9ef509612d8833e07b))

* chore: attempt to produce manual GitHub action to release a RC version

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`6799e63`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6799e632d2eb1d3cee0042c2350477a74bcdce83))

* chore: disable poetry-cache in gh-workflow (#112)

closes #91

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`42f7952`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/42f7952fad512c84fd0a4d08c564af43d8bc5c87))

* chore: removed pdoc3 from main dev dependencies as now covered in docs/requirements.txt

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`89d8382`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/89d8382dc0e8bedb129ca0bbbd95922ea104f95c))

* chore: isolate dependencies for building documentation (#107)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`f2403f6`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/f2403f66c21e55de552b10c473332a1ea72b25bf))

* chore: bump `flake8` to v4 and add `autopep8` (#93)

* chore: bump `flake8` to v4 and add `autopep8`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* chore: make pep8 known in the contrib docs

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`6553dbf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6553dbfefcf6865b28b72771a9a08f1387dbdf11))

* chore: poetry(deps-dev): bump mypy from 0.910 to 0.920 (#103)

Bumps [mypy](https://github.com/python/mypy) from 0.910 to 0.920.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.910...v0.920)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`fdd20ca`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/fdd20ca4be71be78b578f756f46b44d829a76212))

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

### Chore

* chore: reordered deps &amp; updated poetry lock

Merge pull request #90 from CycloneDX/update-poetry-lock ([`d8c7ee2`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d8c7ee2915c23d22bc49c9d562a052783ea7ea87))

* chore: updated poetry lock

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`91b97be`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/91b97bedfa0a22598e9f4e8731bcf7293bc7d57d))

### Fix

* fix: further loosened dependency definitions

see #44

updated some locked dependencies to latest versions

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8bef6ec`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8bef6ecad36f51a003b266d776c9520d33e06034))

### Unknown

* 0.12.1

Automatically generated by python-semantic-release ([`43fc36e`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/43fc36ebc966ac511e5b7dbff9b0bef6f88d5d2c))


## v0.12.0 (2021-12-09)

### Ci

* ci: update to run tox for both our favoured versions of dependencies and lowest supported versions

* add tox env for minimal required dependencies

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* try to fix `TypedDict` typing

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* fix: typing definitions to be PY 3.6 compatible

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* fix: typing definitions to be PY 3.6 compatible

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* straigtened up `sys.version_info` constraints/code-branches

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* removed unused type ignores

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* try to fix type variants

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* try to fix type variants

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* typing for py3.6

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* fixed invalid unittest

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* typing for py3.6

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* mypy silence `warn_unused_ignores`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* mypy in tox for lowest version is pinned

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Co-authored-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`07ebedc`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/07ebedcbab1554970496780bb8bf167f6fe4ad5c))

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

### Ci

* ci: disable git automatic line ending conversions

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`350c097`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/350c097d1dcad367913f65d1026288777e5e4ba4))

* ci: update to run on OSX and Windows

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`6588c4c`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/6588c4cc37351ac006eded165284f793f9f98bc2))

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

### Ci

* ci: update to deploy to pypi.org upon PR merge

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`04e86b5`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/04e86b54d71bf801511c728db949d622ae0c6fdc))

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

### Test

* test: additional tests around issue #8 which confirm level of support currently

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`bc54bed`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/bc54bed79cbeb16dbfcb8c6aaea88d906fd8538a))

* test: additional tests added to validate comments in requirements.txt and that hashes within requirements.txt are not currently supported

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`3a27d54`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/3a27d546d56d5c5c27f77af716a5545723794294))

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

### Refactor

* refactor: moved Vulnerabilities to be nested inside the Component

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`8b4034d`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/8b4034da82a0c5e861161849ddb32c3806adfa0f))

### Test

* test: added test to confirm no Vulnerabilities are output for Schema Version 1.0 (not supported by schema)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`d5aabcf`](https://github.com/CycloneDX/cyclonedx-python-lib/commit/d5aabcff8d46f635b3b74821d70fc279263c420c))

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
