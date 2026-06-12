# This file is part of CycloneDX Python Library
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

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
        self.assertFalse(rn.aliases)
        self.assertFalse(rn.tags)
        self.assertFalse(rn.resolves)
        self.assertFalse(rn.notes)
        self.assertFalse(rn.properties)

    def test_complete(self) -> None:
        timestamp: datetime.datetime = datetime.datetime.utcnow()
        rn = ReleaseNotes(
            type='major', title='Release Notes Title',
            featured_image=XsUri('https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'),
            social_image=XsUri('https://cyclonedx.org/cyclonedx-icon.png'),
            description='This release is a test release', timestamp=timestamp,
            aliases=[
                'First Test Release'
            ],
            tags=['test', 'alpha'],
            resolves=[],
            notes=[]
        )
        rn.aliases.add('Release Alpha')
        rn.tags.add('testing')

        self.assertEqual(rn.type, 'major')
        self.assertEqual(rn.title, 'Release Notes Title')
        self.assertEqual(
            str(rn.featured_image),
            'https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'
        )
        self.assertEqual(str(rn.social_image), 'https://cyclonedx.org/cyclonedx-icon.png')
        self.assertEqual(rn.description, 'This release is a test release')
        self.assertSetEqual(rn.aliases, {'Release Alpha', 'First Test Release'})
        self.assertSetEqual(rn.tags, {'test', 'testing', 'alpha'})
        self.assertSetEqual(rn.resolves, set())
        self.assertFalse(rn.notes)
        self.assertSetEqual(rn.properties, set())

    def test_release_notes_sorting(self) -> None:
        """Test that ReleaseNotes instances can be sorted without triggering TypeError"""
        rn1 = ReleaseNotes(type='major', title='Release 1.0')
        rn2 = ReleaseNotes(type='minor', title='Release 1.1')
        rn3 = ReleaseNotes(type='patch', title='Release 1.1.1')

        # This should not raise TypeError: '<' not supported between instances
        rn_list = [rn3, rn1, rn2]
        sorted_rn = sorted(rn_list)
        self.assertEqual(len(sorted_rn), 3)
