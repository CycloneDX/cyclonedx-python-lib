from abc import abstractmethod

from . import BaseOutput


class Xml(BaseOutput):

    @abstractmethod
    def output_as_string(self) -> str:
        pass

    @abstractmethod
    def output_to_file(self, filename: str):
        pass


class XmlV1Dot2(Xml):

    def output_as_string(self) -> str:
        return ''

    def output_to_file(self, filename: str):
        return ''


class XmlV1Dot3(Xml):

    def output_as_string(self) -> str:
        return ''

    def output_to_file(self, filename: str):
        return ''
