<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 示例 — 快速参考卡

## 🚀 安装快速命令

### 斜杠命令
```bash
# 安装全部
cp 01-slash-commands/*.md .claude/commands/

# 安装指定命令
cp 01-slash-commands/optimize.md .claude/commands/
```

### 记忆
```bash
# 项目记忆
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 个人记忆
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

### 技能
```bash
# 个人技能
cp -r 03-skills/code-review ~/.claude/skills/

# 项目技能
cp -r 03-skills/code-review .claude/skills/
```

### 子代理
```bash
# 安装全部
cp 04-subagents/*.md .claude/agents/

# 安装指定代理
cp 04-subagents/code-reviewer.md .claude/agents/
```

### MCP
```bash
# 设置凭证
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 安装配置（项目级）
cp 05-mcp/github-mcp.json .mcp.json

# 或用户级：添加到 ~/.claude.json
```

### 钩子
```bash
# 安装钩子
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 在设置中配置（~/.claude/settings.json）
```

### 插件
```bash
# 从示例安装（如已发布）
/plugin install pr-review
/plugin install devops-automation
/plugin install documentation
```

### 检查点
```bash
# 每次用户输入时自动创建检查点
# 要回退：按 Esc 键两次或使用：
/rewind

# 然后选择：恢复代码和对话、仅恢复对话、仅恢复代码、
# 从此处摘要、或取消
```

### 高级功能
```bash
# 在设置中配置（.claude/settings.json）
# 参见 09-advanced-features/config-examples.json

# 规划模式
/plan 任务描述

# 权限模式（使用 --permission-mode 标志）
# default        — 对有风险的操作请求批准
# acceptEdits    — 自动接受文件编辑，其他操作请求批准
# plan           — 只读分析，不做修改
# dontAsk        — 接受除有风险外的所有操作
# auto           — 后台分类器自动决定权限
# bypassPermissions — 接受所有操作（需 --dangerously-skip-permissions）

# 会话管理
/resume                # 恢复之前的对话
/rename "name"         # 为当前会话命名
/fork                  # 分叉当前会话
claude -c              # 继续最近的对话
claude -r "session"    # 按名称/ID 恢复会话
```

---

## 📋 功能速查表

| 功能 | 安装路径 | 用法 |
|------|----------|------|
| **斜杠命令（55+）** | `.claude/commands/*.md` | `/command-name` |
| **记忆** | `./CLAUDE.md` | 自动加载 |
| **技能** | `.claude/skills/*/SKILL.md` | 自动调用 |
| **子代理** | `.claude/agents/*.md` | 自动委派 |
| **MCP** | `.mcp.json`（项目级）或 `~/.claude.json`（用户级）| `/mcp__server__action` |
| **钩子（25 个事件）** | `~/.claude/hooks/*.sh` | 事件触发（4 种类型）|
| **插件** | 通过 `/plugin install` | 打包所有功能 |
| **检查点** | 内置功能 | `Esc+Esc` 或 `/rewind` |
| **规划模式** | 内置功能 | `/plan <任务>` |
| **权限模式（6 种）** | 内置功能 | `--allowedTools`、`--permission-mode` |
| **会话** | 内置功能 | `/session <命令>` |
| **后台任务** | 内置功能 | 在后台运行 |
| **远程控制** | 内置功能 | WebSocket API |
| **Web 会话** | 内置功能 | `claude web` |
| **Git 工作树** | 内置功能 | `/worktree` |
| **自动记忆** | 内置功能 | 自动保存到 CLAUDE.md |
| **任务列表** | 内置功能 | `/task list` |
| **捆绑技能（5 个）** | 内置功能 | `/simplify`、`/loop`、`/claude-api`、`/voice`、`/browse` |

---

## 🎯 常见使用场景

### 代码审查
```bash
# 方法 1：斜杠命令
cp 01-slash-commands/optimize.md .claude/commands/
# 使用：/optimize

# 方法 2：子代理
cp 04-subagents/code-reviewer.md .claude/agents/
# 使用：自动委派

# 方法 3：技能
cp -r 03-skills/code-review ~/.claude/skills/
# 使用：自动调用

# 方法 4：插件（最佳方案）
/plugin install pr-review
# 使用：/review-pr
```

### 文档生成
```bash
# 斜杠命令
cp 01-slash-commands/generate-api-docs.md .claude/commands/

# 子代理
cp 04-subagents/documentation-writer.md .claude/agents/

# 技能
cp -r 03-skills/doc-generator ~/.claude/skills/

# 插件（完整方案）
/plugin install documentation
```

### DevOps 运维
```bash
# 完整插件
/plugin install devops-automation

# 命令：/deploy, /rollback, /status, /incident
```

### 团队标准
```bash
# 项目记忆
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 编辑以匹配你的团队
vim CLAUDE.md
```

### 自动化与钩子
```bash
# 安装钩子（25 个事件，4 种类型：工具、HTTP、提示词、代理）
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 示例：
# - 提交前测试：pre-commit.sh
# - 自动格式化代码：format-code.sh
# - 安全扫描：security-scan.sh

# Auto Mode 用于完全自主的工作流
claude --enable-auto-mode -p "重构并测试认证模块"
# 或使用 Shift+Tab 交互式切换模式
```

### 安全重构
```bash
# 每次提示前自动创建检查点
# 尝试重构
# 如果成功：继续
# 如果失败：按 Esc+Esc 或使用 /rewind 回退
```

### 复杂实现
```bash
# 使用规划模式
/plan 实现用户认证系统

# Claude 创建详细计划
# 审阅并批准
# Claude 系统化实施
```

### CI/CD 集成
```bash
# 以无头模式运行（非交互式）
claude -p "运行所有测试并生成报告"

# 带 CI 用权限模式
claude -p "运行测试" --permission-mode dontAsk

# 带 Auto Mode 用于完全自主的 CI 任务
claude --enable-auto-mode -p "运行测试并修复失败"

# 带钩子实现自动化
# 参见 09-advanced-features/README.md
```

### 学习与实验
```bash
# 使用 plan 模式进行安全分析
claude --permission-mode plan

# 安全实验 —— 检查点自动创建
# 如需回退：按 Esc+Esc 或使用 /rewind
```

### 代理团队
```bash
# 启用代理团队
export CLAUDE_AGENT_TEAMS=1

# 或在 settings.json 中
{ "agentTeams": { "enabled": true } }

# 以此开始："使用团队方式实现功能 X"
```

### 定时任务
```bash
# 每 5 分钟运行一次命令
/loop 5m /check-status

# 一次性提醒
/loop 30m "提醒我检查部署状态"
```

---

## 📁 文件位置参考

```
你的项目目录/
├── .claude/
│   ├── commands/              # 斜杠命令放这里
│   ├── agents/                # 子代理放这里
│   ├── skills/                # 项目技能放这里
│   └── settings.json          # 项目设置（钩子等）
├── .mcp.json                  # MCP 配置（项目级）
├── CLAUDE.md                  # 项目记忆
└── src/
    └── api/
        └── CLAUDE.md          # 目录专用记忆

用户主目录/
├── .claude/
│   ├── commands/              # 个人命令
│   ├── agents/                # 个人代理
│   ├── skills/                # 个人技能
│   ├── hooks/                 # 钩子脚本
│   ├── settings.json          # 用户设置
│   ├── managed-settings.d/    # 托管设置（企业/组织）
│   └── CLAUDE.md              # 个人记忆
└── .claude.json               # 个人 MCP 配置（用户级）
```

---

## 🔍 查找示例

### 按类别查找
- **斜杠命令**：`01-slash-commands/`
- **记忆**：`02-memory/`
- **技能**：`03-skills/`
- **子代理**：`04-subagents/`
- **MCP**：`05-mcp/`
- **钩子**：`06-hooks/`
- **插件**：`07-plugins/`
- **检查点**：`08-checkpoints/`
- **高级功能**：`09-advanced-features/`
- **CLI**：`10-cli/`

### 按用途查找
- **性能优化**：`01-slash-commands/optimize.md`
- **安全审查**：`04-subagents/secure-reviewer.md`
- **测试**：`04-subagents/test-engineer.md`
- **文档**：`03-skills/doc-generator/`
- **DevOps**：`07-plugins/devops-automation/`

### 按复杂度查找
- **简单**：斜杠命令
- **中等**：子代理、记忆
- **高级**：技能、钩子
- **完整方案**：插件

---

## 🎓 学习路径

### 第 1 天
```bash
# 阅读概览
cat README.md

# 安装一个命令
cp 01-slash-commands/optimize.md .claude/commands/

# 试用
/optimize
```

### 第 2-3 天
```bash
# 设置记忆
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
vim CLAUDE.md

# 安装子代理
cp 04-subagents/code-reviewer.md .claude/agents/
```

### 第 4-5 天
```bash
# 设置 MCP
export GITHUB_TOKEN="your_token"
cp 05-mcp/github-mcp.json .mcp.json

# 尝试 MCP 命令
/mcp__github__list_prs
```

### 第 2 周
```bash
# 安装技能
cp -r 03-skills/code-review ~/.claude/skills/

# 让它自动调用
# 只需说："审查这段代码的问题"
```

### 第 3 周及以后
```bash
# 安装完整插件
/plugin install pr-review

# 使用打包的功能
/review-pr
/check-security
/check-tests
```

---

## 新功能速览（2026 年 3 月）

| 功能 | 描述 | 用法 |
|------|------|------|
| **Auto Mode（自动模式）** | 完全自主操作，带后台分类器 | `--enable-auto-mode` 标志，`Shift+Tab` 切换模式 |
| **Channels（频道）** | Discord 和 Telegram 集成 | `--channels` 标志，Discord/Telegram Bot |
| **Voice Dictation（语音输入）** | 向 Claude 口述命令和上下文 | `/voice` 命令 |
| **Hooks（25 个事件）** | 扩展的钩子系统，4 种类型 | 工具、HTTP、提示词、代理钩子类型 |
| **MCP Elicitation（引导）** | MCP 服务器可在运行时请求用户输入 | 服务器需要澄清时自动提示 |
| **WebSocket MCP** | WebSocket 传输用于 MCP 连接 | 在 `.mcp.json` 中用 `ws://` URL 配置 |
| **Plugin LSP** | 插件的 LSP 支持 | `userConfig`、`${CLAUDE_PLUGIN_DATA}` 变量 |
| **Remote Control（远程控制）** | 通过 WebSocket API 控制 Claude Code | `claude --remote` 用于外部集成 |
| **Web Sessions（Web 会话）** | 浏览器端 Claude Code 界面 | `claude web` 启动 |
| **Desktop App（桌面应用）** | 原生桌面应用 | 从 claude.ai/download 下载 |
| **Task List（任务列表）** | 管理后台任务 | `/task list`、`/task status <id>` |
| **Auto Memory（自动记忆）** | 从对话中自动保存记忆 | Claude 自动将关键上下文保存到 CLAUDE.md |
| **Git Worktrees（工作树）** | 并行开发的隔离工作区 | `/worktree` 创建隔离工作区 |
| **Model Selection（模型选择）** | 在 Sonnet 4.6 和 Opus 4.6 间切换 | `/model` 或 `--model` 标志 |
| **Agent Teams（代理团队）** | 多个代理协调完成任务 | 通过 `CLAUDE_AGENT_TEAMS=1` 环境变量启用 |
| **Scheduled Tasks（定时任务）** | 用 `/loop` 执行循环任务 | `/loop 5m /command` 或 CronCreate 工具 |
| **Chrome Integration（浏览器集成）** | 浏览器自动化 | `--chrome` 标志或 `/chrome` 命令 |
| **Keyboard Customization（键盘定制）** | 自定义快捷键 | `/keybindings` 命令 |

---

## 技巧与窍门

### 定制化建议
- 先按原样使用示例
- 根据需求修改
- 与团队共享前先测试
- 将配置纳入版本控制

### 最佳实践
- 用记忆记录团队标准
- 用插件管理完整工作流
- 用子代理处理复杂任务
- 用斜杠命令处理快速任务

### 故障排除
```bash
# 检查文件位置
ls -la .claude/commands/
ls -la .claude/agents/

# 验证 YAML 语法
head -20 .claude/agents/code-reviewer.md

# 测试 MCP 连接
echo $GITHUB_TOKEN
```

---

## 📊 功能矩阵

| 需求 | 使用方式 | 示例 |
|------|----------|------|
| 快捷命令 | 斜杠命令（55+）| `01-slash-commands/optimize.md` |
| 团队标准 | 记忆 | `02-memory/project-CLAUDE.md` |
| 自动工作流 | 技能 | `03-skills/code-review/` |
| 专业任务 | 子代理 | `04-subagents/code-reviewer.md` |
| 外部数据 | MCP（含引导、WebSocket）| `05-mcp/github-mcp.json` |
| 事件自动化 | 钩子（25 个事件，4 种类型）| `06-hooks/pre-commit.sh` |
| 完整解决方案 | 插件（含 LSP 支持）| `07-plugins/pr-review/` |
| 安全实验 | 检查点 | `08-checkpoints/checkpoint-examples.md` |
| 完全自主 | Auto Mode | `--enable-auto-mode` 或 `Shift+Tab` |
| 聊天集成 | Channels | `--channels`（Discord、Telegram）|
| CI/CD 流水线 | CLI | `10-cli/README.md` |

---

## 🔗 快速链接

- **主指南**：`README.md`
- **完整索引**：`INDEX.md`
- **摘要**：`EXAMPLES_SUMMARY.md`
- **原始指南**：`claude_concepts_guide.md`

---

## 📞 常见问题

**Q: 我应该用哪个？**
A: 从斜杠命令开始，按需添加功能。

**Q: 可以混合使用吗？**
A: 可以！它们协同工作。记忆 + 命令 + MCP = 强大组合。

**Q: 如何与团队分享？**
A: 将 `.claude/` 目录提交到 Git。

**Q: 密钥怎么办？**
A: 使用环境变量，永远不要硬编码。

**Q: 可以修改示例吗？**
A: 当然可以！它们就是供你定制的模板。

---

## ✅ 入门检查清单

快速入门清单：

- [ ] 阅读 `README.md`
- [ ] 安装 1 个斜杠命令
- [ ] 试用该命令
- [ ] 创建项目 `CLAUDE.md`
- [ ] 安装 1 个子代理
- [ ] 设置 1 个 MCP 集成
- [ ] 安装 1 个技能
- [ ] 试用一个完整插件
- [ ] 按需定制
- [ ] 与团队分享

---

**快速开始**：`cat README.md`

**完整索引**：`cat INDEX.md`

**本卡片**：随时放在手边，方便快速查阅！
