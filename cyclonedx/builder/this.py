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

"""Representation of this very python library."""

__all__ = []

from ..contrib.this import this_tool as _this_tool, this_component as _this_component

# endregion deprecated re-export

this_component = _this_component
"""
Alias of :class:`_this_component`.

This re-export location is deprecated.
Use ``from ...contrib.this import this_component`` instead.
The exported symbol itself is NOT deprecated - only this import path.

.. deprecated:: next
"""

this_tool = _this_tool
"""
Alias of :class:`_this_tool`.

This re-export location is deprecated.
Use ``from ...contrib.this import this_tool`` instead.
The exported symbol itself is NOT deprecated - only this import path.

.. deprecated:: next
"""

# endregion deprecated re-export
