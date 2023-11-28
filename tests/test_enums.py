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


from enum import Enum
from itertools import chain
from json import load as json_load
from os.path import join
from typing import Any, Generator, Type
from unittest import TestCase
from unittest.mock import patch
from xml.etree.ElementTree import parse as xml_parse  # nosec B405

from ddt import ddt, idata, named_data

from cyclonedx.model import AttachedText, ExternalReference, HashType, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, Patch, Pedigree
from cyclonedx.model.license import DisjunctiveLicense
from cyclonedx.model.service import DataClassification, Service
from cyclonedx.output import make_outputter
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.schema._res import BOM_JSON as SCHEMA_JSON, BOM_XML as SCHEMA_XML
from cyclonedx.validation import make_schemabased_validator
from tests import SnapshotMixin, uuid_generator
from tests._data.models import _make_bom

# region SUT: all the enums

from cyclonedx.model import (  # isort:skip
    DataFlow,
    Encoding,
    ExternalReferenceType,
    HashAlgorithm,
)
from cyclonedx.model.component import (  # isort:skip
    ComponentScope,
    ComponentType,
    PatchClassification,
)
from cyclonedx.model.impact_analysis import (  # isort:skip
    ImpactAnalysisAffectedStatus,
    ImpactAnalysisJustification,
    ImpactAnalysisResponse,  # TODO
    ImpactAnalysisState,  # TODO
)
from cyclonedx.model.issue import (  # isort:skip
    IssueClassification,  # TODO
)
from cyclonedx.model.vulnerability import (  # isort:skip
    VulnerabilityScoreSource,  # TODO
    VulnerabilitySeverity, BomTargetVersionRange, BomTarget, Vulnerability, VulnerabilityAnalysis,  # TODO
)

# endregion SUT


SCHEMA_NS = '{http://www.w3.org/2001/XMLSchema}'


def dp_enum_from_xml_schemas(xpath: str) -> Generator[str, None, None]:
    for sf in SCHEMA_XML.values():
        if sf is None:
            continue
        for el in xml_parse(sf).iterfind(f'{xpath}/{SCHEMA_NS}restriction/{SCHEMA_NS}enumeration'):  # nosec B314
            yield el.get('value')


def dp_cases_from_json_schemas(*jsonpointer: str) -> Generator[str, None, None]:
    for sf in SCHEMA_JSON.values():
        if sf is None:
            continue
        with open(sf) as sfh:
            data = json_load(sfh)
        try:
            for pp in jsonpointer:
                data = data[pp]
        except KeyError:
            pass
        else:
            for value in data['enum']:
                yield value


UNSUPPORTED_OF_SV = frozenset([
    (OutputFormat.JSON, SchemaVersion.V1_1),
    (OutputFormat.JSON, SchemaVersion.V1_0),
])

NAMED_OF_SV = tuple(
    (f'{of.name}-{sv.to_version()}', of, sv)
    for of in OutputFormat
    for sv in SchemaVersion
    if (of, sv) not in UNSUPPORTED_OF_SV
)


class _EnumTestCase(TestCase, SnapshotMixin):

    def _test_knows_value(self, enum: Type[Enum], value: str) -> None:
        ec = enum(value)  # throws valueError if value unknown
        self.assertTrue(ec.name)  # TODO test for an expected name

    def _test_cases_render_valid(self, bom: Bom, of: OutputFormat, sv: SchemaVersion) -> None:
        snapshot_name = join(f'enum_{type(self).__name__.removeprefix("TestEnum")}-{sv.to_version()}.{of.name.lower()}')

        output = make_outputter(bom, of, sv).output_as_string(indent=2)
        validation_errors = make_schemabased_validator(of, sv).validate_str(output)

        self.assertIsNone(validation_errors)
        self.assertEqualSnapshot(output, snapshot_name)


