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

from cyclonedx.model import ExternalReference, ExternalReferenceType, Property
from cyclonedx.model.contact import OrganizationalEntity
from cyclonedx.model.model_card import (
    Approach,
    Co2Measure,
    Co2MeasureUnit,
    ConfidenceInterval,
    Considerations,
    EnergyActivity,
    EnergyConsumption,
    EnergyMeasure,
    EnergyMeasureUnit,
    EnergyProvider,
    EnergySource,
    EnvironmentalConsiderations,
    EthicalConsideration,
    FairnessAssessment,
    Graphic,
    GraphicsCollection,
    InputOutputMLParameters,
    MachineLearningApproach,
    ModelCard,
    ModelParameters,
    PerformanceMetric,
    QuantitativeAnalysis,
)
from tests import reorder


class TestCo2MeasureUnit(TestCase):

    def test_enum_value(self) -> None:
        self.assertEqual(Co2MeasureUnit.TCO2EQ.value, 'tCO2eq')

    def test_enum_comparison(self) -> None:
        self.assertEqual(Co2MeasureUnit.TCO2EQ, Co2MeasureUnit('tCO2eq'))


class TestEnergyMeasureUnit(TestCase):

    def test_enum_value(self) -> None:
        self.assertEqual(EnergyMeasureUnit.KWH.value, 'kWh')

    def test_enum_comparison(self) -> None:
        self.assertEqual(EnergyMeasureUnit.KWH, EnergyMeasureUnit('kWh'))


class TestMachineLearningApproach(TestCase):

    def test_all_values_exist(self) -> None:
        self.assertEqual(
            {
                MachineLearningApproach.SUPERVISED.value,
                MachineLearningApproach.UNSUPERVISED.value,
                MachineLearningApproach.REINFORCEMENT_LEARNING.value,
                MachineLearningApproach.SEMI_SUPERVISED.value,
                MachineLearningApproach.SELF_SUPERVISED.value,
            },
            {
                'supervised',
                'unsupervised',
                'reinforcement-learning',
                'semi-supervised',
                'self-supervised',
            },
        )


class TestApproach(TestCase):
    def test_create(self) -> None:
        approach_sup = Approach(type=MachineLearningApproach.SUPERVISED)
        approach_unsup = Approach(type=MachineLearningApproach.UNSUPERVISED)
        approach_reinf = Approach(type=MachineLearningApproach.REINFORCEMENT_LEARNING)
        approach_semi = Approach(type=MachineLearningApproach.SEMI_SUPERVISED)
        approach_self = Approach(type=MachineLearningApproach.SELF_SUPERVISED)
        self.assertIs(MachineLearningApproach.SUPERVISED, approach_sup.type)
        self.assertIs(MachineLearningApproach.UNSUPERVISED, approach_unsup.type)
        self.assertIs(MachineLearningApproach.REINFORCEMENT_LEARNING, approach_reinf.type)
        self.assertIs(MachineLearningApproach.SEMI_SUPERVISED, approach_semi.type)
        self.assertIs(MachineLearningApproach.SELF_SUPERVISED, approach_self.type)

    def test_update(self) -> None:
        approach = Approach(type=MachineLearningApproach.SUPERVISED)
        self.assertIs(MachineLearningApproach.SUPERVISED, approach.type)
        approach.type = MachineLearningApproach.UNSUPERVISED
        self.assertIs(MachineLearningApproach.UNSUPERVISED, approach.type)

    def test_sort(self) -> None:
        expected_order = [4, 3, 2, 1, 0]
        approaches = [
            Approach(type=MachineLearningApproach.UNSUPERVISED),
            Approach(type=MachineLearningApproach.SUPERVISED),
            Approach(type=MachineLearningApproach.SEMI_SUPERVISED),
            Approach(type=MachineLearningApproach.SELF_SUPERVISED),
            Approach(type=MachineLearningApproach.REINFORCEMENT_LEARNING),
        ]
        expected_approaches = reorder(approaches, expected_order)
        sorted_approaches = sorted(approaches)
        self.assertListEqual(sorted_approaches, expected_approaches)

    def test_no_params(self) -> None:
        approach = Approach()
        self.assertIsNone(approach.type)

    def test_same(self) -> None:
        approach_1 = Approach(type=MachineLearningApproach.SUPERVISED)
        approach_2 = Approach(type=MachineLearningApproach.SUPERVISED)

        self.assertNotEqual(id(approach_1), id(approach_2))
        self.assertEqual(hash(approach_1), hash(approach_2))
        self.assertTrue(approach_1 == approach_2)

    def test_not_same(self) -> None:
        approach_1 = Approach(type=MachineLearningApproach.SUPERVISED)
        approach_2 = Approach(type=MachineLearningApproach.UNSUPERVISED)

        self.assertNotEqual(hash(approach_1), hash(approach_2))
        self.assertFalse(approach_1 == approach_2)

    def test_compare_same_type(self) -> None:
        approach_1 = Approach(type=MachineLearningApproach.SUPERVISED)
        approach_2 = Approach(type=MachineLearningApproach.SUPERVISED)

        self.assertFalse(approach_1 < approach_2)
        self.assertTrue(approach_1 <= approach_2)
        self.assertTrue(approach_1 >= approach_2)

    def test_repr(self) -> None:
        approach = Approach(type=MachineLearningApproach.SUPERVISED)

        # 3.10 returns the value, 3.11+ returns the enum member name; accept both
        self.assertIn(
            repr(approach),
            {
                '<Approach type=MachineLearningApproach.SUPERVISED>',
                '<Approach type=supervised>',
            },
        )


