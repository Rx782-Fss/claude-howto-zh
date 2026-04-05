# 更新日志(Changelog)

## v2.2.0 -- 2026-03-26

### 文档更新

- 与 Claude Code v2.1.84 (f78c094) 同步所有教程和参考文档 @luongnv89
  - 更新斜杠命令至 55+ 内置 + 5 个捆绑技能,标记 3 个已废弃
  - 扩展钩子事件从 18 个增至 25 个,新增 `agent` 钩子类型(现共 4 种)
  - 新增 Auto Mode(自动模式)、Channels(频道)、Voice Dictation(语音输入)到高级功能
  - 新增 `effort`、`shell` 技能前置元数据字段;`initialPrompt`、`disallowedTools` 代理字段
  - 新增 WebSocket MCP 传输、Elicitation(引导)、2KB 工具上限
  - 新增插件 LSP 支持、`userConfig`、`${CLAUDE_PLUGIN_DATA}`
  - 更新所有参考文档(CATALOG、QUICK_REFERENCE、LEARNING-ROADMAP、INDEX)
- 将 README 重写为落地页结构化指南 (32a0776) @luongnv89

### Bug 修复

- 添加缺失的 cSpell 单词和 README 章节以符合 CI 合规要求 (93f9d51) @luongnv89
- 将 `Sandboxing` 添加到 cSpell 字典中 (b80ce6f) @luongnv89

**完整变更日志**:https://github.com/luongnv89/claude-howto/compare/v2.1.1...v2.2.0

---

## v2.1.1 -- 2026-03-13

### Bug 修复

- 移除失效的市场链接,修复 CI 链接检查失败问题 (3fdf0d6) @luongnv89
- 将 `sandboxed` 和 `pycache` 添加到 cSpell 字典中 (dc64618) @luongnv89

**完整变更日志**:https://github.com/luongnv89/claude-howto/compare/v2.1.0...v2.1.1

---

## v2.1.0 -- 2026-03-13

### 新功能

- 新增自适应学习路径,包含自我评估和课程测验技能 (1ef46cd) @luongnv89
  - `/self-assessment` -- 覆盖 10 个功能领域的交互式能力测验,提供个性化学习路径
  - `/lesson-quiz [lesson]` -- 每课知识检测,包含 8-10 道针对性题目

### Bug 修复

- 修复损坏的 URL、废弃引用和过时内容 (8fe4520) @luongnv89
- 修复资源和自我评估技能中的断链 (7a05863) @luongnv89
- 在概念指南中对嵌套代码块使用波浪线围栏 (5f82719) @VikalpP
- 向 cSpell 字典添加缺失单词 (8df7572) @luongnv89

### 文档更新

- 第 5 阶段 QA ---- 修复文档的一致性、URL 和术语 (00bbe4c) @luongnv89
- 完成第 3-4 阶段 ---- 新功能覆盖和参考文档更新 (132de29) @luongnv89
- 在 MCP 上下文膨胀部分添加 MCPorter 运行时 (ef52705) @luongnv89
- 在 6 个指南中补充缺失的命令、功能和设置 (4bc8f15) @luongnv89
- 基于现有仓库约定添加风格指南 (84141d0) @luongnv89
- 在指南对比表中添加自我评估行 (8fe0c96) @luongnv89
- 因 PR #7 将 VikalpP 添加到贡献者列表 (d5b4350) @luongnv89
- 在 README 和路线图中添加自我评估及课程测验技能引用 (d5a6106) @luongnv89

### 新贡献者

- @VikalpP 首次参与贡献 #7

**完整变更日志**:https://github.com/luongnv89/claude-howto/compare/v2.0.0...v2.1.0

---

## v2.0.0 -- 2026-02-01

### 新功能

- 与 Claude Code 2026 年 2 月的所有新功能同步文档 (487c96d)
  - 更新全部 10 个教程目录和 7 份参考文档中的 26 个文件
  - 新增 **Auto Memory(自动记忆)** 文档 ---- 每个项目持久化的学习记录
  - 新增 **Remote Control(远程控制)**、**Web Sessions(Web 会话)** 和 **Desktop App(桌面应用)** 文档
  - 新增 **Agent Teams(代理团队)** 文档(实验性多代理协作)
  - 新增 **MCP OAuth 2.0**、**Tool Search(工具搜索)** 和 **Claude.ai Connectors** 文档
  - 新增 **Persistent Memory(持久化记忆)** 和 **Worktree Isolation(工作树隔离)** 子代理文档
  - 新增 **Background Subagents(后台子代理)**、**Task List(任务列表)**、**Prompt Suggestions(提示建议)** 文档
  - 新增 **Sandboxing(沙箱)** 和 **Managed Settings(托管设置)**(企业版)文档
  - 新增 **HTTP Hooks** 和 7 个新钩子事件文档
  - 新增 **Plugin Settings(插件设置)**、**LSP Servers(LSP 服务器)** 和 Marketplace(市场)更新文档
  - 新增 **Summarize from Checkpoint(从检查点摘要)** 回退选项文档
  - 记录 17 个新斜杠命令(`/fork`、`/desktop`、`/teleport`、`/tasks`、`/fast` 等)
  - 记录新的 CLI 标志(`--worktree`、`--from-pr`、`--remote`、`--teleport`、`--teammate-mode` 等)
  - 记录自动记忆、努力程度级别、代理团队等的新环境变量

### 设计改进

- 重新设计 Logo 为指南针-括号标识,采用极简配色方案 (20779db)

### Bug 修复 / 修正

- 更新模型名称:Sonnet 4.5 → **Sonnet 4.6**,Opus 4.5 → **Opus 4.6**
- 修复权限模式名称:将虚构的 "Unrestricted/Confirm/Read-only" 替换为实际的 `default`/`acceptEdits`/`plan`/`dontAsk`/`bypassPermissions`
- 修复钩子事件:移除虚构的 `PreCommit`/`PostCommit`/`PrePush`,添加真实事件(`SubagentStart`、`WorktreeCreate`、`ConfigChange` 等)
- 修复 CLI 语法:将 `claude-code --headless` 替换为 `claude -p`(打印模式)
- 修复检查点命令:将虚构的 `/checkpoint save/list/rewind/diff` 替换为实际的 `Esc+Esc` / `/rewind` 接口
- 修复会话管理:将虚构的 `/session list/new/switch/save` 替换为真实的 `/resume`/`/rename`/`/fork`
- 修复插件清单格式:将 `plugin.yaml` 迁移至 `.claude-plugin/plugin.json`
- 修复 MCP 配置路径:`~/.claude/mcp.json` → `.mcp.json`(项目级)/ `~/.claude.json`(用户级)
- 修复文档 URL:`docs.claude.com` → `docs.anthropic.com`;移除虚构的 `plugins.claude.com`
- 移除多个文件中的虚构配置字段
- 将所有"最后更新"日期更新为 2026 年 2 月

**完整变更日志**:https://github.com/luongnv89/claude-howto/compare/20779db...v2.0.0
