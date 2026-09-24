import secrets
import time

from hermes.core.errors import HermesError

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

_ENTITY_TYPE_FLAGS = {
    "entity": 0,
    "company": 1,
    "country": 2,
    "person": 3,
    "organisation": 4,
    "instrument": 5,
    "event": 6,
    "document": 7,
}

_KNOWN_ENTITY_TYPES = frozenset(_ENTITY_TYPE_FLAGS)

# 22 Base62 digits hold ceil(log2(62^22)) = 131 bits.
# Layout (high to low, 120 bits total): timestamp_ms (41) | entity-type flag (3) | random (76)
_RANDOM_BITS = 76


class InvalidEntityTypeError(HermesError):
    """Raised when hrm_id is called with an unknown entity type."""


def base62_encode(number: int) -> str:
    if number == 0:
        return BASE62[0]

    result = []

    while number:
        number, remainder = divmod(number, 62)
        result.append(BASE62[remainder])

    return "".join(reversed(result))


def hrm_id(entity_type: str, *, timestamp_ms: int | None = None) -> str:
    etype = entity_type.strip().lower()

    if etype not in _ENTITY_TYPE_FLAGS:
        raise InvalidEntityTypeError(
            f"Unknown entity type {entity_type!r}. Known: {sorted(_KNOWN_ENTITY_TYPES)}"
        )

    timestamp = time.time() if timestamp_ms is None else timestamp_ms / 1000
    timestamp_bits = int(timestamp * 1000) if timestamp_ms is None else int(timestamp_ms)

    if not (0 <= timestamp_bits < (1 << 41)):
        raise ValueError("timestamp_ms out of range for hrm_id (must fit 41 bits)")

    flag = _ENTITY_TYPE_FLAGS[etype]
    random_bits = secrets.randbits(_RANDOM_BITS)

    value = (timestamp_bits << (_RANDOM_BITS + 3)) | (flag << _RANDOM_BITS) | random_bits

    encoded = base62_encode(value)

    return f"HRM-{etype.upper()}-{encoded.upper().zfill(22)}"


if __name__ == "__main__":
    for etype in _KNOWN_ENTITY_TYPES:
        for _ in range(100):
            ident = hrm_id(etype)
            init, typ, body = ident.split("-")
            assert len(body) == 22, f"bad body length: {ident}"
            assert init == "HRM" and typ.isalpha() and body.isalnum()
    target = len("HRM-ENTITY-") + 22
    assert len(hrm_id("entity")) == target
    try:
        hrm_id("species")
    except InvalidEntityTypeError:
        pass
    else:
        raise AssertionError("unknown entity type must be rejected")
    print(f"hrm_id self-check ok: {hrm_id('company')}")