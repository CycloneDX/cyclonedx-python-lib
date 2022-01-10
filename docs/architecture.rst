Architecture
============

This library broadly is separated into three key functional areas:

1. **Parser**: Use a parser that suits your needs to automatically gather information about your environment or
   application
2. **Model**: Internal models used to unify data from different parsers
3. **Output**: Choose and configure an output which allows you to define output format as well as the CycloneDX schema
   version

When wishing to generate a BOM, the process is as follows:

1. Generated a Model (either programmatically or from a :py:mod:`cyclonedx.parser`
2. Output the Model using an :py:mod:`cyclonedx.output` instance that reflects the schema version and format you require

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   parsing
   modelling
   outputting
