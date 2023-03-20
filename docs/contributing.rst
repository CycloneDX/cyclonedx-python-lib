Contributing
====================================================

Pull requests are welcome, but please read these contributing guidelines first.

Setup
----------------------------------------------------

This project uses `poetry`_. Have it installed and setup first.

To install dev-dependencies and tools:

.. code-block::

   poetry install

Code style
----------------------------------------------------

This project uses `PEP8`_ Style Guide for Python Code. This project loves sorted imports. Get it all applied via:

.. code-block::

    poetry run isort .
    poetry run flake8 cyclonedx/ tests/ typings/


Documentation
----------------------------------------------------

This project uses `Sphinx`_ to generate documentation which is automatically published to `readthedocs.io`_.

Source for documentation is stored in the ``docs`` folder in `RST`_ format.

You can generate the documentation locally by running:

.. code-block::

    cd docs
    pip install -r requirements.txt
    make html


Testing
----------------------------------------------------

Run all tests in dedicated environments, via:

.. code-block::

    poetry run tox


Sign your commits
----------------------------------------------------

Please sign your commits, to show that you agree to publish your changes under the current terms and licenses of the
project. We can't accept contributions, however great, if you do not sign your commits.

.. code-block::

    git commit --signed-off ...


Pre-commit hooks
----------------------------------------------------

If you like to take advantage of `pre-commit hooks`_, you can do so to cover most of the topics on this page when
contributing.

.. code-block::

    pre-commit install

All our pre-commit checks will run locally before you can commit!


.. _poetry: https://python-poetry.org
.. _PEP8: https://www.python.org/dev/peps/pep-0008
.. _Sphinx: https://www.sphinx-doc.org/
.. _readthedocs.io: https://cyclonedx-python-library.readthedocs.io/
.. _RST: https://en.wikipedia.org/wiki/ReStructuredText
.. _pre-commit hooks: https://pre-commit.com
