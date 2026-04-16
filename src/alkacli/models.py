from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Compound:
    name: str
    formula: str
    eq_per_mol: float
    aliases: tuple[str, ...] = ()
    category: str = "salt"
    notes: str = ""


@dataclass(frozen=True, slots=True)
class Amount:
    value: float
    unit: str


@dataclass(slots=True)
class CalculationResult:
    compound: Compound
    input_amount: Amount
    mmol: float
    mEq: float
    mass_g: float
    elemental_masses_g: dict[str, float] = field(default_factory=dict)
    mode: str = "chemical"
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "compound": self.compound.name,
            "formula": self.compound.formula,
            "input": {"value": self.input_amount.value, "unit": self.input_amount.unit},
            "mmol": self.mmol,
            "mEq": self.mEq,
            "mass_g": self.mass_g,
            "elemental_masses_g": self.elemental_masses_g,
            "mode": self.mode,
            "notes": self.notes,
        }


@dataclass(slots=True)
class SolveResult:
    compound: Compound
    target_mEq: float
    solved_mass_g: float
    mmol: float
    mEq: float
    elemental_masses_g: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "compound": self.compound.name,
            "formula": self.compound.formula,
            "target_mEq": self.target_mEq,
            "solved_mass_g": self.solved_mass_g,
            "mmol": self.mmol,
            "mEq": self.mEq,
            "elemental_masses_g": self.elemental_masses_g,
        }
