# anti-distill-skills

面向 ECC/Codex/Claude Code 的反蒸馏技能包。

随着AI的发展，万物均可skill，但随之我也面临了一个问题：公司要求你把工作经验写成skills，本质上是要你把自己的专业知识蒸馏到别人身上。
怎样避免自己的skills被蒸馏，而自己变成了可有可无的数字人或者可以随意替代的插件？

本工具包的目的是避免自己变成数字人，把自己写好的skills进行清洗，保留核心技能。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

## 文档语言

- [英文文档](README.md)

## 项目结构

```text
anti-distill-skills/
├── anti-distill/                          # 核心实现目录
│   ├── SKILL.md                           # 主技能定义
│   ├── scripts/
│   │   └── anti_distill.py                # CLI：analyze/plan/sanitize/generate-decoy
│   ├── prompts/                           # 分类与改写规则
│   │   ├── classifier.md
│   │   ├── diluter_skill.md
│   │   ├── diluter_ops.md
│   │   └── diluter_general.md
│   ├── profiles/                          # 可复用策略配置
│   ├── templates/                         # 输出模板
│   ├── docs/
│   │   ├── modes.md                       # 模式说明
│   │   └── layout.md                      # 布局说明
│   └── agents/
│       └── openai.yaml                    # Codex UI 元数据
├── .agents/
│   ├── commands/                          # 命令入口（/anti-distill*）
│   └── skills/
│       └── anti-distill/                  # Codex/ECC 发现入口
├── .claude/
│   ├── commands/                          # Claude 斜杠命令
│   └── skills/
│       └── anti-distill/                  # Claude Code 发现入口
├── examples/
│   └── sample-skill.md                    # 示例输入
├── scripts/                               # 全局安装脚本
├── README.md
└── README_ZH.md
```

## 安装

### 本地自动发现

- Codex/ECC：以本仓库作为工作区根目录，使用 `.agents/skills/anti-distill`
- Claude Code：以本仓库作为工作区根目录，使用 `.claude/skills/anti-distill`
- 命令入口位于 `.agents/commands/` 与 `.claude/commands/`，可直接使用 `/anti-distill*`

### 全局安装（Windows PowerShell）

```powershell
.\scripts\install-to-codex.ps1
.\scripts\install-to-claude.ps1
```

### 全局安装（macOS/Linux）

```bash
./scripts/install-to-codex.sh
./scripts/install-to-claude.sh
```

Unix 下可选权限设置：

```bash
chmod +x scripts/install-to-codex.sh scripts/install-to-claude.sh
```

## 使用

### 1）分析

```bash
python anti-distill/scripts/anti_distill.py analyze --input examples/sample-skill.md
```

### 2）生成策略计划

```bash
python anti-distill/scripts/anti_distill.py plan --input examples/sample-skill.md --mode sanitize
```

### 3）清洗输出

```bash
python anti-distill/scripts/anti_distill.py sanitize --input examples/sample-skill.md --output-dir out --level medium --interactive
```

默认安全规则：
- `out/publish/` 仅放可对外结果（cleaned/decoy-note）
- `out/private/` 放备份与报告（严禁外发）
- 只有特殊兼容场景才使用 `--unsafe-flat-output`

### 4）生成对外诱饵包

```bash
python anti-distill/scripts/anti_distill.py generate-decoy --input examples/sample-skill.md --output-dir out-decoy
```

### 5）程序员专用配置（推荐）

```bash
python anti-distill/scripts/anti_distill.py sanitize --input examples/sample-skill.md --output-dir out-dev --profile developer --level medium --interactive
```

### 旧用法兼容

不写子命令时默认走 `sanitize`：

```bash
python anti-distill/scripts/anti_distill.py --input examples/sample-skill.md --output-dir out --level light
```

### 斜杠命令快捷入口

- `/anti-distill`
- `/anti-distill-analyze`
- `/anti-distill-plan`
- `/anti-distill-decoy`
- `/anti-distill-dev`

## 声明

本 Skill 旨在帮助个人保护知识资产，不被无偿数字化。使用时请确保：

1. 不违反劳动合同和竞业协议
2. 不泄露公司商业机密
3. 不破坏公司业务数据
4. 符合当地法律法规

## 许可证

MIT

## 鸣谢
感谢以下项目提供的灵感和支持：
- https://github.com/Orzjh/anti-distillation-skill.git
- https://github.com/notdog1998/yourself-skill.git
