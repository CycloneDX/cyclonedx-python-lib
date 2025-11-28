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

__all__ = ['this_component', 'this_tool', ]

from ..contrib.this import this_component as _this_component, this_tool as _this_tool

# endregion deprecated re-export

this_component = _this_component
"""Deprecated — Alias of :func:`cyclonedx.contrib.this.this_component`.

.. deprecated:: next
    This re-export location is deprecated.
    Use ``from cyclonedx.contrib.this import this_component`` instead.
    The exported symbol itself is NOT deprecated - only this import path.
"""

this_tool = _this_tool
"""Deprecated — Alias of :func:`cyclonedx.contrib.this.this_tool`.

.. deprecated:: next
    This re-export location is deprecated.
    Use ``from cyclonedx.contrib.this import this_tool`` instead.
    The exported symbol itself is NOT deprecated - only this import path.
"""

# endregion deprecated re-export
