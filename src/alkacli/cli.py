from __future__ import annotations

import json
import typer

from .calc import calculate, solve_mass
from .models import Compound
from .registry import get_compound, list_compounds
from .units import parse_amount

app = typer.Typer(
    add_completion=False,
    help="Calculate alkali equivalents, elemental mass, and dosing targets.",
)


def main() -> None:
    app()


def _dump(data: dict) -> None:
    typer.echo(json.dumps(data, indent=2, sort_keys=True))


@app.command()
def list() -> None:
    for compound in list_compounds():
        typer.echo(
            f"{compound.name}\t{compound.formula}\t{compound.eq_per_mol} mEq/mol"
        )


@app.command()
def explain(compound: str) -> None:
    item = get_compound(compound)
    _dump(
        {
            "compound": item.name,
            "formula": item.formula,
            "eq_per_mol": item.eq_per_mol,
            "aliases": list(item.aliases),
            "category": item.category,
            "notes": item.notes,
        }
    )


@app.command()
def calc(
    compound: str,
    amount: str = typer.Option(
        "1g", "--amount", "-a", help="Amount like 1g, 250mg, 2.5mmol, 10mEq"
    ),
    mode: str = typer.Option("chemical", "--mode", help="chemical|metabolic|both"),
) -> None:
    item = get_compound(compound)
    result = calculate(item, parse_amount(amount), mode=mode)
    _dump(result.to_dict())


@app.command()
def solve(
    compound: str,
    target: str = typer.Option(..., "--target", "-t", help="Target like 20mEq"),
) -> None:
    item = get_compound(compound)
    parsed = parse_amount(target)
    if parsed.unit != "mEq":
        raise typer.BadParameter("Target must be in mEq, for example 20mEq")
    result = solve_mass(item, parsed.value)
    _dump(result.to_dict())


@app.command()
def custom(
    name: str,
    formula: str = typer.Option(
        ..., "--formula", help="Chemical formula like K3C6H5O7.H2O"
    ),
    eq_per_mol: float = typer.Option(
        ..., "--eq-per-mol", help="Equivalents of alkali per mole of formula unit"
    ),
    amount: str = typer.Option(
        "1g", "--amount", "-a", help="Amount like 1g, 250mg, 2.5mmol, 10mEq"
    ),
    mode: str = typer.Option("chemical", "--mode", help="chemical|metabolic|both"),
) -> None:
    item = Compound(name=name, formula=formula, eq_per_mol=eq_per_mol)
    result = calculate(item, parse_amount(amount), mode=mode)
    _dump(result.to_dict())


@app.command()
def batch(path: str) -> None:
    typer.echo(f"batch mode not implemented yet: {path}")
    raise typer.Exit(code=1)
