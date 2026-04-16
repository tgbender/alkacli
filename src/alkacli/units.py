from __future__ import annotations

import re

from .models import Amount

_UNIT_ALIASES = {
    "g": "g",
    "mg": "mg",
    "kg": "kg",
    "mol": "mol",
    "mmol": "mmol",
    "meq": "mEq",
    "eq": "mEq",
}

_AMOUNT_RE = re.compile(r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))(?:\s*([A-Za-z]+))?\s*$")


def parse_amount(text: str) -> Amount:
    match = _AMOUNT_RE.match(text)
    if not match:
        raise ValueError(
            f"Invalid amount: {text!r}. Use forms like 1g, 250mg, 2.5mmol, 10mEq."
        )
    value = float(match.group(1))
    unit_raw = match.group(2) or "g"
    unit_key = unit_raw.lower()
    if unit_key not in _UNIT_ALIASES:
        raise ValueError(f"Unsupported unit: {unit_raw!r}")
    return Amount(value=value, unit=_UNIT_ALIASES[unit_key])


def amount_to_base_units(amount: Amount) -> tuple[float, str]:
    unit = amount.unit
    value = amount.value
    if unit == "g":
        return value, "g"
    if unit == "mg":
        return value / 1000.0, "g"
    if unit == "kg":
        return value * 1000.0, "g"
    if unit == "mol":
        return value, "mol"
    if unit == "mmol":
        return value / 1000.0, "mol"
    if unit == "mEq":
        return value, "mEq"
    raise ValueError(f"Unsupported unit: {unit!r}")
