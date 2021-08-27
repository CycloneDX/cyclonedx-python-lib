from unittest import TestCase

import os

from cyclonedx.model.bom import Bom
from cyclonedx.model.cyclonedx import Component
from cyclonedx.parser.requirements import RequirementsFileParser


class TestBom(TestCase):

    def test_bom_simple(self):
        parser = RequirementsFileParser(
            requirements_file=os.path.join(os.path.dirname(__file__), 'fixtures/requirements-simple.txt')
        )
        bom = Bom.from_parser(parser=parser)

        self.assertEqual(bom.component_count(), 1)
        self.assertTrue(bom.has_component(
            Component(name='setuptools', version='50.3.2')
        ))
