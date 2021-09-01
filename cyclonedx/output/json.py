import json
from abc import abstractmethod

from . import BaseOutput
from ..model.cyclonedx import Component


class Json(BaseOutput):

    def output_as_string(self) -> str:
        return json.dumps(self._get_json())

    def output_to_file(self, filename: str):
        pass

    def _get_json(self) -> dict:
        components = list(map(Json._get_component_as_dict, self.get_bom().get_components()))

        return {
            "bomFormat": "CycloneDX",
            "specVersion": str(self._get_schema_version()),
            "serialNumber": "",
            "version": 1,
            "metadata": self._get_metadata_as_dict(),
            "components": components
        }

    @staticmethod
    def _get_component_as_dict(component: Component) -> dict:
        return {
            "type": component.get_type().value,
            "name": component.get_name(),
            "version": component.get_version(),
            "purl": component.get_purl()
        }

    def _get_metadata_as_dict(self) -> dict:
        metadata = self.get_bom().get_metadata()
        return {
            "timestamp": metadata.get_timestamp().isoformat()
        }

    @abstractmethod
    def _get_schema_version(self) -> str:
        pass


class JsonV1Dot2(Json):

    def _get_schema_version(self) -> str:
        return '1.2'


class JsonV1Dot3(Json):

    def _get_schema_version(self) -> str:
        return '1.3'
