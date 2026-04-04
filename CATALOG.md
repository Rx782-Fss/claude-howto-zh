<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 功能目录

> 所有 Claude Code 功能的快速参考指南：命令、代理、技能、插件和钩子。

**导航**：[命令](#slash-commands) | [权限模式](#permission-modes) | [子代理](#subagents) | [技能](#skills) | [插件](#plugins) | [MCP 服务器](#mcp-servers) | [钩子](#hooks) | [记忆文件](#memory-files) | [新功能（2026年3月）](#新功能-2026年3月)

---

## 总览

| 功能 | 内置数量 | 示例 | 总计 | 参考 |
|---------|----------|----------|-------|-----------|
| **Slash Commands（斜杠命令）** | 55+ | 8 | 63+ | [01-slash-commands/](01-slash-commands/) |
| **Subagents（子代理）** | 6 | 10 | 16 | [04-subagents/](04-subagents/) |
| **Skills（技能）** | 5 个内置 | 4 | 9 | [03-skills/](03-skills/) |
| **Plugins（插件）** | - | 3 | 3 | [07-plugins/](07-plugins/) |
| **MCP Servers（MCP 服务器）** | 1 | 8 | 9 | [05-mcp/](05-mcp/) |
| **Hooks（钩子）** | 25 种事件 | 7 | 7 | [06-hooks/](06-hooks/) |
| **Memory（记忆）** | 7 种类型 | 3 | 3 | [02-memory/](02-memory/) |
| **总计** | **99** | **43** | **117** | |

---

## Slash Commands（斜杠命令）

命令是用户手动触发的快捷方式，用于执行特定操作。

### 内置命令

| 命令 | 说明 | 使用场景 |
|---------|-------------|-------------|
| `/help` | 显示帮助信息 | 入门、学习命令 |
| `/btw` | 顺便问一个问题，不添加到上下文 | 快速岔开话题 |
| `/chrome` | 配置 Chrome 集成 | 浏览器自动化 |
| `/clear` | 清除对话历史 | 重新开始、减少上下文 |
| `/diff` | 交互式差异查看器 | 审查变更 |
| `/config` | 查看/编辑配置 | 自定义行为 |
| `/status` | 显示会话状态 | 检查当前状态 |
| `/agents` | 列出可用的代理 | 查看委派选项 |
| `/skills` | 列出可用的技能 | 查看自动调用能力 |
| `/hooks` | 列出已配置的钩子 | 调试自动化 |
| `/insights` | 分析会话模式 | 会话优化 |
| `/install-slack-app` | 安装 Claude Slack 应用 | Slack 集成 |
| `/keybindings` | 自定义键盘快捷键 | 快捷键自定义 |
| `/mcp` | 列出 MCP 服务器 | 检查外部集成 |
| `/memory` | 查看已加载的记忆文件 | 调试上下文加载 |
| `/mobile` | 生成移动端二维码 | 移动端访问 |
| `/passes` | 查看使用通行证 | 订阅信息 |
| `/plugin` | 管理插件 | 安装/卸载扩展 |
| `/plan` | 进入规划模式 | 复杂实现任务 |
| `/rewind` | 回退到检查点 | 撤销变更、探索替代方案 |
| `/checkpoint` | 管理检查点 | 保存/恢复状态 |
| `/cost` | 显示 Token 用量费用 | 监控支出 |
| `/context` | 显示上下文窗口使用情况 | 管理对话长度 |
| `/export` | 导出对话 | 保存以供参考 |
| `/extra-usage` | 配置额外用量限制 | 速率限制管理 |
| `/feedback` | 提交反馈或 Bug 报告 | 报告问题 |
| `/login` | 通过 Anthropic 验证身份 | 访问功能 |
| `/logout` | 登出 | 切换账号 |
| `/sandbox` | 切换沙箱模式 | 安全执行命令 |
| `/vim` | 切换 Vim 模式 | Vim 风格编辑 |
| `/doctor` | 运行诊断 | 故障排除 |
| `/reload-plugins` | 重载已安装的插件 | 插件管理 |
| `/release-notes` | 显示发布说明 | 检查新功能 |
| `/remote-control` | 启用远程控制 | 远程访问 |
| `/permissions` | 管理权限 | 控制访问 |
| `/session` | 管理会话 | 多会话工作流 |
| `/rename` | 重命名当前会话 | 整理会话 |
| `/resume` | 恢复之前的会话 | 继续工作 |
| `/todo` | 查看/管理待办列表 | 跟踪任务 |
| `/tasks` | 查看后台任务 | 监控异步操作 |
| `/copy` | 复制最后一条回复到剪贴板 | 快速分享输出 |
| `/teleport` | 将会话传输到另一台机器 | 远程继续工作 |
| `/desktop` | 打开 Claude 桌面应用 | 切换到桌面界面 |
| `/theme` | 更改颜色主题 | 自定义外观 |
| `/usage` | 显示 API 使用统计 | 监控配额和费用 |
| `/fork` | 分叉当前对话 | 探索替代方案 |
| `/stats` | 显示会话统计信息 | 审查会话指标 |
| `/statusline` | 配置状态栏 | 自定义状态显示 |
| `/stickers` | 查看会话贴纸 | 有趣的奖励 |
| `/fast` | 切换快速输出模式 | 加快响应速度 |
| `/terminal-setup` | 配置终端集成 | 设置终端功能 |
| `/upgrade` | 检查更新 | 版本管理 |

### 自定义命令（示例）

| 命令 | 说明 | 使用场景 | 作用域 | 安装方式 |
|---------|-------------|-------------|-------|--------------|
| `/optimize` | 分析代码优化点 | 性能改进 | 项目级 | `cp 01-slash-commands/optimize.md .claude/commands/` |
| `/pr` | 准备 Pull Request | 提交 PR 前 | 项目级 | `cp 01-slash-commands/pr.md .claude/commands/` |
| `/generate-api-docs` | 生成 API 文档 | 文档化 API | 项目级 | `cp 01-slash-commands/generate-api-docs.md .claude/commands/` |
| `/commit` | 创建带上下文的 Git 提交 | 提交变更 | 用户级 | `cp 01-slash-commands/commit.md .claude/commands/` |
| `/push-all` | 暂存、提交并推送 | 快速部署 | 用户级 | `cp 01-slash-commands/push-all.md .claude/commands/` |
| `/doc-refactor` | 重构文档结构 | 改进文档 | 项目级 | `cp 01-slash-commands/doc-refactor.md .claude/commands/` |
| `/setup-ci-cd` | 设置 CI/CD 流水线 | 新项目 | 项目级 | `cp 01-slash-commands/setup-ci-cd.md .claude/commands/` |
| `/unit-test-expand` | 扩展测试覆盖率 | 改进测试 | 项目级 | `cp 01-slash-commands/unit-test-expand.md .claude/commands/` |

> **作用域**：`User` = 个人工作流（`~/.claude/commands/`），`Project` = 团队共享（`.claude/commands/`）

**参考**：[01-slash-commands/](01-slash-commands/) | [官方文档](https://code.claude.com/docs/en/interactive-mode)

**快速安装（所有自定义命令）**：
```bash
cp 01-slash-commands/*.md .claude/commands/
```

---

## Permission Modes（权限模式）

Claude Code 支持 6 种权限模式，控制工具使用的授权方式。

| 模式 | 说明 | 使用场景 |
|------|-------------|-------------|
| `default` | 每次工具调用时提示确认 | 标准交互式使用 |
| `acceptEdits` | 自动接受文件编辑，其他操作仍需提示 | 可信的编辑工作流 |
| `plan` | 只读工具，不允许写入 | 规划和探索阶段 |
| `auto` | 无需提示接受所有工具 | 全自主运行（研究预览版） |
| `bypassPermissions` | 跳过所有权限检查 | CI/CD、无头环境 |
| `dontAsk` | 跳过需要权限的工具 | 非交互式脚本编程 |

> **注意**：`auto` 模式是研究预览功能（2026 年 3 月）。`bypassPermissions` 仅应在可信的沙箱环境中使用。

**参考**：[官方文档](https://code.claude.com/docs/en/permissions)

---

## Subagents（子代理）

具有隔离上下文、用于特定任务的专用 AI 助手。

### 内置子代理

| 代理 | 说明 | 工具 | 模型 | 使用场景 |
|-------|-------------|-------|-------|-------------|
| **general-purpose** | 多步骤任务、研究 | 所有工具 | 继承当前模型 | 复杂研究、多文件任务 |
| **Plan** | 实现规划 | Read, Glob, Grep, Bash | 继承当前模型 | 架构设计、规划 |
| **Explore** | 代码库探索 | Read, Glob, Grep | Haiku 4.5 | 快速搜索、理解代码 |
| **Bash** | 命令执行 | Bash | 继承当前模型 | Git 操作、终端任务 |
| **statusline-setup** | 状态栏配置 | Bash, Read, Write | Sonnet 4.6 | 配置状态栏显示 |
| **Claude Code Guide** | 帮助和文档 | Read, Glob, Grep | Haiku 4.5 | 获取帮助、学习功能 |

### 子代理配置字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `name` | string | 代理标识符 |
| `description` | string | 代理的功能描述 |
| `model` | string | 模型覆盖（如 `haiku-4.5`） |
| `tools` | array | 允许使用的工具列表 |
| `effort` | string | 推理努力级别（`low`、`medium`、`high`） |
| `initialPrompt` | string | 代理启动时注入的系统提示词 |
| `disallowedTools` | array | 明确禁止该代理使用的工具 |

### 自定义子代理（示例）

| 代理 | 说明 | 使用场景 | 作用域 | 安装方式 |
|-------|-------------|-------------|-------|--------------|
| `code-reviewer` | 全面代码质量审查 | 代码审查会话 | 项目级 | `cp 04-subagents/code-reviewer.md .claude/agents/` |
| `clean-code-reviewer` | Clean Code 原则审查 | 可维护性审查 | 项目级 | `cp 04-subagents/clean-code-reviewer.md .claude/agents/` |
| `test-engineer` | 测试策略与覆盖率 | 测试规划 | 项目级 | `cp 04-subagents/test-engineer.md .claude/agents/` |
| `documentation-writer` | 技术文档撰写 | API 文档、指南 | 项目级 | `cp 04-subagents/documentation-writer.md .claude/agents/` |
| `secure-reviewer` | 安全专项审查 | 安全审计 | 项目级 | `cp 04-subagents/secure-reviewer.md .claude/agents/` |
| `implementation-agent` | 完整功能实现 | 功能开发 | 项目级 | `cp 04-subagents/implementation-agent.md .claude/agents/` |
| `debugger` | 根因分析 | Bug 调查 | 用户级 | `cp 04-subagents/debugger.md .claude/agents/` |
| `data-scientist` | SQL 查询、数据分析 | 数据相关任务 | 用户级 | `cp 04-subagents/data-scientist.md .claude/agents/` |

> **作用域**：`User` = 个人（`~/.claude/agents/`），`Project` = 团队共享（`.claude/agents/`）

**参考**：[04-subagents/](04-subagents/) | [官方文档](https://code.claude.com/docs/en/sub-agents)

**快速安装（所有自定义代理）**：
```bash
cp 04-subagents/*.md .claude/agents/
```

---

## Skills（技能）

自动调用的能力，包含指令、脚本和模板。

### 示例技能

| 技能 | 说明 | 自动触发场景 | 作用域 | 安装方式 |
|-------|-------------|-------------------|-------|--------------|
| `code-review` | 全面代码审查 | "Review this code"、"Check quality" | 项目级 | `cp -r 03-skills/code-review .claude/skills/` |
| `brand-voice` | 品牌语调一致性检查 | 撰写营销文案 | 项目级 | `cp -r 03-skills/brand-voice .claude/skills/` |
| `doc-generator` | API 文档生成器 | "Generate docs"、"Document API" | 项目级 | `cp -r 03-skills/doc-generator .claude/skills/` |
| `refactor` | 系统化代码重构（Martin Fowler 方法） | "Refactor this"、"Clean up code" | 用户级 | `cp -r 03-skills/refactor ~/.claude/skills/` |

> **作用域**：`User` = 个人（`~/.claude/skills/`），`Project` = 团队共享（`.claude/skills/`）

### 技能结构

```
~/.claude/skills/skill-name/
├── SKILL.md          # 技能定义和指令
├── scripts/          # 辅助脚本
└── templates/        # 输出模板
```

### 技能 Frontmatter 字段

技能支持在 `SKILL.md` 中使用 YAML frontmatter 进行配置：

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `name` | string | 技能显示名称 |
| `description` | string | 技能的功能描述 |
| `autoInvoke` | array | 自动触发的触发短语 |
| `effort` | string | 推理努力级别（`low`、`medium`、`high`） |
| `shell` | string | 脚本使用的 Shell（`bash`、`zsh`、`sh`） |

**参考**：[03-skills/](03-skills/) | [官方文档](https://code.claude.com/docs/en/skills)

**快速安装（所有技能）**：
```bash
cp -r 03-skills/* ~/.claude/skills/
```

### 内置技能

| 技能 | 说明 | 自动触发场景 |
|-------|-------------|-------------------|
| `/simplify` | 代码质量审查 | 编写代码后 |
| `/batch` | 对多个文件运行 prompt | 批量操作 |
| `/debug` | 调试失败的测试/错误 | 调试会话 |
| `/loop` | 按间隔重复运行 prompt | 定时任务 |
| `/claude-api` | 使用 Claude API 构建应用 | API 开发 |

---

## Plugins（插件）

打包集合的 commands、agents、MCP servers 和 hooks。

### 示例插件

| 插件 | 说明 | 包含组件 | 使用场景 | 作用域 | 安装方式 |
|--------|-------------|------------|-------------|-------|--------------|
| `pr-review` | PR 审查工作流 | 3 个命令、3 个代理、GitHub MCP | 代码审查 | 项目级 | `/plugin install pr-review` |
| `devops-automation` | 部署与监控 | 4 个命令、3 个代理、K8s MCP | DevOps 任务 | 项目级 | `/plugin install devops-automation` |
| `documentation` | 文档生成套件 | 4 个命令、3 个代理、模板 | 文档编写 | 项目级 | `/plugin install documentation` |

> **作用域**：`Project` = 团队共享，`User` = 个人工作流

### 插件结构

```
.claude-plugin/
├── plugin.json       # 清单文件
├── commands/         # 斜杠命令
├── agents/           # 子代理
├── skills/           # 技能
├── mcp/              # MCP 配置
├── hooks/            # 钩子脚本
└── scripts/          # 工具脚本
```

**参考**：[07-plugins/](07-plugins/) | [官方文档](https://code.claude.com/docs/en/plugins)

**插件管理命令**：
```bash
/plugin list              # 列出已安装的插件
/plugin install <name>    # 安装插件
/plugin remove <name>     # 卸载插件
/plugin update <name>     # 更新插件
```

---

## MCP Servers（MCP 服务器）

用于外部工具和 API 访问的 Model Context Protocol（模型上下文协议）服务器。

### 常用 MCP 服务器

| 服务器 | 说明 | 使用场景 | 作用域 | 安装方式 |
|--------|-------------|-------------|-------|--------------|
| **GitHub** | PR 管理、Issue、代码 | GitHub 工作流 | 项目级 | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` |
| **Database** | SQL 查询、数据访问 | 数据库操作 | 项目级 | `claude mcp add db -- npx -y @modelcontextprotocol/server-postgres` |
| **Filesystem** | 高级文件操作 | 复杂文件任务 | 用户级 | `claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem` |
| **Slack** | 团队通信 | 通知、更新 | 项目级 | 在 settings 中配置 |
| **Google Docs** | 文档访问 | 文档编辑、审查 | 项目级 | 在 settings 中配置 |
| **Asana** | 项目管理 | 任务跟踪 | 项目级 | 在 settings 中配置 |
| **Stripe** | 支付数据 | 金融分析 | 项目级 | 在 settings 中配置 |
| **Memory** | 持久化记忆 | 跨会话回忆 | 用户级 | 在 settings 中配置 |
| **Context7** | 库文档 | 最新文档查询 | 内置 | 内置 |

> **作用域**：`Project` = 团队（`.mcp.json`），`User` = 个人（`~/.claude.json`），`Built-in` = 预装

### MCP 配置示例

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**参考**：[05-mcp/](05-mcp/) | [MCP 协议规范](https://modelcontextprotocol.io)

**快速安装（GitHub MCP）**：
```bash
export GITHUB_TOKEN="your_token" && claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

---

## Hooks（钩子）

响应 Claude Code 事件而自动执行 Shell 命令的事件驱动型自动化。

### 钩子事件

| 事件 | 说明 | 触发时机 | 使用场景 |
|-------|-------------|----------------|-----------|
| `SessionStart` | 会话开始/恢复 | 会话初始化 | 初始化任务 |
| `InstructionsLoaded` | 指令加载完成 | CLAUDE.md 或规则文件加载 | 自定义指令处理 |
| `UserPromptSubmit` | Prompt 处理前 | 用户发送消息 | 输入校验 |
| `PreToolUse` | 工具执行前 | 任何工具运行前 | 校验、日志记录 |
| `PermissionRequest` | 权限对话框显示 | 敏感操作前 | 自定义审批流程 |
| `PostToolUse` | 工具执行成功后 | 任何工具完成后 | 格式化、通知 |
| `PostToolUseFailure` | 工具执行失败后 | 工具出错后 | 错误处理、日志记录 |
| `Notification` | 发送通知时 | Claude 发送通知 | 外部告警 |
| `SubagentStart` | 子代理启动时 | 子代理任务开始 | 初始化子代理上下文 |
| `SubagentStop` | 子代理完成时 | 子代理任务完成 | 链式操作 |
| `Stop` | Claude 完成响应时 | 响应完成 | 清理、报告 |
| `StopFailure` | API 错误结束回合时 | API 错误发生 | 错误恢复、日志记录 |
| `TeammateIdle` | 团队代理空闲时 | 代理团队协调 | 分配工作 |
| `TaskCompleted` | 任务标记为完成时 | 任务完成 | 后续处理 |
| `TaskCreated` | 通过 TaskCreate 创建任务时 | 新任务创建 | 任务跟踪、日志记录 |
| `ConfigChange` | 配置更新时 | 设置修改 | 响应配置变更 |
| `CwdChanged` | 工作目录变更时 | 目录切换 | 目录特定的设置 |
| `FileChanged` | 监控文件变更时 | 文件修改 | 文件监控、重新构建 |
| `PreCompact` | 压缩操作前 | 上下文压缩 | 状态保留 |
| `PostCompact` | 压缩完成后 | 压缩完成 | 后续操作 |
| `WorktreeCreate` | Worktree 创建时 | Git worktree 创建 | 初始化 worktree 环境 |
| `WorktreeRemove` | Worktree 移除时 | Git worktree 移除 | 清理 worktree 资源 |
| `Elicitation` | MCP 服务器请求输入时 | MCP 请求输入 | 输入校验 |
| `ElicitationResult` | 用户响应请求时 | 用户响应 | 响应处理 |
| `SessionEnd` | 会话终止时 | 会话终止 | 清理、保存状态 |

### 示例钩子

| 钩子 | 说明 | 事件 | 作用域 | 安装方式 |
|------|-------------|-------|-------|--------------|
| `validate-bash.py` | 命令校验 | PreToolUse:Bash | 项目级 | `cp 06-hooks/validate-bash.py .claude/hooks/` |
| `security-scan.py` | 安全扫描 | PostToolUse:Write | 项目级 | `cp 06-hooks/security-scan.py .claude/hooks/` |
| `format-code.sh` | 自动格式化 | PostToolUse:Write | 用户级 | `cp 06-hooks/format-code.sh ~/.claude/hooks/` |
| `validate-prompt.py` | Prompt 校验 | UserPromptSubmit | 项目级 | `cp 06-hooks/validate-prompt.py .claude/hooks/` |
| `context-tracker.py` | Token 用量跟踪 | Stop | 用户级 | `cp 06-hooks/context-tracker.py ~/.claude/hooks/` |
| `pre-commit.sh` | 提交前校验 | PreToolUse:Bash | 项目级 | `cp 06-hooks/pre-commit.sh .claude/hooks/` |
| `log-bash.sh` | 命令日志记录 | PostToolUse:Bash | 用户级 | `cp 06-hooks/log-bash.sh ~/.claude/hooks/` |

> **作用域**：`Project` = 团队（`.claude/settings.json`），`User` = 个人（`~/.claude/settings.json`）

### 钩子配置

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "~/.claude/hooks/validate-bash.py"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "~/.claude/hooks/format-code.sh"
      }
    ]
  }
}
```

**参考**：[06-hooks/](06-hooks/) | [官方文档](https://code.claude.com/docs/en/hooks)

**快速安装（所有钩子）**：
```bash
mkdir -p ~/.claude/hooks && cp 06-hooks/*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh
```

---

## Memory Files（记忆文件）

跨会话自动加载的持久化上下文。

### 记忆类型

| 类型 | 位置 | 作用域 | 使用场景 |
|------|----------|-------|-------------|
| **Managed Policy（托管策略）** | 组织管理的策略 | 组织级别 | 强制执行组织范围内的标准 |
| **Project（项目记忆）** | `./CLAUDE.md` | 项目（团队） | 团队规范、项目上下文 |
| **Project Rules（项目规则）** | `.claude/rules/` | 项目（团队） | 模块化的项目规则 |
| **User（用户记忆）** | `~/.claude/CLAUDE.md` | 用户（个人） | 个人偏好 |
| **User Rules（用户规则）** | `~/.claude/rules/` | 用户（个人） | 模块化的个人规则 |
| **Local（本地记忆）** | `./CLAUDE.local.md` | 本地（git 忽略） | 机器特定的覆盖配置（截至 2026 年 3 月官方文档未提及；可能是遗留功能） |
| **Auto Memory（自动记忆）** | 自动 | 会话 | 自动捕获的经验和修正 |

> **作用域**：`Organization` = 管理员管理，`Project` = 通过 git 与团队共享，`User` = 个人偏好，`Local` = 不提交，`Session` = 自动管理

**参考**：[02-memory/](02-memory/) | [官方文档](https://code.claude.com/docs/en/memory)

**快速安装**：
```bash
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

---

## 新功能（2026 年 3 月）

| 功能 | 说明 | 如何使用 |
|---------|-------------|------------|
| **Remote Control（远程控制）** | 通过 API 远程控制 Claude Code 会话 | 使用远程控制 API 以编程方式发送 prompt 并接收响应 |
| **Web Sessions（Web 会话）** | 在浏览器环境中运行 Claude Code | 通过 `claude web` 或 Anthropic Console 访问 |
| **Desktop App（桌面应用）** | Claude Code 原生桌面应用程序 | 使用 `/desktop` 或从 Anthropic 网站下载 |
| **Agent Teams（代理团队）** | 协调多个代理处理相关任务 | 配置协作并共享上下文的队友代理 |
| **Task List（任务列表）** | 后台任务管理与监控 | 使用 `/tasks` 查看和管理后台操作 |
| **Prompt Suggestions（建议提示）** | 基于上下文的命令建议 | 根据当前上下文自动出现建议 |
| **Git Worktrees** | 用于并行开发的隔离 Git worktree | 使用 worktree 命令进行安全的并行分支工作 |
| **Sandboxing（沙箱）** | 用于安全隔离的执行环境 | 使用 `/sandbox` 切换；在受限环境中运行命令 |
| **MCP OAuth** | MCP 服务器的 OAuth 认证 | 在 MCP 服务器设置中配置 OAuth 凭证以实现安全访问 |
| **MCP Tool Search（MCP 工具搜索）** | 动态搜索和发现 MCP 工具 | 使用工具搜索在已连接的服务器中查找可用的 MCP 工具 |
| **Scheduled Tasks（定时任务）** | 使用 `/loop` 和 cron 工具设置定期任务 | 使用 `/loop 5m /command` 或 CronCreate 工具 |
| **Chrome Integration（Chrome 集成）** | 使用无头 Chromium 的浏览器自动化 | 使用 `--chrome` 标志或 `/chrome` 命令 |
| **Keyboard Customization（键盘自定义）** | 自定义快捷键（包括组合键支持） | 使用 `/keybindings` 或编辑 `~/.claude/keybindings.json` |
| **Auto Mode（自动模式）** | 无需权限提示的全自主运行（研究预览版） | 使用 `--mode auto` 或 `/permissions auto`；2026 年 3 月 |
| **Channels（频道）** | 多频道通信（Telegram、Slack 等）（研究预览版） | 配置频道插件；2026 年 3 月 |
| **Voice Dictation（语音听写）** | Prompt 的语音输入 | 使用麦克风图标或语音快捷键 |
| **Agent Hook Type（代理钩子类型）** | 生成子代理而非运行 Shell 命令的钩子 | 在钩子配置中设置 `"type": "agent"` |
| **Prompt Hook Type（提示钩子类型）** | 向对话注入提示文本的钩子 | 在钩子配置中设置 `"type": "prompt"` |
| **MCP Elicitation（MCP 请求输入）** | MCP 服务器可在工具执行期间请求用户输入 | 通过 `Elicitation` 和 `ElicitationResult` 钩子事件处理 |
| **WebSocket MCP Transport** | 基于 WebSocket 的 MCP 服务器连接传输 | 在 MCP 服务器配置中使用 `"transport": "websocket"` |
| **Plugin LSP Support（插件 LSP 支持）** | 通过插件集成 Language Server Protocol | 在 `plugin.json` 中配置 LSP 服务器以获得编辑器功能 |
| **Managed Drop-ins（托管扩展配置）** | 组织管理的扩展配置（v2.1.83） | 通过托管策略由管理员配置；自动应用于所有用户 |

---

## 快速参考矩阵

### 功能选择指南

| 需求 | 推荐功能 | 原因 |
|------|---------------------|-----|
| 快捷操作 | Slash Command（斜杠命令） | 手动触发、即时生效 |
| 持久化上下文 | Memory（记忆） | 自动加载 |
| 复杂自动化 | Skill（技能） | 自动调用 |
| 专业化任务 | Subagent（子代理） | 隔离上下文 |
| 外部数据 | MCP Server（MCP 服务器） | 实时访问 |
| 事件自动化 | Hook（钩子） | 事件触发 |
| 完整解决方案 | Plugin（插件） | 一站式打包 |

### 安装优先级

| 优先级 | 功能 | 命令 |
|----------|---------|---------|
| 1. 核心 | Memory（记忆） | `cp 02-memory/project-CLAUDE.md ./CLAUDE.md` |
| 2. 日常使用 | Slash Commands（斜杠命令） | `cp 01-slash-commands/*.md .claude/commands/` |
| 3. 质量 | Subagents（子代理） | `cp 04-subagents/*.md .claude/agents/` |
| 4. 自动化 | Hooks（钩子） | `cp 06-hooks/*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh` |
| 5. 外部集成 | MCP | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` |
| 6. 高级 | Skills（技能） | `cp -r 03-skills/* ~/.claude/skills/` |
| 7. 完整方案 | Plugins（插件） | `/plugin install pr-review` |

---

## 一键完整安装

安装本仓库中的所有示例：

```bash
# 创建目录
mkdir -p .claude/{commands,agents,skills} ~/.claude/{hooks,skills}

# 安装所有功能
cp 01-slash-commands/*.md .claude/commands/ && \
cp 02-memory/project-CLAUDE.md ./CLAUDE.md && \
cp -r 03-skills/* ~/.claude/skills/ && \
cp 04-subagents/*.md .claude/agents/ && \
cp 06-hooks/*.sh ~/.claude/hooks/ && \
chmod +x ~/.claude/hooks/*.sh
```

---

## 补充资源

- [Claude Code 官方文档](https://code.claude.com/docs/en/overview)
- [MCP 协议规范](https://modelcontextprotocol.io)
- [学习路线图](LEARNING-ROADMAP.md)
- [主 README](README.md)

---

**最后更新**：2026 年 3 月
