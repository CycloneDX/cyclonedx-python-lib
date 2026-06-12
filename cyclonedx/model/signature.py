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
JSF (JSON Signature Format) signature-related classes.

.. note::
    JSON-only. There is no XSD/XML equivalent for JSF signatures in CycloneDX.

.. note::
    Introduced in CycloneDX v1.4

.. note::
    See the JSF specification: https://cyberphone.github.io/doc/security/jsf.html
    See the CycloneDX Schema reference: https://cyclonedx.org/docs/1.4/json/#signature
"""

from enum import Enum
from typing import Any, Optional, Union, cast
from xml.etree.ElementTree import Element as XmlElement  # nosec B405

import py_serializable as serializable

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import InvalidValueException


@serializable.serializable_enum
class JsfAlgorithm(str, Enum):
    """
    Recognized JWA [RFC7518] and RFC8037 asymmetric/symmetric key algorithms for JSF signatures.

    Note: Unlike RFC8037, JSF requires explicit Ed* algorithm names instead of "EdDSA".

    For proprietary algorithms, pass a URI string directly — the ``algorithm`` field on
    :class:`JsfSignature`, :class:`JsfSignatureSigners`, and :class:`JsfSignatureChain`
    accepts both :class:`JsfAlgorithm` enum values and arbitrary strings.
    """

    RS256 = 'RS256'
    RS384 = 'RS384'
    RS512 = 'RS512'
    PS256 = 'PS256'
    PS384 = 'PS384'
    PS512 = 'PS512'
    ES256 = 'ES256'
    ES384 = 'ES384'
    ES512 = 'ES512'
    ED25519 = 'Ed25519'
    ED448 = 'Ed448'
    HS256 = 'HS256'
    HS384 = 'HS384'
    HS512 = 'HS512'


@serializable.serializable_enum
class JsfKeyType(str, Enum):
    """
    Key type indicator for a JSF public key.
    """

    EC = 'EC'
    OKP = 'OKP'
    RSA = 'RSA'


class JsfPublicKey:
    """
    Public key object as defined by the JSF standard.

    Supports three key types (determined by ``kty``):

    - **EC**: requires ``crv``, ``x``, ``y``
    - **OKP**: requires ``crv``, ``x``
    - **RSA**: requires ``n``, ``e``
    """

    def __init__(
        self, *,
        kty: JsfKeyType,
        crv: Optional[str] = None,
        x: Optional[str] = None,
        y: Optional[str] = None,
        n: Optional[str] = None,
        e: Optional[str] = None,
    ) -> None:
        # Validate conditional schema requirements per JSF spec
        if kty == JsfKeyType.EC:
            if not (crv and x and y):
                raise InvalidValueException(
                    'EC public key requires crv, x, and y'
                )
        elif kty == JsfKeyType.OKP:
            if not (crv and x):
                raise InvalidValueException(
                    'OKP public key requires crv and x'
                )
        elif kty == JsfKeyType.RSA:
            if not (n and e):
                raise InvalidValueException(
                    'RSA public key requires n and e'
                )

        self.kty = kty
        self.crv = crv
        self.x = x
        self.y = y
        self.n = n
        self.e = e

    def _as_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {'kty': self.kty.value}
        if self.crv is not None:
            d['crv'] = self.crv
        if self.x is not None:
            d['x'] = self.x
        if self.y is not None:
            d['y'] = self.y
        if self.n is not None:
            d['n'] = self.n
        if self.e is not None:
            d['e'] = self.e
        return d

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> 'JsfPublicKey':
        return cls(
            kty=JsfKeyType(d['kty']),
            crv=d.get('crv'),
            x=d.get('x'),
            y=d.get('y'),
            n=d.get('n'),
            e=d.get('e'),
        )

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.kty, self.crv, self.x, self.y, self.n, self.e))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JsfPublicKey):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, JsfPublicKey):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<JsfPublicKey kty={self.kty}>'


class JsfSignature:
    """
    JSF (JSON Signature Format) signature object — abstract base class.

    The JSF specification defines three mutually exclusive signature modes, each represented by
    a separate concrete class:

    - **Simple signature** (``signaturecore``): :class:`JsfSimpleSignature`: a single signature
      with required ``algorithm`` and ``value``, plus optional ``key_id``, ``public_key``,
      ``certificate_path``, and ``excludes``
    - **Multiple signers** (``multisignature``): :class:`JsfSignatureSigners`: contains a
      ``signers`` list of :class:`JsfSimpleSignature`
    - **Signature chain** (``signaturechain``): :class:`JsfSignatureChain`: contains a
      ``chain`` list of :class:`JsfSimpleSignature`

    .. note::
        JSON-only. There is no XSD/XML equivalent in any CycloneDX schema version.

    .. note::
        Introduced in CycloneDX v1.4
    """

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JsfSignature):
            return _JsfSignatureSerializationHelper._sort_key(self) == _JsfSignatureSerializationHelper._sort_key(other)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, JsfSignature):
            return _JsfSignatureSerializationHelper._sort_key(self) < _JsfSignatureSerializationHelper._sort_key(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(_JsfSignatureSerializationHelper._sort_key(self))


class JsfSimpleSignature(JsfSignature):
    """
    JSF simple signature object: ``signaturecore`` mode.

    Represents a single signature with required ``algorithm`` and ``value``, plus optional
    ``key_id``, ``public_key``, ``certificate_path``, and ``excludes``.
    """

    def __init__(
        self, *,
        algorithm: Union[JsfAlgorithm, str],
        value: str,
        key_id: Optional[str] = None,
        public_key: Optional[JsfPublicKey] = None,
        certificate_path: Optional[list[str]] = None,
        excludes: Optional[list[str]] = None,
    ) -> None:
        self.algorithm = algorithm
        self.value = value
        self.key_id = key_id
        self.public_key = public_key
        self.certificate_path = list(certificate_path) if certificate_path else []
        self.excludes = list(excludes) if excludes else []

    def _as_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            'algorithm': str(self.algorithm),
            'value': self.value,
        }
        if self.key_id is not None:
            d['keyId'] = self.key_id
        if self.public_key is not None:
            d['publicKey'] = self.public_key._as_dict()
        if self.certificate_path:
            d['certificatePath'] = list(self.certificate_path)
        if self.excludes:
            d['excludes'] = list(self.excludes)
        return d

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> 'JsfSimpleSignature':
        pk = d.get('publicKey')
        return cls(
            algorithm=d['algorithm'],
            value=d['value'],
            key_id=d.get('keyId'),
            public_key=JsfPublicKey._from_dict(pk) if pk is not None else None,
            certificate_path=d.get('certificatePath'),
            excludes=d.get('excludes'),
        )

    def __repr__(self) -> str:
        return f'<JsfSimpleSignature algorithm={self.algorithm!r}>'


class JsfSignatureSigners(JsfSignature):
    """
    Multiple-signers JSF signature: ``multisignature`` in the JSF schema.

    Contains a list of :class:`JsfSimpleSignature` objects serialized under the ``signers`` key.
    """

    def __init__(self, *, signers: list['JsfSimpleSignature']) -> None:
        self.signers = list(signers)

    def __repr__(self) -> str:
        return f'<JsfSignatureSigners signers=[{len(self.signers)}]>'


class JsfSignatureChain(JsfSignature):
    """
    Signature-chain JSF signature: ``signaturechain`` in the JSF schema.

    Contains a list of :class:`JsfSimpleSignature` objects serialized under the ``chain`` key.
    """

    def __init__(self, *, chain: list['JsfSimpleSignature']) -> None:
        self.chain = list(chain)

    def __repr__(self) -> str:
        return f'<JsfSignatureChain chain=[{len(self.chain)}]>'


class _JsfSignatureSerializationHelper(serializable.helpers.BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API  """

    @staticmethod
    def _sort_key(o: JsfSignature) -> _ComparableTuple:
        """Generate a comparable tuple key for sorting and equality.

        Handles all three signature modes by delegating to type-specific logic.
        """
        if isinstance(o, JsfSignatureChain):
            return _ComparableTuple(('chain', _ComparableTuple(o.chain)))
        if isinstance(o, JsfSignatureSigners):
            return _ComparableTuple(('signers', _ComparableTuple(o.signers)))
        # Simple signature (JsfSimpleSignature)
        o = cast(JsfSimpleSignature, o)
        return _ComparableTuple((str(o.algorithm), o.value, o.key_id, o.public_key,
                                _ComparableTuple(o.certificate_path),
                                _ComparableTuple(o.excludes)))

    @classmethod
    def json_normalize(cls, o: JsfSignature, *,
                       view: Optional[type[serializable.ViewType]],
                       **__: Any) -> Any:
        if isinstance(o, JsfSignatureSigners):
            return {'signers': [s._as_dict() for s in o.signers]}
        if isinstance(o, JsfSignatureChain):
            return {'chain': [s._as_dict() for s in o.chain]}
        # Simple signature
        o = cast(JsfSimpleSignature, o)
        d: dict[str, Any] = {
            'algorithm': str(o.algorithm),
            'value': o.value,
        }
        if o.key_id is not None:
            d['keyId'] = o.key_id
        if o.public_key is not None:
            d['publicKey'] = o.public_key._as_dict()
        if o.certificate_path:
            d['certificatePath'] = list(o.certificate_path)
        if o.excludes:
            d['excludes'] = list(o.excludes)
        return d

    @classmethod
    def json_denormalize(cls, o: Any, **__: Any) -> JsfSignature:
        if not isinstance(o, dict):
            raise TypeError(f'Expected dict, got {type(o)!r}')
        if 'signers' in o:
            return JsfSignatureSigners(signers=[JsfSimpleSignature._from_dict(s) for s in o['signers']])
        if 'chain' in o:
            return JsfSignatureChain(chain=[JsfSimpleSignature._from_dict(s) for s in o['chain']])
        # Simple signature: must have at least 'algorithm' and 'value'
        pk = o.get('publicKey')
        return JsfSimpleSignature(
            algorithm=o['algorithm'],
            value=o['value'],
            key_id=o.get('keyId'),
            public_key=JsfPublicKey._from_dict(pk) if pk is not None else None,
            certificate_path=o.get('certificatePath'),
            excludes=o.get('excludes'),
        )

    @classmethod
    def xml_normalize(cls, o: JsfSignature, *,
                      element_name: Optional[str],
                      view: Optional[type[serializable.ViewType]],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[XmlElement]:
        return None  # JSF signatures have no XML representation

    @classmethod
    def xml_denormalize(cls, o: XmlElement, *,
                        default_ns: Optional[str],
                        **__: Any) -> Optional[JsfSignature]:
        return None  # JSF signatures have no XML representation
