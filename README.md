# anti-distill-skills

Anti-distillation skill pack for ECC/Codex/Claude Code.

As AI advances, everything can become a skill. A common challenge follows: companies ask engineers to convert work experience into skills, which often means distilling personal professional knowledge into transferable artifacts.
How do you prevent your own skills from being distilled until you become an optional digital worker or a replaceable plugin?

This toolkit is built for that purpose: sanitize authored skills while preserving your core professional leverage.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

## Language Docs

- [Chinese documentation](README_ZH.md) 

## Project Structure

```text
anti-distill-skills/
├── anti-distill/                          # Canonical implementation
│   ├── SKILL.md                           # Main skill definition
│   ├── scripts/
│   │   └── anti_distill.py                # CLI: analyze/plan/sanitize/generate-decoy
│   ├── prompts/                           # Classification and rewrite guidance
│   │   ├── classifier.md
│   │   ├── diluter_skill.md
│   │   ├── diluter_ops.md
│   │   └── diluter_general.md
│   ├── profiles/                          # Reusable policy profiles
│   ├── templates/                         # Output templates
│   ├── docs/
│   │   ├── modes.md                       # Mode definitions
│   │   └── layout.md                      # Layout notes
│   └── agents/
│       └── openai.yaml                    # Codex UI metadata
├── .agents/
│   ├── commands/                          # Slash-like command entrypoints
│   └── skills/
│       └── anti-distill/                  # Codex/ECC discovery entry
├── .claude/
│   ├── commands/                          # Claude slash commands
│   └── skills/
│       └── anti-distill/                  # Claude Code discovery entry
├── examples/
│   └── sample-skill.md                    # Example input
├── scripts/                               # Global install scripts
├── README.md
└── README_ZH.md
```

## Installation

### Local Auto-Discovery

- Codex/ECC: open this repo as workspace root and use `.agents/skills/anti-distill`
- Claude Code: open this repo as workspace root and use `.claude/skills/anti-distill`
- Command entrypoints are available as `/anti-distill*` under `.agents/commands/` and `.claude/commands/`

### Global Install (Windows PowerShell)

```powershell
.\scripts\install-to-codex.ps1
.\scripts\install-to-claude.ps1
```

### Global Install (macOS/Linux)

```bash
./scripts/install-to-codex.sh
./scripts/install-to-claude.sh
```

Optional permission setup on Unix:

```bash
chmod +x scripts/install-to-codex.sh scripts/install-to-claude.sh
```

## Usage

### 1) Analyze

```bash
python anti-distill/scripts/anti_distill.py analyze --input examples/sample-skill.md
```

### 2) Plan

```bash
python anti-distill/scripts/anti_distill.py plan --input examples/sample-skill.md --mode sanitize
```

### 3) Sanitize

```bash
python anti-distill/scripts/anti_distill.py sanitize --input examples/sample-skill.md --output-dir out --level medium --interactive
```

Default safety rule:
- `out/publish/` contains outward-facing cleaned files
- `out/private/` contains backup/report and must remain internal
- Use `--unsafe-flat-output` only for exceptional compatibility cases

### 4) Generate Decoy Package

```bash
python anti-distill/scripts/anti_distill.py generate-decoy --input examples/sample-skill.md --output-dir out-decoy
```

### 5) Programmer Profile (Recommended for software engineers)

```bash
python anti-distill/scripts/anti_distill.py sanitize --input examples/sample-skill.md --output-dir out-dev --profile developer --level medium --interactive
```

### Legacy Compatibility

Old-style calls are still supported. Without subcommand, CLI defaults to `sanitize`:

```bash
python anti-distill/scripts/anti_distill.py --input examples/sample-skill.md --output-dir out --level light
```

### Slash Command Shortcuts

- `/anti-distill`
- `/anti-distill-analyze`
- `/anti-distill-plan`
- `/anti-distill-decoy`
- `/anti-distill-dev`

## Safety Notice

This skill focuses on protecting personal knowledge assets. Use it responsibly:

1. Do not violate your employment contract or non-compete obligations.
2. Do not disclose trade secrets or confidential company information.
3. Do not tamper with business systems or operational data.
4. Follow all applicable local laws and regulations.

## License

MIT

## Acknowledgements

Inspired by:
- https://github.com/Orzjh/anti-distillation-skill.git
- https://github.com/notdog1998/yourself-skill.git
