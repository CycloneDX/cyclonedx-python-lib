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

import json as _json
import xml.etree.ElementTree as ElementTree  # nosec B405
from unittest import TestCase
from warnings import warn

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.model import AttachedText, Encoding, ExternalReference, ExternalReferenceType, Property, XsUri
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
from tests import reorder


class TestModelCardOnComponent(TestCase):
    """Test cases for ModelCard integration within Component objects."""

    def _make_basic_model_card(self) -> ModelCard:
        """Helper to create a basic ModelCard instance."""
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
        """Test basic ModelCard serialization in BOM 1.5 JSON and XML formats."""
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
        """Test ModelCard with EnvironmentalConsiderations in BOM 1.6 JSON and XML formats."""
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

    def test_model_card_environmental_not_in_v15(self) -> None:
        """Test that EnvironmentalConsiderations are omitted in BOM 1.5 JSON and XML formats."""
        provider = EnergyProvider(
            organization=OrganizationalEntity(name='GridCo'),
            energy_source=EnergySource.SOLAR,
            energy_provided=EnergyMeasure(value=5.0),
        )
        env = EnvironmentalConsiderations(
            energy_consumptions=[
                EnergyConsumption(
                    activity=EnergyActivity.INFERENCE,
                    energy_providers=[provider],
                    activity_energy_cost=EnergyMeasure(value=1.0),
                )
            ]
        )
        mc = self._make_basic_model_card()
        mc.considerations = Considerations(environmental_considerations=env)

        c = Component(name='m', type=ComponentType.MACHINE_LEARNING_MODEL, model_card=mc)
        bom = Bom(components=[c])

        # JSON 1.5 should omit environmentalConsiderations
        json = JSON_BY_SCHEMA_VERSION[SchemaVersion.V1_5](bom).output_as_string(indent=2)
        self.assertIn('"modelCard"', json)
        self.assertNotIn('"environmentalConsiderations"', json)

        # XML 1.5 should omit environmentalConsiderations
        xml = XML_BY_SCHEMA_VERSION[SchemaVersion.V1_5](bom).output_as_string(indent=2)
        self.assertIn('<modelCard>', xml)
        self.assertNotIn('<environmentalConsiderations>', xml)

    def test_model_card_full_v17_json_xml(self) -> None:
        """Test full-featured ModelCard serialization in BOM 1.7 JSON and XML formats."""
        # Build a rich model card with most fields populated
        graphics = QuantitativeAnalysis(
            performance_metrics=[
                PerformanceMetric(
                    type='f1', value='0.88',
                    slice='en',
                    confidence_interval=None,
                ),
                PerformanceMetric(
                    type='accuracy', value='0.95',
                ),
            ],
            graphics=None,
        )

        mc = ModelCard(
            bom_ref='mc-1',
            model_parameters=ModelParameters(
                approach=Approach(type=MachineLearningApproach.UNSUPERVISED),
                task='clustering',
                architecture_family='Transformer',
                model_architecture='X-Transformer',
                inputs=[InputOutputMLParameters(format='text/plain')],
                outputs=[InputOutputMLParameters(format='cluster-id')],
            ),
            quantitative_analysis=graphics,
            considerations=Considerations(
                users=['ml-engineer', 'data-scientist'],
                use_cases=['topic-grouping', 'anomaly-detection'],
                technical_limitations=['small-context', 'limited-training-data'],
                performance_tradeoffs=['speed-over-accuracy', 'low-memory-footprint'],
            ),
            # Test properties serialization via custom helper
            # due to json-xml asymmetry in spec (see model_card.py)
            properties=[Property(name='release', value='2024-01-01')],
        )

        # Add rich environmental considerations
        provider = EnergyProvider(
            bom_ref='prov-1',
            description='Primary renewable provider',
            organization=OrganizationalEntity(name='Wind&Co'),
            energy_source=EnergySource.WIND,
            energy_provided=EnergyMeasure(value=321.0),
            external_references=[
                ExternalReference(
                    type=ExternalReferenceType.EVIDENCE,
                    url=XsUri('https://example.org/energy'),
                )
            ],
        )
        env = EnvironmentalConsiderations(
            energy_consumptions=[
                EnergyConsumption(
                    activity=EnergyActivity.TRAINING,
                    energy_providers=[provider],
                    activity_energy_cost=EnergyMeasure(value=42.0),
                    co2_cost_equivalent=Co2Measure(value=0.7),
                    properties=[Property(name='phase', value='exp1')],
                )
            ],
            properties=[Property(name='footprint', value='low')],
        )
        # Currently users, use_cases, technical_limitations, performance_tradeoffs can only contain one string each
        # in the xml specification. This will be addressed in spec issue #737.
        mc.considerations = Considerations(
            users=['ml-engineer'],
            use_cases=['topic-grouping'],
            technical_limitations=['small-context'],
            performance_tradeoffs=['speed-over-accuracy'],
            environmental_considerations=env,
        )

        # Embed in component and serialize in 1.7
        c = Component(name='advanced-model', type=ComponentType.MACHINE_LEARNING_MODEL, model_card=mc)
        bom = Bom(components=[c])

        # JSON 1.7
        json = JSON_BY_SCHEMA_VERSION[SchemaVersion.V1_7](bom).output_as_string(indent=2)
        try:
            err = JsonStrictValidator(SchemaVersion.V1_7).validate_str(json)
        except MissingOptionalDependencyException:
            warn('!!! skipped schema validation', category=UserWarning, stacklevel=0)
        else:
            self.assertIsNone(err, json)
        self.assertIn('"modelCard"', json)
        self.assertIn('"bom-ref": "mc-1"', json)
        self.assertIn('"environmentalConsiderations"', json)
        self.assertIn('"energyProviders"', json)
        self.assertIn('"bom-ref": "prov-1"', json)

        # Verify JSON/XML asymmetry for modelCard.properties
        # Assert JSON contains modelCard.properties (array of objects)
        j = _json.loads(json)
        self.assertIn('components', j)
        self.assertGreaterEqual(len(j['components']), 1)
        mc_json = j['components'][0].get('modelCard', {})
        self.assertIn('properties', mc_json)
        self.assertIsInstance(mc_json['properties'], list)
        self.assertIn({'name': 'release', 'value': '2024-01-01'}, mc_json['properties'])

        # XML 1.7
        xml = XML_BY_SCHEMA_VERSION[SchemaVersion.V1_7](bom).output_as_string(indent=2)
        try:
            errx = XmlValidator(SchemaVersion.V1_7).validate_str(xml)
        except MissingOptionalDependencyException:
            warn('!!! skipped schema validation', category=UserWarning, stacklevel=0)
        else:
            self.assertIsNone(errx, xml)
        self.assertIn('<modelCard', xml)
        self.assertIn('bom-ref="mc-1"', xml)
        self.assertIn('<environmentalConsiderations>', xml)
        self.assertIn('<energyProviders ', xml)
        self.assertIn('bom-ref="prov-1"', xml)

        # XML omits properties under <modelCard>, nested ones remain
        root = ElementTree.fromstring(xml)  # nosec B314
        ns = {'bom': 'http://cyclonedx.org/schema/bom/1.7'}
        model_card_e = root.find('.//bom:modelCard', ns)
        self.assertIsNotNone(model_card_e)
        # No direct <properties> child under modelCard (JSON/XML asymmetry workaround)
        self.assertIsNone(model_card_e.find('bom:properties', ns))
        # But nested properties (e.g., under environmentalConsiderations) do exist
        env_props = root.findall('.//bom:environmentalConsiderations/bom:properties', ns)
        self.assertGreaterEqual(len(env_props), 1)


