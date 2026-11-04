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

import ast
from collections.abc import Generator, Iterable
from decimal import Decimal
from enum import Enum
from glob import glob
from itertools import chain
from json import load as json_load
from os import path
from typing import Any, Optional
from unittest import TestCase
from warnings import warn
from xml.etree.ElementTree import parse as xml_parse  # nosec B405

from ddt import ddt, idata, named_data

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.exception.serialization import SerializationOfUnsupportedComponentTypeException
from cyclonedx.model import AttachedText, ExternalReference, HashType, XsUri
from cyclonedx.model.bom import Bom, BomMetaData, DistributionConstraints, TlpClassification
from cyclonedx.model.component import Component, Patch, Pedigree
from cyclonedx.model.component_evidence import ComponentEvidence, Identity as CEIdentity, Method as CEMethod
from cyclonedx.model.contact import OrganizationalEntity
from cyclonedx.model.crypto import (
    AlgorithmProperties,
    CryptoProperties,
    ProtocolProperties,
    RelatedCryptoMaterialProperties,
)
from cyclonedx.model.issue import IssueType
from cyclonedx.model.license import DisjunctiveLicense
from cyclonedx.model.lifecycle import LifecyclePhase, PredefinedLifecycle
from cyclonedx.model.model_card import (
    Approach,
    Co2Measure,
    Considerations,
    EnergyConsumption,
    EnergyMeasure,
    EnergyProvider,
    EnvironmentalConsiderations,
    ModelCard,
    ModelParameters,
)
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
from tests import PROJECT_LIB_MODELS_DIRECTORY, SnapshotMixin
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
from cyclonedx.model.component_evidence import (  # isort:skip
    AnalysisTechnique,
    IdentityField,
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
from cyclonedx.model.license import (  # isort:skip
    LicenseAcknowledgement
)
from cyclonedx.model.vulnerability import (  # isort:skip
    VulnerabilityScoreSource,
    VulnerabilitySeverity,
)
from cyclonedx.model.crypto import (  # isort:skip
    CryptoAssetType,
    CryptoCertificationLevel,
    CryptoExecutionEnvironment,
    CryptoFunction,
    CryptoImplementationPlatform,
    CryptoMode,
    CryptoPadding,
    CryptoPrimitive,
    ProtocolPropertiesType,
    RelatedCryptoMaterialState,
    RelatedCryptoMaterialType,
)
from cyclonedx.model.model_card import (  # isort:skip
    Co2MeasureUnit,
    EnergyActivity,
    EnergyMeasureUnit,
    EnergySource,
    MachineLearningApproach,
)

# endregion SUT


SCHEMA_NS = '{http://www.w3.org/2001/XMLSchema}'


def dp_cases_from_xml_schema(sf: str, xpath: str) -> Generator[str, None, None]:
    for el in xml_parse(sf).iterfind(f'{xpath}/{SCHEMA_NS}restriction/{SCHEMA_NS}enumeration'):  # nosec B314
        yield el.get('value')
    # warn if no such structure


def dp_cases_from_xml_schemas(xpath: str) -> set[str]:
    cases: set[str] = set()
    for sf in SCHEMA_XML.values():
        if sf is None:
            continue
        cases.update(dp_cases_from_xml_schema(sf, xpath))
    if len(cases) == 0:
        raise ValueError(f'no values for xpath: {xpath!r}')
    return cases


def dp_cases_from_json_schema(sf: str, jsonpointer: Iterable[str]) -> Generator[str, None, None]:
    with open(sf) as sfh:
        data = json_load(sfh)
    try:
        for pp in jsonpointer:
            data = data[pp]
    except KeyError:
        # warn if no such structure
        return
    yield from data['enum']


def dp_cases_from_json_schemas(*jsonpointer: str) -> set[str]:
    cases: set[str] = set()
    for sf in SCHEMA_JSON.values():
        if sf is None:
            continue
        cases.update(dp_cases_from_json_schema(sf, jsonpointer))
    if len(cases) == 0:
        raise ValueError(f'no values for jsonpointer: {jsonpointer!r}')
    return cases


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

    def _test_knows_value(self, enum: type[Enum], value: str) -> None:
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
    def unsupported_cases(cls) -> Generator[tuple[str, OutputFormat, SchemaVersion, ComponentType], None, None]:
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
        dp_cases_from_json_schemas('definitions', 'metadata', 'properties', 'lifecycles',
                                   'items', 'oneOf', 0, 'properties', 'phase'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(LifecyclePhase, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(metadata=BomMetaData(
            lifecycles=[PredefinedLifecycle(phase=phase) for phase in LifecyclePhase]
        ))
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumTlpClassification(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='tlpClassificationType']"),
        dp_cases_from_json_schemas('definitions', 'tlpClassification'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(TlpClassification, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(metadata=BomMetaData(
            distribution_constraints=DistributionConstraints(tlp=TlpClassification.CLEAR)
        ))
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumLicenseAcknowledgement(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='licenseAcknowledgementEnumerationType']"),
        dp_cases_from_json_schemas('definitions', 'licenseAcknowledgementEnumeration'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(LicenseAcknowledgement, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[Component(name='dummy', type=ComponentType.LIBRARY, bom_ref='dummy', licenses=(
            DisjunctiveLicense(name=f'LicenseAcknowledgement: {la.name}',
                               acknowledgement=la,
                               ) for la in LicenseAcknowledgement
        ))])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumIdentityField(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='identityFieldType']"),
        dp_cases_from_json_schemas('definitions', 'componentIdentityEvidence', 'properties', 'field'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(IdentityField, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(components=[
            Component(
                name='dummy', type=ComponentType.LIBRARY, bom_ref='dummy',
                evidence=ComponentEvidence(identity=[
                    CEIdentity(
                        field=ce_if,
                        concluded_value=f'{ce_if.name}'
                    ) for ce_if in IdentityField
                ]))
        ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumAnalysisTechnique(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='evidenceTechnique']"),
        dp_cases_from_json_schemas('definitions', 'componentIdentityEvidence', 'properties',
                                   'methods', 'items', 'properties', 'technique'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(AnalysisTechnique, value)

    @named_data(*NAMED_OF_SV)
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name='dummy', type=ComponentType.LIBRARY, bom_ref='dummy',
                    evidence=ComponentEvidence(identity=[
                        CEIdentity(
                            field=IdentityField.NAME,
                            methods=[
                                CEMethod(
                                    confidence=Decimal(1.0),
                                    value=f'AnalysisTechnique: {ce_at.name}',
                                    technique=ce_at,
                                ) for ce_at in AnalysisTechnique
                            ])
                    ])
                )
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCryptoAssetType(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='assetType']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties', 'assetType'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(CryptoAssetType, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'CryptoAssetType: {cat.name}', bom_ref=f'dummy-CAT:{cat.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=cat
                    )
                ) for cat in CryptoAssetType
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCryptoPrimitive(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='algorithmProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='primitive']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'algorithmProperties', 'properties', 'primitive'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(CryptoPrimitive, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'CryptoPrimitive: {cp.name}', bom_ref=f'dummy-CP:{cp.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.ALGORITHM,
                        algorithm_properties=AlgorithmProperties(
                            primitive=cp
                        )
                    )
                ) for cp in CryptoPrimitive
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCryptoExecutionEnvironment(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='algorithmProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='executionEnvironment']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'algorithmProperties', 'properties', 'executionEnvironment'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(CryptoExecutionEnvironment, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'CryptoExecutionEnvironment: {cee.name}', bom_ref=f'dummy-CEE:{cee.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.ALGORITHM,
                        algorithm_properties=AlgorithmProperties(
                            execution_environment=cee
                        )
                    )
                ) for cee in CryptoExecutionEnvironment
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCryptoImplementationPlatform (_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='algorithmProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='implementationPlatform']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'algorithmProperties', 'properties', 'implementationPlatform'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(CryptoImplementationPlatform, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'CryptoImplementationPlatform: {cip.name}', bom_ref=f'dummy-CIP:{cip.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.ALGORITHM,
                        algorithm_properties=AlgorithmProperties(
                            implementation_platform=cip
                        )
                    )
                ) for cip in CryptoImplementationPlatform
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCryptoCertificationLevel (_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='algorithmProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='certificationLevel']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'algorithmProperties', 'properties', 'certificationLevel', 'items'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(CryptoCertificationLevel, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'CryptoCertificationLevel: {ccl.name}', bom_ref=f'dummy-CCL:{ccl.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.ALGORITHM,
                        algorithm_properties=AlgorithmProperties(
                            certification_levels=[ccl]
                        )
                    )
                ) for ccl in CryptoCertificationLevel
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCryptoMode(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='algorithmProperties']/{SCHEMA_NS}complexType"
            f"/{SCHEMA_NS}sequence/{SCHEMA_NS}element[@name='mode']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'algorithmProperties', 'properties', 'mode'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(CryptoMode, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'CryptoMode: {cm.name}', bom_ref=f'dummy-CM:{cm.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.ALGORITHM,
                        algorithm_properties=AlgorithmProperties(
                            mode=cm
                        )
                    )
                ) for cm in CryptoMode
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCryptoPadding(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='algorithmProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='padding']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'algorithmProperties', 'properties', 'padding'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(CryptoPadding, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'CryptoPadding: {cp.name}', bom_ref=f'dummy-CP:{cp.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.ALGORITHM,
                        algorithm_properties=AlgorithmProperties(
                            padding=cp
                        )
                    )
                ) for cp in CryptoPadding
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCryptoFunction(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='algorithmProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='cryptoFunctions']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='cryptoFunction']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'algorithmProperties', 'properties', 'cryptoFunctions', 'items'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(CryptoFunction, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'CryptoFunction: {cf.name}', bom_ref=f'dummy-CF:{cf.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.ALGORITHM,
                        algorithm_properties=AlgorithmProperties(
                            crypto_functions=[cf]
                        )
                    )
                ) for cf in CryptoFunction
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumRelatedCryptoMaterialType(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='relatedCryptoMaterialProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='type']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'relatedCryptoMaterialProperties', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(RelatedCryptoMaterialType, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'RelatedCryptoMaterialType: {rcmt.name}', bom_ref=f'dummy-RCMT:{rcmt.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.RELATED_CRYPTO_MATERIAL,
                        related_crypto_material_properties=RelatedCryptoMaterialProperties(
                            type=rcmt
                        )
                    )
                ) for rcmt in RelatedCryptoMaterialType
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumRelatedCryptoMaterialState(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='relatedCryptoMaterialProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='state']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'relatedCryptoMaterialProperties', 'properties', 'state'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(RelatedCryptoMaterialState, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'RelatedCryptoMaterialState: {rcms.name}', bom_ref=f'dummy-RCMS:{rcms.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.RELATED_CRYPTO_MATERIAL,
                        related_crypto_material_properties=RelatedCryptoMaterialProperties(
                            state=rcms
                        )
                    )
                ) for rcms in RelatedCryptoMaterialState
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumProtocolPropertiesType(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='cryptoPropertiesType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='protocolProperties']/{SCHEMA_NS}complexType/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='type']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'cryptoProperties', 'properties',
                                   'protocolProperties', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(ProtocolPropertiesType, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'ProtocolPropertiesType: {ppt.name}', bom_ref=f'dummy-PPT:{ppt.name}',
                    type=ComponentType.CRYPTOGRAPHIC_ASSET,
                    crypto_properties=CryptoProperties(
                        asset_type=CryptoAssetType.PROTOCOL,
                        protocol_properties=ProtocolProperties(
                            type=ppt
                        )
                    )
                ) for ppt in ProtocolPropertiesType
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumMachineLearningApproach(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(f"./{SCHEMA_NS}simpleType[@name='machineLearningApproachType']"),
        dp_cases_from_json_schemas('definitions', 'modelCard', 'properties', 'modelParameters',
                                   'properties', 'approach', 'properties', 'type'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(MachineLearningApproach, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_5))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'MachineLearningApproach: {mla.name}', bom_ref=f'dummy-MLA:{mla.name}',
                    type=ComponentType.MACHINE_LEARNING_MODEL,
                    model_card=ModelCard(
                        model_parameters=ModelParameters(
                            approach=Approach(type=mla)
                        )
                    )
                ) for mla in MachineLearningApproach
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumEnergyActivity(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='energyConsumptionType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='activity']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'energyConsumption', 'properties', 'activity'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(EnergyActivity, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'EnergyActivity: {ea.name}', bom_ref=f'dummy-EA:{ea.name}',
                    type=ComponentType.MACHINE_LEARNING_MODEL,
                    model_card=ModelCard(
                        considerations=Considerations(
                            environmental_considerations=EnvironmentalConsiderations(
                                energy_consumptions=[
                                    EnergyConsumption(
                                        activity=ea,
                                        energy_providers=[EnergyProvider(
                                            organization=OrganizationalEntity(name='test-org'),
                                            energy_source=EnergySource.SOLAR,
                                            energy_provided=EnergyMeasure(value=1.0),
                                        )],
                                        activity_energy_cost=EnergyMeasure(value=1.0),
                                    )
                                ]
                            )
                        )
                    )
                ) for ea in EnergyActivity
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumEnergySource(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='energyProviderType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='energySource']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'energyProvider', 'properties', 'energySource'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(EnergySource, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'EnergySource: {es.name}', bom_ref=f'dummy-ES:{es.name}',
                    type=ComponentType.MACHINE_LEARNING_MODEL,
                    model_card=ModelCard(
                        considerations=Considerations(
                            environmental_considerations=EnvironmentalConsiderations(
                                energy_consumptions=[
                                    EnergyConsumption(
                                        activity=EnergyActivity.TRAINING,
                                        energy_providers=[EnergyProvider(
                                            organization=OrganizationalEntity(name='test-org'),
                                            energy_source=es,
                                            energy_provided=EnergyMeasure(value=1.0),
                                        )],
                                        activity_energy_cost=EnergyMeasure(value=1.0),
                                    )
                                ]
                            )
                        )
                    )
                ) for es in EnergySource
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumEnergyMeasureUnit(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='energyMeasureType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='unit']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'energyMeasure', 'properties', 'unit'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(EnergyMeasureUnit, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'EnergyMeasureUnit: {emu.name}', bom_ref=f'dummy-EMU:{emu.name}',
                    type=ComponentType.MACHINE_LEARNING_MODEL,
                    model_card=ModelCard(
                        considerations=Considerations(
                            environmental_considerations=EnvironmentalConsiderations(
                                energy_consumptions=[
                                    EnergyConsumption(
                                        activity=EnergyActivity.TRAINING,
                                        energy_providers=[EnergyProvider(
                                            organization=OrganizationalEntity(name='test-org'),
                                            energy_source=EnergySource.SOLAR,
                                            energy_provided=EnergyMeasure(value=1.0, unit=emu),
                                        )],
                                        activity_energy_cost=EnergyMeasure(value=1.0, unit=emu),
                                    )
                                ]
                            )
                        )
                    )
                ) for emu in EnergyMeasureUnit
            ])
        super()._test_cases_render(bom, of, sv)


@ddt
class TestEnumCo2MeasureUnit(_EnumTestCase):

    @idata(set(chain(
        dp_cases_from_xml_schemas(
            f"./{SCHEMA_NS}complexType[@name='co2MeasureType']/{SCHEMA_NS}sequence"
            f"/{SCHEMA_NS}element[@name='unit']/{SCHEMA_NS}simpleType"),
        dp_cases_from_json_schemas('definitions', 'co2Measure', 'properties', 'unit'),
    )))
    def test_knows_value(self, value: str) -> None:
        super()._test_knows_value(Co2MeasureUnit, value)

    @named_data(*(d for d in NAMED_OF_SV if d[2] >= SchemaVersion.V1_6))
    def test_cases_render_valid(self, of: OutputFormat, sv: SchemaVersion, *_: Any, **__: Any) -> None:
        bom = _make_bom(
            components=[
                Component(
                    name=f'Co2MeasureUnit: {cmu.name}', bom_ref=f'dummy-CMU:{cmu.name}',
                    type=ComponentType.MACHINE_LEARNING_MODEL,
                    model_card=ModelCard(
                        considerations=Considerations(
                            environmental_considerations=EnvironmentalConsiderations(
                                energy_consumptions=[
                                    EnergyConsumption(
                                        activity=EnergyActivity.TRAINING,
                                        energy_providers=[EnergyProvider(
                                            organization=OrganizationalEntity(name='test-org'),
                                            energy_source=EnergySource.SOLAR,
                                            energy_provided=EnergyMeasure(value=1.0),
                                        )],
                                        activity_energy_cost=EnergyMeasure(value=1.0),
                                        co2_cost_equivalent=Co2Measure(value=1.0, unit=cmu),
                                    )
                                ]
                            )
                        )
                    )
                ) for cmu in Co2MeasureUnit
            ])
        super()._test_cases_render(bom, of, sv)


# add new test cases above this line


@ddt
class TestCaseCompleteness(TestCase):
    """
    Test that all defined enum models are covered by a test case in here.
    """

    __TestCasePrefix = 'TestEnum'

    __defined_enumcases: Optional[tuple[str, ...]] = None

    @classmethod
    def __get_defined_enumcases(cls) -> tuple[str, ...]:
        if cls.__defined_enumcases is None:
            cls.__defined_enumcases = tuple(
                name for name, obj
                in globals().items()
                if isinstance(obj, type)
                and obj.__module__
                and obj.__module__ == __name__
                and issubclass(obj, _EnumTestCase)
                and obj is not _EnumTestCase
            )
        return cls.__defined_enumcases

    @staticmethod
    def __get_defined_model_enums() -> Generator[tuple[str, str], None, None]:
        model_files = glob(path.join(PROJECT_LIB_MODELS_DIRECTORY, '**', '*.py'), recursive=True)
        for model_file in model_files:
            model_file_rel = path.relpath(model_file, PROJECT_LIB_MODELS_DIRECTORY)
            with open(model_file, encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=model_file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for base in node.bases:
                            # Case 1: direct name: "Enum"
                            if isinstance(base, ast.Name) and base.id == 'Enum':
                                yield model_file_rel, node.name
                                break
                            # Case 2: qualified name: "enum.Enum"
                            if isinstance(base, ast.Attribute) and base.attr == 'Enum':
                                yield model_file_rel, node.name
                                break

    @idata(
        __get_defined_model_enums.__func__()  # py3.9 compat
    )
    def test_case_exists(self, defined_model_enums: tuple[str, str]) -> None:
        model_file_rel, enum_name = defined_model_enums
        self.assertIn(f'{self.__TestCasePrefix}{enum_name}',
                      self.__get_defined_enumcases(),
                      f'Missing Test Case for Enum {enum_name!r} from File {model_file_rel!r}')
