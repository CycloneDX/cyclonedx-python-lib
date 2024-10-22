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

from typing import Optional, Union

from ..model.bom_ref import BomRef


def bom_ref_from_str(bom_ref: Optional[Union[str, BomRef]]) -> BomRef:
    if isinstance(bom_ref, BomRef):
        return bom_ref
    else:
        return BomRef(value=str(bom_ref) if bom_ref else None)