class TestInputOutputMLParameters(TestCase):

    def test_constructor_and_property(self) -> None:
        obj = InputOutputMLParameters(format='JSON')

        self.assertEqual(obj.format, 'JSON')

    def test_setter(self) -> None:
        obj = InputOutputMLParameters(format='JSON')

        obj.format = 'CSV'

        self.assertEqual(obj.format, 'CSV')

    def test_equality(self) -> None:
        self.assertEqual(
            InputOutputMLParameters(format='JSON'),
            InputOutputMLParameters(format='JSON'),
        )

    def test_inequality(self) -> None:
        self.assertNotEqual(
            InputOutputMLParameters(format='JSON'),
            InputOutputMLParameters(format='CSV'),
        )

    def test_comparison(self) -> None:
        first = InputOutputMLParameters(format='CSV')
        second = InputOutputMLParameters(format='JSON')

        self.assertTrue(first < second)
        self.assertTrue(first <= second)
        self.assertTrue(second >= first)

    def test_hash(self) -> None:
        self.assertEqual(
            hash(InputOutputMLParameters(format='JSON')),
            hash(InputOutputMLParameters(format='JSON')),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(InputOutputMLParameters(format='JSON')),
            "<IOParam format='JSON'>",
        )


class TestModelParameters(TestCase):

    def test_defaults(self) -> None:
        obj = ModelParameters()

        self.assertIsNone(obj.approach)
        self.assertIsNone(obj.task)
        self.assertEqual(len(obj.inputs), 0)
        self.assertEqual(len(obj.outputs), 0)

    def test_constructor(self) -> None:
        input_param = InputOutputMLParameters(format='JSON')
        output_param = InputOutputMLParameters(format='TEXT')

        obj = ModelParameters(
            task='classification',
            architecture_family='transformer',
            model_architecture='bert',
            inputs=[input_param],
            outputs=[output_param],
        )

        self.assertEqual(obj.task, 'classification')
        self.assertEqual(obj.architecture_family, 'transformer')
        self.assertEqual(obj.model_architecture, 'bert')
        self.assertIn(input_param, obj.inputs)
        self.assertIn(output_param, obj.outputs)

    def test_property_setters(self) -> None:
        obj = ModelParameters()

        obj.task = 'generation'
        obj.architecture_family = 'cnn'
        obj.model_architecture = 'resnet'

        self.assertEqual(obj.task, 'generation')
        self.assertEqual(obj.architecture_family, 'cnn')
        self.assertEqual(obj.model_architecture, 'resnet')

    def test_dataset_not_supported(self) -> None:
        with self.assertRaises(NotImplementedError):
            ModelParameters(datasets=['dataset'])

    def test_sorted_input_collection(self) -> None:
        first = InputOutputMLParameters(format='A')
        second = InputOutputMLParameters(format='B')

        obj = ModelParameters(inputs=[second, first])

        self.assertEqual(
            list(obj.inputs),
            [first, second],
        )

    def test_equality(self) -> None:
        self.assertEqual(
            ModelParameters(task='test'),
            ModelParameters(task='test'),
        )

    def test_inequality(self) -> None:
        self.assertNotEqual(
            ModelParameters(task='a'),
            ModelParameters(task='b'),
        )

    def test_comparison(self) -> None:
        first = ModelParameters(task='a')
        second = ModelParameters(task='b')

        self.assertTrue(first < second)
        self.assertTrue(first <= second)
        self.assertTrue(second >= first)

    def test_hash(self) -> None:
        self.assertEqual(
            hash(ModelParameters(task='test')),
            hash(ModelParameters(task='test')),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(ModelParameters(task='classification')),
            "<ModelParameters task='classification' arch=None>",
        )


