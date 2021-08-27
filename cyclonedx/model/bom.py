from typing import List
from .cyclonedx import Component
from ..parser import BaseParser


class Bom:
    """
    This is our internal representation of the BOM.

    We can pass a BOM instance to a Generator to produce CycloneDX in the required format and according
    to the requested schema version.
    """

    _components: List[Component] = []

    @staticmethod
    def from_parser(parser: BaseParser):
        bom = Bom()
        bom.add_components(parser.get_components())
        return bom

    def __init__(self):
        self._components.clear()

    def add_component(self, component: Component):
        self._components.add(component)

    def add_components(self, components: List[Component]):
        self._components = self._components + components

    def component_count(self) -> int:
        return len(self._components)

    def has_component(self, component: Component) -> bool:
        print("Checking if {} is contained within {}".format(component, self._components))
        return component in self._components
