# 更新日志

## [v2.4.0] — 2026-04-27

### 同步到 Claude Code v2.1.119

将教程覆盖范围从 Claude Code v2.1.112 提升到 v2.1.119（2026 年 4 月 23 日发布）。
v2.1.120 于 4 月 24 日发布但因回归问题回滚；客户端已自动回滚到 v2.1.119，该版本仍为稳定目标。

### 新增内容（英文文档）

- 原生二进制包说明（v2.1.113）—— CLI 现在以平台特定原生二进制文件形式发布
- 原生 macOS/Linux 构建上的 `bfs`/`ugrep` Glob/Grep 替代脚注（v2.1.117）
- `mcp_tool` hook 类型及示例（v2.1.118）
- PostToolUse / PostToolUseFailure 输入的 `duration_ms` 字段（v2.1.119）
- `prUrlTemplate` 设置（v2.1.119）和扩展的 `--from-pr` 提供商列表（GitLab、Bitbucket）
- `cleanupPeriodDays` 扩展范围（checkpoints + tasks + shell-snapshots + backups，v2.1.117）
- Plugin marketplace 在每个生命周期事件上强制执行（v2.1.117）以及 `hostPattern`/`pathPattern` 正则表达式（v2.1.119）
- 新环境变量：`DISABLE_UPDATES`、`CLAUDE_CODE_HIDE_CWD`、`CLAUDE_CODE_FORK_SUBAGENT`、`OTEL_LOG_TOOL_DETAILS`、`ENABLE_TOOL_SEARCH` Vertex opt-in
- 新 slash commands：`/btw`、支持自定义主题的 `/theme`
- `/usage` 规范命令（合并了 `/cost` + `/stats`，v2.1.118）
- Forked subagents（`CLAUDE_CODE_FORK_SUBAGENT=1`，v2.1.117）
- Auto mode `"$defaults"` token（v2.1.118）
- `wslInheritsWindowsSettings` 托管策略（v2.1.118）
- Vim visual / visual-line 模式（v2.1.118）
- `claude install [version]` 和 `claude plugin tag` 子命令

### 变更

- 文档主机迁移：`docs.anthropic.com/en/docs/claude-code/*` → `code.claude.com/docs/en/*`
- Opus 4.7 effort 级别：自 2026-04-16 发布以来，`xhigh` 现在是 Claude Code 默认值；Opus 4.7 原生上下文窗口确认为 1M（v2.1.117 修复了 `/context` 将其误计为 200K 的问题）
- Pro/Max 订阅者在 Opus 4.6 / Sonnet 4.6 上的默认 effort 从 `medium` 提升到 `high`（v2.1.117）
- `STYLE_GUIDE.md` 来源 URL 从 Claude Apps 文章更新为 `code.claude.com/docs/en/changelog`

### 已弃用（已跟踪，未移除）

- `includeCoAuthoredBy` 设置 → 使用 `attribution.commit` / `attribution.pr`
- `voiceEnabled` 设置 → 使用 `voice.enabled`

### 给翻译维护者的说明

`vi/`、`zh/` 和 `uk/` 本地化树由社区维护，可能落后于英文源。同步翻译的贡献者应针对此版本中更新的英文文件进行 diff 对比。

---

## v2.1.112 — 2026-04-16

### 亮点

- 将所有英文教程与 Claude Code v2.1.112 及新的 Opus 4.7 模型（`claude-opus-4-7`）同步，包括新的 `xhigh` effort 级别（Opus 4.7 的默认值，位于 `high` 与 `max` 之间）、两个新的内置 slash 命令（`/ultrareview`、`/less-permission-prompts`）、Max 订阅者在 Opus 4.7 上不再需要 `--enable-auto-mode`、Windows 上的 PowerShell 工具、“Auto (match terminal)” 主题，以及按提示命名的 plan 文件。所有 18 份英文文档页脚都已提升到 Claude Code v2.1.112。@Luong NGUYEN

### 功能

- 在所有模块、根目录文档、示例和参考资料中添加完整的乌克兰语（uk）本地化（039dde2）@Evgenij I

### Bug 修复

- 修复 pre-tool-check.sh hook 协议错误（bce7cf8）@yarlinghe
- 将错误的 mermaid 示例改为文本块以通过 CI（b8a7b1f）@Evgenij I
- 修复乌克兰语 claude_concepts_guide.md 目录中的 CP1251 编码（d970cc6）@Evgenij I
- 用完整翻译替换占位乌克兰语 README，并修复损坏的锚点（f6d73e2）@Evgenij I
- 将所有页脚中的 Claude Code 版本更正为 2.1.97（63a1416）@Luong NGUYEN
- 应用 2026-04-09 的文档准确性更新（e015f39）@Luong NGUYEN

### 文档

