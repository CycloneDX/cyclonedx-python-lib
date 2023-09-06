from cyclonedx.factory.license import LicenseChoiceFactory, LicenseFactory
from cyclonedx.model import OrganizationalEntity, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output.json import JsonV1Dot4
from cyclonedx.output.xml import XmlV1Dot4
from packageurl import PackageURL

lc_factory = LicenseChoiceFactory(license_factory=LicenseFactory())

# region build the BOM

bom = Bom()
bom.metadata.component = rootComponent = Component(
    name='myApp',
    type=ComponentType.APPLICATION,
    licenses=[lc_factory.make_from_string('MIT')],
    bom_ref='myApp',
)

component1 = Component(
    type=ComponentType.LIBRARY,
    name='some-component',
    group='acme',
    version='1.33.7-beta.1',
    licenses=[lc_factory.make_from_string('(c) 2021 Acme inc.')],
    supplier=OrganizationalEntity(
        name='Acme Inc',
        urls=[XsUri('https://www.acme.org')]
    ),
    bom_ref='myComponent@1.33.7-beta.1',
    purl=PackageURL('generic', 'acme', 'some-component', '1.33.7-beta.1')
)
bom.components.add(component1)
bom.register_dependency(rootComponent, [component1])

component2 = Component(
    type=ComponentType.LIBRARY,
    name='some-library',
    licenses=[lc_factory.make_from_string('GPL-3.0-only WITH Classpath-exception-2.0')]
)
bom.components.add(component2)
bom.register_dependency(component1, [component2])

# endregion build the BOM

serializedJSON = JsonV1Dot4(bom).output_as_string()
print(serializedJSON)

serializedXML = XmlV1Dot4(bom).output_as_string()
print(serializedXML)
