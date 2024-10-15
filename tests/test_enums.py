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


from enum import Enum
from itertools import chain
from json import load as json_load
from typing import Any, Generator, Iterable, Tuple, Type
from unittest import TestCase
from warnings import warn
from xml.etree.ElementTree import parse as xml_parse  # nosec B405

from ddt import ddt, idata, named_data

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.exception.serialization import SerializationOfUnsupportedComponentTypeException
from cyclonedx.model import AttachedText, ExternalReference, HashType, XsUri
from cyclonedx.model.bom import Bom, BomMetaData
from cyclonedx.model.component import Component, Patch, Pedigree
from cyclonedx.model.issue import IssueType
from cyclonedx.model.license import DisjunctiveLicense
from cyclonedx.model.lifecycle import LifecyclePhase, PredefinedLifecycle
from cyclonedx.model.service import DataClassification, Service
from cyclonedx.model.vulnerability import (
    BomTarget,
    BomTargetVersionRange,
    Vulnerability,
    VulnerabilityAnalysis,
    VulnerabilityRating,
)
from cyclonedx.output import make_outputter
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.schema._res import BOM_JSON as SCHEMA_JSON, BOM_XML as SCHEMA_XML
from cyclonedx.validation import make_schemabased_validator
from tests import SnapshotMixin
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
    ImpactAnalysisResponse,
    ImpactAnalysisState,
)
from cyclonedx.model.issue import (  # isort:skip
    IssueClassification,
)
from cyclonedx.model.vulnerability import (  # isort:skip
    VulnerabilityScoreSource,
    VulnerabilitySeverity,
)

# endregion SUT


SCHEMA_NS = '{http://www.w3.org/2001/XMLSchema}'


def dp_cases_from_xml_schema(sf: str, xpath: str) -> Generator[str, None, None]:
    for el in xml_parse(sf).iterfind(f'{xpath}/{SCHEMA_NS}restriction/{SCHEMA_NS}enumeration'):  # nosec B314
        yield el.get('value')


def dp_cases_from_xml_schemas(xpath: str) -> Generator[str, None, None]:
    for sf in SCHEMA_XML.values():
        if sf is None:
            continue
        yield from dp_cases_from_xml_schema(sf, xpath)


def dp_cases_from_json_schema(sf: str, jsonpointer: Iterable[str]) -> Generator[str, None, None]:
    with open(sf) as sfh:
        data = json_load(sfh)
    try:
        for pp in jsonpointer:
            data = data[pp]
    except KeyError:
        return
    for value in data['enum']:
        yield value


def dp_cases_from_json_schemas(*jsonpointer: str) -> Generator[str, None, None]:
    for sf in SCHEMA_JSON.values():
        if sf is None:
            continue
        yield from dp_cases_from_json_schema(sf, jsonpointer)


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

    @staticmethod
    def __str_rmp(s: str, p: str) -> str:
        # str.removeprefix() for all py versions
        pl = len(p)
        return s[pl:] if s[:pl] == p else s

    def _test_cases_render(self, bom: Bom, of: OutputFormat, sv: SchemaVersion) -> None:
        snapshot_name = f'enum_{self.__str_rmp(type(self).__name__, "TestEnum")}-{sv.to_version()}.{of.name.lower()}'

        output = make_outputter(bom, of, sv).output_as_string(indent=2)

        try:
            validation_errors = make_schemabased_validator(of, sv).validate_str(output)
        except MissingOptionalDependencyException:
            warn('!!! skipped schema validation',
                 category=UserWarning, stacklevel=0)
        else:
            self.assertIsNone(validation_errors)

        self.assertEqualSnapshot(output, snapshot_name)


