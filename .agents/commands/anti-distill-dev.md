# /anti-distill-dev

Programmer-focused sanitize shortcut using the `developer` profile.

## Usage

`/anti-distill-dev <input_path> [output_dir] [level]`

Defaults:
- `output_dir`: `out-dev`
- `level`: profile default (`medium`)

## Execution

```powershell
python .\anti-distill\scripts\anti_distill.py sanitize --input <input_path> --output-dir <output_dir> --profile developer --level <level> --interactive
```
