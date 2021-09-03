import sys

if sys.version_info >= (3, 8, 0):
    from importlib.metadata import metadata
else:
    from importlib_metadata import metadata

from . import BaseParser

from ..model.cyclonedx import Component


class EnvironmentParser(BaseParser):
    """
    This will look at the current Python environment and list out all installed packages.

    Best used when you have virtual Python environments per project.
    """

    def __init__(self):
        import pkg_resources

        i: pkg_resources.DistInfoDistribution
        for i in iter(pkg_resources.working_set):
            c = Component(name=i.project_name, version=i.version)

            i_metadata = self._get_metadata_for_package(i.project_name)
            if 'Author' in i_metadata.keys():
                c.set_author(i_metadata.get('Author'))

            self._components.append(c)

    @staticmethod
    def _get_metadata_for_package(package_name: str):
        if sys.version_info >= (3, 8, 0):
            return metadata(package_name)
        else:
            return metadata(package_name)
