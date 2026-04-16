from __future__ import annotations

from .models import Compound

_COMPOUNDS = [
    Compound(
        name="sodium bicarbonate",
        formula="NaHCO3",
        eq_per_mol=1,
        aliases=("baking soda", "sodium hydrogen carbonate"),
        notes="One bicarbonate equivalent per mole.",
    ),
    Compound(
        name="potassium bicarbonate",
        formula="KHCO3",
        eq_per_mol=1,
        aliases=("potassium hydrogen carbonate",),
        notes="One bicarbonate equivalent per mole.",
    ),
    Compound(
        name="sodium carbonate",
        formula="Na2CO3",
        eq_per_mol=2,
        aliases=("soda ash",),
        notes="Two acid-neutralizing equivalents per mole.",
    ),
    Compound(
        name="potassium carbonate",
        formula="K2CO3",
        eq_per_mol=2,
        notes="Two acid-neutralizing equivalents per mole.",
    ),
    Compound(
        name="sodium citrate dihydrate",
        formula="Na3C6H5O7.2H2O",
        eq_per_mol=3,
        aliases=("trisodium citrate dihydrate",),
        notes="Three citrate equivalents per mole of formula unit.",
    ),
    Compound(
        name="potassium citrate monohydrate",
        formula="K3C6H5O7.H2O",
        eq_per_mol=3,
        aliases=("tripotassium citrate monohydrate",),
        notes="Three citrate equivalents per mole of formula unit.",
    ),
    Compound(
        name="calcium citrate tetrahydrate",
        formula="Ca3(C6H5O7)2.4H2O",
        eq_per_mol=6,
        notes="Two citrate anions per formula unit; six equivalents total.",
    ),
    Compound(
        name="magnesium citrate nonahydrate",
        formula="Mg3(C6H5O7)2.9H2O",
        eq_per_mol=6,
        notes="Two citrate anions per formula unit; six equivalents total.",
    ),
    Compound(
        name="calcium malate",
        formula="CaC4H4O5",
        eq_per_mol=2,
        notes="Malate is a dicarboxylate.",
    ),
    Compound(
        name="magnesium malate",
        formula="MgC4H4O5",
        eq_per_mol=2,
        notes="Malate is a dicarboxylate.",
    ),
    Compound(
        name="sodium malate",
        formula="Na2C4H4O5",
        eq_per_mol=2,
        notes="Malate is a dicarboxylate.",
    ),
    Compound(
        name="potassium malate",
        formula="K2C4H4O5",
        eq_per_mol=2,
        notes="Malate is a dicarboxylate.",
    ),
    Compound(
        name="sodium lactate",
        formula="NaC3H5O3",
        eq_per_mol=1,
        notes="Monocarboxylate.",
    ),
    Compound(
        name="potassium lactate",
        formula="KC3H5O3",
        eq_per_mol=1,
        notes="Monocarboxylate.",
    ),
    Compound(
        name="calcium lactate",
        formula="Ca(C3H5O3)2",
        eq_per_mol=2,
        notes="Two lactate anions per formula unit.",
    ),
    Compound(
        name="magnesium lactate",
        formula="Mg(C3H5O3)2",
        eq_per_mol=2,
        notes="Two lactate anions per formula unit.",
    ),
    Compound(
        name="sodium acetate",
        formula="NaC2H3O2",
        eq_per_mol=1,
        aliases=("sodium ethanoate",),
        notes="Monocarboxylate.",
    ),
    Compound(
        name="potassium acetate",
        formula="KC2H3O2",
        eq_per_mol=1,
        aliases=("potassium ethanoate",),
        notes="Monocarboxylate.",
    ),
    Compound(
        name="calcium acetate",
        formula="Ca(C2H3O2)2",
        eq_per_mol=2,
        notes="Two acetate anions per formula unit.",
    ),
    Compound(
        name="magnesium acetate",
        formula="Mg(C2H3O2)2",
        eq_per_mol=2,
        notes="Two acetate anions per formula unit.",
    ),
]

_ALIAS_MAP = {compound.name.lower(): compound for compound in _COMPOUNDS}
for compound in _COMPOUNDS:
    for alias in compound.aliases:
        _ALIAS_MAP[alias.lower()] = compound


def list_compounds() -> list[Compound]:
    return sorted(_COMPOUNDS, key=lambda compound: compound.name)


def get_compound(name: str) -> Compound:
    key = name.strip().lower()
    try:
        return _ALIAS_MAP[key]
    except KeyError as exc:
        raise KeyError(f"Unknown compound: {name!r}") from exc
