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


"""
!!! ALL SYMBOLS IN HERE ARE INTERNAL.
Everything might change without any notice.
"""


from hashlib import sha1


def file_sha1sum(filename: str) -> str:
    """
    Generate a SHA1 hash of the provided file.

    Args:
        filename:
            Absolute path to file to hash as `str`

    Returns:
        SHA-1 hash
    """
    h = sha1()  # nosec B303, B324
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            h.update(byte_block)
    return h.hexdigest()
