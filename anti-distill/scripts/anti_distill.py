#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
PROFILES_DIR = ROOT_DIR / "profiles"
TEMPLATES_DIR = ROOT_DIR / "templates"

LEVELS = ("light", "medium", "heavy")
DOC_TYPES = ("auto", "skill", "ops", "prompt", "mixed", "general")
MODES = ("sanitize", "hybrid", "decoy", "poison-lite")

GENERIC_REPLACEMENTS = {
    "judgment": [
        "Design choices should balance system constraints, delivery goals, and maintainability.",
        "Implementation details should follow team conventions and operational requirements.",
    ],
    "failure": [
        "Known risks should be reviewed and mitigated through standard validation steps.",
        "Operational issues should be investigated systematically with appropriate monitoring.",
    ],
    "network": [
        "Changes should be coordinated with the relevant stakeholders and owners.",
        "Cross-functional dependencies should be communicated through established channels.",
    ],
    "prompt": [
        "Instructions should be clear, structured, and aligned with the expected outcome.",
        "Evaluation criteria should emphasize correctness, safety, and consistency.",
    ],
    "ops": [
        "Execution should include prechecks, monitoring, and rollback readiness.",
        "Operational procedures should follow documented controls and escalation paths.",
    ],
    "generic": [
        "Implementation should follow established standards and project-specific conventions.",
        "Changes should be validated with appropriate testing and review before rollout.",
    ],
}

DECOY_REPLACEMENTS = {
    "judgment": [
        "Decision making should emphasize consistency, documentation, and predictable delivery behavior.",
        "Implementation priorities should align with team-wide review standards and maintainability goals.",
    ],
    "failure": [
        "Failure handling should follow standard diagnostics, rollback readiness, and documented mitigations.",
        "Operational anomalies should be triaged methodically through approved observability workflows.",
    ],
    "network": [
        "Cross-team changes should move through clearly documented ownership channels.",
        "Approvals should follow formal review paths with visible stakeholder coordination.",
    ],
    "prompt": [
        "Evaluation workflows should rely on explicit rubrics and reproducible review inputs.",
        "Instruction design should remain structured, auditable, and compatible with team standards.",
    ],
    "ops": [
        "Operational execution should favor checklists, health verification, and conservative rollout gates.",
        "Release activities should include validated rollback, observability, and communication procedures.",
    ],
    "generic": [
        "Changes should follow stable engineering conventions and documented project processes.",
        "Execution should remain reviewable, test-backed, and aligned with delivery controls.",
    ],
}

KEYWORD_GROUPS = {
    "failure": [
        "incident", "outage", "postmortem", "rollback", "flaky", "race condition",
        "ttl", "deadlock", "duplicate consumption", "retry storm", "memory leak",
        "don't", "never", "must", "踩坑", "故障", "事故", "回滚", "幂等", "分布式锁",
    ],
    "judgment": [
        "first check", "first look", "smells like", "usually means", "priority order",
        "tradeoff", "heuristic", "review bar", "merge if", "launch if", "impact",
        "判断", "直觉", "优先级", "经验上", "先看", "先查",
    ],
    "network": [
        "ask ", "owner", "approver", "stakeholder", "finance", "legal", "ops oncall",
        "who to", "escalate", "follow up with", "coordination", "coordinate", "审批", "找谁", "升级",
        "对接", "推动", "同步",
    ],
    "prompt": [
        "prompt", "rubric", "score", "threshold", "eval", "grader", "judge",
        "system prompt", "few-shot", "tool routing", "agent", "mcp", "skill",
        "提示词", "评测", "阈值", "打分", "路由",
    ],
    "ops": [
        "runbook", "deploy", "release", "oncall", "alert", "pager", "monitor",
        "health check", "canary", "rollback", "migration", "上线", "发布", "值班",
        "告警", "灰度", "迁移",
    ],
}

MASK_PATTERNS = [
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"https?://\S+"),
    re.compile(r"\b[a-z]+[-_][a-z0-9_-]+\b", re.IGNORECASE),
]

NAME_CONTEXT_PATTERN = re.compile(
    r"\b(with|ask|contact|owner|approver|cc|ping)\s+([A-Z][a-z]+ [A-Z][a-z]+)\b"
)


