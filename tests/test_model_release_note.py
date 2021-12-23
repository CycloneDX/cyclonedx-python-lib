import datetime
from unittest import TestCase

from cyclonedx.model import XsUri
from cyclonedx.model.release_note import ReleaseNotes


class TestModelReleaseNote(TestCase):

    def test_simple(self) -> None:
        rn = ReleaseNotes(type='major')
        self.assertEqual(rn.get_type(), 'major')
        self.assertIsNone(rn.get_title())
        self.assertIsNone(rn.get_featured_image())
        self.assertIsNone(rn.get_social_image())
        self.assertIsNone(rn.get_description())
        self.assertIsNone(rn.get_timestamp())
        self.assertIsNone(rn.get_aliases())
        self.assertIsNone(rn.get_tags())
        self.assertIsNone(rn.get_resolves())
        self.assertIsNone(rn.get_notes())
        self.assertIsNone(rn.get_properties())

    def test_complete(self) -> None:
        timestamp: datetime.datetime = datetime.datetime.utcnow()
        rn = ReleaseNotes(
            type='major', title="Release Notes Title",
            featured_image=XsUri('https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'),
            social_image=XsUri('https://cyclonedx.org/cyclonedx-icon.png'),
            description="This release is a test release", timestamp=timestamp,
            aliases=[
                "First Test Release"
            ],
            tags=['test', 'alpha'],
            resolves=[],
            notes=[],
            properties=[]
        )
        rn.add_alias(alias="Release Alpha")
        rn.add_tag(tag='testing')

        self.assertEqual(rn.get_type(), 'major')
        self.assertEqual(rn.get_title(), 'Release Notes Title')
        self.assertEqual(
            rn.get_featured_image(),
            'https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'
        )
        self.assertEqual(rn.get_social_image(), 'https://cyclonedx.org/cyclonedx-icon.png')
        self.assertEqual(rn.get_description(), 'This release is a test release'),
        self.assertListEqual(rn.get_aliases(), ["First Test Release", "Release Alpha"])
        self.assertListEqual(rn.get_tags(), ['test', 'alpha', 'testing'])
        self.assertIsNone(rn.get_resolves())
        self.assertIsNone(rn.get_notes())
        self.assertIsNone(rn.get_properties())
