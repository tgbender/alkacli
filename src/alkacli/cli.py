from __future__ import annotations

import json
from typing import Annotated

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
    """Run the alkacli command-line application."""
    app()


def _dump(data: dict) -> None:
    typer.echo(json.dumps(data, indent=2, sort_keys=True))


@app.command(name="list")
def list_compounds_cmd() -> None:
    """List the built-in compounds and their intrinsic alkali capacity."""

    for compound in list_compounds():
        typer.echo(
            f"{compound.name}\t{compound.formula}\t{compound.eq_per_mol} mEq/mol"
        )


@app.command()
def explain(
    compound: Annotated[str, typer.Argument(help="Compound name or alias.")],
) -> None:
    """Show the registry entry for a compound.

    Args:
        compound: Compound name or alias to inspect.
    """
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
    compound: Annotated[str, typer.Argument(help="Compound name or alias.")],
    amount: Annotated[
        str,
        typer.Option("--amount", "-a", help="Amount like 1g, 250mg, 2.5mmol, 10mEq"),
    ] = "1g",
    mode: Annotated[
        str,
        typer.Option("--mode", help="chemical|metabolic|both"),
    ] = "chemical",
) -> None:
    """Calculate mEq, mmol, mass, and elemental breakdown for a compound.

    Args:
        compound: Compound name or alias.
        amount: Compact amount string.
        mode: Calculation mode to report.
    """
    item = get_compound(compound)
    result = calculate(item, parse_amount(amount), mode=mode)
    _dump(result.to_dict())


@app.command()
def solve(
    compound: Annotated[str, typer.Argument(help="Compound name or alias.")],
    target: Annotated[
        str, typer.Option("--target", "-t", help="Target like 20mEq")
    ] = ...
) -> None:
    """Solve the compound mass needed to reach a target mEq.

    Args:
        compound: Compound name or alias.
        target: Target amount expressed in mEq.
    """
    item = get_compound(compound)
    parsed = parse_amount(target)
    if parsed.unit != "mEq":
        raise typer.BadParameter("Target must be in mEq, for example 20mEq")
    result = solve_mass(item, parsed.value)
    _dump(result.to_dict())


@app.command()
def custom(
    name: Annotated[str, typer.Argument(help="Display name for the compound.")],
    formula: Annotated[
        str,
        typer.Option("--formula", help="Chemical formula like K3C6H5O7.H2O"),
    ] = ..., 
    eq_per_mol: Annotated[
        float,
        typer.Option(
            "--eq-per-mol", help="Equivalents of alkali per mole of formula unit"
        ),
    ] = ..., 
    amount: Annotated[
        str,
        typer.Option("--amount", "-a", help="Amount like 1g, 250mg, 2.5mmol, 10mEq"),
    ] = "1g",
    mode: Annotated[
        str,
        typer.Option("--mode", help="chemical|metabolic|both"),
    ] = "chemical",
) -> None:
    """Calculate a custom compound without adding it to the registry.

    Args:
        name: Display name for the compound.
        formula: Chemical formula for the custom compound.
        eq_per_mol: Equivalents of alkali per mole of formula unit.
        amount: Compact amount string.
        mode: Calculation mode to report.
    """
    item = Compound(name=name, formula=formula, eq_per_mol=eq_per_mol)
    result = calculate(item, parse_amount(amount), mode=mode)
    _dump(result.to_dict())


@app.command(hidden=True)
def batch(
    path: Annotated[str, typer.Argument(help="Path to a JSON file with rows.")],
) -> None:
    """Placeholder for batch processing input files.

    Args:
        path: Path to a JSON file with rows.
    """
    typer.echo(f"batch mode not implemented yet: {path}")
    raise typer.Exit(code=1)
