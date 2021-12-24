import datetime
from unittest import TestCase

from cyclonedx.model import XsUri
from cyclonedx.model.release_note import ReleaseNotes


class TestModelReleaseNote(TestCase):

    def test_simple(self) -> None:
        rn = ReleaseNotes(type='major')
        self.assertEqual(rn.type, 'major')
        self.assertIsNone(rn.title)
        self.assertIsNone(rn.featured_image)
        self.assertIsNone(rn.social_image)
        self.assertIsNone(rn.description)
        self.assertIsNone(rn.timestamp)
        self.assertIsNone(rn.aliases)
        self.assertIsNone(rn.tags)
        self.assertIsNone(rn.resolves)
        self.assertIsNone(rn.notes)
        self.assertIsNone(rn.properties)

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
            notes=[]
        )
        rn.add_alias(alias="Release Alpha")
        rn.add_tag(tag='testing')

        self.assertEqual(rn.type, 'major')
        self.assertEqual(rn.title, 'Release Notes Title')
        self.assertEqual(
            rn.featured_image,
            'https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'
        )
        self.assertEqual(rn.social_image, 'https://cyclonedx.org/cyclonedx-icon.png')
        self.assertEqual(rn.description, 'This release is a test release')
        self.assertListEqual(rn.aliases, ["First Test Release", "Release Alpha"])
        self.assertListEqual(rn.tags, ['test', 'alpha', 'testing'])
        self.assertIsNone(rn.resolves)
        self.assertIsNone(rn.notes)
        self.assertIsNone(rn.properties)
