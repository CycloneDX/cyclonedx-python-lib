import pkg_resources

from . import BaseParser

from ..model.cyclonedx import Component


class RequirementsParser(BaseParser):

    def __init__(self, requirements_content: str):
        requirements = pkg_resources.parse_requirements(requirements_content)
        for requirement in requirements:
            """
            @todo
            Note that the below line will get the first (lowest) version specified in the Requirement and
            ignore the operator (it might not be ==). This is passed to the Component.
            
            For example if a requirement was listed as: "PickyThing>1.6,<=1.9,!=1.8.6", we'll be interpretting this
            as if it were written "PickyThing==1.6"
            """
            (op, version) = requirement.specs[0]
            self._components.append(Component(
                name=requirement.project_name, version=version
            ))


class RequirementsFileParser(RequirementsParser):

    def __init__(self, requirements_file: str):
        with open(requirements_file) as r:
            super(RequirementsFileParser, self).__init__(requirements_content=r.read())
            r.close()
