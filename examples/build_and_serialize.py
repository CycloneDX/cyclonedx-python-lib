from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import OrganizationalEntity, XsUri
from cyclonedx.model.bom import Bom, LicenseChoice
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.dependency import Dependency
from cyclonedx.output.json import JsonV1Dot4
from cyclonedx.output.xml import XmlV1Dot4
from packageurl import PackageURL

lFac = LicenseFactory()

# region build the BOM

bom = Bom()
bom.metadata.component = rootComponent = Component(
    name='myApp',
    type=ComponentType.APPLICATION,
    licenses=[LicenseChoice(license=lFac.make_from_string('MIT'))],
    bom_ref='myApp',
)

component = Component(
    type=ComponentType.LIBRARY,
    name='some-component',
    group='acme',
    version='1.33.7-beta.1',
    licenses=[LicenseChoice(license=lFac.make_from_string('(c) 2021 Acme inc.'))],
    supplier=OrganizationalEntity(
        name='Acme Inc',
        urls=[XsUri('https://www.acme.org')]
    ),
    bom_ref='myComponent@1.33.7-beta.1',
    purl=PackageURL('generic', 'acme', 'some-component', '1.33.7-beta.1')
)

bom.components.add(component)
bom.dependencies.add(Dependency(rootComponent.bom_ref, [Dependency(component.bom_ref)]))

# endregion build the BOM

serializedJSON = JsonV1Dot4(bom).output_as_string()
print(serializedJSON)

serializedXML = XmlV1Dot4(bom).output_as_string()
print(serializedXML)