@ddt
class TestEnumDataFlow(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='dataFlowType']"),
        dp_cases_from_json_schemas('definitions', 'dataFlowDirection'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(DataFlow, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(services=[Service(name='dummy', bom_ref='dummy', data=(
            DataClassification(flow=df, classification=df.name)
            for df in DataFlow
        ))])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumEncoding(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='encoding']"),
        dp_cases_from_json_schemas('definitions', 'attachment', 'properties', 'encoding'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(Encoding, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[Component(name='dummy', type=ComponentType.LIBRARY, bom_ref='dummy', licenses=(
            DisjunctiveLicense(name=f'att.encoding: {encoding.name}', text=AttachedText(
                content=f'att.encoding: {encoding.name}', encoding=encoding
            )) for encoding in Encoding
        ))])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumExternalReferenceType(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='externalReferenceType']"),
        dp_cases_from_json_schemas('definitions', 'externalReference', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ExternalReferenceType, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[
            Component(name='dummy', type=ComponentType.LIBRARY, bom_ref='dummy', external_references=(
                ExternalReference(type=extref, url=XsUri(f'tests/{extref.name}'))
                for extref in ExternalReferenceType
            ))
        ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumHashAlgorithm(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='hashAlg']"),
        dp_cases_from_json_schemas('definitions', 'hash-alg'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(HashAlgorithm, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[Component(name='dummy', type=ComponentType.LIBRARY, bom_ref='dummy', hashes=(
            HashType(alg=alg, content='ae2b1fca515949e5d54fb22b8ed95575')
            for alg in HashAlgorithm
        ))])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumComponentScope(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='scope']"),
        dp_cases_from_json_schemas('definitions', 'component', 'properties', 'scope'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ComponentScope, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=(
            Component(bom_ref=f'scoped-{scope.name}', name=f'dummy-{scope.name}',
                      type=ComponentType.LIBRARY, scope=scope)
            for scope in ComponentScope
        ))
        super()._test_cases_render(bom, of, sv)


class _DP_ComponentType():  # noqa: N801
    XML_SCHEMA_XPATH = f"./{SCHEMA_NS}simpleType[@name='classification']"
    JSON_SCHEMA_POINTER = ('definitions', 'component', 'properties', 'type')

    @classmethod
    def unsupported_cases(cls) -> Generator[Tuple[str, OutputFormat, SchemaVersion, ComponentType], None, None]:
        for name, of, sv in NAMED_OF_SV:
            if OutputFormat.XML is of:
                schema_cases = set(dp_cases_from_xml_schema(SCHEMA_XML[sv], cls.XML_SCHEMA_XPATH))
            elif OutputFormat.JSON is of:
                schema_cases = set(dp_cases_from_json_schema(SCHEMA_JSON[sv], cls.JSON_SCHEMA_POINTER))
            else:
                raise ValueError(f'unexpected of: {of!r}')
            for ct in ComponentType:
                if ct.value not in schema_cases:
                    yield f'{name}-{ct.name}', of, sv, ct


@ddt
class TestEnumComponentType(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(_DP_ComponentType.XML_SCHEMA_XPATH),
        dp_cases_from_json_schemas(*_DP_ComponentType.JSON_SCHEMA_POINTER),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ComponentType, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        if OutputFormat.XML is of:
            schema_cases = set(dp_cases_from_xml_schema(SCHEMA_XML[sv], _DP_ComponentType.XML_SCHEMA_XPATH))
        elif OutputFormat.JSON is of:
            schema_cases = set(dp_cases_from_json_schema(SCHEMA_JSON[sv], _DP_ComponentType.JSON_SCHEMA_POINTER))
        else:
            raise ValueError(f'unexpected of: {of!r}')
        bom = _make_bom(components=(
            Component(bom_ref=f'typed-{ct.name}', name=f'dummy {ct.name}', type=ct)
            for ct in ComponentType
            if ct.value in schema_cases
        ))
        super()._test_cases_render(bom, of, sv)

    @named_data(*_DP_ComponentType.unsupported_cases())
    def test_cases_render_raises_on_unsupported(self, of: OutputFormat, sv: SchemaVersion,
                                                ct: ComponentType,
                                                *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[
            Component(bom_ref=f'typed-{ct.name}', name=f'dummy {ct.name}', type=ct)
        ])
        with self.assertRaises(SerializationOfUnsupportedComponentTypeException):
            super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumPatchClassification(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='patchClassification']"),
        dp_cases_from_json_schemas('definitions', 'patch', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(PatchClassification, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[
            Component(name='dummy', type=ComponentType.LIBRARY, bom_ref='dummy', pedigree=Pedigree(patches=(
                Patch(type=pc)
                for pc in PatchClassification
            )))
        ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumImpactAnalysisAffectedStatus(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='impactAnalysisAffectedStatusType']"),
        dp_cases_from_json_schemas('definitions', 'affectedStatus'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ImpactAnalysisAffectedStatus, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(vulnerabilities=[Vulnerability(
            bom_ref='dummy', id='dummy', affects=[BomTarget(ref='urn:cdx:bom23/1#comp42', versions=(
                BomTargetVersionRange(version=f'1.33.7+{iaas.name}', status=iaas)
                for iaas in ImpactAnalysisAffectedStatus
            ))]
        )])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumImpactAnalysisJustification(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='impactAnalysisJustificationType']"),
        dp_cases_from_json_schemas('definitions', 'impactAnalysisJustification'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ImpactAnalysisJustification, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(vulnerabilities=(
            Vulnerability(
                bom_ref=f'vuln-with-{iaj.name}', id=f'vuln-with-{iaj.name}',
                analysis=VulnerabilityAnalysis(justification=iaj)
            ) for iaj in ImpactAnalysisJustification
        ))
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumImpactAnalysisResponse(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='impactAnalysisResponsesType']"),
        dp_cases_from_json_schemas('definitions', 'vulnerability', 'properties', 'analysis', 'properties', 'response',
                                   'items'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ImpactAnalysisResponse, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(vulnerabilities=[Vulnerability(
            bom_ref='dummy', id='dummy',
            analysis=VulnerabilityAnalysis(responses=(
                iar for iar in ImpactAnalysisResponse
            ))
        )])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumImpactAnalysisState(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='impactAnalysisStateType']"),
        dp_cases_from_json_schemas('definitions', 'impactAnalysisState'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ImpactAnalysisState, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(vulnerabilities=(
            Vulnerability(
                bom_ref=f'vuln-wit-state-{ias.name}', id=f'vuln-wit-state-{ias.name}',
                analysis=VulnerabilityAnalysis(state=ias)
            ) for ias in ImpactAnalysisState
        ))
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumIssueClassification(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='issueClassification']"),
        dp_cases_from_json_schemas('definitions', 'issue', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(IssueClassification, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[
            Component(name='dummy', type=ComponentType.LIBRARY, bom_ref='dummy', pedigree=Pedigree(patches=[
                Patch(type=PatchClassification.BACKPORT, resolves=(
                    IssueType(type=ic, id=f'issue-{ic.name}')
                    for ic in IssueClassification
                ))
            ]))
        ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumVulnerabilityScoreSource(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='scoreSourceType']"),
        dp_cases_from_json_schemas('definitions', 'scoreMethod'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(VulnerabilityScoreSource, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(vulnerabilities=[Vulnerability(bom_ref='dummy', id='dummy', ratings=(
            VulnerabilityRating(method=vss)
            for vss in VulnerabilityScoreSource
        ))])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumVulnerabilitySeverity(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='severityType']"),
        dp_cases_from_json_schemas('definitions', 'severity'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(VulnerabilitySeverity, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(vulnerabilities=[Vulnerability(bom_ref='dummy', id='dummy', ratings=(
            VulnerabilityRating(severity=vs)
            for vs in VulnerabilitySeverity
        ))])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumLifecyclePhase(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='lifecyclePhaseType']"),
        dp_cases_from_json_schemas('definitions', 'metadata', 'properties', 'lifecycles', 'items', 'phase'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(LifecyclePhase, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(metadata=BomMetaData(
            lifecycles=[PredefinedLifecycle(phase=phase) for phase in LifecyclePhase]
        ))
        super()._test_cases_render(bom, of, sv)