class TestConfidenceInterval(TestCase):

    def test_defaults(self) -> None:
        obj = ConfidenceInterval()

        self.assertIsNone(obj.lower_bound)
        self.assertIsNone(obj.upper_bound)

    def test_constructor(self) -> None:
        obj = ConfidenceInterval(
            lower_bound='0.8',
            upper_bound='0.9',
        )

        self.assertEqual(obj.lower_bound, '0.8')
        self.assertEqual(obj.upper_bound, '0.9')

    def test_setters(self) -> None:
        obj = ConfidenceInterval()

        obj.lower_bound = '0.1'
        obj.upper_bound = '0.2'

        self.assertEqual(obj.lower_bound, '0.1')
        self.assertEqual(obj.upper_bound, '0.2')

    def test_equality(self) -> None:
        self.assertEqual(
            ConfidenceInterval(
                lower_bound='0.1',
                upper_bound='0.2',
            ),
            ConfidenceInterval(
                lower_bound='0.1',
                upper_bound='0.2',
            ),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            ConfidenceInterval(
                lower_bound='0.1',
                upper_bound='0.2',
            )
            < ConfidenceInterval(
                lower_bound='0.2',
                upper_bound='0.3',
            )
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(ConfidenceInterval(
                lower_bound='0.1',
                upper_bound='0.2',
            )),
            hash(ConfidenceInterval(
                lower_bound='0.1',
                upper_bound='0.2',
            )),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(ConfidenceInterval(
                lower_bound='0.1',
                upper_bound='0.2',
            )),
            '<ConfidenceInterval 0.1,0.2>',
        )


class TestPerformanceMetric(TestCase):

    def test_constructor(self) -> None:
        interval = ConfidenceInterval(
            lower_bound='0.8',
            upper_bound='0.9',
        )

        obj = PerformanceMetric(
            type='accuracy',
            value='0.95',
            slice_='test',
            confidence_interval=interval,
        )

        self.assertEqual(obj.type, 'accuracy')
        self.assertEqual(obj.value, '0.95')
        self.assertEqual(obj.slice_, 'test')
        self.assertEqual(obj.confidence_interval, interval)

    def test_setters(self) -> None:
        obj = PerformanceMetric()

        obj.type = 'precision'
        obj.value = '0.8'

        self.assertEqual(obj.type, 'precision')
        self.assertEqual(obj.value, '0.8')

    def test_equality(self) -> None:
        self.assertEqual(
            PerformanceMetric(type='accuracy', value='1'),
            PerformanceMetric(type='accuracy', value='1'),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            PerformanceMetric(type='a')
            < PerformanceMetric(type='b')
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(PerformanceMetric(type='accuracy')),
            hash(PerformanceMetric(type='accuracy')),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(PerformanceMetric(type='accuracy', value='1')),
            "<PerformanceMetric type='accuracy' value='1'>",
        )


