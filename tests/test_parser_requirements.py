import os
from unittest import TestCase

from cyclonedx.parser.requirements import RequirementsParser


class TestRequirementsParser(TestCase):

    def test_simple(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-simple.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(1, parser.component_count())

    def test_example_1(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-example-1.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(3, parser.component_count())