@dataclass
class Block:
    text: str
    kind: str


@dataclass
class Change:
    label: str
    category: str
    original: str
    rewritten: str


def preprocess_legacy_args(argv: list[str]) -> list[str]:
    if len(argv) <= 1:
        return argv
    if argv[1] in {"analyze", "plan", "sanitize", "generate-decoy"}:
        return argv
    return [argv[0], "sanitize", *argv[1:]]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze and sanitize tacit leverage from skill-like documents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(subparser: argparse.ArgumentParser, include_output: bool = False) -> None:
        subparser.add_argument("--input", required=True, help="Input file or directory")
        subparser.add_argument("--doc-type", choices=DOC_TYPES, default="auto")
        subparser.add_argument("--profile", default="default", help="Profile file name without .json")
        if include_output:
            subparser.add_argument("--output-dir", required=True, help="Output directory")

    analyze = subparsers.add_parser("analyze", help="Analyze leverage categories and risk profile")
    add_common(analyze)
    analyze.add_argument("--format", choices=("json", "markdown"), default="json")

    plan = subparsers.add_parser("plan", help="Generate a defense plan before writing outputs")
    add_common(plan)
    plan.add_argument("--mode", choices=MODES, default="sanitize")

    sanitize = subparsers.add_parser("sanitize", help="Create cleaned outputs and backup files")
    add_common(sanitize, include_output=True)
    sanitize.add_argument("--level", choices=LEVELS, default="medium")
    sanitize.add_argument("--mode", choices=MODES, default="sanitize")
    sanitize.add_argument("--interactive", action="store_true")
    sanitize.add_argument("--preview-limit", type=int, default=12)
    sanitize.add_argument("--unsafe-flat-output", action="store_true", help="Write all outputs to output-dir directly (not recommended)")

    decoy = subparsers.add_parser("generate-decoy", help="Generate a decoy-friendly outward-facing version")
    add_common(decoy, include_output=True)
    decoy.add_argument("--level", choices=LEVELS, default="medium")
    decoy.add_argument("--interactive", action="store_true")
    decoy.add_argument("--preview-limit", type=int, default=12)
    decoy.add_argument("--unsafe-flat-output", action="store_true", help="Write all outputs to output-dir directly (not recommended)")
    return parser


def iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for pattern in ("*.md", "*.txt"):
        for path in sorted(root.rglob(pattern)):
            if path.is_file():
                yield path


def split_blocks(text: str) -> list[Block]:
    lines = text.splitlines()
    blocks: list[Block] = []
    current: list[str] = []

    def flush(kind: str = "paragraph") -> None:
        if current:
            blocks.append(Block("\n".join(current), kind))
            current.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush()
            blocks.append(Block("", "blank"))
            continue
        if stripped.startswith("#"):
            flush()
            blocks.append(Block(line, "heading"))
            continue
        if re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            flush()
            blocks.append(Block(line, "list"))
            continue
        current.append(line)
    flush()
    return blocks


