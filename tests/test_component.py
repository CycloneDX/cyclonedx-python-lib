from unittest import TestCase

from cyclonedx.model.cyclonedx import Component
from packageurl import PackageURL


class TestComponent(TestCase):
    _component: Component

    @classmethod
    def setUpClass(cls) -> None:
        cls._component = Component(name='setuptools', version='50.3.2').get_purl()
        cls._component_with_qualifiers = Component(name='setuptools', version='50.3.2',
                                                   qualifiers='extension=tar.gz').get_purl()

    def test_purl_correct(self):
        self.assertEqual(
            str(PackageURL(
                type='pypi', name='setuptools', version='50.3.2'
            )),
            TestComponent._component
        )

    def test_purl_incorrect_version(self):
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.1'
        )
        self.assertNotEqual(
            str(purl),
            TestComponent._component
        )
        self.assertEqual(purl.type, 'pypi')
        self.assertEqual(purl.name, 'setuptools')
        self.assertEqual(purl.version, '50.3.1')

    def test_purl_incorrect_name(self):
        purl = PackageURL(
            type='pypi', name='setuptoolz', version='50.3.2'
        )
        self.assertNotEqual(
            str(purl),
            TestComponent._component
        )
        self.assertEqual(purl.type, 'pypi')
        self.assertEqual(purl.name, 'setuptoolz')
        self.assertEqual(purl.version, '50.3.2')

    def test_purl_with_qualifiers(self):
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
        )
        self.assertEqual(
            str(purl),
            TestComponent._component_with_qualifiers
        )
        self.assertNotEqual(
            str(purl),
            TestComponent._component
        )
        self.assertEqual(purl.qualifiers, {'extension': 'tar.gz'})