class TestGraphic(TestCase):

    def test_constructor(self) -> None:
        obj = Graphic(name='plot')

        self.assertEqual(obj.name, 'plot')
        self.assertIsNone(obj.image)

    def test_setters(self) -> None:
        obj = Graphic()

        obj.name = 'chart'

        self.assertEqual(obj.name, 'chart')

    def test_equality(self) -> None:
        self.assertEqual(
            Graphic(name='a'),
            Graphic(name='a'),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            Graphic(name='a')
            < Graphic(name='b')
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(Graphic(name='a')),
            hash(Graphic(name='a')),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(Graphic(name='chart')),
            "<Graphic name='chart'>",
        )


class TestGraphicsCollection(TestCase):

    def test_defaults(self) -> None:
        obj = GraphicsCollection()

        self.assertEqual(len(obj.collection), 0)

    def test_constructor(self) -> None:
        graphics = [
            Graphic(name='b'),
            Graphic(name='a'),
        ]

        obj = GraphicsCollection(
            description='images',
            collection=graphics,
        )

        self.assertEqual(obj.description, 'images')
        self.assertEqual(
            list(obj.collection),
            sorted(graphics),
        )

    def test_sorted_collection(self) -> None:
        obj = GraphicsCollection(
            collection=[
                Graphic(name='b'),
                Graphic(name='a'),
            ]
        )

        self.assertEqual(
            [g.name for g in obj.collection],
            ['a', 'b'],
        )

    def test_equality(self) -> None:
        self.assertEqual(
            GraphicsCollection(description='x'),
            GraphicsCollection(description='x'),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            GraphicsCollection(description='a')
            < GraphicsCollection(description='b')
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(GraphicsCollection(description='x')),
            hash(GraphicsCollection(description='x')),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(GraphicsCollection()),
            '<GraphicsCollection count=0>',
        )


class TestQuantitativeAnalysis(TestCase):

    def test_defaults(self) -> None:
        obj = QuantitativeAnalysis()

        self.assertEqual(len(obj.performance_metrics), 0)
        self.assertIsNone(obj.graphics)

    def test_constructor(self) -> None:
        metric = PerformanceMetric(
            type='accuracy',
            value='0.9',
        )
        graphics = GraphicsCollection(description='plots')

        obj = QuantitativeAnalysis(
            performance_metrics=[metric],
            graphics=graphics,
        )

        self.assertIn(metric, obj.performance_metrics)
        self.assertEqual(obj.graphics, graphics)

    def test_sorted_metrics(self) -> None:
        first = PerformanceMetric(type='a')
        second = PerformanceMetric(type='b')

        obj = QuantitativeAnalysis(
            performance_metrics=[second, first],
        )

        self.assertEqual(
            list(obj.performance_metrics),
            [first, second],
        )

    def test_setter(self) -> None:
        obj = QuantitativeAnalysis()

        obj.graphics = GraphicsCollection()

        self.assertIsNotNone(obj.graphics)

    def test_equality(self) -> None:
        self.assertEqual(
            QuantitativeAnalysis(),
            QuantitativeAnalysis(),
        )

    def test_comparison(self) -> None:
        first = QuantitativeAnalysis(
            performance_metrics=[PerformanceMetric(type='a')]
        )
        second = QuantitativeAnalysis(
            performance_metrics=[PerformanceMetric(type='b')]
        )

        self.assertTrue(first < second)

    def test_hash(self) -> None:
        self.assertEqual(
            hash(QuantitativeAnalysis()),
            hash(QuantitativeAnalysis()),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(QuantitativeAnalysis()),
            '<QuantitativeAnalysis metrics=0>',
        )


