from __future__ import annotations

from .calc import calculate as _calculate
from .calc import solve_mass as _solve_mass
from .models import Amount, CalculationResult, Compound, SolveResult
from .registry import get_compound as _get_compound
from .registry import list_compounds as _list_compounds
from .units import parse_amount as _parse_amount


def resolve_compound(compound: str | Compound) -> Compound:
    if isinstance(compound, Compound):
        return compound
    return _get_compound(compound)


def resolve_amount(amount: str | Amount) -> Amount:
    if isinstance(amount, Amount):
        return amount
    return _parse_amount(amount)


def calculate(
    compound: str | Compound, amount: str | Amount, mode: str = "chemical"
) -> CalculationResult:
    return _calculate(resolve_compound(compound), resolve_amount(amount), mode=mode)


def solve(compound: str | Compound, target_mEq: float | str) -> SolveResult:
    resolved = resolve_compound(compound)
    if isinstance(target_mEq, str):
        target = _parse_amount(target_mEq)
        if target.unit != "mEq":
            raise ValueError("Target must use mEq, for example '50mEq'.")
        target_value = target.value
    else:
        target_value = float(target_mEq)
    return _solve_mass(resolved, target_value)


def get_compound(name: str) -> Compound:
    return _get_compound(name)


def list_compounds() -> list[Compound]:
    return _list_compounds()


__all__ = [
    "Amount",
    "CalculationResult",
    "Compound",
    "SolveResult",
    "calculate",
    "get_compound",
    "list_compounds",
    "resolve_amount",
    "resolve_compound",
    "solve",
]
