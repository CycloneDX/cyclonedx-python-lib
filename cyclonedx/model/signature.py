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
    These classes are a data model only. This library does not create, verify, or canonicalize
    (RFC 8785/JCS) signatures. Re-serializing a signed BOM through this library (property
    reordering, normalization, dropped unknown fields) will in general invalidate an existing signature.

.. note::
    See the JSF specification: https://cyberphone.github.io/doc/security/jsf.html
    See the CycloneDX Schema reference: https://cyclonedx.org/docs/1.4/json/#signature
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
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

# Curve enum each JSF public-key type requires for `crv`.
_PUBLIC_KEY_CURVE_TYPES: 'dict[JsfKeyType, type[Enum]]' = {
    JsfKeyType.EC: JsfEcCurve,
    JsfKeyType.OKP: JsfOkpCurve,
}


class JsfPublicKey:
    """
    Public key object as defined by the JSF standard.

    Supports three key types (determined by ``kty``):

    - **EC**: requires ``crv``, ``x``, ``y``
    - **OKP**: requires ``crv``, ``x``
    - **RSA**: requires ``n``, ``e``

    The conditional requirements are validated on construction and on every property assignment.
    An assignment that would make the key invalid raises :class:`~cyclonedx.exception.model.InvalidValueException`
    and leaves the key unchanged. To switch the key type, create a new :class:`JsfPublicKey`.
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
        self._kty = kty
        self._crv = crv
        self._x = x
        self._y = y
        self._n = n
        self._e = e
        self._validate()

    def _validate(self) -> None:
        # Validate conditional schema requirements per JSF spec
        kty = self._kty
        if kty == JsfKeyType.EC:
            if self._crv is None or self._x is None or self._y is None:
                raise InvalidValueException('EC public key requires crv, x, and y')
        elif kty == JsfKeyType.OKP:
            if self._crv is None or self._x is None:
                raise InvalidValueException('OKP public key requires crv and x')
        elif kty == JsfKeyType.RSA:
            if self._n is None or self._e is None:
                raise InvalidValueException('RSA public key requires n and e')
        else:
            raise InvalidValueException(f'kty must be a JsfKeyType instance, got {kty!r}')
        curve_type = _PUBLIC_KEY_CURVE_TYPES.get(kty)
        if curve_type is not None and not isinstance(self._crv, curve_type):
            raise InvalidValueException(
                f'{kty.value} public key crv must be a {curve_type.__name__} instance, '
                f'got {type(self._crv).__name__!r}'
            )
        present = [f for f in _FORBIDDEN_PUBLIC_KEY_FIELDS[kty] if getattr(self, f'_{f}') is not None]
        if present:
            raise InvalidValueException(f'{kty.value} public key must not include fields: {", ".join(present)}')

    def _set(self, attr: str, value: Any) -> None:
        old = getattr(self, attr)
        setattr(self, attr, value)
        try:
            self._validate()
        except InvalidValueException:
            setattr(self, attr, old)
            raise

    @property
    def kty(self) -> JsfKeyType:
        return self._kty

    @kty.setter
    def kty(self, kty: JsfKeyType) -> None:
        self._set('_kty', kty)

    @property
    def crv(self) -> Optional[Union[JsfEcCurve, JsfOkpCurve]]:
        return self._crv

    @crv.setter
    def crv(self, crv: Optional[Union[JsfEcCurve, JsfOkpCurve]]) -> None:
        self._set('_crv', crv)

    @property
    def x(self) -> Optional[str]:
        return self._x

    @x.setter
    def x(self, x: Optional[str]) -> None:
        self._set('_x', x)

    @property
    def y(self) -> Optional[str]:
        return self._y

    @y.setter
    def y(self, y: Optional[str]) -> None:
        self._set('_y', y)

    @property
    def n(self) -> Optional[str]:
        return self._n

    @n.setter
    def n(self, n: Optional[str]) -> None:
        self._set('_n', n)

    @property
    def e(self) -> Optional[str]:
        return self._e

    @e.setter
    def e(self, e: Optional[str]) -> None:
        self._set('_e', e)

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
        crv = d.get('crv')
        curve_type = _PUBLIC_KEY_CURVE_TYPES.get(kty)
        if crv is not None and curve_type is not None:
            crv = curve_type(crv)
        # a `crv` on an RSA key stays raw, so validation rejects it
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

    @abstractmethod
    def _comparable_tuple(self) -> _ComparableTuple:
        """Comparable key; its first element discriminates the signature mode."""
        ...  # pragma: no cover

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JsfSignature):
            return self._comparable_tuple() == other._comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, JsfSignature):
            return self._comparable_tuple() < other._comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._comparable_tuple())


def _check_simple_signatures(name: str, signatures: Iterable['JsfSimpleSignature']) -> 'list[JsfSimpleSignature]':
    signatures = list(signatures)
    if not all(isinstance(s, JsfSimpleSignature) for s in signatures):
        raise InvalidValueException(f'{name} must contain only JsfSimpleSignature instances')
    return signatures


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
        certificate_path: Optional[Iterable[str]] = None,
        excludes: Optional[Iterable[str]] = None,
    ) -> None:
        self.algorithm = algorithm
        self.value = value
        self.key_id = key_id
        self.public_key = public_key
        self.certificate_path = certificate_path or []
        self.excludes = excludes or []

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

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        if not isinstance(value, str):
            raise InvalidValueException(f'value must be a str, got {type(value).__name__!r}')
        self._value = value

    @property
    def key_id(self) -> Optional[str]:
        return self._key_id

    @key_id.setter
    def key_id(self, key_id: Optional[str]) -> None:
        self._key_id = key_id

    @property
    def public_key(self) -> Optional[JsfPublicKey]:
        return self._public_key

    @public_key.setter
    def public_key(self, public_key: Optional[JsfPublicKey]) -> None:
        self._public_key = public_key

    @property
    def certificate_path(self) -> list[str]:
        """Ordered certificate chain; order is significant and preserved."""
        return self._certificate_path

    @certificate_path.setter
    def certificate_path(self, certificate_path: Iterable[str]) -> None:
        self._certificate_path = list(certificate_path)

    @property
    def excludes(self) -> list[str]:
        return self._excludes

    @excludes.setter
    def excludes(self, excludes: Iterable[str]) -> None:
        self._excludes = list(excludes)

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

    def _comparable_tuple(self) -> _ComparableTuple:
        algo_str = self.algorithm.value if isinstance(self.algorithm, JsfAlgorithm) else str(self.algorithm)
        return _ComparableTuple((0, algo_str, self.value, self.key_id, self.public_key,
                                 _ComparableTuple(self.certificate_path), _ComparableTuple(self.excludes)))

    def __repr__(self) -> str:
        return f'<JsfSimpleSignature algorithm={self.algorithm!r}>'


class JsfSignatureSigners(JsfSignature):
    """
    Multiple-signers JSF signature: ``multisignature`` in the JSF schema.

    Contains a list of :class:`JsfSimpleSignature` objects serialized under the ``signers`` key.

    .. note::
        An empty ``signers`` list is schema-valid, but carries no signature.
    """

    def __init__(self, *, signers: Iterable['JsfSimpleSignature']) -> None:
        self.signers = signers

    @property
    def signers(self) -> 'list[JsfSimpleSignature]':
        return self._signers

    @signers.setter
    def signers(self, signers: Iterable['JsfSimpleSignature']) -> None:
        self._signers = _check_simple_signatures('signers', signers)

    def _as_dict(self) -> dict[str, Any]:
        return {'signers': [s._as_dict() for s in self.signers]}

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> 'JsfSignatureSigners':
        return cls(signers=[JsfSimpleSignature._from_dict(s) for s in d['signers']])

    def _comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((1, _ComparableTuple(self.signers)))

    def __repr__(self) -> str:
        return f'<JsfSignatureSigners signers=[{len(self.signers)}]>'


class JsfSignatureChain(JsfSignature):
    """
    Signature-chain JSF signature: ``signaturechain`` in the JSF schema.

    Contains a list of :class:`JsfSimpleSignature` objects serialized under the ``chain`` key.

    .. note::
        An empty ``chain`` list is schema-valid, but carries no signature.
    """

    def __init__(self, *, chain: Iterable['JsfSimpleSignature']) -> None:
        self.chain = chain

    @property
    def chain(self) -> 'list[JsfSimpleSignature]':
        return self._chain

    @chain.setter
    def chain(self, chain: Iterable['JsfSimpleSignature']) -> None:
        self._chain = _check_simple_signatures('chain', chain)

    def _as_dict(self) -> dict[str, Any]:
        return {'chain': [s._as_dict() for s in self.chain]}

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> 'JsfSignatureChain':
        return cls(chain=[JsfSimpleSignature._from_dict(s) for s in d['chain']])

    def _comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((2, _ComparableTuple(self.chain)))

    def __repr__(self) -> str:
        return f'<JsfSignatureChain chain=[{len(self.chain)}]>'


class _JsfSignatureSerializationHelper(serializable.helpers.BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API  """

    @classmethod
    def json_normalize(cls, o: JsfSignature, *,
                       view: Optional[type[serializable.ViewType]],
                       **__: Any) -> Any:
        return o._as_dict()

    @classmethod
    def json_denormalize(cls, o: Any, **__: Any) -> JsfSignature:
        if not isinstance(o, dict):
            raise InvalidValueException(f'JSF signature must be an object, got {type(o).__name__!r}')
        if 'signers' in o and 'chain' in o:
            raise InvalidValueException('JSF signature cannot contain both signers and chain')
        try:
            if 'signers' in o:
                return JsfSignatureSigners._from_dict(o)
            if 'chain' in o:
                return JsfSignatureChain._from_dict(o)
            return JsfSimpleSignature._from_dict(o)
        except (KeyError, ValueError, TypeError) as err:
            raise InvalidValueException(f'invalid JSF signature: {err!r}') from err

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
