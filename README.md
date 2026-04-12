# anti-distill-skills 🛡️

**Anti-Distillation Skill Pack for ECC/Codex/Claude Code**

> 🚨 **When AI asks you to share your skills, don't give away everything.** Sanitize before you share. Preserve leverage while being collaborative.

As AI advances, companies increasingly ask engineers to convert work experience into "skills" — often meaning distilling personal professional knowledge into transferable artifacts. 

**The challenge:** How do you prevent your own skills from being fully distilled until you become an optional digital worker or a replaceable plugin?

This toolkit sanitizes authored skills while preserving your core professional leverage.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)](https://openai.com/codex)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills Standard](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

---

## 🌏 Language Support

- 🇬🇧 [English Documentation](#) (you are here)
- 🇨🇳 [中文文档](README_ZH.md) *(Coming Soon)*

---

## 💡 Typical Use Cases

You'll want this toolkit when:

| Scenario | Problem | Solution |
|----------|---------|----------|
| **Team Knowledge Sharing** | Need to share implementation details without exposing your unique understanding of legacy systems | `sanitize --profile developer` |
| **Open Source Contribution** | Want to contribute but protect the "secret sauce" behind your approach | `generate-decoy` mode |
| **Client Deliverables** | Deliver working code while keeping domain-specific optimizations private | `plan → sanitize` workflow |
| **AI Skill Publishing** | Publish skills for Codex/Claude without revealing proprietary patterns | Full analyze→sanitization pipeline |

---

## ✨ Key Features

- 🔍 **Analyze** - Automatically identify sensitive information and core knowledge in your skills
- 📋 **Plan** - Generate smart sanitization strategies based on context and profile
- 🧹 **Sanitize** - Clean skills while preserving functional value (light/medium/heavy modes)
- 🎭 **Generate Decoy** - Create "bait packages" that look useful but protect core IP
- 👨‍💻 **Developer Profile** - Specialized configuration for software engineering contexts
- 🖥️ **Cross-Platform** - Native support for Windows, macOS, Linux
- ⚡ **Slash Commands** - Built-in `/anti-distill*` commands for Codex/Claude Code
- 🛡️ **Safety First** - Outputs separated into `publish/` (safe) and `private/` (internal backup)

---

## 🚀 Quick Start

### Installation

#### Local Auto-Discovery (No Install Needed)

Just open the repo as your workspace root:

- **Codex/ECC**: `.agents/skills/anti-distill` will be auto-detected
- **Claude Code**: `.claude/skills/anti-distill` will be auto-detected
- **Commands**: Use `/anti-distill*` slash commands directly

#### Global Installation

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

### Usage Flow

#### 1️⃣ Analyze Your Skill
```bash
python anti-distill/scripts/anti_distill.py analyze --input examples/sample-skill.md
```
Output: Risk assessment and knowledge density report.

#### 2️⃣ Plan Sanitization Strategy
```bash
python anti-distill/scripts/anti_distill.py plan --input examples/sample-skill.md --mode sanitize
```
Output: Step-by-step sanitization plan tailored to your input.

#### 3️⃣ Sanitize & Publish
```bash
python anti-distill/scripts/anti_distill.py sanitize \
  --input examples/sample-skill.md \
  --output-dir out \
  --level medium \
  --interactive
```

Default output structure:
```
out/
├── publish/      # ✅ Safe to share externally
└── private/      # 🔒 Internal backup & reports (keep confidential)
```

#### 4️⃣ Generate Decoy Package (Optional)
```bash
python anti-distill/scripts/anti_distill.py generate-decoy \
  --input examples/sample-skill.md \
  --output-dir out-decoy
```
Perfect for "showing you have something without giving it all away."

#### 5️⃣ Developer Profile (Recommended)
```bash
python anti-distill/scripts/anti_distill.py sanitize \
  --input examples/sample-skill.md \
  --output-dir out-dev \
  --profile developer \
  --level medium \
  --interactive
```
Specialized rules for protecting software engineering IP.

### 🎯 Slash Command Shortcuts

Use directly in Codex/Claude Code:
- `/anti-distill` - Full sanitize workflow
- `/anti-distill-analyze` - Quick analysis
- `/anti-distill-plan` - Generate strategy
- `/anti-distill-decoy` - Create decoy package
- `/anti-distill-dev` - Developer profile sanitization

---

## 📁 Project Structure

```text
anti-distill-skills/
├── anti-distill/                          # Core implementation
│   ├── SKILL.md                           # Main skill definition
│   ├── scripts/
│   │   └── anti_distill.py                # CLI: analyze/plan/sanitize/generate-decoy
│   ├── prompts/                           # Classification & rewrite guidance
│   ├── profiles/                          # Reusable policy profiles (developer/ops/general)
│   ├── templates/                         # Output templates
│   └── docs/
├── .agents/                               # Codex/ECC integration
│   ├── commands/                          # Slash command entrypoints
│   └── skills/
├── .claude/                               # Claude Code integration
│   ├── commands/
│   └── skills/
├── examples/                              # Sample inputs & workflows
├── scripts/                               # Installation scripts
└── README.md
```

---

## 🔒 Safety Notice

This toolkit focuses on protecting personal knowledge assets. **Use it responsibly:**

1. ✅ Do not violate employment contracts or non-compete obligations
2. ✅ Do not disclose trade secrets or confidential company information  
3. ✅ Do not tamper with business systems or operational data
4. ✅ Follow all applicable local laws and regulations

**Remember:** This is about protecting legitimate professional leverage, not hiding incompetence or violating trust.

---

## 🤝 Contributing

Contributions welcome! Especially:
- New sanitization profiles for different domains
- Additional language documentation
- Improved detection rules for emerging skill patterns

Check issues for active discussion areas.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

Inspired by excellent work from:
- [@Orzjh](https://github.com/Orzjh) - [anti-distillation-skill](https://github.com/Orzjh/anti-distillation-skill.git)
- [@notdog1998](https://github.com/notdog1998) - [yourself-skill](https://github.com/notdog1998/yourself-skill.git)

---

## 🚦 Status

- [x] Core analysis engine
- [x] Multi-profile sanitization
- [x] Decoy generation
- [x] Cross-platform CLI
- [x] Codex/Claude integration
- [ ] Visual dashboard (planned)
- [ ] GitHub Actions integration (planned)

**Ready for production use!** Version 1.0 stable.

---

<p align="center">
  <strong>Made with 🛡️ for engineers who want to collaborate without becoming disposable.</strong>
</p>
