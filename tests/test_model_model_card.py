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
from warnings import warn

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.contact import OrganizationalEntity
from cyclonedx.model.model_card import (
    Approach,
    Co2Measure,
    Considerations,
    EnergyActivity,
    EnergyConsumption,
    EnergyMeasure,
    EnergyProvider,
    EnergySource,
    EnvironmentalConsiderations,
    InputOutputMLParameters,
    MachineLearningApproach,
    ModelCard,
    ModelParameters,
    PerformanceMetric,
    QuantitativeAnalysis,
)
from cyclonedx.output.json import BY_SCHEMA_VERSION as JSON_BY_SCHEMA_VERSION
from cyclonedx.output.xml import BY_SCHEMA_VERSION as XML_BY_SCHEMA_VERSION
from cyclonedx.schema import SchemaVersion
from cyclonedx.validation.json import JsonStrictValidator
from cyclonedx.validation.xml import XmlValidator


class TestModelCardOnComponent(TestCase):

    def _make_basic_model_card(self) -> ModelCard:
        return ModelCard(
            model_parameters=ModelParameters(
                approach=Approach(type=MachineLearningApproach.SUPERVISED),
                task='classification',
                architecture_family='Transformer',
                model_architecture='Tiny-Transformer',
                inputs=[InputOutputMLParameters(format='text')],
                outputs=[InputOutputMLParameters(format='label')],
            ),
            quantitative_analysis=QuantitativeAnalysis(
                performance_metrics=[PerformanceMetric(type='accuracy', value='0.95')]
            ),
            considerations=Considerations(
                users=['ml-engineer'],
                use_cases=['spam-detection'],
            ),
        )

    def test_model_card_basic_v15_json_xml(self) -> None:
        mc = self._make_basic_model_card()
        c = Component(name='mymodel', type=ComponentType.MACHINE_LEARNING_MODEL, model_card=mc)
        bom = Bom(components=[c])

        # JSON 1.5
        json = JSON_BY_SCHEMA_VERSION[SchemaVersion.V1_5](bom).output_as_string(indent=2)
        try:
            err = JsonStrictValidator(SchemaVersion.V1_5).validate_str(json)
        except MissingOptionalDependencyException:
            warn('!!! skipped schema validation', category=UserWarning, stacklevel=0)
        else:
            self.assertIsNone(err, json)
        self.assertIn('"modelCard"', json)

        # XML 1.5
        xml = XML_BY_SCHEMA_VERSION[SchemaVersion.V1_5](bom).output_as_string(indent=2)
        try:
            errx = XmlValidator(SchemaVersion.V1_5).validate_str(xml)
        except MissingOptionalDependencyException:
            warn('!!! skipped schema validation', category=UserWarning, stacklevel=0)
        else:
            self.assertIsNone(errx, xml)
        self.assertIn('<modelCard>', xml)

    def test_model_card_environmental_v16_json_xml(self) -> None:
        provider = EnergyProvider(
            organization=OrganizationalEntity(name='GridCo'),
            energy_source=EnergySource.WIND,
            energy_provided=EnergyMeasure(value=123.4),
        )
        consumption = EnergyConsumption(
            activity=EnergyActivity.TRAINING,
            energy_providers=[provider],
            activity_energy_cost=EnergyMeasure(value=12.0),
            co2_cost_equivalent=Co2Measure(value=0.5),
        )
        env = EnvironmentalConsiderations(energy_consumptions=[consumption])

        mc = self._make_basic_model_card()
        # add environmental considerations (1.6+ only)
        mc.considerations = Considerations(environmental_considerations=env)

        c = Component(name='mymodel', type=ComponentType.MACHINE_LEARNING_MODEL, model_card=mc)
        bom = Bom(components=[c])

        # JSON 1.6
        json = JSON_BY_SCHEMA_VERSION[SchemaVersion.V1_6](bom).output_as_string(indent=2)
        try:
            err = JsonStrictValidator(SchemaVersion.V1_6).validate_str(json)
        except MissingOptionalDependencyException:
            warn('!!! skipped schema validation', category=UserWarning, stacklevel=0)
        else:
            self.assertIsNone(err, json)
        self.assertIn('"environmentalConsiderations"', json)

        # XML 1.6
        xml = XML_BY_SCHEMA_VERSION[SchemaVersion.V1_6](bom).output_as_string(indent=2)
        try:
            errx = XmlValidator(SchemaVersion.V1_6).validate_str(xml)
        except MissingOptionalDependencyException:
            warn('!!! skipped schema validation', category=UserWarning, stacklevel=0)
        else:
            self.assertIsNone(errx, xml)
        self.assertIn('<environmentalConsiderations>', xml)