class TestModelCardValueObjects(TestCase):
    """Test cases for value objects within the ModelCard data structures."""

    def test_approach_sort(self) -> None:
        """Test sorting of Approach instances based on MachineLearningApproach enum values."""
        a = [
            Approach(type=MachineLearningApproach.SUPERVISED),
            Approach(type=MachineLearningApproach.UNSUPERVISED),
            Approach(type=MachineLearningApproach.REINFORCEMENT_LEARNING),
        ]
        # expected order: by enum value
        expected = reorder(a, [2, 0, 1])
        self.assertListEqual(sorted(a), expected)

    def test_io_params_sort(self) -> None:
        """Test sorting of InputOutputMLParameters by format string."""
        items = [
            InputOutputMLParameters(format='b'),
            InputOutputMLParameters(format='a'),
        ]
        expected = reorder(items, [1, 0])
        self.assertListEqual(sorted(items), expected)

    def test_graphic_and_text(self) -> None:
        """Test AttachedText and PerformanceMetric equality and sorting."""
        img_a = AttachedText(content='imgA', content_type='image/png', encoding=Encoding.BASE_64)
        img_b = AttachedText(content='imgB')
        g1 = PerformanceMetric(type='acc', value='0.9')
        g2 = PerformanceMetric(type='f1', value='0.8')
        qa1 = QuantitativeAnalysis(performance_metrics=[g1, g2])
        self.assertEqual(len(qa1.performance_metrics), 2)
        # Ensure AttachedText sorting is stable via imported tests for AttachedText
        self.assertNotEqual(img_a, img_b)


