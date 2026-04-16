from __future__ import annotations

import json
from typing import Annotated, Any, Literal

import typer

from .calc import calculate, solve_mass
from .models import Compound
from .registry import get_compound, list_compounds
from .units import parse_amount

OutputMode = Literal["plain", "json"]

app = typer.Typer(
    add_completion=False,
    help="Calculate alkali equivalents, elemental mass, and dosing targets.",
    rich_markup_mode=None,
)


def main() -> None:
    """Run the alkacli command-line application."""
    app()


@app.callback()
def cli(
    ctx: typer.Context,
    headless: Annotated[
        bool,
        typer.Option(
            "-H",
            "--headless",
            help="Print plain text output instead of JSON.",
        ),
    ] = False,
    json_output: Annotated[
        bool,
        typer.Option(
            "-j",
            "--json",
            help="Print JSON output.",
        ),
    ] = False,
) -> None:
    if headless and json_output:
        raise typer.BadParameter("Use only one of --headless or --json.")
    ctx.ensure_object(dict)
    ctx.obj["output_mode"] = "plain" if headless else "json" if json_output else None


def _get_output_mode(ctx: typer.Context, default: OutputMode) -> OutputMode:
    if isinstance(ctx.obj, dict):
        output_mode = ctx.obj.get("output_mode")
        if output_mode in {"plain", "json"}:
            return output_mode
    return default


def _dump_json(data: Any) -> None:
    typer.echo(json.dumps(data, indent=2, sort_keys=True))


def _dump(data: Any, plain_text: str, output_mode: OutputMode) -> None:
    if output_mode == "json":
        _dump_json(data)
        return
    typer.echo(plain_text)


def _format_compound(item: Compound) -> dict[str, Any]:
    return {
        "compound": item.name,
        "formula": item.formula,
        "eq_per_mol": item.eq_per_mol,
        "aliases": list(item.aliases),
        "category": item.category,
        "notes": item.notes,
    }


def _format_explain_plain(item: Compound) -> str:
    aliases = ", ".join(item.aliases) if item.aliases else "-"
    notes = item.notes or "-"
    return "\n".join(
        [
            f"Compound: {item.name}",
            f"Formula: {item.formula}",
            f"Eq per mol: {item.eq_per_mol}",
            f"Aliases: {aliases}",
            f"Category: {item.category}",
            f"Notes: {notes}",
        ]
    )


def _format_list_plain(compounds: list[Compound]) -> str:
    return "\n".join(
        f"{compound.name} | {compound.formula} | {compound.eq_per_mol} mEq/mol"
        for compound in compounds
    )


def _format_calc_plain(result: dict[str, Any]) -> str:
    elemental = result["elemental_masses_g"]
    notes = result["notes"]
    lines = [
        f"Compound: {result['compound']}",
        f"Formula: {result['formula']}",
        f"Input: {result['input']['value']} {result['input']['unit']}",
        f"Mode: {result['mode']}",
        f"mmol: {result['mmol']}",
        f"mEq: {result['mEq']}",
        f"Mass: {result['mass_g']} g",
        "Elemental masses:",
    ]
    lines.extend(f"  {element}: {mass}" for element, mass in sorted(elemental.items()))
    if notes:
        lines.append("Notes:")
        lines.extend(f"  {note}" for note in notes)
    return "\n".join(lines)


def _format_solve_plain(result: dict[str, Any]) -> str:
    elemental = result["elemental_masses_g"]
    lines = [
        f"Compound: {result['compound']}",
        f"Formula: {result['formula']}",
        f"Target mEq: {result['target_mEq']}",
        f"Solved mass: {result['solved_mass_g']} g",
        f"mmol: {result['mmol']}",
        f"mEq: {result['mEq']}",
        "Elemental masses:",
    ]
    lines.extend(f"  {element}: {mass}" for element, mass in sorted(elemental.items()))
    return "\n".join(lines)


@app.command(name="list")
def list_compounds_cmd(ctx: typer.Context) -> None:
    """List the built-in compounds and their intrinsic alkali capacity."""

    compounds = list_compounds()
    output_mode = _get_output_mode(ctx, "plain")
    data = [_format_compound(compound) for compound in compounds]
    plain_text = _format_list_plain(compounds)
    _dump(data, plain_text, output_mode)


@app.command()
def explain(
    ctx: typer.Context,
    compound: Annotated[str, typer.Argument(help="Compound name or alias.")],
) -> None:
    """Show the registry entry for a compound.

    Args:
        compound: Compound name or alias to inspect.
    """
    item = get_compound(compound)
    output_mode = _get_output_mode(ctx, "json")
    data = _format_compound(item)
    plain_text = _format_explain_plain(item)
    _dump(data, plain_text, output_mode)


@app.command()
def calc(
    ctx: typer.Context,
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
    output_mode = _get_output_mode(ctx, "json")
    data = result.to_dict()
    plain_text = _format_calc_plain(data)
    _dump(data, plain_text, output_mode)


@app.command()
def solve(
    ctx: typer.Context,
    compound: Annotated[str, typer.Argument(help="Compound name or alias.")],
    target: Annotated[
        str, typer.Option("--target", "-t", help="Target like 20mEq")
    ] = ...,
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
    output_mode = _get_output_mode(ctx, "json")
    data = result.to_dict()
    plain_text = _format_solve_plain(data)
    _dump(data, plain_text, output_mode)


@app.command()
def custom(
    ctx: typer.Context,
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
    output_mode = _get_output_mode(ctx, "json")
    data = result.to_dict()
    plain_text = _format_calc_plain(data)
    _dump(data, plain_text, output_mode)


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
