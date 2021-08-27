from unittest import TestCase

from cyclonedx.parser.environment import EnvironmentParser


class TestRequirementsParser(TestCase):

    def test_simple(self):
        """
        @todo This test is a vague as it will detect the unique environment where tests are being executed -
                so is this valid?

        :return:
        """
        parser = EnvironmentParser()
        self.assertGreater(parser.component_count(), 1)
