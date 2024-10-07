Upgrading to v8
===============

Version 8 is not backwards compatible. Some behaviours and integrations changed.
This document covers all breaking changes and should give guidance how to migrate from previous versions.

This document is not a full :doc:`change log <changelog>`, but a migration path.

Add this library to Metadata Tools
----------------------------------

This library no longer adds itself to the metadata.

Downstream users SHOULD add the following to their BOM build processes, to keep track of the used library.

.. code-block:: python

    from cyclonedx.builder.this import this_component as cdx_lib_component
    from cyclonedx.model.bom import Bom

    bom = Bom()
    bom.metadata.tools.components.add(cdx_lib_component())

Import model Tool
-----------------

Class `cyclonedx.model.Tool` was moved to :class:`cyclonedx.model.tool.Tool`.
Therefore, the imports need to be migrated.

Old: ``from cyclonedx.model import Tool``

New: ``from cyclonedx.model.tool import Tool``

Alter Metadata Tools
--------------------

Property :attr:`cyclonedx.model.bom.BomMetaData.tools` is an instance of :class:`cyclonedx.model.tool.ToolRepository`, now.
Therefore, the process of adding new tools needs to be migrated.

Old: ``my_bom.metadata.tools.add(my_tool)``

New: ``my_bom.metadata.tools.tools.add(my_tool)``

Alter Vulnerability Tools
-------------------------

Property :attr:`cyclonedx.model.vulnerability.Vulnerability.tools` is an instance of :class:`cyclonedx.model.tool.ToolRepository`, now.
Therefore, the process of adding new tools needs to be migrated.

Old: ``my_vulnerability.tools.add(my_tool)``

New: ``my_vulnerability.tools.tools.add(my_tool)``

Set LicenseExpression Acknowledgement
-------------------------------------

:class:`cyclonedx.model.license.LicenseExpression()` no longer accepts optional arguments in a positional way, but in a key-word way.

Old: ``LicenseExpression(my_exp, my_acknowledgement)``

New: ``LicenseExpression(my_exp, acknowledgement=my_acknowledgement)``
