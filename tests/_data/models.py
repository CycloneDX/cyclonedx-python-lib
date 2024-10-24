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

import base64
import sys
from datetime import datetime, timezone
from decimal import Decimal
from inspect import getmembers, isfunction
from typing import Any, List, Optional, Tuple
from uuid import UUID

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL

from cyclonedx.builder.this import this_component, this_tool
from cyclonedx.model import (
    AttachedText,
    Copyright,
    DataClassification,
    DataFlow,
    Encoding,
    ExternalReference,
    ExternalReferenceType,
    HashType,
    Note,
    NoteText,
    Property,
    XsUri,
)
from cyclonedx.model.bom import Bom, BomMetaData
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.component import (
    Commit,
    Component,
    ComponentEvidence,
    ComponentScope,
    ComponentType,
    Diff,
    OmniborId,
    Patch,
    PatchClassification,
    Pedigree,
    Swhid,
    Swid,
)
from cyclonedx.model.contact import OrganizationalContact, OrganizationalEntity, PostalAddress
from cyclonedx.model.crypto import (
    AlgorithmProperties,
    CertificateProperties,
    CryptoAssetType,
    CryptoCertificationLevel,
    CryptoExecutionEnvironment,
    CryptoFunction,
    CryptoImplementationPlatform,
    CryptoMode,
    CryptoPadding,
    CryptoPrimitive,
    CryptoProperties,
    ProtocolProperties,
    ProtocolPropertiesCipherSuite,
    ProtocolPropertiesType,
    RelatedCryptoMaterialProperties,
    RelatedCryptoMaterialSecuredBy,
    RelatedCryptoMaterialState,
    RelatedCryptoMaterialType,
)
from cyclonedx.model.definition import Definitions, Standard
from cyclonedx.model.dependency import Dependency
from cyclonedx.model.impact_analysis import (
    ImpactAnalysisAffectedStatus,
    ImpactAnalysisJustification,
    ImpactAnalysisResponse,
    ImpactAnalysisState,
)
from cyclonedx.model.issue import IssueClassification, IssueType, IssueTypeSource
from cyclonedx.model.license import DisjunctiveLicense, License, LicenseAcknowledgement, LicenseExpression
from cyclonedx.model.lifecycle import LifecyclePhase, NamedLifecycle, PredefinedLifecycle
from cyclonedx.model.release_note import ReleaseNotes
from cyclonedx.model.service import Service
from cyclonedx.model.tool import Tool, ToolRepository
from cyclonedx.model.vulnerability import (
    BomTarget,
    BomTargetVersionRange,
    Vulnerability,
    VulnerabilityAdvisory,
    VulnerabilityAnalysis,
    VulnerabilityCredits,
    VulnerabilityRating,
    VulnerabilityReference,
    VulnerabilityScoreSource,
    VulnerabilitySeverity,
    VulnerabilitySource,
)

MOCK_TIMESTAMP = datetime.fromisoformat('2023-08-15 01:23:45.678900+00:00')

MOCK_UUID = (
    'be2c6502-7e9a-47db-9a66-e34f729810a3',
    '17e3b199-dc0b-42ef-bfdd-1fa81a1e3eda',
    '0b049d09-64c0-4490-a0f5-c84d9aacf857',
    'cd3e9c95-9d41-49e7-9924-8cf0465ae789',
    'bb5911d6-1a1d-41c9-b6e0-46e848d16655',
    'df70b5f1-8f53-47a4-be48-669ae78795e6',
    '6f266d1c-760f-4552-ae3b-41a9b74232fa',
    '77d15ab9-5602-4cca-8ed2-59ae579aafd3',
    '859ff614-35a7-4d37-803b-d89130cb2577',
    '0afa65bc-4acd-428b-9e17-8e97b1969745',
    '3e671687-395b-41f5-a30f-a58921a69b79',
    'd0b24ba4-102b-497e-b31f-4fdc3f0a3005',
    'd0e0a795-6177-478b-b293-b0d19e4469f4',
    '7b2a7a2c-66d5-4b30-8ee2-df966a41024e',
    '68f7b744-84c2-4f0d-ac8b-c14bd48c37ff',
    '1a2f9dfc-3c86-48c7-8ca7-1db488d5c2a0',
    'a3f4096d-4211-4d68-9d2b-13973c86aca9',
)

BOM_SERIAL_NUMBER = UUID('1441d33a-e0fc-45b5-af3b-61ee52a88bac')
BOM_TIMESTAMP = datetime.fromisoformat('2023-01-07 13:44:32.312678+00:00')


def _make_bom(**kwargs: Any) -> Bom:
    bom = Bom(**kwargs)
    bom.serial_number = BOM_SERIAL_NUMBER
    bom.metadata.timestamp = BOM_TIMESTAMP
    bom.properties = get_properties_1()
    return bom


def get_bom_with_component_setuptools_basic() -> Bom:
    return _make_bom(components=[get_component_setuptools_simple()])


def get_bom_with_component_setuptools_with_cpe() -> Bom:
    component = get_component_setuptools_simple()
    component.cpe = 'cpe:2.3:a:python:setuptools:50.3.2:*:*:*:*:*:*:*'
    return _make_bom(components=[component])


def get_crypto_properties_algorithm() -> CryptoProperties:
    return CryptoProperties(
        asset_type=CryptoAssetType.ALGORITHM,
        algorithm_properties=AlgorithmProperties(
            primitive=CryptoPrimitive.KEM,
            parameter_set_identifier='a-parameter-set-id',
            curve='9n8y2oxty3ao83n8qc2g2x3qcw4jt4wj',
            execution_environment=CryptoExecutionEnvironment.SOFTWARE_PLAIN_RAM,
            implementation_platform=CryptoImplementationPlatform.GENERIC,
            certification_levels=[
                CryptoCertificationLevel.FIPS140_1_L1,
                CryptoCertificationLevel.FIPS140_2_L3,
                CryptoCertificationLevel.OTHER
            ],
            mode=CryptoMode.ECB,
            padding=CryptoPadding.PKCS7,
            crypto_functions=[
                CryptoFunction.SIGN,
                CryptoFunction.UNKNOWN
            ],
            classical_security_level=2,
            nist_quantum_security_level=2
        ),
        oid='an-oid-here'
    )


