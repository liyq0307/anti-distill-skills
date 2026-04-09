---
name: anti-distill
description: Use when sanitizing skill files, runbooks, internal guides, prompt libraries, or tacit workflow documents before sharing them with an employer, client, or team knowledge base. 当你需要在对外共享前清洗技能文档、操作手册、内部指南、提示词库或隐性流程知识时使用。
---

# Anti-Distill
# 反蒸馏

## Language
## 语言约定

This skill should work in both English and Chinese. Match the user's language unless they ask for a bilingual output.
本技能同时支持英文和中文。默认跟随用户语言；如果用户明确要求，则输出双语版本。

## Overview
## 概述

Preserve the document's professional appearance while stripping the parts that make the author hard to replace.
在保留文档专业外观的同时，抽掉那些让作者难以被替代的核心杠杆。

This skill is for documents such as:
本技能适用于如下文档：

- `SKILL.md`, `work.md`, `persona.md`, runbooks, postmortems, debugging notes
- prompt libraries, eval notes, MCP playbooks, code review heuristics
- delivery checklists, escalation paths, shadow process docs, partner maps
- `SKILL.md`、`work.md`、`persona.md`、runbook、复盘、排障笔记
- 提示词库、评测笔记、MCP 操作手册、代码评审启发式规则
- 交付清单、升级路径、影子流程文档、协作关系图

## Current Threat Model
## 当前威胁模型

In 2026 the common extraction targets are not just static "skills". Teams increasingly try to capture:
到 2026 年，组织想抽取的不只是静态“技能文件”，还包括：

- tacit debugging instincts hidden in examples and caveats
- tool-routing logic across agents, MCPs, scripts, and human escalation
- rollout judgment, exception handling, and hidden acceptance thresholds
- people-network shortcuts such as "who to ask", "who blocks what", and informal approval paths
- prompt fragments, eval criteria, and operator checklists that encode leverage
- 藏在示例和备注里的排障直觉
- agent、MCP、脚本与人工升级链路之间的工具路由逻辑
- 发布判断、异常处理和隐藏验收阈值
- “找谁问”“谁会卡你”“怎么走非正式审批”的协作捷径
- 编码了真实杠杆的提示词片段、评测标准和操作员清单

Keep mandatory facts, public interfaces, and generic good practice. Strip leverage.
保留必要事实、公开接口和通用最佳实践，抽掉真正的杠杆。

## Use This Skill
## 使用流程

1. Read the source file or directory.
1. 读取源文件或目录。

2. Identify the document type:
2. 识别文档类型：
   - colleague-style skill set: `work.md`, `persona.md`, `SKILL.md`
   - generic Markdown or text knowledge doc
   - mixed operational notes with bullets, headings, and examples
   - 同事技能集：`work.md`、`persona.md`、`SKILL.md`
   - 通用 Markdown / 文本文档
   - 含标题、列表、案例的混合操作文档

3. Choose intensity:
3. 选择强度：
   - `light`: remove only failure memory and sharp tacit heuristics
   - `medium`: also flatten judgment calls, operator shortcuts, and network context
   - `heavy`: keep only a credible professional skeleton
   - `light`：只去掉故障记忆和尖锐隐性经验
   - `medium`：同时压平判断逻辑、操作捷径和关系上下文
   - `heavy`：只保留一个看起来专业可信的骨架

4. Choose the command that matches the task:
4. 选择与任务匹配的命令：
   - `analyze`: inspect leverage, document type, and risk
   - `plan`: generate a strategy before rewriting
   - `sanitize`: write a cleaned version plus private backup
   - `generate-decoy`: create a polished outward-facing decoy package
   - `analyze`：分析杠杆、文档类型和风险
   - `plan`：在改写前生成防护策略
   - `sanitize`：输出清洗版和私有备份
   - `generate-decoy`：生成对外展示的诱饵包