class TestModelCardContainers(TestCase):
    """Test cases for container objects within the ModelCard data structures."""

    def test_model_parameters_equality(self) -> None:
        """Test equality comparison of ModelParameters instances."""
        mp1 = ModelParameters(
            approach=Approach(type=MachineLearningApproach.SELF_SUPERVISED),
            task='t',
            architecture_family='fam',
            model_architecture='arch',
            inputs=[InputOutputMLParameters(format='x')],
            outputs=[InputOutputMLParameters(format='y')],
        )
        mp2 = ModelParameters(
            approach=Approach(type=MachineLearningApproach.SELF_SUPERVISED),
            task='t',
            architecture_family='fam',
            model_architecture='arch',
            inputs=[InputOutputMLParameters(format='x')],
            outputs=[InputOutputMLParameters(format='y')],
        )
        self.assertEqual(mp1, mp2)

    def test_model_card_equality_and_sort(self) -> None:
        """Test equality and sorting of ModelCard instances."""
        mc1 = ModelCard(bom_ref='a', model_parameters=ModelParameters(task='a'))
        mc2 = ModelCard(bom_ref='a', model_parameters=ModelParameters(task='a'))
        mc3 = ModelCard(bom_ref='b', model_parameters=ModelParameters(task='a'))
        self.assertEqual(hash(mc1), hash(mc2))
        self.assertEqual(mc1, mc2)
        # sort by bom-ref then nested fields
        sorted_list = sorted([mc3, mc1])
        self.assertListEqual(sorted_list, [mc1, mc3])


class TestModelCardEnvironmental(TestCase):
    """Test cases for EnvironmentalConsiderations related value objects."""

    def test_energy_measure_equality(self) -> None:
        """Test equality comparison of EnergyMeasure instances."""
        e1 = EnergyMeasure(value=1.0)
        e2 = EnergyMeasure(value=1.0)
        self.assertEqual(e1, e2)

    def test_energy_provider_sort(self) -> None:
        """Test sorting of EnergyProvider instances by bom-ref and other fields."""
        org = OrganizationalEntity(name='Org')
        p1 = EnergyProvider(organization=org, energy_source=EnergySource.COAL,
                            energy_provided=EnergyMeasure(value=1.0), bom_ref='a')
        p2 = EnergyProvider(organization=org, energy_source=EnergySource.OIL,
                            energy_provided=EnergyMeasure(value=1.0), bom_ref='b')
        p3 = EnergyProvider(organization=org, energy_source=EnergySource.WIND,
                            energy_provided=EnergyMeasure(value=2.0), bom_ref='a')
        # Comparable tuple uses bom-ref first
        expected = reorder([p1, p2, p3], [0, 2, 1])
        self.assertListEqual(sorted([p2, p3, p1]), expected)

    def test_energy_consumption_sort(self) -> None:
        """Test sorting of EnergyConsumption instances by energy providers and other fields."""
        org = OrganizationalEntity(name='GridCo')
        prov_a = EnergyProvider(organization=org, energy_source=EnergySource.WIND,
                                energy_provided=EnergyMeasure(value=1.0))
        prov_b = EnergyProvider(organization=org, energy_source=EnergySource.SOLAR,
                                energy_provided=EnergyMeasure(value=2.0))

        c1 = EnergyConsumption(
            activity=EnergyActivity.TRAINING,
            energy_providers=[prov_a],
            activity_energy_cost=EnergyMeasure(value=10.0),
        )
        c2 = EnergyConsumption(
            activity=EnergyActivity.TRAINING,
            energy_providers=[prov_b],
            activity_energy_cost=EnergyMeasure(value=10.0),
        )
        # energy_providers affects ordering
        # Solar providers sort before Wind providers
        expected = reorder([c1, c2], [1, 0])
        self.assertListEqual(sorted([c2, c1]), expected)