- 同步到 Claude Code v2.1.112（Opus 4.7、`xhigh` effort、`/ultrareview`、`/less-permission-prompts`、PowerShell 工具、Auto-match-terminal 主题）@Luong NGUYEN
- 同步到 Claude Code v2.1.110（TUI、推送通知、会话回顾）（15f0085）@Luong NGUYEN
- 同步到 Claude Code v2.1.101，包含 `/team-onboarding`、`/ultraplan`、Monitor 工具（2deba3a）@Luong NGUYEN
- 将越南语文档与英文源同步（561c6cb）@Thiên Toán
- 更新所有文件的 Last Updated 日期和 Claude Code 版本（7f2e773）@Luong NGUYEN
- 在语言切换器中添加乌克兰语链接（9c224ff）@Luong NGUYEN
- 移除贡献者部分（f07313d）@Luong NGUYEN
- 将 GitHub 指标更新到 21,800+ stars、2,585+ forks（4f55374）@Luong NGUYEN

## v2.3.0 — 2026-04-07

### 功能

- 构建和发布每种语言的 EPUB 制品（90e9c30）@Thiên Toán
- 将缺失的 pre-tool-check.sh hook 添加到 06-hooks（b511ed1）@JiayuWang
- 在 zh/ 目录中添加中文翻译（89e89d4）@Luong NGUYEN
- 添加性能优化器子代理和依赖检查 hook（f53d080）@qk

### Bug 修复

- Windows Git Bash 兼容性 + stdin JSON 协议（2cbb10c）@Luong NGUYEN
- 修正 08-checkpoints 中的 autoCheckpoint 配置文档（749c79f）@JiayuWang
- 用占位符替代 SVG 图像嵌入（1b16709）@Thiên Toán
- 修复内存 README 中的嵌套代码围栏渲染（ce24423）@Zhaoshan Duan
- 应用由 squash merge 丢弃的审查修复（34259ca）@Luong NGUYEN
- 使 hook 脚本与 Windows Git Bash 兼容并使用 stdin JSON 协议（107153d）@binyu li

### 文档

- 与 Claude Code 最新文档（2026 年 4 月）同步所有教程（72d3b01）@Luong NGUYEN
- 在语言切换器中添加中文语言链接（6cbaa4d）@Luong NGUYEN
- 在英文和越南文之间添加语言切换器（100c45e）@Luong NGUYEN
- 添加 GitHub #1 Trending 徽章（0ca8c37）@Luong NGUYEN
- 为上下文区域监控引入 cc-context-stats（d41b335）@Luong NGUYEN
- 引入 luongnv89/skills 集合和 luongnv89/asm skill 管理器（7e3c0b6）@Luong NGUYEN
- 更新 README 统计数据以反映当前 GitHub 指标（5900+ stars, 690+ forks）（5001525）@Luong NGUYEN
- 更新 README 统计数据以反映当前 GitHub 指标（3900+ stars, 460+ forks）（9cb92d6）@Luong NGUYEN

### 重构

- 使用本地 mmdc 渲染替代 Kroki HTTP 依赖（e76bbe4）@Luong NGUYEN
- 将质量检查转移到 pre-commit，CI 作为第二道防线（6d1e0ae）@Luong NGUYEN
- 缩小自动模式权限基线（2790fb2）@Luong NGUYEN
- 用一次性权限设置脚本替换自动适配 hook（995a5d6）@Luong NGUYEN

### 其他

- 左移质量关卡 — 向 pre-commit 添加 mypy，修复 CI 失败（699fb39）@Luong NGUYEN
- 添加越南语（Tiếng Việt）本地化（a70777e）@Thiên Toán

**完整更新日志**：https://github.com/luongnv89/claude-howto/compare/v2.2.0...v2.3.0

---

## v2.2.0 — 2026-03-26

### 文档

- 与 Claude Code v2.1.84（f78c094）同步更新所有教程和参考文档 @luongnv89
  - 将 slash commands 更新为 55+ 个内置命令 + 5 个 bundled skills，并标记 3 个已弃用项
  - 将 hook 事件从 18 个扩展到 25 个，新增 `agent` hook 类型（现在共 4 类）
  - 在高级功能中加入自动模式（Auto Mode）、通道（Channels）、语音输入（Voice Dictation）
  - 为 skill frontmatter 增加 `effort`、`shell` 字段；为 agent 增加 `initialPrompt`、`disallowedTools` 字段
  - 增加 WebSocket MCP transport、elicitation、2KB 工具上限
  - 增加 plugin 的 LSP 支持、`userConfig`、`${CLAUDE_PLUGIN_DATA}`
  - 更新所有参考文档（CATALOG、QUICK_REFERENCE、LEARNING-ROADMAP、INDEX）
- 将 README 重写为落地页结构化指南（32a0776）@luongnv89

### Bug 修复

- 为通过 CI 词典检查，补充缺失的 cSpell 词条和 README 章节（93f9d51）@luongnv89
- 在 cSpell 词典中加入 `Sandboxing`（b80ce6f）@luongnv89

**完整更新日志**：https://github.com/luongnv89/claude-howto/compare/v2.1.1...v2.2.0

---

## v2.1.1 — 2026-03-13

### Bug 修复

- 移除导致 CI 链接检查失败的失效 marketplace 链接（3fdf0d6）@luongnv89
- 将 `sandboxed` 和 `pycache` 加入 cSpell 词典（dc64618）@luongnv89

