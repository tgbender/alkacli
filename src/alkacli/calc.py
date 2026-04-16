from __future__ import annotations

from .chem import elemental_masses_g, molar_mass_g_per_mol
from .models import Amount, CalculationResult, Compound, SolveResult
from .units import amount_to_base_units


def _value_to_moles(
    amount: Amount, molar_mass: float, eq_per_mol: float
) -> tuple[float, float, float]:
    base_value, base_unit = amount_to_base_units(amount)
    if base_unit == "g":
        moles = base_value / molar_mass
        mmol = moles * 1000.0
        mEq = moles * eq_per_mol * 1000.0
        return moles, mmol, mEq
    if base_unit == "mol":
        moles = base_value
        mmol = moles * 1000.0
        mEq = moles * eq_per_mol * 1000.0
        return moles, mmol, mEq
    if base_unit == "mEq":
        moles = base_value / 1000.0 / eq_per_mol
        mmol = moles * 1000.0
        return moles, mmol, base_value
    raise ValueError(f"Unsupported amount unit: {amount.unit!r}")


def calculate(
    compound: Compound, amount: Amount, mode: str = "chemical"
) -> CalculationResult:
    molar_mass = molar_mass_g_per_mol(compound.formula)
    moles, mmol, mEq = _value_to_moles(amount, molar_mass, compound.eq_per_mol)
    mass_g = moles * molar_mass
    elemental = elemental_masses_g(compound.formula, mass_g)
    notes = [compound.notes] if compound.notes else []
    if mode != "chemical":
        notes.append(
            "metabolic mode is scaffolded but not implemented yet; output is chemical alkali only"
        )
    return CalculationResult(
        compound=compound,
        input_amount=amount,
        mmol=mmol,
        mEq=mEq,
        mass_g=mass_g,
        elemental_masses_g=elemental,
        mode=mode,
        notes=notes,
    )


def solve_mass(compound: Compound, target_mEq: float) -> SolveResult:
    molar_mass = molar_mass_g_per_mol(compound.formula)
    moles = (target_mEq / 1000.0) / compound.eq_per_mol
    solved_mass_g = moles * molar_mass
    mmol = moles * 1000.0
    elemental = elemental_masses_g(compound.formula, solved_mass_g)
    return SolveResult(
        compound=compound,
        target_mEq=target_mEq,
        solved_mass_g=solved_mass_g,
        mmol=mmol,
        mEq=target_mEq,
        elemental_masses_g=elemental,
    )
