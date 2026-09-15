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

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional, Union
from urllib.parse import urlsplit as _urlsplit
from xml.etree.ElementTree import Element as XmlElement  # nosec B405

import py_serializable as serializable

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import InvalidValueException
from . import XsUri


@serializable.serializable_enum
class JsfAlgorithm(str, Enum):
    """
    Recognized JWA [RFC7518] and RFC8037 asymmetric/symmetric key algorithms for JSF signatures.

    Note: Unlike RFC8037, JSF requires explicit Ed* algorithm names instead of "EdDSA".

    For proprietary algorithms, pass an absolute :class:`~cyclonedx.model.XsUri` to
    :class:`JsfSimpleSignature`.
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


@serializable.serializable_enum
class JsfEcCurve(str, Enum):
    """
    Elliptic curve names for EC public keys in JSF signatures.

    Supported curves per the JSF 0.82 specification.
    """

    P_256 = 'P-256'
    P_384 = 'P-384'
    P_521 = 'P-521'


@serializable.serializable_enum
class JsfOkpCurve(str, Enum):
    """
    Curve names for OKP (Octet Key Pair) public keys in JSF signatures.

    Supported curves per the JSF 0.82 specification.
    """

    ED25519 = 'Ed25519'
    ED448 = 'Ed448'


# Fields each JSF public-key type must not carry, per the JSF schema (`additionalProperties: false`).
_FORBIDDEN_PUBLIC_KEY_FIELDS: 'dict[JsfKeyType, tuple[str, ...]]' = {
    JsfKeyType.EC: ('n', 'e'),
    JsfKeyType.OKP: ('y', 'n', 'e'),
    JsfKeyType.RSA: ('crv', 'x', 'y'),
}


def _check_no_rsa_fields(kty: JsfKeyType, n: Optional[str], e: Optional[str]) -> None:
    if n is not None or e is not None:
        raise InvalidValueException(
            f'{kty.value} public key must not include RSA-specific fields (n, e)'
        )


def _check_no_y_field(y: Optional[str]) -> None:
    if y is not None:
        raise InvalidValueException('OKP public key must not include y')


def _check_no_ec_okp_fields(
    crv: 'Optional[Union[JsfEcCurve, JsfOkpCurve]]',
    x: Optional[str],
    y: Optional[str],
) -> None:
    if crv is not None or x is not None or y is not None:
        raise InvalidValueException(
            'RSA public key must not include EC/OKP-specific fields (crv, x, y)'
        )


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
        crv: Optional[Union[JsfEcCurve, JsfOkpCurve]] = None,
        x: Optional[str] = None,
        y: Optional[str] = None,
        n: Optional[str] = None,
        e: Optional[str] = None,
    ) -> None:
        # Validate conditional schema requirements per JSF spec
        if kty == JsfKeyType.EC:
            if crv is None or x is None or y is None:
                raise InvalidValueException('EC public key requires crv, x, and y')
            if not isinstance(crv, JsfEcCurve):
                raise InvalidValueException(
                    f'EC public key crv must be a JsfEcCurve instance, got {type(crv).__name__!r}'
                )
            _check_no_rsa_fields(kty, n, e)
        elif kty == JsfKeyType.OKP:
            if crv is None or x is None:
                raise InvalidValueException('OKP public key requires crv and x')
            if not isinstance(crv, JsfOkpCurve):
                raise InvalidValueException(
                    f'OKP public key crv must be a JsfOkpCurve instance, got {type(crv).__name__!r}'
                )
            _check_no_y_field(y)
            _check_no_rsa_fields(kty, n, e)
        elif kty == JsfKeyType.RSA:
            if n is None or e is None:
                raise InvalidValueException('RSA public key requires n and e')
            _check_no_ec_okp_fields(crv, x, y)

        self.kty = kty
        self.crv: Optional[Union[JsfEcCurve, JsfOkpCurve]] = crv
        self.x = x
        self.y = y
        self.n = n
        self.e = e

    def _as_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {'kty': self.kty.value}
        if self.crv is not None:
            d['crv'] = self.crv.value
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
        kty = JsfKeyType(d['kty'])
        forbidden = _FORBIDDEN_PUBLIC_KEY_FIELDS[kty]
        if any(field in d for field in forbidden):
            raise InvalidValueException(f'{kty.value} public key must not include fields: {", ".join(forbidden)}')
        crv_raw = d.get('crv')
        crv: Optional[Union[JsfEcCurve, JsfOkpCurve]] = None
        if crv_raw is not None:
            if kty == JsfKeyType.EC:
                crv = JsfEcCurve(crv_raw)
            elif kty == JsfKeyType.OKP:
                crv = JsfOkpCurve(crv_raw)
        return cls(kty=kty, crv=crv, x=d.get('x'), y=d.get('y'), n=d.get('n'), e=d.get('e'))

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


class JsfSignature(ABC):
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

    @abstractmethod
    def _as_dict(self) -> dict[str, Any]:
        ...  # pragma: no cover

    @classmethod
    @abstractmethod
    def _from_dict(cls, d: dict[str, Any]) -> 'JsfSignature':
        ...  # pragma: no cover

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
        algorithm: Union[JsfAlgorithm, XsUri],
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
        self.certificate_path = list(certificate_path or [])
        self.excludes = list(excludes or [])

    @property
    def algorithm(self) -> Union[JsfAlgorithm, XsUri]:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: Union[JsfAlgorithm, XsUri]) -> None:
        if not isinstance(algorithm, (JsfAlgorithm, XsUri)):
            raise InvalidValueException('algorithm must be a JsfAlgorithm or XsUri instance')
        if isinstance(algorithm, XsUri) and not _urlsplit(str(algorithm)).scheme:
            raise InvalidValueException(f'Proprietary JSF algorithm must be an absolute URI, got {algorithm!r}')
        self._algorithm = algorithm

    def _as_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            'algorithm': self.algorithm.value if isinstance(self.algorithm, JsfAlgorithm) else str(self.algorithm),
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
        try:
            algorithm: Union[JsfAlgorithm, XsUri] = JsfAlgorithm(d['algorithm'])
        except ValueError:
            algorithm = XsUri(d['algorithm'])
        pk = d.get('publicKey')
        return cls(
            algorithm=algorithm,
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
        if not all(isinstance(signer, JsfSimpleSignature) for signer in signers):
            raise InvalidValueException('signers must contain only JsfSimpleSignature instances')
        self.signers = list(signers)

    def _as_dict(self) -> dict[str, Any]:
        return {'signers': [s._as_dict() for s in self.signers]}

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> 'JsfSignatureSigners':
        return cls(signers=[JsfSimpleSignature._from_dict(s) for s in d['signers']])

    def __repr__(self) -> str:
        return f'<JsfSignatureSigners signers=[{len(self.signers)}]>'


class JsfSignatureChain(JsfSignature):
    """
    Signature-chain JSF signature: ``signaturechain`` in the JSF schema.

    Contains a list of :class:`JsfSimpleSignature` objects serialized under the ``chain`` key.
    """

    def __init__(self, *, chain: list['JsfSimpleSignature']) -> None:
        if not all(isinstance(signature, JsfSimpleSignature) for signature in chain):
            raise InvalidValueException('chain must contain only JsfSimpleSignature instances')
        self.chain = list(chain)

    def _as_dict(self) -> dict[str, Any]:
        return {'chain': [s._as_dict() for s in self.chain]}

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> 'JsfSignatureChain':
        return cls(chain=[JsfSimpleSignature._from_dict(s) for s in d['chain']])

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
        if isinstance(o, JsfSimpleSignature):
            algo_str = o.algorithm.value if isinstance(o.algorithm, JsfAlgorithm) else str(o.algorithm)
            return _ComparableTuple((algo_str, o.value, o.key_id, o.public_key,
                                    _ComparableTuple(o.certificate_path),
                                    _ComparableTuple(o.excludes)))
        raise TypeError(f'Unknown JsfSignature subtype: {type(o)!r}')  # pragma: no cover

    @classmethod
    def json_normalize(cls, o: JsfSignature, *,
                       view: Optional[type[serializable.ViewType]],
                       **__: Any) -> Any:
        return o._as_dict()

    @classmethod
    def json_denormalize(cls, o: Any, **__: Any) -> JsfSignature:
        if not isinstance(o, dict):
            raise TypeError(f'Expected dict, got {type(o)!r}')
        if 'signers' in o and 'chain' in o:
            raise InvalidValueException('JSF signature cannot contain both signers and chain')
        if 'signers' in o:
            return JsfSignatureSigners._from_dict(o)
        if 'chain' in o:
            return JsfSignatureChain._from_dict(o)
        return JsfSimpleSignature._from_dict(o)

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
