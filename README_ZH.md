# anti-distill-skills 🛡️

**面向 ECC/Codex/Claude Code 的反蒸馏技能包**

> 🚨 **当公司让你把经验写成 AI 技能时，别把所有家底都交出去。** 先清理再分享，保留你的核心杠杆。

随着 AI 的发展，越来越多的公司要求工程师把工作经验转化为"可分享的 AI 技能"——本质上是要你把个人专业知识蒸馏成别人也能用的通用资产。

**问题：** 当你的所有核心知识都被提取成标准化技能时，你自己会不会变得可有可无，变成一个可随意替换的数字插件？

本工具包帮你清洗对外分享的技能，同时保留不可替代的专业杠杆。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)](https://openai.com/codex)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills 标准](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

---

## 🌏 多语言支持

- 🇬🇧 [English Documentation](README.md)
- 🇨🇳 中文文档（你在这里）

---

## 💡 典型使用场景

在以下场景中，你会需要这个工具：

| 场景 | 痛点 | 解决方案 |
|------|------|----------|
| **团队知识共享** | 需要分享实现细节，但不想暴露自己对遗留系统的独特理解 | `sanitize --profile developer` |
| **开源贡献** | 想参与开源，但要保护自己的"独门秘籍" | `generate-decoy` 模式 |
| **客户交付** | 交付可用代码的同时，隐藏领域特定的优化思路 | `plan → sanitize` 流程 |
| **AI 技能发布** | 为 Codex/Claude 发布技能，但不想泄露专有模式 | 完整的分析→清理管道 |

---

## ✨ 核心功能

- 🔍 **分析** - 自动识别技能中的敏感信息和核心知识密度
- 📋 **规划** - 根据上下文和专业配置生成智能清理策略
- 🧹 **清洗** - 清理技能但保留实用价值（轻度/中度/深度三种强度）
- 🎭 **生成诱饵** - 创建"看似有用但保护核心 IP"的诱饵包
- 👨‍💻 **开发者专用** - 针对软件工程场景的特殊配置
- 🖥️ **跨平台** - 原生支持 Windows / macOS / Linux
- ⚡ **斜杠命令** - 内置 `/anti-distill*` 快捷命令（Codex/Claude Code）
- 🛡️ **安全第一** - 输出分为 `publish/`（安全可公开）和 `private/`（内部备份）

---

## 🚀 快速开始

### 安装

#### 本地自动发现（无需安装）

只需将仓库作为工作区根目录打开：

- **Codex/ECC**：`.agents/skills/anti-distill` 会自动被检测到
- **Claude Code**：`.claude/skills/anti-distill` 会自动被检测到
- **命令**：直接使用 `/anti-distill*` 斜杠命令

#### 全局安装

**Windows PowerShell:**
```powershell
.\scripts\install-to-codex.ps1
.\scripts\install-to-claude.ps1
```

**macOS/Linux:**
```bash
chmod +x scripts/install-to-codex.sh scripts/install-to-claude.sh
./scripts/install-to-codex.sh
./scripts/install-to-claude.sh
```

### 使用流程

#### 1️⃣ 分析你的技能
```bash
python anti-distill/scripts/anti_distill.py analyze --input examples/sample-skill.md
```
**输出：** 风险评估报告 + 知识密度分析。

#### 2️⃣ 制定清理策略
```bash
python anti-distill/scripts/anti_distill.py plan --input examples/sample-skill.md --mode sanitize
```
**输出：** 针对你的输入量身定制的分步清理计划。

#### 3️⃣ 清洗并输出
```bash
python anti-distill/scripts/anti_distill.py sanitize \
  --input examples/sample-skill.md \
  --output-dir out \
  --level medium \
  --interactive
```

默认输出结构：
```
out/
├── publish/      # ✅ 安全，可对外分享
└── private/      # 🔒 内部备份与报告（严禁外传）
```

#### 4️⃣ 生成诱饵包（可选）
```bash
python anti-distill/scripts/anti_distill.py generate-decoy \
  --input examples/sample-skill.md \
  --output-dir out-decoy
```
适合"展示你有东西，但不全盘托出"的场景。

#### 5️⃣ 开发者专用模式（强烈推荐）
```bash
python anti-distill/scripts/anti_distill.py sanitize \
  --input examples/sample-skill.md \
  --output-dir out-dev \
  --profile developer \
  --level medium \
  --interactive
```
专为软件工程师设计，保护技术 IP 的特殊规则集。

### 🎯 斜杠命令快捷方式

在 Codex/Claude Code 中直接使用：
- `/anti-distill` - 完整清洗流程
- `/anti-distill-analyze` - 快速分析
- `/anti-distill-plan` - 生成策略
- `/anti-distill-decoy` - 创建诱饵包
- `/anti-distill-dev` - 开发者模式清洗

---

## 📁 项目结构

```text
anti-distill-skills/
├── anti-distill/                          # 核心实现
│   ├── SKILL.md                           # 主技能定义
│   ├── scripts/
│   │   └── anti_distill.py                # CLI：analyze/plan/sanitize/generate-decoy
│   ├── prompts/                           # 分类与改写规则
│   ├── profiles/                          # 可复用策略配置（developer/ops/general）
│   ├── templates/                         # 输出模板
│   └── docs/
├── .agents/                               # Codex/ECC 集成
│   ├── commands/                          # 斜杠命令入口
│   └── skills/
├── .claude/                               # Claude Code 集成
│   ├── commands/
│   └── skills/
├── examples/                              # 示例输入与工作流
├── scripts/                               # 安装脚本
└── README.md
```

---

## 🔒 声明与注意事项

本工具旨在帮助个人保护知识资产，避免被无偿数字化。**请负责任地使用：**

1. ✅ 不违反劳动合同和竞业协议
2. ✅ 不泄露公司商业机密或保密信息
3. ✅ 不破坏公司业务系统或操作数据
4. ✅ 遵守当地法律法规

**记住：** 这是为了保护合理的职业杠杆，不是隐藏无能或违背信任。

---

## 🤝 贡献指南

欢迎各种形式的贡献！尤其是：
- 不同领域的清理策略配置
- 更多语言的文档
- 针对新兴技能模式的检测规则改进

查看 issues 了解活跃讨论。

---

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

---

## 🙏 鸣谢

灵感来源于以下优秀项目：
- [@Orzjh](https://github.com/Orzjh) - [anti-distillation-skill](https://github.com/Orzjh/anti-distillation-skill.git)
- [@notdog1998](https://github.com/notdog1998) - [yourself-skill](https://github.com/notdog1998/yourself-skill.git)

---

## 🚦 项目状态

- [x] 核心分析引擎
- [x] 多配置文件清洗
- [x] 诱饵包生成
- [x] 跨平台 CLI
- [x] Codex/Claude 集成
- [ ] 可视化仪表盘（规划中）
- [ ] GitHub Actions 集成（规划中）

**已可用于生产环境！** v1.0 稳定版。

---

<p align="center">
  <strong>致敬那些想在合作中不被当成可替代品的工程师们 🛡️</strong>
</p>