class TestEthicalConsideration(TestCase):

    def test_defaults(self) -> None:
        obj = EthicalConsideration()

        self.assertIsNone(obj.name)
        self.assertIsNone(obj.mitigation_strategy)

    def test_constructor(self) -> None:
        obj = EthicalConsideration(
            name='privacy',
            mitigation_strategy='anonymization',
        )

        self.assertEqual(obj.name, 'privacy')
        self.assertEqual(obj.mitigation_strategy, 'anonymization')

    def test_setters(self) -> None:
        obj = EthicalConsideration()

        obj.name = 'fairness'
        obj.mitigation_strategy = 'bias monitoring'

        self.assertEqual(obj.name, 'fairness')
        self.assertEqual(obj.mitigation_strategy, 'bias monitoring')

    def test_equality(self) -> None:
        self.assertEqual(
            EthicalConsideration(
                name='a',
                mitigation_strategy='b',
            ),
            EthicalConsideration(
                name='a',
                mitigation_strategy='b',
            ),
        )

    def test_inequality(self) -> None:
        self.assertNotEqual(
            EthicalConsideration(
                name='a',
                mitigation_strategy='b',
            ),
            EthicalConsideration(
                name='a',
                mitigation_strategy='c',
            ),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            EthicalConsideration(name='a')
            < EthicalConsideration(name='b')
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(EthicalConsideration(name='a')),
            hash(EthicalConsideration(name='a')),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(EthicalConsideration(name='privacy')),
            "<EthicalConsideration name='privacy'>",
        )


class TestFairnessAssessment(TestCase):

    def test_defaults(self) -> None:
        obj = FairnessAssessment()

        self.assertIsNone(obj.group_at_risk)
        self.assertIsNone(obj.benefits)
        self.assertIsNone(obj.harms)
        self.assertIsNone(obj.mitigation_strategy)

    def test_constructor(self) -> None:
        obj = FairnessAssessment(
            group_at_risk='users',
            benefits='equal outcomes',
            harms='bias',
            mitigation_strategy='retraining',
        )

        self.assertEqual(obj.group_at_risk, 'users')
        self.assertEqual(obj.benefits, 'equal outcomes')
        self.assertEqual(obj.harms, 'bias')
        self.assertEqual(obj.mitigation_strategy, 'retraining')

    def test_setters(self) -> None:
        obj = FairnessAssessment()

        obj.group_at_risk = 'group'

        self.assertEqual(obj.group_at_risk, 'group')

    def test_equality(self) -> None:
        self.assertEqual(
            FairnessAssessment(group_at_risk='a'),
            FairnessAssessment(group_at_risk='a'),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            FairnessAssessment(group_at_risk='a')
            < FairnessAssessment(group_at_risk='b')
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(FairnessAssessment(group_at_risk='a')),
            hash(FairnessAssessment(group_at_risk='a')),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(FairnessAssessment(group_at_risk='users')),
            "<FairnessAssessment group_at_risk='users'>",
        )


class TestEnvironmentalConsiderations(TestCase):

    def test_defaults(self) -> None:
        obj = EnvironmentalConsiderations()

        self.assertEqual(len(obj.energy_consumptions), 0)
        self.assertEqual(len(obj.properties), 0)

    def test_constructor(self) -> None:
        obj = EnvironmentalConsiderations(
            energy_consumptions=[],
            properties=[],
        )

        self.assertEqual(len(obj.energy_consumptions), 0)
        self.assertEqual(len(obj.properties), 0)

    def test_sorted_properties(self) -> None:
        prop_a = Property(name='a', value='1')
        prop_b = Property(name='b', value='2')

        obj = EnvironmentalConsiderations(
            properties=[prop_b, prop_a],
        )

        self.assertEqual(
            list(obj.properties),
            [prop_a, prop_b],
        )

    def test_energy_consumptions(self) -> None:
        consumption = EnergyConsumption(
            activity=EnergyActivity.TRAINING,
            energy_providers=[],
            activity_energy_cost=EnergyMeasure(value=10),
        )

        obj = EnvironmentalConsiderations(
            energy_consumptions=[consumption],
        )

        self.assertIn(consumption, obj.energy_consumptions)

    def test_equality(self) -> None:
        self.assertEqual(
            EnvironmentalConsiderations(),
            EnvironmentalConsiderations(),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            EnvironmentalConsiderations()
            <= EnvironmentalConsiderations()
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(EnvironmentalConsiderations()),
            hash(EnvironmentalConsiderations()),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(EnvironmentalConsiderations()),
            '<EnvironmentalConsiderations energies=0>',
        )


