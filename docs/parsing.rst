Parsing
=======

Parsers are provided as a quick way to generate a BOM for Python applications or from Python environments.

    **WARNING**: Limited information will be available when generating a BOM using some Parsers due to limited
    information kept/supplied by those package managers. See below for details of what fields can be completed by
    different Parsers.

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

Parser Schema Support
---------------------

Different parsers support population of different information about your dependencies due to how information is
obtained and limitations of what information is available to each Parser. The sections below explain coverage as to what
information is obtained by each set of Parsers. It does NOT guarantee the information is output in the resulting
CycloneDX BOM document.

The below tables do not state whether specific schema versions support the attributes/items, just whether this library
does.

xPath is used to refer to data attributes according to the `Cyclone DX Specification`_.

``bom.components.component``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------------+-------------------------------------------------------------------+
|                         | Parser Support                                                    |
| Data Path               +------------+-------------+------------+------------+--------------+
|                         | Conda      | Environment | Pip        | Poetry     | Requirements |
+=========================+============+=============+============+============+==============+
| ``.supplier``           | N          | N - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.author``             | N          | Y - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.publisher``          | N          | N - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.group``              | N          | N           | N          | N          | N            |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.name``               | Y          | Y           | Y          | Y          | Y            |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.version``            | Y          | Y           | Y          | Y          | Y            |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.description``        | N          | N           | N/A        | N          | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.scope``              | N          | N           | N/A        | N          | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.hashes``             | Y - Note 2 | N/A         | Y - Note 3 | Y - Note 3 | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.licenses``           | N          | Y - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.copyright``          | N          | N - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.cpe``                | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.purl``               | Y          | Y           | Y          | Y          | Y            |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.swid``               | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.modified``           | *Deprecated - not used*                                           |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.pedigree``           | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.externalReferences`` | Y - Note 3 | N/A         | Y - Note 1 | Y - Note 1 | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.properties``         | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.components``         | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.evidence``           | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.releaseNotes``       | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+

    **Legend:**

    * **Y**: YES with any caveat states.
    * **N**: Not currently supported, but support believed to be possible.
    * **N/A**: Not supported and not deemed possible (i.e. the Parser would never be able to reliably determine this
      info).

**Notes**

1. If contained in the packaages ``METADATA``
2. MD5 hashses are available when using the ``CondaListExplicitParser`` with output from the
   conda command ``conda list --explicit --md5`` only
3. Python packages are regularly available as both ``.whl`` and ``.tar.gz`` packages. This means for that for a given
   package and version multiple artefacts are possible - which would mean multiple hashes are possible. CycloneDX
   supports only a single set of hashes identifying a single artefact at ``component.hashes``. To cater for this
   situation in Python, we add the hashes to `component.externalReferences`, as we cannot determine which package was
   actually obtained and installed to meet a given dependency.

.. _Cyclone DX Specification: https://cyclonedx.org/docs/latest