**完整更新日志**：https://github.com/luongnv89/claude-howto/compare/v2.1.0...v2.1.1

---

## v2.1.0 — 2026-03-13

### 功能

- 新增自适应学习路径，包含自我评估和 lesson quiz skills（1ef46cd）@luongnv89
  - `/self-assessment` - 覆盖 10 个功能领域的交互式能力测验，并生成个性化学习路径
  - `/lesson-quiz [lesson]` - 每课知识检查，包含 8-10 道针对性问题

### Bug 修复

- 更新失效 URL、弃用项和过时引用（8fe4520）@luongnv89
- 修复 resources 和 self-assessment skill 中的损坏链接（7a05863）@luongnv89
- 在 concepts guide 中为嵌套代码块使用 tilde fences（5f82719）@VikalpP
- 为 cSpell 词典补充缺失词汇（8df7572）@luongnv89

### 文档

- Phase 5 QA - 修复各文档中的一致性、URL 和术语问题（00bbe4c）@luongnv89
- 完成 Phase 3-4 - 补充新功能覆盖和参考文档更新（132de29）@luongnv89
- 在 MCP 上下文膨胀章节加入 MCPorter runtime（ef52705）@luongnv89
- 为 6 份指南补充缺失命令、功能和设置（4bc8f15）@luongnv89
- 基于仓库现有规范补充 style guide（84141d0）@luongnv89
- 在指南对比表中加入自我评估行（8fe0c96）@luongnv89
- 将 VikalpP 加入贡献者名单，记录 PR #7（d5b4350）@luongnv89
- 在 README 和 roadmap 中加入 self-assessment 与 lesson-quiz skill 参考（d5a6106）@luongnv89

### 新贡献者

- @VikalpP 完成了他们的首次贡献，见 #7

**完整更新日志**：https://github.com/luongnv89/claude-howto/compare/v2.0.0...v2.1.0

---

## v2.0.0 — 2026-02-01

### 功能

- 与 Claude Code 2026 年 2 月功能同步更新全部文档（487c96d）
  - 更新所有 10 个教程目录和 7 份参考文档中的 26 个文件
  - 补充 **Auto Memory** 文档 - 每个项目的持久学习能力
  - 补充 **Remote Control**、**Web Sessions** 和 **Desktop App** 文档
  - 补充 **Agent Teams** 文档（实验性多 agent 协作）
  - 补充 **MCP OAuth 2.0**、**Tool Search** 和 **Claude.ai Connectors** 文档
  - 补充 subagents 的 **Persistent Memory** 和 **Worktree Isolation** 文档
  - 补充 **Background Subagents**、**Task List**、**Prompt Suggestions** 文档
  - 补充 **Sandboxing** 和 **Managed Settings**（Enterprise）文档
  - 补充 **HTTP Hooks** 和 7 个新 hook 事件的文档
  - 补充 **Plugin Settings**、**LSP Servers** 和 marketplace 更新文档
  - 补充 Checkpoint 的 **Summarize from Checkpoint** 回退选项文档
  - 记录 17 个新的 slash commands（`/fork`、`/desktop`、`/teleport`、`/tasks`、`/fast` 等）
  - 记录新的 CLI flags（`--worktree`、`--from-pr`、`--remote`、`--teleport`、`--teammate-mode` 等）
  - 记录 auto memory、effort 等级、agent teams 等新的环境变量

### 设计

- 将 logo 重设计为简洁调色的 compass-bracket 标志（20779db）

### Bug 修复 / 修正

- 更新模型名称：Sonnet 4.5 → **Sonnet 4.6**，Opus 4.5 → **Opus 4.6**
- 修正 permission mode 名称：用真实的 `default` / `acceptEdits` / `plan` / `dontAsk` / `bypassPermissions` 替代虚构的 “Unrestricted/Confirm/Read-only”
- 修正 hook 事件：移除虚构的 `PreCommit` / `PostCommit` / `PrePush`，加入真实事件（`SubagentStart`、`WorktreeCreate`、`ConfigChange` 等）
- 修正 CLI 语法：用 `claude -p`（print mode）替代虚构的 `claude-code --headless`
- 修正 checkpoint 命令：用真实的 `Esc+Esc` / `/rewind` 界面替代虚构的 `/checkpoint save/list/rewind/diff`
- 修正 session 管理：用真实的 `/resume` / `/rename` / `/fork` 替代虚构的 `/session list/new/switch/save`
- 修正 plugin manifest 格式：从 `plugin.yaml` 迁移到 `.claude-plugin/plugin.json`
- 修正 MCP 配置路径：`~/.claude/mcp.json` → `.mcp.json`（项目）/ `~/.claude.json`（用户）
- 修正文档 URL：`docs.claude.com` → `docs.anthropic.com`；移除虚构的 `plugins.claude.com`
- 移除多个文件中虚构的配置字段
- 将所有 “Last Updated” 日期更新到 2026 年 2 月

**完整更新日志**：https://github.com/luongnv89/claude-howto/compare/20779db...v2.0.0