class TestEnergyActivity(TestCase):

    def test_values_exist(self) -> None:
        self.assertEqual(
            EnergyActivity.TRAINING.value,
            'training',
        )

        self.assertEqual(
            EnergyActivity.INFERENCE.value,
            'inference',
        )


class TestEnergyMeasure(TestCase):

    def test_defaults(self) -> None:
        obj = EnergyMeasure(value=10.5)

        self.assertEqual(obj.value, 10.5)
        self.assertEqual(obj.unit, EnergyMeasureUnit.KWH)

    def test_constructor(self) -> None:
        obj = EnergyMeasure(
            value=20,
            unit=EnergyMeasureUnit.KWH,
        )

        self.assertEqual(obj.value, 20)

    def test_setters(self) -> None:
        obj = EnergyMeasure(value=1)

        obj.value = 5

        self.assertEqual(obj.value, 5)

    def test_equality(self) -> None:
        self.assertEqual(
            EnergyMeasure(value=1),
            EnergyMeasure(value=1),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            EnergyMeasure(value=1)
            < EnergyMeasure(value=2)
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(EnergyMeasure(value=1)),
            hash(EnergyMeasure(value=1)),
        )

    def test_repr(self) -> None:
        self.assertIn(
            'EnergyMeasure',
            repr(EnergyMeasure(value=1)),
        )


class TestCo2Measure(TestCase):

    def test_defaults(self) -> None:
        obj = Co2Measure(value=1.5)

        self.assertEqual(obj.value, 1.5)
        self.assertEqual(obj.unit, Co2MeasureUnit.TCO2EQ)

    def test_constructor(self) -> None:
        obj = Co2Measure(
            value=10,
            unit=Co2MeasureUnit.TCO2EQ,
        )

        self.assertEqual(obj.value, 10)

    def test_setters(self) -> None:
        obj = Co2Measure(value=1)

        obj.value = 2

        self.assertEqual(obj.value, 2)

    def test_equality(self) -> None:
        self.assertEqual(
            Co2Measure(value=1),
            Co2Measure(value=1),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            Co2Measure(value=1)
            < Co2Measure(value=2)
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(Co2Measure(value=1)),
            hash(Co2Measure(value=1)),
        )

    def test_repr(self) -> None:
        self.assertIn(
            'Co2Measure',
            repr(Co2Measure(value=1)),
        )


class TestEnergySource(TestCase):

    def test_values_exist(self) -> None:
        self.assertEqual(EnergySource.SOLAR.value, 'solar')
        self.assertEqual(EnergySource.WIND.value, 'wind')
        self.assertEqual(EnergySource.UNKNOWN.value, 'unknown')


