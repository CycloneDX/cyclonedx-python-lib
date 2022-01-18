from unittest import TestCase

from cyclonedx.model.dependency import Dependency
from packageurl import PackageURL


class TestModelDependency(TestCase):

    def test_dependency_equal(self) -> None:
        d = Dependency(
            purl=PackageURL(type="pypi", name="dependency", version="1.2.3")
        )
        d2 = Dependency(
            purl=PackageURL(type="pypi", name="dependency", version="1.2.3")
        )

        self.assertEqual(d, d2)

    def test_dependency_not_equal(self) -> None:
        d = Dependency(
            purl=PackageURL(type="pypi", name="other-dependency", version="1.2.3")
        )
        d2 = Dependency(
            purl=PackageURL(type="pypi", name="dependency", version="1.2.3")
        )
        self.assertNotEqual(d, d2)

        d = Dependency(
            purl=PackageURL(type="pkgpi", name="dependency", version="1.2.3")
        )
        d2 = Dependency(
            purl=PackageURL(type="pypi", name="dependency", version="1.2.3")
        )
        self.assertNotEqual(d, d2)

        d = Dependency(
            purl=PackageURL(type="pypi", name="dependency", version="1.2.3")
        )
        d2 = Dependency(
            purl=PackageURL(type="pypi", name="dependency", version="3.2.1")
        )
        self.assertNotEqual(d, d2)
