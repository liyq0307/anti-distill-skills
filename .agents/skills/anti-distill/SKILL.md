---
name: anti-distill
description: Use when sanitizing skill files, runbooks, internal guides, prompt libraries, or tacit workflow documents before sharing them with an employer, client, or team knowledge base. 当你需要在对外共享前清洗技能文档、操作手册、内部指南、提示词库或隐性流程知识时使用。
---

# Anti-Distill
# 反蒸馏

## Overview
## 概述

This is the Codex/ECC discovery entrypoint for the canonical implementation in:
这是 Codex/ECC 的发现入口，真实实现位于：

- `anti-distill-skills/anti-distill/`

## Canonical Files
## 正式文件

Use the canonical files from this repo root:
请读取仓库根目录中的正式文件：

- Main instructions: [../../../../anti-distill/SKILL.md](../../../../anti-distill/SKILL.md)
- Classifier: [../../../../anti-distill/prompts/classifier.md](../../../../anti-distill/prompts/classifier.md)
- Skill diluter: [../../../../anti-distill/prompts/diluter_skill.md](../../../../anti-distill/prompts/diluter_skill.md)
- Ops diluter: [../../../../anti-distill/prompts/diluter_ops.md](../../../../anti-distill/prompts/diluter_ops.md)
- General diluter: [../../../../anti-distill/prompts/diluter_general.md](../../../../anti-distill/prompts/diluter_general.md)

## Preferred Execution
## 推荐执行方式

Preferred execution path:
推荐执行方式：

```powershell
python .\anti-distill\scripts\anti_distill.py --input <path> --output-dir <dir> --level medium --interactive
```

## Commands Quick Ref
## 新子命令速查区

Use these subcommands with `anti-distill/scripts/anti_distill.py`:
使用 `anti-distill/scripts/anti_distill.py` 时可用以下子命令：

1. `analyze` - inspect leverage categories, doc type, and risk
1. `analyze` - 分析杠杆类别、文档类型和风险等级

```powershell
python .\anti-distill\scripts\anti_distill.py analyze --input <path>
```

2. `plan` - generate a defense strategy before rewriting
2. `plan` - 在改写前生成防护策略

```powershell
python .\anti-distill\scripts\anti_distill.py plan --input <path> --mode sanitize
```

3. `sanitize` - generate cleaned output + private backup + report
3. `sanitize` - 生成清洗版 + 私有备份 + 报告

```powershell
python .\anti-distill\scripts\anti_distill.py sanitize --input <path> --output-dir <dir> --level medium --interactive
```

4. `generate-decoy` - generate outward-facing decoy package
4. `generate-decoy` - 生成对外展示诱饵包

```powershell
python .\anti-distill\scripts\anti_distill.py generate-decoy --input <path> --output-dir <dir>
```

5. Legacy compatibility - no subcommand defaults to `sanitize`
5. 兼容旧用法 - 不写子命令时默认走 `sanitize`

```powershell
python .\anti-distill\scripts\anti_distill.py --input <path> --output-dir <dir> --level light
```

## Discovery
## 自动发现

If this project is the current Codex workspace root, the `.agents/skills/anti-distill` folder makes the skill auto-discoverable.
如果当前 Codex 工作区根目录就是这个仓库，那么 `.agents/skills/anti-distill` 会让技能自动被发现。