class TestEnergyProvider(TestCase):

    def _organization(self) -> OrganizationalEntity:
        return OrganizationalEntity(name='provider')

    def test_constructor(self) -> None:
        obj = EnergyProvider(
            organization=self._organization(),
            energy_source=EnergySource.SOLAR,
            energy_provided=EnergyMeasure(value=100),
        )

        self.assertEqual(obj.energy_source, EnergySource.SOLAR)
        self.assertEqual(obj.energy_provided, EnergyMeasure(value=100))

    def test_description(self) -> None:
        obj = EnergyProvider(
            organization=self._organization(),
            energy_source=EnergySource.WIND,
            energy_provided=EnergyMeasure(value=10),
            description='green energy',
        )

        self.assertEqual(obj.description, 'green energy')

    def test_bom_ref(self) -> None:
        obj = EnergyProvider(
            organization=self._organization(),
            energy_source=EnergySource.SOLAR,
            energy_provided=EnergyMeasure(value=1),
            bom_ref='provider-ref',
        )

        self.assertEqual(obj.bom_ref.value, 'provider-ref')

    def test_external_references(self) -> None:
        reference = ExternalReference(
            type=ExternalReferenceType.WEBSITE,
            url='https://example.com',
        )

        obj = EnergyProvider(
            organization=self._organization(),
            energy_source=EnergySource.SOLAR,
            energy_provided=EnergyMeasure(value=1),
            external_references=[reference],
        )

        self.assertIn(reference, obj.external_references)

    def test_equality(self) -> None:
        organization = self._organization()

        self.assertEqual(
            EnergyProvider(
                organization=organization,
                energy_source=EnergySource.SOLAR,
                energy_provided=EnergyMeasure(value=1),
            ),
            EnergyProvider(
                organization=organization,
                energy_source=EnergySource.SOLAR,
                energy_provided=EnergyMeasure(value=1),
            ),
        )

    def test_comparison(self) -> None:
        organization = self._organization()

        self.assertTrue(
            EnergyProvider(
                organization=organization,
                energy_source=EnergySource.SOLAR,
                energy_provided=EnergyMeasure(value=1),
            )
            <= EnergyProvider(
                organization=organization,
                energy_source=EnergySource.SOLAR,
                energy_provided=EnergyMeasure(value=1),
            )
        )

    def test_hash(self) -> None:
        organization = self._organization()

        self.assertEqual(
            hash(EnergyProvider(
                organization=organization,
                energy_source=EnergySource.SOLAR,
                energy_provided=EnergyMeasure(value=1),
            )),
            hash(EnergyProvider(
                organization=organization,
                energy_source=EnergySource.SOLAR,
                energy_provided=EnergyMeasure(value=1),
            )),
        )

    def test_repr(self) -> None:
        self.assertIn(
            'EnergyProvider',
            repr(EnergyProvider(
                organization=self._organization(),
                energy_source=EnergySource.SOLAR,
                energy_provided=EnergyMeasure(value=1),
            )),
        )


class TestEnergyConsumption(TestCase):

    def _provider(self) -> EnergyProvider:
        return EnergyProvider(
            organization=OrganizationalEntity(name='provider'),
            energy_source=EnergySource.SOLAR,
            energy_provided=EnergyMeasure(value=10),
        )

    def test_constructor(self) -> None:
        obj = EnergyConsumption(
            activity=EnergyActivity.TRAINING,
            energy_providers=[self._provider()],
            activity_energy_cost=EnergyMeasure(value=100),
        )

        self.assertEqual(obj.activity, EnergyActivity.TRAINING)
        self.assertEqual(len(obj.energy_providers), 1)

    def test_optional_co2_values(self) -> None:
        obj = EnergyConsumption(
            activity=EnergyActivity.TRAINING,
            energy_providers=[self._provider()],
            activity_energy_cost=EnergyMeasure(value=1),
            co2_cost_equivalent=Co2Measure(value=1),
            co2_cost_offset=Co2Measure(value=2),
        )

        self.assertEqual(obj.co2_cost_equivalent, Co2Measure(value=1))
        self.assertEqual(obj.co2_cost_offset, Co2Measure(value=2))

    def test_properties(self) -> None:
        prop = Property(name='key', value='value')

        obj = EnergyConsumption(
            activity=EnergyActivity.TRAINING,
            energy_providers=[self._provider()],
            activity_energy_cost=EnergyMeasure(value=1),
            properties=[prop],
        )

        self.assertIn(prop, obj.properties)

    def test_equality(self) -> None:
        provider = self._provider()

        self.assertEqual(
            EnergyConsumption(
                activity=EnergyActivity.TRAINING,
                energy_providers=[provider],
                activity_energy_cost=EnergyMeasure(value=1),
            ),
            EnergyConsumption(
                activity=EnergyActivity.TRAINING,
                energy_providers=[provider],
                activity_energy_cost=EnergyMeasure(value=1),
            ),
        )

    def test_comparison(self) -> None:
        provider = self._provider()

        self.assertTrue(
            EnergyConsumption(
                activity=EnergyActivity.TRAINING,
                energy_providers=[provider],
                activity_energy_cost=EnergyMeasure(value=1),
            )
            <= EnergyConsumption(
                activity=EnergyActivity.TRAINING,
                energy_providers=[provider],
                activity_energy_cost=EnergyMeasure(value=1),
            )
        )

    def test_hash(self) -> None:
        provider = self._provider()

        self.assertEqual(
            hash(EnergyConsumption(
                activity=EnergyActivity.TRAINING,
                energy_providers=[provider],
                activity_energy_cost=EnergyMeasure(value=1),
            )),
            hash(EnergyConsumption(
                activity=EnergyActivity.TRAINING,
                energy_providers=[provider],
                activity_energy_cost=EnergyMeasure(value=1),
            )),
        )

    def test_repr(self) -> None:
        self.assertIn(
            'EnergyConsumption',
            repr(EnergyConsumption(
                activity=EnergyActivity.TRAINING,
                energy_providers=[],
                activity_energy_cost=EnergyMeasure(value=1),
            )),
        )