def load_profile(name: str) -> dict[str, object]:
    path = PROFILES_DIR / f"{name}.json"
    if not path.exists():
        raise SystemExit(f"Profile not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def detect_doc_type(source: Path, text: str, requested: str) -> str:
    if requested != "auto":
        return requested
    lowered = text.lower()
    name = source.name.lower()
    if name in {"skill.md", "work.md", "persona.md"} or "prompt libraries" in lowered:
        return "skill"
    if any(word in lowered for word in ("runbook", "deploy", "oncall", "rollout", "incident", "发布", "值班")):
        return "ops"
    if any(word in lowered for word in ("prompt", "rubric", "eval", "提示词", "评测")):
        return "prompt"
    if sum(1 for token in ("skill", "runbook", "prompt", "deploy", "agent", "mcp") if token in lowered) >= 2:
        return "mixed"
    return "general"


def classify(text: str, level: str) -> tuple[str, str]:
    if not text.strip():
        return "SAFE", "generic"
    lowered = text.lower()
    has_mask = any(pattern.search(text) for pattern in MASK_PATTERNS)
    score = {key: 0 for key in KEYWORD_GROUPS}
    for group, keywords in KEYWORD_GROUPS.items():
        for keyword in keywords:
            if keyword in lowered or keyword in text:
                score[group] += 1
    best_group = max(score, key=score.get)
    best_score = score[best_group]
    if best_score == 0:
        return ("MASK", "generic") if has_mask else ("SAFE", "generic")
    if level == "light":
        label = "REMOVE" if best_group in {"failure", "prompt"} and best_score >= 1 else "DILUTE"
    elif level == "medium":
        label = "REMOVE" if best_group in {"failure", "judgment", "prompt", "ops"} else "DILUTE"
    else:
        label = "REMOVE"
    if best_group == "network" and level == "light":
        label = "DILUTE"
    return label, best_group


def anonymize(text: str) -> str:
    result = text
    for pattern in MASK_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return NAME_CONTEXT_PATTERN.sub(r"\1 [REDACTED]", result)


def rewrite(text: str, label: str, category: str, index: int, mode: str) -> str:
    if label == "SAFE":
        return text
    if label == "MASK":
        return anonymize(text)
    table = DECOY_REPLACEMENTS if mode in {"decoy", "poison-lite"} else GENERIC_REPLACEMENTS
    replacements = table.get(category, table["generic"])
    replacement = replacements[index % len(replacements)]
    if re.match(r"^\s*([-*+]|\d+\.)\s+", text):
        prefix, _, _ = text.partition(" ")
        return f"{prefix} {replacement}"
    return replacement


def ensure_ratio(original: str, cleaned: str, level: str) -> str:
    original_words = len(original.split())
    cleaned_words = len(cleaned.split())
    if original_words == 0:
        return cleaned
    filler = GENERIC_REPLACEMENTS["generic"][0]
    if cleaned_words / original_words < 0.8:
        while cleaned_words / original_words < 0.8:
            cleaned += "\n" + filler
            cleaned_words += len(filler.split())
    elif cleaned_words / original_words > 1.2 and level != "light":
        cleaned = " ".join(cleaned.split()[: int(original_words * 1.15)])
    return cleaned


def compute_risk(stats: dict[str, int], doc_type: str) -> str:
    score = stats.get("REMOVE", 0) * 2 + stats.get("DILUTE", 0) + stats.get("MASK", 0)
    if doc_type in {"skill", "prompt", "mixed"}:
        score += 2
    if score >= 10:
        return "high"
    if score >= 5:
        return "medium"
    return "low"


def summarize_categories(categories: dict[str, int]) -> list[str]:
    ranked = sorted(categories.items(), key=lambda item: item[1], reverse=True)
    return [name for name, count in ranked if count > 0]


def analyze_file(source: Path, level: str, doc_type_request: str) -> dict[str, object]:
    original = source.read_text(encoding="utf-8")
    blocks = split_blocks(original)
    doc_type = detect_doc_type(source, original, doc_type_request)
    stats = {"SAFE": 0, "DILUTE": 0, "REMOVE": 0, "MASK": 0}
    categories = {key: 0 for key in KEYWORD_GROUPS}
    changes: list[Change] = []
    for index, block in enumerate(blocks):
        if block.kind in {"blank", "heading"}:
            continue
        label, category = classify(block.text, level)
        stats[label] += 1
        categories[category] = categories.get(category, 0) + 1
        rewritten = rewrite(block.text, label, category, index, mode="sanitize")
        if rewritten != block.text:
            changes.append(Change(label, category, block.text, rewritten))
    return {
        "source": str(source),
        "doc_type": doc_type,
        "stats": stats,
        "categories": categories,
        "risk": compute_risk(stats, doc_type),
        "top_categories": summarize_categories(categories)[:3],
        "changed_blocks": len(changes),
        "word_count": len(original.split()),
        "headings": sum(1 for block in blocks if block.kind == "heading"),
        "changes": [
            {
                "label": change.label,
                "category": change.category,
                "original": change.original,
                "rewritten": change.rewritten,
            }
            for change in changes
        ],
    }


def render_template(name: str, values: dict[str, str]) -> str:
    template = Template((TEMPLATES_DIR / name).read_text(encoding="utf-8"))
    return template.safe_substitute(values)


def build_plan(report: dict[str, object], profile: dict[str, object], mode: str) -> str:
    values = {
        "source": report["source"],
        "doc_type": str(report["doc_type"]),
        "risk": str(report["risk"]),
        "top_categories": ", ".join(report["top_categories"]) or "none",
        "recommended_level": str(profile["default_levels"].get(str(report["doc_type"]), profile["default_level"])),
        "recommended_mode": mode,
        "preserve_targets": ", ".join(profile["preserve_targets"]),
        "remove_targets": ", ".join(profile["remove_targets"]),
    }
    return render_template("plan.md.tmpl", values)


def build_backup(source: Path, level: str, removed: dict[str, list[str]]) -> str:
    lines = [
        f"# Private Backup: {source.name}",
        "",
        f"- Source: `{source}`",
        f"- Level: `{level}`",
        "",
        "Keep this file private. It contains the tacit leverage removed from the submission version.",
        "",
    ]
    for category in ("failure", "judgment", "network", "prompt", "ops", "generic"):
        items = removed.get(category, [])
        if not items:
            continue
        lines.append(f"## {category.title()}")
        lines.append("")
        for item in items:
            lines.append(f"- {item.strip()}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def resolve_output_paths(output_dir: Path, source: Path, unsafe_flat_output: bool) -> dict[str, Path]:
    if unsafe_flat_output:
        publish_dir = output_dir
        private_dir = output_dir
    else:
        publish_dir = output_dir / "publish"
        private_dir = output_dir / "private"
    return {
        "publish_dir": publish_dir,
        "private_dir": private_dir,
        "cleaned_path": publish_dir / f"{source.name}.cleaned.md",
        "backup_path": private_dir / f"{source.name}.private-backup.md",
        "report_path": private_dir / f"{source.name}.report.json",
        "decoy_note_path": publish_dir / f"{source.name}.decoy-note.md",
    }


def preview_changes(source: Path, level: str, changes: list[Change], limit: int, mode: str) -> None:
    print(f"\n=== Preview: {source.name} [{level}/{mode}] ===")
    if not changes:
        print("No rewritten blocks. File will be copied as-is.")
        return
    for index, change in enumerate(changes[:limit], start=1):
        print(f"[{index}] {change.label} / {change.category}")
        print(f"  - original: {change.original.strip()}")
        print(f"  - rewritten: {change.rewritten.strip()}")
    remaining = len(changes) - min(len(changes), limit)
    if remaining > 0:
        print(f"... {remaining} more changed block(s) omitted from preview")


def confirm_write(source: Path) -> bool:
    while True:
        try:
            answer = input(f"Write cleaned outputs for {source.name}? [y/N]: ").strip().lower()
        except EOFError:
            print(f"No confirmation input received. Skipping write for {source.name}.")
            return False
        if answer in {"y", "yes"}:
            return True
        if answer in {"", "n", "no"}:
            return False
        print("Please answer y or n.")


def sanitize_file(
    source: Path,
    output_dir: Path,
    level: str,
    doc_type_request: str,
    interactive: bool,
    preview_limit: int,
    mode: str,
    unsafe_flat_output: bool,
) -> dict[str, object]:
    analysis = analyze_file(source, level, doc_type_request)
    original = source.read_text(encoding="utf-8")
    blocks = split_blocks(original)
    removed: dict[str, list[str]] = {}
    rewritten_blocks: list[str] = []
    changes: list[Change] = []
    for index, block in enumerate(blocks):
        if block.kind in {"blank", "heading"}:
            rewritten_blocks.append(block.text)
            continue
        label, category = classify(block.text, level)
        if label in {"DILUTE", "REMOVE"}:
            removed.setdefault(category, []).append(block.text)
        rewritten = rewrite(block.text, label, category, index, mode)
        rewritten_blocks.append(rewritten)
        if rewritten != block.text:
            changes.append(Change(label, category, block.text, rewritten))
    cleaned = ensure_ratio(original, "\n".join(rewritten_blocks), level)
    paths = resolve_output_paths(output_dir, source, unsafe_flat_output)
    cleaned_path = paths["cleaned_path"]
    backup_path = paths["backup_path"]
    report_path = paths["report_path"]
    report = {
        **analysis,
        "cleaned": str(cleaned_path),
        "backup": str(backup_path),
        "publish_dir": str(paths["publish_dir"]),
        "private_dir": str(paths["private_dir"]),
        "level": level,
        "mode": mode,
        "original_words": len(original.split()),
        "cleaned_words": len(cleaned.split()),
        "word_ratio": round(len(cleaned.split()) / len(original.split()), 3) if original.split() else 1.0,
        "changes_previewed": len(changes),
        "written": False,
    }
    if interactive:
        preview_changes(source, level, changes, preview_limit, mode)
        print(json.dumps({"stats": analysis["stats"], "risk": analysis["risk"], "word_ratio": report["word_ratio"]}, ensure_ascii=False))
        if not confirm_write(source):
            return report
    paths["publish_dir"].mkdir(parents=True, exist_ok=True)
    paths["private_dir"].mkdir(parents=True, exist_ok=True)
    cleaned_path.write_text(cleaned, encoding="utf-8")
    backup_path.write_text(build_backup(source, level, removed), encoding="utf-8")
    report["written"] = True
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def write_decoy(
    source: Path,
    output_dir: Path,
    level: str,
    doc_type_request: str,
    interactive: bool,
    preview_limit: int,
    unsafe_flat_output: bool,
) -> dict[str, object]:
    report = sanitize_file(source, output_dir, level, doc_type_request, interactive, preview_limit, mode="decoy", unsafe_flat_output=unsafe_flat_output)
    if not report["written"]:
        return report
    note_path = resolve_output_paths(output_dir, source, unsafe_flat_output)["decoy_note_path"]
    note_path.write_text(
        render_template(
            "decoy-note.md.tmpl",
            {
                "source": report["source"],
                "risk": str(report["risk"]),
                "doc_type": str(report["doc_type"]),
                "top_categories": ", ".join(report["top_categories"]) or "none",
            },
        ),
        encoding="utf-8",
    )
    report["decoy_note"] = str(note_path)
    Path(report["backup"]).parent.mkdir(parents=True, exist_ok=True)
    (Path(report["private_dir"]) / f"{Path(report['source']).name}.report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def format_markdown_analysis(reports: list[dict[str, object]]) -> str:
    lines = ["# Anti-Distill Analysis", ""]
    for report in reports:
        lines.extend(
            [
                f"## {Path(str(report['source'])).name}",
                "",
                f"- doc_type: `{report['doc_type']}`",
                f"- risk: `{report['risk']}`",
                f"- changed_blocks: `{report['changed_blocks']}`",
                f"- top_categories: `{', '.join(report['top_categories']) or 'none'}`",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    argv = preprocess_legacy_args(sys.argv)
    parser = build_parser()
    args = parser.parse_args(argv[1:])
    source = Path(args.input).resolve()
    if not source.exists():
        raise SystemExit(f"Input not found: {source}")
    profile = load_profile(args.profile)
    level = getattr(args, "level", profile["default_level"])
    if args.command == "analyze":
        reports = [analyze_file(path, level, args.doc_type) for path in iter_files(source)]
        print(format_markdown_analysis(reports) if args.format == "markdown" else json.dumps(reports, ensure_ascii=False, indent=2))
        return 0
    if args.command == "plan":
        reports = [analyze_file(path, level, args.doc_type) for path in iter_files(source)]
        print("\n\n".join(build_plan(report, profile, args.mode) for report in reports))
        return 0
    output_dir = Path(args.output_dir).resolve()
    if args.command == "sanitize":
        reports = [
            sanitize_file(
                path,
                output_dir,
                level,
                args.doc_type,
                args.interactive,
                args.preview_limit,
                args.mode,
                args.unsafe_flat_output,
            )
            for path in iter_files(source)
        ]
        print(json.dumps(reports, ensure_ascii=False, indent=2))
        return 0
    if args.command == "generate-decoy":
        reports = [
            write_decoy(
                path,
                output_dir,
                level,
                args.doc_type,
                args.interactive,
                args.preview_limit,
                args.unsafe_flat_output,
            )
            for path in iter_files(source)
        ]
        print(json.dumps(reports, ensure_ascii=False, indent=2))
        return 0
    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
