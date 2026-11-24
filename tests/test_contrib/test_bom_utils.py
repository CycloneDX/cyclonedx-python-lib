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


from datetime import datetime, timezone
from unittest import TestCase

from cyclonedx.contrib.bom.utils import BomDependencyGraphFlatMerger, BomRefDiscriminator
from cyclonedx.model.annotation import Annotation, Annotator
from cyclonedx.model.bom import Bom
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.dependency import Dependency
from cyclonedx.model.service import Service


class TestBomRefDiscriminator(TestCase):

    def test_discriminate_and_reset_manually(self) -> None:
        bomref1 = BomRef('djdlkfjdslkf')
        bomref2 = BomRef('djdlkfjdslkf')
        self.assertEqual(bomref1.value, bomref2.value, 'blank')
        discr = BomRefDiscriminator([bomref1, bomref2])
        self.assertEqual(bomref1.value, bomref2.value, 'init')
        discr.discriminate()
        self.assertNotEqual(bomref1.value, bomref2.value, 'should be discriminated')
        discr.reset()
        self.assertEqual('djdlkfjdslkf', bomref1.value)
        self.assertEqual('djdlkfjdslkf', bomref2.value)

    def test_discriminate_and_reset_with(self) -> None:
        bomref1 = BomRef('djdlkfjdslkf')
        bomref2 = BomRef('djdlkfjdslkf')
        self.assertEqual(bomref1.value, bomref2.value, 'blank')
        discr = BomRefDiscriminator([bomref1, bomref2])
        self.assertEqual(bomref1.value, bomref2.value, 'init')
        with discr:
            self.assertNotEqual(bomref1.value, bomref2.value, 'should be discriminated')
        self.assertEqual('djdlkfjdslkf', bomref1.value)
        self.assertEqual('djdlkfjdslkf', bomref2.value)

    def test_from_bom_with_annotations(self) -> None:
        comp = Component(name='c', type=ComponentType.APPLICATION, bom_ref='dup')
        nested_comp = Component(name='nc', type=ComponentType.APPLICATION, bom_ref='dup-nested')
        annotator_comp = Component(
            name='ac', type=ComponentType.APPLICATION, bom_ref='dup-ac',
            components=[nested_comp]
        )
        annotator_srv = Service(name='as', bom_ref='dup-as')
        annotation1 = Annotation(
            bom_ref='dup',
            subjects=[comp.bom_ref],
            annotator=Annotator(component=annotator_comp),
            timestamp=datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            text='t1'
        )
        annotation2 = Annotation(
            bom_ref='dup-2',
            subjects=[comp.bom_ref],
            annotator=Annotator(service=annotator_srv),
            timestamp=datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            text='t2'
        )
        annotation3 = Annotation(
            bom_ref='dup-nested',
            subjects=[comp.bom_ref],
            annotator=Annotator(component=Component(name='ac2', type=ComponentType.APPLICATION, bom_ref='dup-ac')),
            timestamp=datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            text='t3'
        )
        bom = Bom(components=[comp], annotations=[annotation1, annotation2, annotation3])
        discr = BomRefDiscriminator.from_bom(bom)
        with discr:
            all_refs = [
                comp.bom_ref.value,
                annotation1.bom_ref.value,
                annotator_comp.bom_ref.value,
                nested_comp.bom_ref.value,
                annotation2.bom_ref.value,
                annotator_srv.bom_ref.value,
                annotation3.bom_ref.value,
            ]
            self.assertEqual(len(all_refs), len(set(all_refs)), 'All bom-refs must be unique')
        self.assertEqual(comp.bom_ref.value, 'dup')
        self.assertEqual(annotation1.bom_ref.value, 'dup')
        self.assertEqual(nested_comp.bom_ref.value, 'dup-nested')


class TestBomDependencyGraphFlatMerger(TestCase):

    def test_flatten_merge_and_reset_manually(self) -> None:
        root_bom_ref = BomRef('root_bom_ref')
        component1_bom_ref = BomRef('component1_bom_ref')
        component2_bom_ref = BomRef('component2_bom_ref')
        component3_bom_ref = BomRef('component3_bom_ref')
        component4_bom_ref = BomRef('component4_bom_ref')
        component5_bom_ref = BomRef('component5_bom_ref')
        bom = Bom(dependencies=[
            Dependency(
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
            Dependency(component5_bom_ref, (
                component1_bom_dep,
                component2_bom_dep,
                component2_bom_dep2,
                component3_bom_dep,
                component3_bom_dep2,
                component4_bom_dep,
                component4_bom_dep2,
                Dependency(root_bom_ref)
            ))
        ])
        bom_dependencies = bom.dependencies
        merger = BomDependencyGraphFlatMerger(bom)
        merger.flatten_merge()
        self.assertEqual(6, len(bom.dependencies), 'not expected len()')
        self.assertSetEqual({
            Dependency(root_bom_ref, (Dependency(component1_bom_ref), Dependency(component2_bom_ref))),
            Dependency(component1_bom_ref, (Dependency(component2_bom_ref), )),
            Dependency(component2_bom_ref, (Dependency(component3_bom_ref), Dependency(component4_bom_ref), )),
            Dependency(component3_bom_ref, (Dependency(component4_bom_ref), )),
            Dependency(component4_bom_ref),
            Dependency(component5_bom_ref, (
                Dependency(root_bom_ref),
                Dependency(component1_bom_ref),
                Dependency(component2_bom_ref),
                Dependency(component3_bom_ref),
                Dependency(component4_bom_ref),
            )),
        }, bom.dependencies)
        merger.reset()
        self.assertIs(bom_dependencies, bom.dependencies)
        self.assertSetEqual(bom_dependencies, bom.dependencies)

    def test_flatten_merge_and_reset_with(self) -> None:
        root_bom_ref = BomRef('root_bom_ref')
        component1_bom_ref = BomRef('component1_bom_ref')
        component2_bom_ref = BomRef('component2_bom_ref')
        component3_bom_ref = BomRef('component3_bom_ref')
        component4_bom_ref = BomRef('component4_bom_ref')
        component5_bom_ref = BomRef('component5_bom_ref')
        bom = Bom(dependencies=[
            Dependency(
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
            Dependency(component5_bom_ref, (
                Dependency(root_bom_ref),
                component1_bom_dep,
                component2_bom_dep,
                component2_bom_dep2,
                component3_bom_dep,
                component3_bom_dep2,
                component4_bom_dep,
                component4_bom_dep2,
            ))
        ])
        bom_dependencies = bom.dependencies
        merger = BomDependencyGraphFlatMerger(bom)
        with merger:
            self.assertEqual(6, len(bom.dependencies), 'not expected len()')
            self.assertSetEqual({
                Dependency(root_bom_ref, (Dependency(component1_bom_ref), Dependency(component2_bom_ref))),
                Dependency(component1_bom_ref, (Dependency(component2_bom_ref), )),
                Dependency(component2_bom_ref, (Dependency(component3_bom_ref), Dependency(component4_bom_ref), )),
                Dependency(component3_bom_ref, (Dependency(component4_bom_ref), )),
                Dependency(component4_bom_ref),
                Dependency(component5_bom_ref, (
                    Dependency(root_bom_ref),
                    Dependency(component1_bom_ref),
                    Dependency(component2_bom_ref),
                    Dependency(component3_bom_ref),
                    Dependency(component4_bom_ref),
                )),
            }, bom.dependencies)
        self.assertIs(bom_dependencies, bom.dependencies)
        self.assertSetEqual(bom_dependencies, bom.dependencies)
