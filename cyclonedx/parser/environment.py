from . import BaseParser

from ..model.cyclonedx import Component


class EnvironmentParser(BaseParser):
    """
    This will look at the current Python environment and list out all installed packages.

    Best used when you have virtual Python environments per project.
    """

    def __init__(self):
        import pkg_resources
        for i in iter(pkg_resources.working_set):
            self._components.append(Component(name=i.project_name, version=i.version, type='pypi'))
