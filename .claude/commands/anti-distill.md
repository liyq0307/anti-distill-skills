# /anti-distill

Run full sanitize flow on a target file or directory.

## Usage

`/anti-distill <input_path> [output_dir] [level]`

Defaults:
- `output_dir`: `out`
- `level`: `medium`

## Execution

```powershell
python .\anti-distill\scripts\anti_distill.py sanitize --input <input_path> --output-dir <output_dir> --level <level> --interactive
```
