Modelling
=========

You can create a BOM Model from either a :py:mod:`cyclonedx.parser` instance or manually using the methods available
directly on the :py:mod:`cyclonedx.model.bom.Bom` class.

Vulnerabilities are supported by the Model as of version 0.3.0.

    **Note:** Known vulnerabilities associated with Components can be sourced from various data sources, but this library
    will not source them for you. Perhaps look at `Jake`_ if you're interested in this.

Examples
--------

From a Parser
~~~~~~~~~~~~~

    **Note:** Concreate parser implementations were moved out of this library and into `CycloneDX Python`_ as of version
    ``1.0.0``.

.. code-block:: python

    from cyclonedx.model.bom import Bom
    from cyclonedx_py.parser.environment import EnvironmentParser

    parser = EnvironmentParser()
    bom = Bom.from_parser(parser=parser)


.. _CycloneDX Python: https://github.com/CycloneDX/cyclonedx-python
.. _Jake: https://pypi.org/project/jake