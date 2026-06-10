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


from unittest import TestCase

from cyclonedx.contrib.bom.utils import BomDependencyGraphFlatMerger
from cyclonedx.model.bom import Bom
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.dependency import Dependency


class TestBomDependencyGraphFlatMerger(TestCase):

    def test_flatten_merge_and_reset_manually(self) -> None:
        root_bom_ref = BomRef('root_bom_ref')
        component1_bom_ref = BomRef('component1_bom_ref')
        component2_bom_ref = BomRef('component2_bom_ref')
        component3_bom_ref = BomRef() # unassigned value
        component4_bom_ref = BomRef() # unassigned value
        bom = Bom(dependencies=[
            root_bom_dep := Dependency(
                root_bom_ref,
                dependencies=[
                    component1_bom_dep := Dependency(
                        component1_bom_ref,
                        dependencies=[
                            component2_bom_dep := Dependency(
                                component2_bom_ref,
                               dependencies=[
                                   component3_bom_dep := Dependency(component3_bom_ref),
                               ]
                           ),
                        ]
                    ),
                    component2_bom_dep2 := Dependency(
                        component2_bom_ref,
                        dependencies=[
                            component4_bom_dep := Dependency(component4_bom_ref),
                        ]
                    ),
                ]
            ),
            component3_bom_dep2 := Dependency(
               component3_bom_ref,
               dependencies=[
                   component4_bom_dep2 := Dependency(component4_bom_ref),
               ]
           ),
        ])
        bom_dependencies = bom.dependencies
        merger = BomDependencyGraphFlatMerger(bom)
        merger.flatten_merge()
        # TODO: assert dependencies flattened
        merger.reset()
        self.assertIs(bom_dependencies, bom.dependencies)
        # TODO: assert dependencies is unaltered

    def test_flatten_merge_and_reset_with(self) -> None:
        bom = Bom()
        merger = BomDependencyGraphFlatMerger(bom)
        with merger:
            pass # TODO: assert dependencies flattened
        # TODO: assert dependencies resetted
