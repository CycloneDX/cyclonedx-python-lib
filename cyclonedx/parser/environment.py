from . import BaseParser

from ..model.cyclonedx import Component


class EnvironmentParser(BaseParser):
    """
    This will look at the current Python environment and list out all installed packages.

    Best used when you have virtual Python environments per project.
    """

    def __init__(self):
        import pkg_resources
        from importlib.metadata import metadata

        i: pkg_resources.DistInfoDistribution
        for i in iter(pkg_resources.working_set):
            c = Component(name=i.project_name, version=i.version)
            i_metadata = metadata(i.project_name)

            if 'Author' in i_metadata.keys():
                c.set_author(i_metadata.get('Author'))

            self._components.append(c)
