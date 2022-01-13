from unittest import TestCase

from cyclonedx.model import ExternalReference, ExternalReferenceType
from cyclonedx.model.component import Component, ComponentType


class TestModelComponent(TestCase):

    def test_empty_basic_component(self) -> None:
        c = Component(
            name='test-component', version='1.2.3'
        )
        self.assertEqual(c.name, 'test-component')
        self.assertEqual(c.version, '1.2.3')
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertEqual(len(c.external_references), 0)
        self.assertEqual(len(c.hashes), 0)
        self.assertEqual(len(c.get_vulnerabilities()), 0)

    def test_multiple_basic_components(self) -> None:
        c1 = Component(
            name='test-component', version='1.2.3'
        )
        self.assertEqual(c1.name, 'test-component')
        self.assertEqual(c1.version, '1.2.3')
        self.assertEqual(c1.type, ComponentType.LIBRARY)
        self.assertEqual(len(c1.external_references), 0)
        self.assertEqual(len(c1.hashes), 0)
        self.assertEqual(len(c1.get_vulnerabilities()), 0)

        c2 = Component(
            name='test2-component', version='3.2.1'
        )
        self.assertEqual(c2.name, 'test2-component')
        self.assertEqual(c2.version, '3.2.1')
        self.assertEqual(c2.type, ComponentType.LIBRARY)
        self.assertEqual(len(c2.external_references), 0)
        self.assertEqual(len(c2.hashes), 0)
        self.assertEqual(len(c2.get_vulnerabilities()), 0)

        self.assertNotEqual(c1, c2)

    def test_external_references(self) -> None:
        c = Component(
            name='test-component', version='1.2.3'
        )
        c.add_external_reference(ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        ))
        self.assertEqual(c.name, 'test-component')
        self.assertEqual(c.version, '1.2.3')
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertEqual(len(c.external_references), 1)
        self.assertEqual(len(c.hashes), 0)
        self.assertEqual(len(c.get_vulnerabilities()), 0)

        c2 = Component(
            name='test2-component', version='3.2.1'
        )
        self.assertEqual(c2.name, 'test2-component')
        self.assertEqual(c2.version, '3.2.1')
        self.assertEqual(c2.type, ComponentType.LIBRARY)
        self.assertEqual(len(c2.external_references), 0)
        self.assertEqual(len(c2.hashes), 0)
        self.assertEqual(len(c2.get_vulnerabilities()), 0)

    def test_empty_basic_component_no_version(self) -> None:
        c = Component(
            name='test-component'
        )
        self.assertEqual(c.name, 'test-component')
        self.assertIsNone(c.version, None)
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertEqual(len(c.external_references), 0)
        self.assertEqual(len(c.hashes), 0)
        self.assertEqual(len(c.get_vulnerabilities()), 0)

    def test_component_equal(self) -> None:
        c = Component(
            name='test-component', version='1.2.3'
        )
        c.add_external_reference(ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        ))

        c2 = Component(
            name='test-component', version='1.2.3'
        )
        c2.add_external_reference(ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        ))

        self.assertEqual(c, c2)
