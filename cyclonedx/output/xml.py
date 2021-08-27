from cyclonedx.model.bom import Bom


class Xml:

    _bom: Bom

    def __init__(self, bom: Bom):
        self._bom = bom