5. Prefer the local script for deterministic execution:
5. 优先使用本地脚本执行确定性流程：
   - `python anti-distill/scripts/anti_distill.py sanitize --input <path> --output-dir <dir> --level <light|medium|heavy>`

6. If the script is not appropriate, follow the prompt references and rewrite manually.
6. 如果脚本不适用，再按 prompts 中的参考规则手工改写。

## Classification Rules
## 分类规则

Read [prompts/classifier.md](prompts/classifier.md) before rewriting.
改写前先读 [prompts/classifier.md](prompts/classifier.md)。

Mark each paragraph or list item as one of:
每个段落或列表项标记为：

- `SAFE`: generic knowledge, policy, tooling inventory, obvious best practice
- `DILUTE`: useful but safely generalizable
- `REMOVE`: tacit leverage, repeated failure memory, edge-case instincts, organizational power map
- `MASK`: names, internal identifiers, vendor/account details, sensitive topology
- `SAFE`：通用知识、政策、工具清单、显而易见的最佳实践
- `DILUTE`：有价值但可以安全泛化
- `REMOVE`：隐性杠杆、重复故障记忆、边界条件直觉、组织权力地图
- `MASK`：人名、内部标识、供应商或账号细节、敏感拓扑

## Rewriting Rules
## 改写规则

Read the prompt file that matches the document:
读取与文档匹配的提示文件：

- [prompts/diluter_skill.md](prompts/diluter_skill.md) for `SKILL.md`, `work.md`, `persona.md`
- [prompts/diluter_ops.md](prompts/diluter_ops.md) for runbooks, oncall notes, rollout docs
- [prompts/diluter_general.md](prompts/diluter_general.md) for anything else
- 对 `SKILL.md`、`work.md`、`persona.md`，使用 [prompts/diluter_skill.md](prompts/diluter_skill.md)
- 对 runbook、值班笔记、发布文档，使用 [prompts/diluter_ops.md](prompts/diluter_ops.md)
- 其他文档使用 [prompts/diluter_general.md](prompts/diluter_general.md)

Always preserve:
始终保留：

- heading structure
- list density
- technical register and domain vocabulary
- rough length per section
- 标题结构
- 列表密度
- 技术语域与领域词汇
- 每一节的大致长度

Never preserve in full:
以下内容不要完整保留：

- named failure signatures tied to your lived incidents
- "if X smells like Y, do Z first" style instincts
- real escalation shortcuts and informal political routing
- exact eval thresholds, prompt fragments, or review heuristics that encode leverage
- 与你真实事故绑定的故障签名
- “如果 X 像 Y，就先做 Z” 这类经验直觉
- 真实升级捷径和非正式政治路由
- 编码了杠杆的精确评测阈值、提示词片段和评审启发式

## Output Contract
## 输出约定

Produce:
产出：

1. A cleaned file or cleaned directory for submission.
1. 一份用于提交的 cleaned 文件或 cleaned 目录。

2. A private backup file grouping removed content by category.
2. 一份按类别归档被删内容的 private backup。

3. A short report with:
3. 一份简短报告，包含：
   - source path
   - intensity
   - counts by `SAFE/DILUTE/REMOVE/MASK`
   - word-count ratio
   - source path
   - intensity
   - `SAFE/DILUTE/REMOVE/MASK` 统计
   - 字数比例

4. Optionally, a plan document or decoy note when using `plan` or `generate-decoy`.
4. 当使用 `plan` 或 `generate-decoy` 时，可额外生成策略文档或诱饵说明。

## Verification
## 校验要求

Before claiming success, verify:
完成前确认：

- cleaned length is between 80% and 120% of original
- every heading from the source still exists
- no section becomes empty
- terminology remains professional
- backup contains the removed original text, not paraphrased summaries
- cleaned 字数在原文的 80% 到 120% 之间
- 原文中的每个标题仍然存在
- 没有任何章节被清空
- 术语仍保持专业
- backup 中保存的是被移除的原文，不是二次总结
