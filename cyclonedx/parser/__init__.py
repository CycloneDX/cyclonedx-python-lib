from abc import ABC
from typing import List

from ..model.cyclonedx import Component


class BaseParser(ABC):
    _components: List[Component] = []

    def component_count(self) -> int:
        return len(self._components)

    def get_components(self) -> List[Component]:
        return self._components