@ddt
class TestEnumDataFlow(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='dataFlowType']"),
        dp_cases_from_json_schemas('definitions', 'dataFlowDirection'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(DataFlow, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(services=[Service(name='dummy', data=(
            DataClassification(flow=df, classification=df.name) for df in DataFlow
        ))])
        super()._test_cases_render_valid(bom, of, sv)


@ddt
class TestEnumEncoding(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='encoding']"),
        dp_cases_from_json_schemas('definitions', 'attachment', 'properties', 'encoding'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(Encoding, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[Component(name='dummy', type=ComponentType.LIBRARY, licenses=(
            DisjunctiveLicense(name=f'att.encoding: {encoding.name}', text=AttachedText(
                content=f'att.encoding: {encoding.name}', encoding=encoding
            ))
            for encoding in Encoding
        ))])
        super()._test_cases_render_valid(bom, of, sv)


@ddt
class TestEnumExternalReferenceType(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='externalReferenceType']"),
        dp_cases_from_json_schemas('definitions', 'externalReference', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ExternalReferenceType, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[Component(name='dummy', type=ComponentType.LIBRARY, external_references=(
            ExternalReference(type=extref, url=XsUri(f'tests/{extref.name}'))
            for extref in ExternalReferenceType
        ))])
        super()._test_cases_render_valid(bom, of, sv)


@ddt
class TestEnumHashAlgorithm(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='hashAlg']"),
        dp_cases_from_json_schemas('definitions', 'hash-alg'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(HashAlgorithm, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[Component(name='dummy', type=ComponentType.LIBRARY, hashes=(
            HashType(alg=alg, content='ae2b1fca515949e5d54fb22b8ed95575')
            for alg in HashAlgorithm
        ))])
        super()._test_cases_render_valid(bom, of, sv)


@ddt
class TestEnumComponentScope(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='scope']"),
        dp_cases_from_json_schemas('definitions', 'component', 'properties', 'scope'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ComponentScope, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=(
            Component(name=f'dummy scoped: {scope.name}', type=ComponentType.LIBRARY, scope=scope)
            for scope in ComponentScope
        ))
        super()._test_cases_render_valid(bom, of, sv)


@ddt
class TestEnumComponentType(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='classification']"),
        dp_cases_from_json_schemas('definitions', 'component', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ComponentType, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=(
            Component(name=f'dummy type: {ct.name}', type=ct)
            for ct in ComponentType
        ))
        super()._test_cases_render_valid(bom, of, sv)


@ddt
class TestEnumPatchClassification(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='patchClassification']"),
        dp_cases_from_json_schemas('definitions', 'patch', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(PatchClassification, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[Component(name=f'dummy', type=ComponentType.LIBRARY, pedigree=Pedigree(patches=(
            Patch(type=pc)
            for pc in PatchClassification
        )))])
        super()._test_cases_render_valid(bom, of, sv)


@ddt
class TestEnumImpactAnalysisAffectedStatus(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='impactAnalysisAffectedStatusType']"),
        dp_cases_from_json_schemas('definitions', 'affectedStatus'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ImpactAnalysisAffectedStatus, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(vulnerabilities=[Vulnerability(
            bom_ref='dummy', affects=[BomTarget(ref='urn:cdx:bom23/1#comp42', versions=(
                BomTargetVersionRange(version=f'1.33.7+{iaas.name}', status=iaas)
                for iaas in ImpactAnalysisAffectedStatus
            ))])])
        super()._test_cases_render_valid(bom, of, sv)


@ddt
class TestEnumImpactAnalysisJustification(_EnumTestCase):

    @idata(set(chain(
        dp_enum_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='impactAnalysisJustificationType']"),
        dp_cases_from_json_schemas('definitions', 'impactAnalysisJustification'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ImpactAnalysisJustification, value)

    @named_data(*NAMED_OF_SV)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(vulnerabilities=(
            Vulnerability(
                bom_ref=f'vuln-with-{iaj.name}',
                analysis=VulnerabilityAnalysis(justification=iaj)
            ) for iaj in ImpactAnalysisJustification
        ))
        super()._test_cases_render_valid(bom, of, sv)