class TestConsiderations(TestCase):

    def test_defaults(self) -> None:
        obj = Considerations()

        self.assertEqual(len(obj.users), 0)
        self.assertEqual(len(obj.use_cases), 0)
        self.assertIsNone(obj.environmental_considerations)

    def test_constructor(self) -> None:
        obj = Considerations(
            users=['developer'],
            use_cases=['classification'],
            technical_limitations=['latency'],
            performance_tradeoffs=['accuracy'],
        )

        self.assertIn('developer', obj.users)
        self.assertIn('classification', obj.use_cases)

    def test_sorted_values(self) -> None:
        obj = Considerations(users=['b', 'a'])

        self.assertEqual(
            list(obj.users),
            ['a', 'b'],
        )

    def test_equality(self) -> None:
        self.assertEqual(
            Considerations(),
            Considerations(),
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(Considerations()),
            hash(Considerations()),
        )

    def test_repr(self) -> None:
        self.assertIn(
            'Considerations',
            repr(Considerations()),
        )


class TestModelCard(TestCase):

    def test_defaults(self) -> None:
        obj = ModelCard()

        self.assertIsNotNone(obj.bom_ref)
        self.assertIsNone(obj.model_parameters)
        self.assertIsNone(obj.quantitative_analysis)
        self.assertIsNone(obj.considerations)
        self.assertEqual(len(obj.properties), 0)

    def test_constructor(self) -> None:
        model_parameters = ModelParameters(task='classification')
        quantitative_analysis = QuantitativeAnalysis()
        considerations = Considerations()

        obj = ModelCard(
            model_parameters=model_parameters,
            quantitative_analysis=quantitative_analysis,
            considerations=considerations,
        )

        self.assertEqual(obj.model_parameters, model_parameters)
        self.assertEqual(obj.quantitative_analysis, quantitative_analysis)
        self.assertEqual(obj.considerations, considerations)

    def test_property_setters(self) -> None:
        obj = ModelCard()

        value = Considerations()

        obj.considerations = value

        self.assertEqual(obj.considerations, value)

    def test_properties(self) -> None:
        prop = Property(name='key', value='value')

        obj = ModelCard(properties=[prop])

        self.assertIn(prop, obj.properties)

    def test_bom_ref(self) -> None:
        obj = ModelCard(
            bom_ref='model-card-ref',
        )

        self.assertEqual(
            obj.bom_ref.value,
            'model-card-ref',
        )

    def test_equality(self) -> None:
        self.assertEqual(
            ModelCard(),
            ModelCard(),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            ModelCard() <= ModelCard()
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(ModelCard()),
            hash(ModelCard()),
        )

    def test_repr(self) -> None:
        self.assertIn(
            'ModelCard',
            repr(ModelCard()),
        )