def get_crypto_properties_certificate() -> CryptoProperties:
    return CryptoProperties(
        asset_type=CryptoAssetType.CERTIFICATE,
        certificate_properties=CertificateProperties(
            subject_name='cyclonedx.org',
            issuer_name='Cloudflare Inc ECC CA-3',
            not_valid_before=datetime(year=2023, month=5, day=19, hour=1, minute=0, second=0, microsecond=0,
                                      tzinfo=timezone.utc),
            not_valid_after=datetime(year=2024, month=5, day=19, hour=0, minute=59, second=59, microsecond=999999,
                                     tzinfo=timezone.utc),
            signature_algorithm_ref=None,
            subject_public_key_ref=None,
            certificate_format='pem',
            certificate_extension='csr'
        ),
        oid='an-oid-here'
    )


def get_crypto_properties_protocol() -> CryptoProperties:
    return CryptoProperties(
        asset_type=CryptoAssetType.PROTOCOL,
        protocol_properties=ProtocolProperties(
            type=ProtocolPropertiesType.TLS,
            version='1.3',
            cipher_suites=[
                ProtocolPropertiesCipherSuite(
                    name='TLS_AES_128_GCM_SHA256',
                    algorithms=None,
                    identifiers=[
                        'TLS_AES_128_GCM_SHA256'
                    ]
                ),
                ProtocolPropertiesCipherSuite(
                    name='TLS_AES_256_GCM_SHA384',
                    algorithms=None,
                    identifiers=[
                        'TLS_AES_256_GCM_SHA384'
                    ]
                ),
                ProtocolPropertiesCipherSuite(
                    name='TLS_CHACHA20_POLY1305_SHA256',
                    algorithms=None,
                    identifiers=[
                        'TLS_CHACHA20_POLY1305_SHA256'
                    ]
                ),
                ProtocolPropertiesCipherSuite(
                    name='TLS_AES_128_CCM_SHA256',
                    algorithms=None,
                    identifiers=[
                        'TLS_AES_128_CCM_SHA256'
                    ]
                ),
                ProtocolPropertiesCipherSuite(
                    name='TLS_AES_128_CCM_8_SHA256',
                    algorithms=None,
                    identifiers=[
                        'TLS_AES_128_CCM_8_SHA256'
                    ]
                )
            ],
        ),
        oid='an-oid-here'
    )


def get_crypto_properties_related_material() -> CryptoProperties:
    return CryptoProperties(
        asset_type=CryptoAssetType.RELATED_CRYPTO_MATERIAL,
        related_crypto_material_properties=RelatedCryptoMaterialProperties(
            type=RelatedCryptoMaterialType.DIGEST,
            id='some-identifier',
            state=RelatedCryptoMaterialState.ACTIVE,
            algorithm_ref=None,
            creation_date=datetime(year=2023, month=5, day=19, hour=1, minute=0, second=0, microsecond=0,
                                   tzinfo=timezone.utc),
            activation_date=datetime(year=2023, month=5, day=19, hour=1, minute=0, second=0, microsecond=0,
                                     tzinfo=timezone.utc),
            update_date=None,
            expiration_date=datetime(year=2024, month=5, day=19, hour=0, minute=59, second=59, microsecond=999999,
                                     tzinfo=timezone.utc),
            value='some-random-value',
            size=32,
            format='a-format',
            secured_by=RelatedCryptoMaterialSecuredBy(
                mechanism='hard-work',
                algorithm_ref=None
            )
        ),
        oid='an-oid-here'
    )


def get_bom_with_component_setuptools_with_v16_fields() -> Bom:
    component = get_component_setuptools_simple()
    component.manufacturer = get_org_entity_1()
    component.authors = [get_org_contact_1(), get_org_contact_2()]
    component.omnibor_ids = [OmniborId('gitoid:blob:sha1:261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64')]
    component.swhids = [
        Swhid('swh:1:cnt:94a9ed024d3859793618152ea559a168bbcbb5e2'),
        Swhid('swh:1:rel:22ece559cc7cc2364edc5e5593d63ae8bd229f9f'),
        Swhid('swh:1:cnt:4d99d2d18326621ccdd70f5ea66c2e2ac236ad8b;'
              'origin=https://gitorious.org/ocamlp3l/ocamlp3l_cvs.git;'
              'visit=swh:1:snp:d7f1b9eb7ccb596c2622c4780febaa02549830f9;'
              'anchor=swh:1:rev:2db189928c94d62a3b4757b3eec68f0a4d4113f0;'
              'path=/Examples/SimpleFarm/simplefarm.ml;lines=9-15'),
        Swhid('swh:1:cnt:f10371aa7b8ccabca8479196d6cd640676fd4a04;origin=https://github.com/web-platform-tests/wpt;'
              'visit=swh:1:snp:b37d435721bbd450624165f334724e3585346499;'
              'anchor=swh:1:rev:259d0612af038d14f2cd889a14a3adb6c9e96d96;'
              'path=/html/semantics/document-metadata/the-meta-element/pragma-directives/attr-meta-http-equiv-refresh/'
              'support/x%3Burl=foo/')
    ]
    return _make_bom(components=[component])


def get_bom_with_component_setuptools_with_v16_fields_omnibor_id_invalid() -> Bom:
    component = get_component_setuptools_simple()
    component.manufacturer = get_org_entity_1()
    component.authors = [get_org_contact_1(), get_org_contact_2()]
    component.omnibor_ids = [OmniborId('gitoid:stuff:sha1:261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64')]
    return _make_bom(components=[component])


def get_bom_with_component_setuptools_with_v16_fields_swhid_invalid() -> Bom:
    component = get_component_setuptools_simple()
    component.manufacturer = get_org_entity_1()
    component.authors = [get_org_contact_1(), get_org_contact_2()]
    component.omnibor_ids = [OmniborId('gitoid:blob:sha1:261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64')]
    component.swhids = [
        Swhid('swh:1:cntp:94a9ed024d3859793618152ea559a168bbcbb5e2'),
    ]
    return _make_bom(components=[component])


def get_component_crypto_asset_algorithm(
    bom_ref: Optional[str] = '8182921e-0588-472e-b8f9-9c527c68f067'
) -> Component:
    return Component(
        name='My Algorithm', version='1.0', type=ComponentType.CRYPTOGRAPHIC_ASSET,
        bom_ref=bom_ref,
        crypto_properties=get_crypto_properties_algorithm(),
        tags=['algorithm']
    )


def get_component_crypto_asset_certificate(
    bom_ref: Optional[str] = '1f4ed1e4-582a-4fa0-8c38-1b4facc16972'
) -> Component:
    return Component(
        name='My Certificate', version='1.0', type=ComponentType.CRYPTOGRAPHIC_ASSET,
        bom_ref=bom_ref,
        crypto_properties=get_crypto_properties_certificate(),
        tags=['certificate']
    )


