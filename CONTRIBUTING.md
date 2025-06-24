# Contributing

Any contribution is welcome.  
Please read the [CycloneDX contributing guidelines](https://github.com/CycloneDX/.github/blob/master/CONTRIBUTING.md) first.

Pull-requests from forks are welcome.  
We love to see your purposed changes, but we also like to discuss things first. Please open a ticket and explain your intended changes to the community. And don't forget to mention that discussion in your pull-request later. 
Find the needed basics here:
* [how to fork a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
* [how create a pull request from a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)

## Setup

This project uses [poetry]. Have it installed and setup first.

To install dev-dependencies and tools:

```shell
poetry install --all-extras
```

## Code style

THis project loves latest python features.  
This project loves sorted imports.  
This project uses [PEP8] Style Guide for Python Code.  

Get it all applied via:

```shell
poetry run -- tox r -e pyupgrade -- --exit-zero-even-if-changed
poetry run -- tox r -e isort
poetry run -- tox r -e autopep8
```

This project prefers `f'strings'` over `'string'.format()`.  
This project prefers `'single quotes'` over `"double quotes"`.  
This project prefers `lower_snake_case` variable names.  

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
poetry run tox run
```

See also: [python test snapshots docs](tests/_data/snapshots/README.md)

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
