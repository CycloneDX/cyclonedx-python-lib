import json

from . import BaseOutput
from .schema import BaseSchemaVersion, SchemaVersion1Dot0, SchemaVersion1Dot1, SchemaVersion1Dot2, SchemaVersion1Dot3
from ..model.cyclonedx import Component


class Json(BaseOutput, BaseSchemaVersion):

    def output_as_string(self) -> str:
        return json.dumps(self._get_json())

    def output_to_file(self, filename: str):
        raise NotImplementedError

    def _get_json(self) -> dict:
        components = list(map(self._get_component_as_dict, self.get_bom().get_components()))

        response = {
            "bomFormat": "CycloneDX",
            "specVersion": str(self.get_schema_version()),
            "serialNumber": self.get_bom().get_urn_uuid(),
            "version": 1,
            "components": components
        }

        if self.bom_supports_metadata():
            response['metadata'] = self._get_metadata_as_dict()

        return response

    def _get_component_as_dict(self, component: Component) -> dict:
        c = {
            "type": component.get_type().value,
            "name": component.get_name(),
            "version": component.get_version(),
            "purl": component.get_purl()
        }

        if self.component_supports_author() and component.get_author() is not None:
            c['author'] = component.get_author()

        return c

    def _get_metadata_as_dict(self) -> dict:
        metadata = self.get_bom().get_metadata()
        return {
            "timestamp": metadata.get_timestamp().isoformat()
        }


class JsonV1Dot0(Json, SchemaVersion1Dot0):
    pass


class JsonV1Dot1(Json, SchemaVersion1Dot1):
    pass


class JsonV1Dot2(Json, SchemaVersion1Dot2):
    pass


class JsonV1Dot3(Json, SchemaVersion1Dot3):
    pass
