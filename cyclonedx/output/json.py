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
        components = list(map(self._get_component_as_dict, self.get_bom().get_components()))

        response = {
            "bomFormat": "CycloneDX",
            "specVersion": str(self._get_schema_version()),
            "serialNumber": self.get_bom().get_urn_uuid(),
            "version": 1,
            "components": components
        }

        if self._bom_supports_metadata():
            response['metadata'] = self._get_metadata_as_dict()

        return response

    def _get_component_as_dict(self, component: Component) -> dict:
        c = {
            "type": component.get_type().value,
            "name": component.get_name(),
            "version": component.get_version(),
            "purl": component.get_purl()
        }

        if self._component_supports_author() and component.get_author() is not None:
            c['author'] = component.get_author()

        return c

    def _bom_supports_metadata(self) -> bool:
        return True

    def _component_supports_author(self) -> bool:
        return True

    def _get_metadata_as_dict(self) -> dict:
        metadata = self.get_bom().get_metadata()
        return {
            "timestamp": metadata.get_timestamp().isoformat()
        }

    @abstractmethod
    def _get_schema_version(self) -> str:
        pass


class JsonV1Dot0(Json):

    def _get_schema_version(self) -> str:
        return '1.0'

    def _bom_supports_metadata(self) -> bool:
        return False

    def _component_supports_author(self) -> bool:
        return False


class JsonV1Dot1(Json):

    def _get_schema_version(self) -> str:
        return '1.1'

    def _bom_supports_metadata(self) -> bool:
        return False

    def _component_supports_author(self) -> bool:
        return False


class JsonV1Dot2(Json):

    def _get_schema_version(self) -> str:
        return '1.2'


class JsonV1Dot3(Json):

    def _get_schema_version(self) -> str:
        return '1.3'
