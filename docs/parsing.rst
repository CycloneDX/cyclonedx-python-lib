Parsing
=======

Parsers are provided as a quick way to generate a BOM for Python applications or from Python environments.

    **WARNING**: Limited information will be available when generating a BOM using some Parsers due to limited
    information kept/suppled by those package managers. See
    :py:mod:`cyclonedx.parser` for details of what fields can be completed by different Parsers.

Easily create your parser instance as follows:

.. code-block:: python

   from cyclonedx.parser.environment import EnvironmentParser

   parser = EnvironmentParser()

Parsers
-------

Conda
~~~~~

* :py:mod:`cyclonedx.parser.conda.CondaListJsonParser`: Parses input provided as a ``str`` that is output from
  ``conda list --json``
* :py:mod:`cyclonedx.parser.conda.CondaListExplicitParser`: Parses input provided as a ``str`` that is output from:
  ``conda list --explicit`` or ``conda list --explicit --md5``

Environment
~~~~~~~~~~~

* :py:mod:`cyclonedx.parser.environment.EnvironmentParser`: Looks at the packages installed in your current Python
  environment

Pip
~~~~~~~

* :py:mod:`cyclonedx.parser.pipenv.PipEnvParser`: Parses ``Pipfile.lock`` content passed in as a string
* :py:mod:`cyclonedx.parser.pipenv.PipEnvFileParser`: Parses the ``Pipfile.lock`` file at the supplied path

Poetry
~~~~~~

* :py:mod:`cyclonedx.parser.poetry.PoetryParser`: Parses ``poetry.lock`` content passed in as a string
* :py:mod:`cyclonedx.parser.poetry.PoetryFileParser`: Parses the ``poetry.lock`` file at the supplied path

Requirements
~~~~~~~~~~~~

* :py:mod:`cyclonedx.parser.requirements.RequirementsParser`: Parses a multiline string that you provide that conforms
  to the ``requirements.txt`` :pep:`508` standard.
* :py:mod:`cyclonedx.parser.requirements.RequirementsFileParser`: Parses a file that you provide the path to that
  conforms to the ``requirements.txt`` :pep:`508` standard.

CycloneDX software bill-of-materials require pinned versions of requirements. If your `requirements.txt` does not have
pinned versions, warnings will be recorded and the dependencies without pinned versions will be excluded from the
generated CycloneDX. CycloneDX schemas (from version 1.0+) require a component to have a version when included in a
CycloneDX bill of materials (according to schema).

If you need to use a ``requirements.txt`` in your project that does not have pinned versions an acceptable workaround
might be to:

.. code-block:: bash

   pip install -r requirements.txt
   pip freeze > requirements-frozen.txt

You can then feed in the frozen requirements from ``requirements-frozen.txt`` `or` use the ``Environment`` parser once
you have installed your dependencies.