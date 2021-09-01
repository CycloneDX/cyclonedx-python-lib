from abc import ABC


class BaseSchemaVersion(ABC):

    def bom_supports_metadata(self) -> bool:
        return True

    def component_supports_author(self) -> bool:
        return True

    def component_supports_bom_ref(self) -> bool:
        return True

    def get_schema_version(self) -> str:
        pass


class SchemaVersion1Dot3(BaseSchemaVersion):

    def get_schema_version(self) -> str:
        return '1.3'


class SchemaVersion1Dot2(BaseSchemaVersion):

    def get_schema_version(self) -> str:
        return '1.2'


class SchemaVersion1Dot1(BaseSchemaVersion):

    def bom_supports_metadata(self) -> bool:
        return False

    def component_supports_author(self) -> bool:
        return False

    def get_schema_version(self) -> str:
        return '1.1'


class SchemaVersion1Dot0(BaseSchemaVersion):

    def bom_supports_metadata(self) -> bool:
        return False

    def component_supports_author(self) -> bool:
        return False

    def component_supports_bom_ref(self) -> bool:
        return False

    def get_schema_version(self) -> str:
        return '1.0'
