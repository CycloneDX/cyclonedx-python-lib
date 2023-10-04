# Contributing

Pull requests are welcome.
But please read the
[CycloneDX contributing guidelines](https://github.com/CycloneDX/.github/blob/master/CONTRIBUTING.md)
first.

## Setup

This project uses [poetry]. Have it installed and setup first.

To install dev-dependencies and tools:

```shell
poetry install
```

## Code style

This project uses [PEP8] Style Guide for Python Code.  
This project loves sorted imports.  
Get it all applied via:

```shell
poetry run isort .
poetry run flake8 cyclonedx/ tests/ typings/
```

## Documentation

This project uses [Sphinx] to generate documentation which is automatically published to [readthedocs.io].

Source for documentation is stored in the `docs` folder in [RST] format.

You can generate the documentation locally by running:

```shell
cd docs
pip install -r requirements.txt
make html
```

## Testing

Run all tests in dedicated environments, via:

```shell
poetry run tox
```

## Sign off your commits

Please sign off your commits, to show that you agree to publish your changes under the current terms and licenses of the project
, and to indicate agreement with [Developer Certificate of Origin (DCO)](https://developercertificate.org/).

```shell
git commit --signed-off ...
```

## Pre-commit hooks

If you like to take advantage of [pre-commit hooks], you can do so to cover most of the topics on this page when
contributing.

```shell
pre-commit install
```

All our pre-commit checks will run locally before you can commit!

[poetry]: https://python-poetry.org
[PEP8]: https://www.python.org/dev/peps/pep-0008
[Sphinx]: https://www.sphinx-doc.org/
[readthedocs.io]: https://cyclonedx-python-library.readthedocs.io/
[RST]: https://en.wikipedia.org/wiki/ReStructuredText
[pre-commit hooks]: https://pre-commit.com
