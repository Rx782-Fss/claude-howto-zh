<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Hooks(钩子)

Hooks 是在 Claude Code 会话期间响应特定事件而自动执行的自动化脚本。它们实现了自动化、验证、权限管理和自定义工作流。

## 概览

Hooks 是在 Claude Code 中发生特定事件时自动执行的自动化操作(Shell 命令、HTTP Webhook、LLM 提示词或子代理评估)。它们接收 JSON 格式的输入,并通过退出码和 JSON 输出来返回结果。

**核心特性**:
- 事件驱动型自动化
- 基于 JSON 的输入/输出
- 支持 command(命令)、prompt(提示)、HTTP(网络请求)和 agent(子代理)四种钩子类型
- 支持针对特定工具的模式匹配

## 配置位置

Hooks 在以下设置文件中进行配置:

- `~/.claude/settings.json` -- 用户设置(所有项目)
- `.claude/settings.json` -- 项目设置(可共享,提交到 git)
- `.claude/settings.local.json` -- 本地项目设置(不提交)
- 托管策略 -- 组织范围的设置
- Plugin `hooks/hooks.json` -- 插件作用域的钩子
- Skill/Agent frontmatter -- 组件生命周期的钩子

## 基本配置结构

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**关键字段说明**:

| 字段 | 说明 | 示例 |
|------|--------|------|
| `matcher` | 匹配工具名称的模式(区分大小写) | `"Write"`、`"Edit\|Write"`、`"*"` |
| `hooks` | 钩子定义数组 | `[{ "type": "command", ... }]` |
| `type` | 钩子类型:`"command"`(Shell)、`"prompt"`(LLM)、`"http"`(Webhook)、`"agent"`(子代理) | `"command"` |
| `command` | 要执行的 Shell 命令 | `"$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"` |
| `timeout` | 可选的超时时间(秒),默认 60 | `30` |
| `once` | 如果为 `true`,每会话仅运行一次 | `true` |

## Matcher 匹配模式

| 模式 | 说明 | 示例 |
|------|--------|------|
| 精确匹配 | 匹配特定工具 | `"Write"` |
| 正则表达式 | 匹配多个工具 | `"Edit\|Write"` |
| 通配符 | 匹配所有工具 | `"*"` 或 `""` |
| MCP 工具 | 服务器+工具模式 | `"mcp__memory__.*"` |

## 四种钩子类型

### 1. Command Hooks(命令钩子)-- 默认类型

执行 Shell 命令,通过 JSON stdin/stdout 和退出码进行通信。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

### 2. Prompt Hooks(提示钩子)

向对话注入 LLM 提示文本。

### 3. HTTP Hooks(网络钩子)

向外部 URL 发送 HTTP 请求。

### 4. Agent Hooks(代理钩子)

生成子代理而非运行 Shell 命令。

## 25 种 Hook 事件

### Tool Hooks(工具钩子)
| 事件 | 触发时机 |
|------|----------|
| `PreToolUse` | 工具执行前 |
| `PostToolUse` | 工具执行成功后 |
| `PostToolUseFailure` | 工具执行失败后 |
| `PermissionRequest` | 权限对话框显示时 |

### Session Hooks(会话钩子)
| 事件 | 触发时机 |
|------|----------|
| `SessionStart` | 会话开始/恢复时 |
| `SessionEnd` | 会话终止时 |
| `Stop` | Claude 完成响应时 |
| `StopFailure` | API 错误结束回合时 |
| `SubagentStart` | 子代理启动时 |
| `SubagentStop` | 子代理完成时 |

### Task Hooks(任务钩子)
| 事件 | 触发时机 |
|------|----------|
| `UserPromptSubmit` | 用户提交 prompt 时 |
| `TaskCompleted` | 任务完成时 |
| `TaskCreated` | 通过 TaskCreate 创建任务时 |
| `TeammateIdle` | 团队代理空闲时 |

### Lifecycle Hooks(生命周期钩子)
| 事件 | 触发时机 |
|------|----------|
| `ConfigChange` | 配置更新时 |
| `CwdChanged` | 工作目录变更时 |
| `FileChanged` | 监控文件变更时 |
| `PreCompact` | 上下文压缩前 |
| `PostCompact` | 上下文压缩完成后 |
| `WorktreeCreate` | Worktree 创建时 |
| `WorktreeRemove` | Worktree 移除时 |
| `Notification` | 发送通知时 |
| `InstructionsLoaded` | CLAUDE.md 加载完成时 |
| `Elicitation` | MCP 请求输入时 |
| `ElicitationResult` | 用户响应请求时 |

## 最佳实践

✅ **推荐做法**:
- 使用 PreToolUse 进行输入验证和安全检查
- 使用 PostToolUse 进行格式化和通知
- 为长时间运行的钩子设置合理的超时时间
- 使用 `once: true` 避免重复执行初始化逻辑

❌ **避免事项**:
- 不要在关键路径上阻塞式运行耗时操作
- 不要忽略错误处理----始终检查退出码
- 不要在钩子中硬编码路径----使用环境变量

> 💡 **中文开发者提示**:Hooks 是实现团队代码质量门禁的核心机制。最实用的组合是:PreToolUse:Bash + validate-bash.py(防止危险命令)+ PostToolUse:Write + format-code.sh(自动格式化)。建议从这两个钩子开始搭建你团队的自动化体系。

---

**最后更新**:2026 年 3 月
