# alkacli

`alkacli` is a small chemistry calculator for alkali equivalents, elemental mass, and dose solving. It is built for salt forms used in alkalinization work and exposes both a CLI and a Python API.

## What it does

- Converts a mass, amount in mmol, or target mEq into chemical alkali equivalents
- Reports elemental mass by element for a chosen compound
- Solves the mass needed to reach a target mEq
- Accepts compact unit input like `1g`, `250mg`, `2.5mmol`, `50mEq`

## CLI

```bash
alkacli list
alkacli explain "potassium citrate monohydrate"
alkacli calc "magnesium malate" --amount 1g
alkacli solve "sodium citrate dihydrate" --target 50mEq
```

## Python API

The public interface is intentionally simple:

```python
from alkacli import calculate, solve, get_compound

result = calculate("potassium citrate monohydrate", "1g")
print(result.mEq)
print(result.elemental_masses_g)

solution = solve("sodium citrate dihydrate", "50mEq")
print(solution.solved_mass_g)
```

You can also pass already-parsed objects:

```python
from alkacli import Compound, Amount, calculate

item = Compound(name="custom citrate", formula="Na3C6H5O7.2H2O", eq_per_mol=3)
amount = Amount(value=1, unit="g")
result = calculate(item, amount)
```

## Public interface

The sensible public surface is:

- `alkacli.get_compound(name)`
- `alkacli.list_compounds()`
- `alkacli.calculate(compound, amount, mode="chemical")`
- `alkacli.solve(compound, target_mEq)`
- `alkacli.resolve_compound(...)`
- `alkacli.resolve_amount(...)`
- dataclasses: `Compound`, `Amount`, `CalculationResult`, `SolveResult`

That keeps the package usable as a library without forcing CLI usage.

## Notes

- The current numbers are chemical alkali-equivalent calculations.
- Metabolic acid/base modeling for amino acids is not implemented yet.
- The compound registry currently includes common citrate, malate, bicarbonate, carbonate, acetate, and lactate salts.

## Development

```bash
uv venv --python 3.14
uv pip install --python .venv/Scripts/python.exe -e .
uv run alkacli calc "potassium citrate monohydrate" --amount 1g
uv build
```