def get_component_crypto_asset_protocol_tls_v13(
    bom_ref: Optional[str] = '26b1ce0f-bec6-4bfe-9db1-03b75a4ed1ec'
) -> Component:
    return Component(
        name='TLS', version='v1.3', type=ComponentType.CRYPTOGRAPHIC_ASSET,
        bom_ref=bom_ref,
        crypto_properties=get_crypto_properties_protocol(),
        tags=['protocl', 'tls']
    )


def get_component_crypto_asset_related_material(
    bom_ref: Optional[str] = '332b3cee-078c-4789-ab15-887565b6fac5'
) -> Component:
    return Component(
        name='My Encrypted Thing', version='1.0', type=ComponentType.CRYPTOGRAPHIC_ASSET,
        bom_ref=bom_ref,
        crypto_properties=get_crypto_properties_related_material(),
        tags=['encrypted', 'data']
    )


def get_bom_v1_6_with_crypto_algorithm() -> Bom:
    c = get_component_crypto_asset_algorithm()
    b = _make_bom(components=[c])
    b.register_dependency(c)
    return b


def get_bom_v1_6_with_crypto_certificate() -> Bom:
    c = get_component_crypto_asset_certificate()
    b = _make_bom(components=[c])
    b.register_dependency(c)
    return b


def get_bom_v1_6_with_crypto_protocol() -> Bom:
    c = get_component_crypto_asset_protocol_tls_v13()
    b = _make_bom(components=[c])
    b.register_dependency(c)
    return b


def get_bom_v1_6_with_crypto_related_material() -> Bom:
    c = get_component_crypto_asset_related_material()
    b = _make_bom(components=[c])
    b.register_dependency(c)
    return b


def get_bom_with_component_setuptools_no_component_version() -> Bom:
    return _make_bom(components=[get_component_setuptools_simple_no_version()])


def get_bom_with_component_setuptools_with_release_notes() -> Bom:
    component = get_component_setuptools_simple()
    component.release_notes = get_release_notes()
    return _make_bom(components=[component])


def get_bom_with_dependencies_valid() -> Bom:
    c1 = get_component_setuptools_simple()
    c2 = get_component_toml_with_hashes_with_references()
    return _make_bom(
        components=[c1, c2], dependencies=[
            Dependency(ref=c1.bom_ref, dependencies=[
                Dependency(ref=c2.bom_ref)
            ]),
            Dependency(ref=c2.bom_ref)
        ]
    )


def get_bom_with_dependencies_hanging() -> Bom:
    """
    A bom with a RootComponent and components,
    but no dependencies are connected to RootComponent.
    """
    c1 = get_component_setuptools_simple('setuptools')
    c2 = get_component_toml_with_hashes_with_references('toml')
    bom = _make_bom(
        version=23,
        metadata=BomMetaData(
            component=Component(name='rootComponent', type=ComponentType.APPLICATION, bom_ref='root-component'),
        ),
        components=[c1, c2],
        dependencies=[
            Dependency(c1.bom_ref, [
                Dependency(c2.bom_ref)
            ]),
            Dependency(c2.bom_ref)
        ]
    )
    return bom


def get_bom_with_dependencies_unlinked_invalid() -> Bom:
    """generate a bom with an unlinked dependency.
    it is expected to throw on output.
    """
    c1 = get_component_setuptools_simple()
    return _make_bom(components=[c1], dependencies=[Dependency(ref=BomRef('link-to-ref-not-in-document'))])


def get_bom_with_metadata_component_and_dependencies() -> Bom:
    cs = get_component_toml_with_hashes_with_references()
    bom = _make_bom(components=[cs])
    bom.metadata.component = get_component_setuptools_simple()
    bom.dependencies.add(
        Dependency(ref=bom.metadata.component.bom_ref, dependencies=[
            Dependency(ref=cs.bom_ref)
        ])
    )
    return bom


def get_bom_with_component_setuptools_complete() -> Bom:
    return _make_bom(components=[get_component_setuptools_complete()])


