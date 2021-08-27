from enum import Enum

PURL_TYPE_PREFIX = 'pypi'


class ComponentType(Enum):
    """
    Enum object that defines the permissable 'types' for a Component according to the CycloneDX
    schemas.
    """
    APPLICATION = 'application'
    CONTAINER = 'container'
    DEVICE = 'device'
    FILE = 'file'
    FIRMWARE = 'firmware'
    FRAMEWORK = 'framework'
    LIBRARY = 'library'
    OPERATING_SYSTEM = 'operating-system'


class Component:
    """
    An object that mirrors the Component type in the CycloneDX schema.
    """
    _type: ComponentType
    _name: str
    _version: str
    _qualifiers: str

    def __init__(self, name: str, version: str, qualifiers: str = None, type: ComponentType = ComponentType.LIBRARY):
        self._name = name
        self._version = version
        self._type = type
        self._qualifiers = qualifiers

    def get_purl(self) -> str:
        base_purl = 'pkg:{}/{}@{}'.format(PURL_TYPE_PREFIX, self._name, self._version)
        if self._qualifiers:
            base_purl = '{}?{}'.format(base_purl, self._qualifiers)
        return base_purl

    def __eq__(self, other):
        return other.get_purl() == self.get_purl()

    def __repr__(self):
        return '<Component {}={}>'.format(self._name, self._version)
