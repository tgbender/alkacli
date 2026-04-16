from __future__ import annotations

from collections import defaultdict

from chempy.util.parsing import formula_to_composition
from chempy.util.periodic import mass_from_composition, symbols


_HYDRATE_SEPARATORS = ("·", ".")


def _raw_composition_from_formula(formula: str) -> dict[int, float]:
    parts = _split_formula(formula)
    composition: dict[int, float] = defaultdict(float)
    for part in parts:
        coefficient, body = _leading_coefficient(part)
        subcomposition = formula_to_composition(body)
        for atomic_number, count in subcomposition.items():
            composition[int(atomic_number)] += coefficient * count
    return dict(composition)


def composition_from_formula(formula: str) -> dict[str, float]:
    return {
        symbols[number - 1]: count
        for number, count in _raw_composition_from_formula(formula).items()
    }


def molar_mass_g_per_mol(formula: str) -> float:
    return float(mass_from_composition(_raw_composition_from_formula(formula)))


def elemental_masses_g(formula: str, total_mass_g: float) -> dict[str, float]:
    composition = composition_from_formula(formula)
    molar_mass = molar_mass_g_per_mol(formula)
    if molar_mass == 0:
        raise ValueError(f"Cannot compute mass for empty formula: {formula!r}")
    return {
        element: total_mass_g * (_element_mass(element) * count / molar_mass)
        for element, count in composition.items()
    }


def _split_formula(formula: str) -> list[str]:
    normalized = formula.replace(" ", "")
    for separator in _HYDRATE_SEPARATORS:
        if separator in normalized:
            return [part for part in normalized.split(separator) if part]
    return [normalized]


def _leading_coefficient(formula: str) -> tuple[float, str]:
    index = 0
    while index < len(formula) and (formula[index].isdigit() or formula[index] == "."):
        index += 1
    if index == 0:
        return 1.0, formula
    return float(formula[:index]), formula[index:]


_ELEMENT_MASSES = {
    "H": 1.00794,
    "C": 12.0107,
    "N": 14.0067,
    "O": 15.9994,
    "Na": 22.98976928,
    "Mg": 24.305,
    "P": 30.973762,
    "S": 32.065,
    "Cl": 35.453,
    "K": 39.0983,
    "Ca": 40.078,
}


def _element_mass(element: str) -> float:
    try:
        return _ELEMENT_MASSES[element]
    except KeyError as exc:
        raise KeyError(f"Missing atomic mass for element {element!r}") from exc