def get_bom_with_component_setuptools_with_vulnerability() -> Bom:
    bom = _make_bom()
    component = get_component_setuptools_simple()
    if not component.purl:
        raise ValueError('purl is required here')
    bom.components.add(component)
    bom.vulnerabilities.add(Vulnerability(
        bom_ref='my-vuln-ref-1', id='CVE-2018-7489', source=get_vulnerability_source_nvd(),
        references=[
            VulnerabilityReference(id='SOME-OTHER-ID', source=VulnerabilitySource(
                name='OSS Index', url=XsUri('https://ossindex.sonatype.org/component/pkg:pypi/setuptools')
            ))
        ],
        ratings=[
            VulnerabilityRating(
                source=get_vulnerability_source_nvd(), score=Decimal('9.8'), severity=VulnerabilitySeverity.CRITICAL,
                method=VulnerabilityScoreSource.CVSS_V3,
                vector='AN/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', justification='Some justification'
            ),
            VulnerabilityRating(
                source=get_vulnerability_source_owasp(), score=Decimal('2.7'), severity=VulnerabilitySeverity.LOW,
                method=VulnerabilityScoreSource.CVSS_V3,
                vector='AV:L/AC:H/PR:N/UI:R/S:C/C:L/I:N/A:N', justification='Some other justification'
            )
        ],
        cwes=[22, 33], description='A description here', detail='Some detail here',
        recommendation='Upgrade', workaround='Describe the workarounds here',
        advisories=[
            VulnerabilityAdvisory(url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2018-7489')),
            VulnerabilityAdvisory(url=XsUri('http://www.securitytracker.com/id/1040693'))
        ],
        created=datetime(year=2021, month=9, day=1, hour=10, minute=50, second=42, microsecond=51979,
                         tzinfo=timezone.utc),
        published=datetime(year=2021, month=9, day=2, hour=10, minute=50, second=42, microsecond=51979,
                           tzinfo=timezone.utc),
        updated=datetime(year=2021, month=9, day=3, hour=10, minute=50, second=42, microsecond=51979,
                         tzinfo=timezone.utc),
        credits=VulnerabilityCredits(
            organizations=[
                get_org_entity_1()
            ],
            individuals=[get_org_contact_2()]
        ),
        tools=ToolRepository(tools=(
            Tool(vendor='CycloneDX', name='cyclonedx-python-lib'),
        )),
        analysis=VulnerabilityAnalysis(
            state=ImpactAnalysisState.EXPLOITABLE, justification=ImpactAnalysisJustification.REQUIRES_ENVIRONMENT,
            responses=[ImpactAnalysisResponse.CAN_NOT_FIX], detail='Some extra detail'
        ),
        affects=[
            BomTarget(
                ref=component.purl.to_string(),
                versions=[BomTargetVersionRange(
                    range='49.0.0 - 54.0.0', status=ImpactAnalysisAffectedStatus.AFFECTED
                )]
            )
        ],
        properties=get_properties_1()
    ))
    return bom


def get_bom_with_component_toml_1() -> Bom:
    return _make_bom(components=[get_component_toml_with_hashes_with_references()])


def get_bom_just_complete_metadata() -> Bom:
    bom = _make_bom()
    bom.metadata.authors = [get_org_contact_1(), get_org_contact_2()]
    bom.metadata.component = get_component_setuptools_complete()
    bom.metadata.component.manufacturer = get_org_entity_1()
    bom.metadata.manufacture = get_org_entity_1()  # Deprecated from v1.6 onwards
    bom.metadata.supplier = get_org_entity_2()
    bom.metadata.licenses = [DisjunctiveLicense(
        id='Apache-2.0',
        url=XsUri('https://www.apache.org/licenses/LICENSE-2.0.txt'),
        text=AttachedText(
            encoding=Encoding.BASE_64,
            content='VGVzdCBjb250ZW50IC0gdGhpcyBpcyBub3QgdGhlIEFwYWNoZSAyLjAgbGljZW5zZSE='
        )
    )]
    bom.metadata.lifecycles = [PredefinedLifecycle(LifecyclePhase.BUILD)]
    bom.metadata.properties = get_properties_1()
    return bom


def get_bom_with_external_references() -> Bom:
    bom = _make_bom(external_references=[
        get_external_reference_1(), get_external_reference_2()
    ])
    return bom


def get_bom_with_services_simple() -> Bom:
    bom = _make_bom(services=[
        Service(name='my-first-service', bom_ref='my-specific-bom-ref-for-my-first-service'),
        Service(name='my-second-service', bom_ref='my-specific-bom-ref-for-my-second-service')
    ])
    bom.metadata.component = Component(
        name='cyclonedx-python-lib', version='1.0.0', type=ComponentType.LIBRARY,
        bom_ref='my-specific-bom-ref-for-cpl'
    )
    return bom


def get_bom_with_services_complex() -> Bom:
    bom = _make_bom(services=[
        Service(
            name='my-first-service', bom_ref='my-specific-bom-ref-for-my-first-service',
            provider=get_org_entity_1(), group='a-group', version='1.2.3',
            description='Description goes here', endpoints=[
                XsUri('/api/thing/1'),
                XsUri('/api/thing/2')
            ],
            authenticated=False, x_trust_boundary=True, data=[
                DataClassification(flow=DataFlow.OUTBOUND, classification='public')
            ],
            licenses=[DisjunctiveLicense(name='Commercial')],
            external_references=[
                get_external_reference_1()
            ],
            properties=get_properties_1(),
            release_notes=get_release_notes()
        ),
        Service(name='my-second-service', bom_ref='my-specific-bom-ref-for-my-second-service')
    ])
    bom.metadata.component = Component(
        name='cyclonedx-python-lib', version='1.0.0', type=ComponentType.LIBRARY,
        bom_ref='my-specific-bom-ref-for-cpl'
    )
    return bom


def get_bom_with_nested_services() -> Bom:
    bom = _make_bom(services=[
        Service(
            name='my-first-service', bom_ref='my-specific-bom-ref-for-my-first-service',
            provider=get_org_entity_1(), group='a-group', version='1.2.3',
            description='Description goes here', endpoints=[
                XsUri('/api/thing/1'),
                XsUri('/api/thing/2')
            ],
            authenticated=False, x_trust_boundary=True, data=[
                DataClassification(flow=DataFlow.OUTBOUND, classification='public')
            ],
            licenses=[DisjunctiveLicense(name='Commercial')],
            external_references=[
                get_external_reference_1()
            ],
            properties=get_properties_1(),
            services=[
                Service(
                    name='first-nested-service', bom_ref='my-specific-bom-ref-for-first-nested-service',
                ),
                Service(
                    name='second-nested-service', bom_ref='my-specific-bom-ref-for-second-nested-service',
                    provider=get_org_entity_1(), group='no-group', version='3.2.1',
                    authenticated=True, x_trust_boundary=False,
                )
            ],
            release_notes=get_release_notes()
        ),
        Service(
            name='my-second-service',
            bom_ref='my-specific-bom-ref-for-my-second-service',
            services=[
                Service(
                    name='yet-another-nested-service',
                    bom_ref='yet-another-nested-service',
                    provider=get_org_entity_1(), group='what-group', version='6.5.4'
                ),
                Service(
                    name='another-nested-service',
                    bom_ref='my-specific-bom-ref-for-another-nested-service',
                )
            ],
        )
    ])
    bom.metadata.component = Component(
        name='cyclonedx-python-lib', version='1.0.0', type=ComponentType.LIBRARY,
        bom_ref='my-specific-bom-ref-for-cpl'
    )
    return bom


def get_bom_for_issue_275_components() -> Bom:
    """regression test for issue #275
    see https://github.com/CycloneDX/cyclonedx-python-lib/issues/275
    """

    app = Component(bom_ref=MOCK_UUID[0], name='app', version='1.0.0')
    comp_a = Component(bom_ref=MOCK_UUID[1], name='comp_a', version='1.0.0')
    comp_b = Component(bom_ref=MOCK_UUID[2], name='comp_b', version='1.0.0')
    comp_c = Component(bom_ref=MOCK_UUID[3], name='comp_c', version='1.0.0')

    comp_b.components.add(comp_c)
    # comp_b.dependencies.add(comp_c.bom_ref)

    libs = [comp_a, comp_b]
    # app.dependencies.add(comp_a.bom_ref)
    # app.dependencies.add(comp_b.bom_ref)

    bom = _make_bom(components=libs)
    bom.metadata.component = app
    bom.register_dependency(target=app, depends_on=[comp_a, comp_b])
    bom.register_dependency(target=comp_b, depends_on=[comp_c])
    return bom


# def get_bom_for_issue_275_services() -> Bom:
#    """regression test for issue #275
#    see https://github.com/CycloneDX/cyclonedx-python-lib/issues/275
#    """
#    app = Component(name="app", version="1.0.0")
#    serv_a = Service(name='Service A')
#    serv_b = Service(name='Service B')
#    serv_c = Service(name='Service C')
#
#    serv_b.services.add(serv_c)
#    serv_b.dependencies.add(serv_c.bom_ref)
#
#    bom = _makeBom(services=[serv_a, serv_b])
#    bom.metadata.component = app
#    return bom


def get_bom_for_issue_328_components() -> Bom:
    """regression test for issue #328
    see https://github.com/CycloneDX/cyclonedx-python-lib/issues/328
    """
    bom = _make_bom()

    comp_root = Component(type=ComponentType.APPLICATION,
                          name='my-project', version='1', bom_ref='my-project')
    comp_a = Component(name='A', version='0.1', bom_ref='component-A')
    comp_b = Component(name='B', version='1.0', bom_ref='component-B')
    comp_c = Component(name='C', version='1.0', bom_ref='component-C')

    # Make a tree of components A -> B -> C
    comp_a.components = [comp_b]
    comp_b.components = [comp_c]

    bom.metadata.component = comp_root
    bom.register_dependency(comp_root, [comp_a])
    bom.components = [comp_a]

    # Declare dependencies the same way: A -> B -> C
    bom.register_dependency(comp_a, [comp_b])
    bom.register_dependency(comp_b, [comp_c])

    return bom


def get_component_setuptools_complete(include_pedigree: bool = True) -> Component:
    component = get_component_setuptools_simple(bom_ref='my-specific-bom-ref-for-dings')
    component.supplier = get_org_entity_1()
    component.publisher = 'CycloneDX'
    component.description = 'This component is awesome'
    component.scope = ComponentScope.REQUIRED
    component.copyright = 'Apache 2.0 baby!'
    component.cpe = 'cpe:2.3:a:python:setuptools:50.3.2:*:*:*:*:*:*:*'
    component.swid = get_swid_1()
    if include_pedigree:
        component.pedigree = get_pedigree_1()
    component.external_references.add(
        get_external_reference_1()
    )
    component.properties = get_properties_1()
    component.components.update([
        get_component_setuptools_simple(),
        get_component_toml_with_hashes_with_references()
    ])
    component.evidence = ComponentEvidence(copyright=[Copyright(text='Commercial'), Copyright(text='Commercial 2')])
    component.release_notes = get_release_notes()
    return component


def get_component_setuptools_simple(
    bom_ref: Optional[str] = 'pkg:pypi/setuptools@50.3.2?extension=tar.gz'
) -> Component:
    return Component(
        name='setuptools', version='50.3.2',
        bom_ref=bom_ref,
        purl=PackageURL(
            type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
        ),
        licenses=[DisjunctiveLicense(id='MIT')],
        author='Test Author'
    )


def get_component_setuptools_simple_no_version(bom_ref: Optional[str] = None) -> Component:
    return Component(
        name='setuptools', bom_ref=bom_ref or 'pkg:pypi/setuptools?extension=tar.gz',
        purl=PackageURL(
            type='pypi', name='setuptools', qualifiers='extension=tar.gz'
        ),
        licenses=[DisjunctiveLicense(id='MIT')],
        author='Test Author'
    )


def get_component_toml_with_hashes_with_references(bom_ref: Optional[str] = None) -> Component:
    return Component(
        name='toml', version='0.10.2', bom_ref=bom_ref or 'pkg:pypi/toml@0.10.2?extension=tar.gz',
        purl=PackageURL(
            type='pypi', name='toml', version='0.10.2', qualifiers='extension=tar.gz'
        ), hashes=[
            HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        ], external_references=[
            get_external_reference_1()
        ]
    )


def get_external_reference_1() -> ExternalReference:
    return ExternalReference(
        type=ExternalReferenceType.DISTRIBUTION,
        url=XsUri('https://cyclonedx.org'),
        comment='No comment',
        hashes=[
            HashType.from_composite_str(
                'sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        ]
    )


def get_external_reference_2() -> ExternalReference:
    return ExternalReference(
        type=ExternalReferenceType.WEBSITE,
        url=XsUri('https://cyclonedx.org')
    )


def get_issue_1() -> IssueType:
    return IssueType(
        type=IssueClassification.SECURITY, id='CVE-2021-44228', name='Apache Log3Shell',
        description='Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features...',
        source=IssueTypeSource(name='NVD', url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2021-44228')),
        references=[
            XsUri('https://logging.apache.org/log4j/2.x/security.html'),
            XsUri('https://central.sonatype.org/news/20211213_log4shell_help')
        ]
    )


def get_issue_2() -> IssueType:
    return IssueType(
        type=IssueClassification.SECURITY, id='CVE-2021-44229', name='Apache Log4Shell',
        description='Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features...',
        source=IssueTypeSource(name='NVD', url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2021-44228')),
        references=[
            XsUri('https://logging.apache.org/log4j/2.x/security.html'),
            XsUri('https://central.sonatype.org/news/20211213_log4shell_help')
        ]
    )


def get_org_contact_1() -> OrganizationalContact:
    return OrganizationalContact(name='Paul Horton', email='paul.horton@owasp.org')


def get_org_contact_2() -> OrganizationalContact:
    return OrganizationalContact(name='A N Other', email='someone@somewhere.tld', phone='+44 (0)1234 567890')


def get_postal_address_1() -> PostalAddress:
    return PostalAddress(country='GB', region='England', locality='Cheshire', street_address='100 Main Street')


def get_postal_address_2() -> PostalAddress:
    return PostalAddress(country='US', region='Texas', locality='Austin', street_address='100 Yee-Ha Street',
                         postal_code='12345', post_office_box_number='105a')


def get_org_entity_1() -> OrganizationalEntity:
    return OrganizationalEntity(
        name='CycloneDX', urls=[XsUri('https://cyclonedx.org'), XsUri('https://cyclonedx.org/docs')],
        contacts=[get_org_contact_1(), get_org_contact_2()], address=get_postal_address_1()
    )


def get_org_entity_2() -> OrganizationalEntity:
    return OrganizationalEntity(
        name='Cyclone DX', urls=[XsUri('https://cyclonedx.org/')], contacts=[get_org_contact_2()],
        address=get_postal_address_2()
    )


def get_pedigree_1() -> Pedigree:
    return Pedigree(
        ancestors=[
            get_component_setuptools_simple(bom_ref='ccc8d7ee-4b9c-4750-aee0-a72585152291'),
            get_component_setuptools_simple_no_version(bom_ref='8a3893b3-9923-4adb-a1d3-47456636ba0a')
        ],
        descendants=[
            get_component_setuptools_simple_no_version(bom_ref='28b2d8ce-def0-446f-a221-58dee0b44acc'),
            get_component_toml_with_hashes_with_references(bom_ref='555ca729-93c6-48f3-956e-bdaa4a2f0bfa')
        ],
        variants=[
            get_component_toml_with_hashes_with_references(bom_ref='e7abdcca-5ba2-4f29-b2cf-b1e1ef788e66'),
            get_component_setuptools_simple(bom_ref='ded1d73e-1fca-4302-b520-f1bc53979958')
        ],
        commits=[Commit(uid='a-random-uid', message='A commit message')],
        patches=[Patch(type=PatchClassification.BACKPORT, diff=Diff(
            url=XsUri('https://acme.com/my-patch.diff'),
            text=AttachedText(encoding=Encoding.BASE_64, content_type='text/x-diff',
                              content='LS0tIGZvbwkyMDI0LTAzLTA0IDEyOjQxOjExLjQxODc1OTE0NSArMDEwMAorKysgYmFyCTIwMjQtMDMt'
                                      'MDQgMTI6NDE6MjguMzE1NTE3ODQ3ICswMTAwCkBAIC0xLDIgKzEsMiBAQAotaGVsbG8gd29ybGQuCitI'
                                      'ZWxsbyB3b3JsZC4KIAo=')
        ))],
        notes='Some notes here please'
    )


def get_properties_1() -> List[Property]:
    return [
        Property(name='key1', value='val1'),
        Property(name='key2', value='val2')
    ]


def get_release_notes() -> ReleaseNotes:
    text_content: str = base64.b64encode(
        bytes('Some simple plain text', encoding='UTF-8')
    ).decode(encoding='UTF-8')

    return ReleaseNotes(
        type='major', title='Release Notes Title',
        featured_image=XsUri('https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'),
        social_image=XsUri('https://cyclonedx.org/cyclonedx-icon.png'),
        description='This release is a test release', timestamp=MOCK_TIMESTAMP,
        aliases=[
            'First Test Release'
        ],
        tags=['test', 'alpha'],
        resolves=[get_issue_1()],
        notes=[
            Note(
                text=NoteText(
                    content=text_content, content_type='text/plain; charset=UTF-8',
                    encoding=Encoding.BASE_64
                ), locale='en-GB'
            ),
            Note(
                text=NoteText(
                    content=text_content, content_type='text/plain; charset=UTF-8',
                    encoding=Encoding.BASE_64
                ), locale='en-US'
            )
        ],
        properties=get_properties_1()
    )


def get_swid_1() -> Swid:
    return Swid(
        tag_id='swidgen-242eb18a-503e-ca37-393b-cf156ef09691_9.1.1', name='Test Application',
        version='3.4.5', text=AttachedText(
            content='PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiID8+CjxTb2Z0d2FyZUlkZW50aXR5IHhtbDpsYW5nPSJFTiIgbm'
                    'FtZT0iQWNtZSBBcHBsaWNhdGlvbiIgdmVyc2lvbj0iOS4xLjEiIAogdmVyc2lvblNjaGVtZT0ibXVsdGlwYXJ0bnVtZXJpYyIg'
                    'CiB0YWdJZD0ic3dpZGdlbi1iNTk1MWFjOS00MmMwLWYzODItM2YxZS1iYzdhMmE0NDk3Y2JfOS4xLjEiIAogeG1sbnM9Imh0dH'
                    'A6Ly9zdGFuZGFyZHMuaXNvLm9yZy9pc28vMTk3NzAvLTIvMjAxNS9zY2hlbWEueHNkIj4gCiB4bWxuczp4c2k9Imh0dHA6Ly93'
                    'd3cudzMub3JnLzIwMDEvWE1MU2NoZW1hLWluc3RhbmNlIiAKIHhzaTpzY2hlbWFMb2NhdGlvbj0iaHR0cDovL3N0YW5kYXJkcy'
                    '5pc28ub3JnL2lzby8xOTc3MC8tMi8yMDE1LWN1cnJlbnQvc2NoZW1hLnhzZCBzY2hlbWEueHNkIiA+CiAgPE1ldGEgZ2VuZXJh'
                    'dG9yPSJTV0lEIFRhZyBPbmxpbmUgR2VuZXJhdG9yIHYwLjEiIC8+IAogIDxFbnRpdHkgbmFtZT0iQWNtZSwgSW5jLiIgcmVnaW'
                    'Q9ImV4YW1wbGUuY29tIiByb2xlPSJ0YWdDcmVhdG9yIiAvPiAKPC9Tb2Z0d2FyZUlkZW50aXR5Pg==',
            content_type='text/xml', encoding=Encoding.BASE_64
        )
    )


def get_swid_2() -> Swid:
    return Swid(
        tag_id='swidgen-242eb18a-503e-ca37-393b-cf156ef09691_9.1.1', name='Test Application',
        version='3.4.5', url=XsUri('https://cyclonedx.org')
    )


def get_vulnerability_source_nvd() -> VulnerabilitySource:
    return VulnerabilitySource(name='NVD', url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2018-7489'))


def get_vulnerability_source_owasp() -> VulnerabilitySource:
    return VulnerabilitySource(name='OWASP', url=XsUri('https://owasp.org'))


def get_bom_with_licenses() -> Bom:
    return _make_bom(
        metadata=BomMetaData(
            licenses=[DisjunctiveLicense(id='CC-BY-1.0')],
            component=Component(name='app', type=ComponentType.APPLICATION, bom_ref='my-app',
                                licenses=[DisjunctiveLicense(name='proprietary')])
        ),
        components=[
            Component(name='c-with-expression', type=ComponentType.LIBRARY, bom_ref='C1',
                      licenses=[LicenseExpression(value='Apache-2.0 OR MIT',
                                                  acknowledgement=LicenseAcknowledgement.CONCLUDED)]),
            Component(name='c-with-SPDX', type=ComponentType.LIBRARY, bom_ref='C2',
                      licenses=[DisjunctiveLicense(id='Apache-2.0',
                                                   url=XsUri('https://www.apache.org/licenses/LICENSE-2.0.html'),
                                                   acknowledgement=LicenseAcknowledgement.CONCLUDED)]),
            Component(name='c-with-name', type=ComponentType.LIBRARY, bom_ref='C3',
                      licenses=[
                          DisjunctiveLicense(name='some commercial license',
                                             text=AttachedText(content='this is a license text')),
                          DisjunctiveLicense(name='some additional',
                                             text=AttachedText(content='this is additional license text')),
                      ]),
        ],
        services=[
            Service(name='s-with-expression', bom_ref='S1',
                    licenses=[LicenseExpression(value='Apache-2.0 OR MIT',
                                                acknowledgement=LicenseAcknowledgement.DECLARED)]),
            Service(name='s-with-SPDX', bom_ref='S2',
                    licenses=[DisjunctiveLicense(id='Apache-2.0',
                                                 url=XsUri('https://www.apache.org/licenses/LICENSE-2.0.html'),
                                                 acknowledgement=LicenseAcknowledgement.DECLARED)]),
            Service(name='s-with-name', bom_ref='S3',
                    licenses=[
                        DisjunctiveLicense(name='some commercial license',
                                           text=AttachedText(content='this is a license text')),
                        DisjunctiveLicense(name='some additional',
                                           text=AttachedText(content='this is additional license text')),
                    ]),
        ])


def get_bom_metadata_licenses_invalid() -> Bom:
    return Bom(metadata=BomMetaData(licenses=get_invalid_license_repository()))


def get_invalid_license_repository() -> List[License]:
    """
    license expression and a license -- this is an invalid constellation according to schema
    see https://github.com/CycloneDX/specification/pull/205
    """
    return [
        LicenseExpression(value='Apache-2.0 OR MIT'),
        DisjunctiveLicense(id='GPL-2.0-only'),
    ]


def get_component_licenses_invalid() -> Component:
    return Component(name='foo', type=ComponentType.LIBRARY,
                     licenses=get_invalid_license_repository())


def get_bom_metadata_component_licenses_invalid() -> Bom:
    comp = get_component_licenses_invalid()
    return Bom(metadata=BomMetaData(component=comp),
               dependencies=[Dependency(comp.bom_ref)])


def get_bom_metadata_component_nested_licenses_invalid() -> Bom:
    comp = Component(name='bar', type=ComponentType.LIBRARY,
                     components=[get_component_licenses_invalid()])
    return Bom(metadata=BomMetaData(component=comp),
               dependencies=[Dependency(comp.bom_ref)])


def get_bom_component_licenses_invalid() -> Bom:
    return Bom(components=[get_component_licenses_invalid()])


def get_bom_component_nested_licenses_invalid() -> Bom:
    return Bom(components=[
        Component(name='bar', type=ComponentType.LIBRARY,
                  components=[get_component_licenses_invalid()])
    ])


def get_bom_service_licenses_invalid() -> Bom:
    return Bom(services=[
        Service(name='foo', licenses=get_invalid_license_repository())
    ])


def get_bom_with_multiple_licenses() -> Bom:
    multi_licenses = (
        DisjunctiveLicense(id='MIT'),
        DisjunctiveLicense(name='foo license'),
    )
    return _make_bom(
        metadata=BomMetaData(
            licenses=multi_licenses,
            component=Component(name='app', type=ComponentType.APPLICATION, bom_ref='my-app',
                                licenses=multi_licenses)
        ),
        components=[Component(name='comp', type=ComponentType.LIBRARY, bom_ref='my-compo',
                              licenses=multi_licenses)],
        services=[Service(name='serv', bom_ref='my-serv',
                          licenses=multi_licenses)]
    )


def get_bom_with_tools() -> Bom:
    return _make_bom(
        metadata=BomMetaData(
            tools=(
                this_tool(),
                Tool(name='test-tool-b'),
                Tool(vendor='example',
                     name='test-tool-a',
                     version='1.33.7',
                     hashes=[HashType.from_composite_str(
                         'sha256:adbbbe72c8f023b4a2d96a3978f69d94873ab2fef424e0298287c3368519c1a6')],
                     external_references=[get_external_reference_1()],
                     ),
            )
        )
    )


def get_bom_with_tools_with_component_migrate() -> Bom:
    return _make_bom(
        metadata=BomMetaData(
            tools=ToolRepository(
                components=(
                    this_component(),
                    Component(name='test-component', bom_ref='test-component'),
                    Component(type=ComponentType.APPLICATION,
                              bom_ref='other-component',
                              group='acme',
                              name='other-component',
                              hashes=[HashType.from_composite_str(
                                  'sha256:49b420bd8d8182542a76d4422e0c7890dcc88a3d8ddad04da06366d8c40ac8ca')],
                              external_references=[get_external_reference_1()],
                              ),
                )
            )
        )
    )


def get_bom_with_tools_with_service_migrate() -> Bom:
    return _make_bom(
        metadata=BomMetaData(
            tools=ToolRepository(
                services=(
                    Service(name='test-service', bom_ref='test-service'),
                    Service(group='acme',
                            name='other-service',
                            bom_ref='other-service',
                            external_references=[get_external_reference_1()],
                            ),
                )
            )
        )
    )


def get_bom_with_tools_with_component_and_service_migrate() -> Bom:
    return _make_bom(
        metadata=BomMetaData(
            tools=ToolRepository(
                components=(
                    this_component(),
                    Component(name='test-component', bom_ref='test-component'),
                    Component(type=ComponentType.APPLICATION,
                              bom_ref='other-component',
                              group='acme',
                              name='other-component',
                              hashes=[HashType.from_composite_str(
                                  'sha256:49b420bd8d8182542a76d4422e0c7890dcc88a3d8ddad04da06366d8c40ac8ca')],
                              external_references=[get_external_reference_1()],
                              ),
                ),
                services=(
                    Service(name='test-service', bom_ref='test-service'),
                    Service(group='acme',
                            name='other-service',
                            bom_ref='other-service',
                            external_references=[get_external_reference_1()],
                            ),
                )
            )
        )
    )


def get_bom_with_tools_with_component_and_service_and_tools_irreversible_migrate() -> Bom:
    tools = ToolRepository()
    tcomp = tools.components
    tserv = tools.services
    ttools = tools.tools
    tcomp.update((
        this_component(),
        Component(name='test-component', bom_ref='test-component'),
        Component(type=ComponentType.APPLICATION,
                  bom_ref='other-component',
                  group='acme',
                  name='other-component',
                  hashes=[HashType.from_composite_str(
                          'sha256:49b420bd8d8182542a76d4422e0c7890dcc88a3d8ddad04da06366d8c40ac8ca')],
                  external_references=[get_external_reference_1()],
                  ),
    ))
    tserv.update((
        Service(name='test-service', bom_ref='test-service'),
        Service(group='acme',
                name='other-service',
                bom_ref='other-service',
                external_references=[get_external_reference_1()],
                ),
    ))
    ttools.update((
        this_tool(),
        Tool(name='test-tool-b'),
        Tool(vendor='example',
             name='test-tool-a',
             version='1.33.7',
             hashes=[HashType.from_composite_str(
                 'sha256:adbbbe72c8f023b4a2d96a3978f69d94873ab2fef424e0298287c3368519c1a6')],
             external_references=[get_external_reference_1()],
             ),
    ))
    return _make_bom(metadata=BomMetaData(tools=tools))


def get_bom_with_tools_with_component_and_service_and_duplicated_tools_irreversible_migrate() -> Bom:
    """on serialization, it is expected that only tools are emitted, and that they are deduplicated"""
    tools = ToolRepository()
    tcomp = tools.components
    tserv = tools.services
    ttools = tools.tools
    tcomp.update((
        this_component(),
        Component(name='test-component'),
        Component(type=ComponentType.APPLICATION,
                  group='acme',
                  name='other-component'),
    ))
    tserv.update((
        Service(name='test-service'),
        Service(group='acme',
                name='other-service'),
    ))
    ttools.clear()
    # duplicate components and services as tools
    ttools.update(map(Tool.from_component, tcomp))
    ttools.update(map(Tool.from_service, tserv))
    return _make_bom(metadata=BomMetaData(tools=tools))


def get_bom_for_issue_497_urls() -> Bom:
    """regression test for issue #497
    see https://github.com/CycloneDX/cyclonedx-python-lib/issues/497
    """
    return _make_bom(components=[
        Component(name='dummy', bom_ref='dummy', external_references=[
            ExternalReference(
                type=ExternalReferenceType.OTHER,
                comment='nothing special',
                url=XsUri('https://acme.org')
            ),
            ExternalReference(
                type=ExternalReferenceType.OTHER,
                comment='control characters',
                url=XsUri('https://acme.org/?'
                          'foo=sp ace&'
                          'bar[23]=42&'
                          'lt=1<2&'
                          'gt=3>2&'
                          'cb={lol}&'
                          'quote="test"is\'test\''
                          )
            ),
            ExternalReference(
                type=ExternalReferenceType.OTHER,
                comment='pre-encoded',
                url=XsUri('https://acme.org/?bar%5b23%5D=42')
            ),
        ])
    ])


def get_bom_for_issue_598_multiple_components_with_purl_qualifiers() -> Bom:
    """regression test for issue #598
    see https://github.com/CycloneDX/cyclonedx-python-lib/issues/598
    """
    return _make_bom(components=[
        Component(
            name='dummy', version='2.3.5', bom_ref='dummy-a',
            purl=PackageURL(
                type='pypi', namespace=None, name='pathlib2', version='2.3.5', subpath=None,
                qualifiers={}
            )
        ),
        Component(
            name='dummy', version='2.3.5', bom_ref='dummy-b',
            purl=PackageURL(
                type='pypi', namespace=None, name='pathlib2', version='2.3.5', subpath=None,
                qualifiers={
                    'vcs_url': 'git+https://github.com/jazzband/pathlib2.git@5a6a88db3cc1d08dbc86fbe15edfb69fb5f5a3d6'
                }
            )
        )
    ])


def bom_all_same_bomref() -> Tuple[Bom, int]:
    bom = Bom()
    bom.metadata.component = Component(name='root', bom_ref='foo', components=[
        Component(name='root.sub', bom_ref='foo')])
    bom.components.add(Component(name='comp', bom_ref='foo', components=[
        Component(name='comp.sub', bom_ref='foo')]))
    bom.services.add(Service(name='serv', bom_ref='foo'))
    bom.vulnerabilities.add(Vulnerability(id='vuln', bom_ref='foo'))
    nr_bomrefs = 6  # number of bom-refs used
    return bom, nr_bomrefs


def get_bom_for_issue_630_empty_property() -> Bom:
    """regression test for issue #630
    see https://github.com/CycloneDX/cyclonedx-python-lib/issues/630
    """
    return _make_bom(components={
        Component(
            bom_ref='example@15.8.0',
            type=ComponentType.LIBRARY,
            name='example',
            version='15.8.0',
            properties=[Property(name='cdx:npm:package:path')]
        )
    })


def get_bom_with_lifecycles() -> Bom:
    return _make_bom(
        metadata=BomMetaData(
            lifecycles=[
                PredefinedLifecycle(LifecyclePhase.BUILD),
                PredefinedLifecycle(LifecyclePhase.POST_BUILD),
                NamedLifecycle(name='platform-integration-testing',
                               description='Integration testing specific to the runtime platform'),
            ],
            component=Component(name='app', type=ComponentType.APPLICATION, bom_ref='my-app'),
        )
    )


def get_bom_with_definitions_standards() -> Bom:
    """
    Returns a BOM with definitions and standards only.
    """
    return _make_bom(
        definitions=Definitions(standards=[
            Standard(name='Some Standard', version='1.2.3', description='Some description', bom_ref='some-standard',
                     owner='Some Owner', external_references=[get_external_reference_2()]
                     )
        ])
    )


# ---


all_get_bom_funct_valid = tuple(
    (n, f) for n, f in getmembers(sys.modules[__name__], isfunction)
    if n.startswith('get_bom_') and not n.endswith('_invalid')
)

all_get_bom_funct_valid_immut = tuple(
    (n, f) for n, f in getmembers(sys.modules[__name__], isfunction)
    if n.startswith('get_bom_') and not n.endswith('_invalid') and not n.endswith('_migrate')
)

all_get_bom_funct_valid_reversible_migrate = tuple(
    (n, f) for n, f in getmembers(sys.modules[__name__], isfunction)
    if n.startswith('get_bom_') and n.endswith('_migrate') and not n.endswith('_irreversible_migrate')
)

all_get_bom_funct_invalid = tuple(
    (n, f) for n, f in getmembers(sys.modules[__name__], isfunction)
    if n.startswith('get_bom_') and n.endswith('_invalid')
)

all_get_bom_funct_with_incomplete_deps = {
    # List of functions that return BOM with an incomplete dependency graph.
    # It is expected that some process auto-fixes this before actual serialization takes place.
    get_bom_just_complete_metadata,
    get_bom_with_component_setuptools_basic,
    get_bom_with_component_setuptools_complete,
    get_bom_with_component_setuptools_no_component_version,
    get_bom_with_component_setuptools_with_cpe,
    get_bom_with_component_setuptools_with_release_notes,
    get_bom_with_component_setuptools_with_vulnerability,
    get_bom_with_component_toml_1,
    get_bom_with_dependencies_hanging,
    get_bom_with_metadata_component_and_dependencies,
    get_bom_with_nested_services,
    get_bom_with_services_complex,
    get_bom_with_services_simple,
    get_bom_with_licenses,
    get_bom_with_multiple_licenses,
    get_bom_for_issue_497_urls,
    get_bom_for_issue_598_multiple_components_with_purl_qualifiers,
    get_bom_with_component_setuptools_with_v16_fields,
    get_bom_for_issue_630_empty_property,
    get_bom_with_lifecycles,
    get_bom_with_definitions_standards,
}
