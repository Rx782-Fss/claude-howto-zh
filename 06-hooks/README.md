<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# 钩子（Hooks）

钩子是在 Claude Code 会话期间响应特定事件而自动执行的脚本。它们支持自动化、验证、权限管理和自定义工作流程。

## 概述

钩子是自动化操作（Shell 命令、HTTP Webhook、LLM 提示词、MCP 工具调用或子代理评估），当 Claude Code 中发生特定事件时自动执行。它们接收 JSON 输入，并通过退出码和 JSON 输出传递结果。

**核心特性：**
- 事件驱动的自动化
- 基于 JSON 的输入/输出
- 支持 `command`（命令）、`http`（HTTP）、`mcp_tool`（MCP 工具）、`prompt`（提示词）和 `agent`（代理）五种钩子类型
- 支持工具特定的模式匹配

## 配置

钩子在设置文件中通过特定结构进行配置：

- `~/.claude/settings.json` - 用户设置（适用于所有项目）
- `.claude/settings.json` - 项目设置（可共享，可提交）
- `.claude/settings.local.json` - 本地项目设置（不提交）
- 托管策略 - 组织范围的设置
- 插件 `hooks/hooks.json` - 插件作用域的钩子
- 技能/代理 frontmatter - 组件生命周期的钩子

### 基本配置结构

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

**关键字段：**

| 字段 | 描述 | 示例 |
|------|------|------|
| `matcher` | 匹配工具名称的模式（区分大小写） | `"Write"`, `"Edit\|Write"`, `"*"` |
| `hooks` | 钩子定义数组 | `[{ "type": "command", ... }]` |
| `type` | 钩子类型：`"command"` (bash)、`"prompt"` (LLM)、`"http"` (webhook)、`"mcp_tool"` (MCP 工具调用, v2.1.118+) 或 `"agent"` (子代理) | `"command"` |
| `command` | 要执行的 Shell 命令 | `"$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"` |
| `timeout` | 可选的超时时间（秒）（默认 60） | `30` |
| `once` | 如果为 `true`，每个会话只运行一次该钩子 | `true` |

### 匹配器模式

| 模式 | 描述 | 示例 |
|------|------|------|
| 精确字符串 | 匹配特定工具 | `"Write"` |
| 正则表达式模式 | 匹配多个工具 | `"Edit\|Write"` |
| 通配符 | 匹配所有工具 | `"*"` 或 `""` |
| MCP 工具 | 服务器和工具模式 | `"mcp__memory__.*"` |

**InstructionsLoaded 匹配器值：**

| 匹配器值 | 描述 |
|-----------|------|
| `session_start` | 在会话启动时加载的指令 |
| `nested_traversal` | 在嵌套目录遍历时加载的指令 |
| `path_glob_match` | 通过路径 glob 模式匹配加载的指令 |

## 钩子类型

Claude Code 支持五种钩子类型：

### 命令钩子（Command Hooks）

默认的钩子类型。执行 Shell 命令，并通过 JSON stdin/stdout 和退出码进行通信。

```json
{
  "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py\"",
  "timeout": 60
}
```

### HTTP 钩子（HTTP Hooks）

> 添加于 v2.1.63。

远程 Webhook 端点，接收与命令钩子相同的 JSON 输入。HTTP 钩子向 URL POST JSON 并接收 JSON 响应。当启用沙箱隔离时，HTTP 钩子会通过沙箱路由。URL 中的环境变量插值需要显式的 `allowedEnvVars` 列表以确保安全性。

```json
{
  "hooks": {
    "PostToolUse": [{
      "type": "http",
      "url": "https://my-webhook.example.com/hook",
      "matcher": "Write"
    }]
  }
}
```

**关键属性：**
- `"type": "http"` -- 标识这是一个 HTTP 钩子
- `"url"` -- Webhook 端点的 URL
- 当启用沙箱时会通过沙箱路由
- URL 中的任何环境变量插值都需要显式的 `allowedEnvVars` 列表

### 提示词钩子（Prompt Hooks）

LLM 评估的提示词，其中钩子内容是 Claude 评估的提示词。主要与 `Stop` 和 `SubagentStop` 事件一起使用，用于智能任务完成检查。

```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude completed all requested tasks.",
  "timeout": 30
}
```

LLM 评估提示词并返回结构化决策（详见[基于提示词的钩子](#基于提示词的钩子)部分）。

### MCP 工具钩子（MCP Tool Hooks）

> 添加于 v2.1.118。

`mcp_tool` 类型直接调用已配置的 MCP 工具；配置引用的是 MCP 服务器和工具名称，而不是 Shell 命令或 URL。当验证或反应逻辑已经存在于您已配置的 MCP 服务器中时，这非常有用。

```json
{
  "matcher": "Edit",
  "hooks": [{
    "type": "mcp_tool",
    "server": "my-mcp-server",
    "tool": "validate_edit"
  }]
}
```

**关键属性：**
- `"type": "mcp_tool"` -- 标识这是一个 MCP 工具钩子
- `"server"` -- 已配置的 MCP 服务器名称
- `"tool"` -- 该服务器上要调用的工具名称

钩子输入（工具名称、工具输入、会话上下文）作为 MCP 工具的参数传递。有关配置 MCP 服务器的信息，请参阅 [MCP 服务器设置](../05-mcp/README.md)。

### 代理钩子（Agent Hooks）

基于子代理的验证钩子，生成专门的代理来评估条件或执行复杂检查。与提示词钩子（单轮 LLM 评估）不同，代理钩子可以使用工具并执行多步推理。

```json
{
  "type": "agent",
  "prompt": "Verify the code changes follow our architecture guidelines. Check the relevant design docs and compare.",
  "timeout": 120
}
```

**关键属性：**
- `"type": "agent"` -- 标识这是一个代理钩子
- `"prompt"` -- 子代理的任务描述
- 代理可以使用工具（Read、Grep、Bash 等）来执行其评估
- 返回与提示词钩子类似的结构化决策

## 钩子事件

Claude Code 支持 **28 个钩子事件**：

| 事件 | 触发时机 | 匹配器输入 | 可阻塞 | 常见用途 |
|------|----------|------------|--------|----------|
| **SessionStart** | 会话开始/恢复/清除/压缩 | startup/resume/clear/compact | 否 | 环境设置 |
| **InstructionsLoaded** | 加载 CLAUDE.md 或规则文件后 | (无) | 否 | 修改/过滤指令 |
| **UserPromptSubmit** | 用户提交提示词 | (无) 是 | 验证提示词 |
| **UserPromptExpansion** | 用户提示词被扩展后（例如 `@` 提及、斜杠命令解析） | (无) | 是 | 转换或检查扩展后的提示词 |
| **PreToolUse** | 工具执行前 | 工具名称 | 是（允许/拒绝/询问） | 验证、修改输入 |
| **PermissionRequest** | 显示权限对话框 | 工具名称 | 是 | 自动批准/拒绝 |
| **PermissionDenied** | 用户拒绝权限提示 | 工具名称 | 否 | 日志记录、分析、策略执行 |
| **PostToolUse** | 工具成功后 | 工具名称 | 否 | 添加上下文、反馈 |
| **PostToolUseFailure** | 工具执行失败 | 工具名称 | 否 | 错误处理、日志记录 |
| **PostToolBatch** | 一批工具使用完成后 | (无) | 否 | 聚合报告、批量验证 |
| **Notification** | 发送通知 | 通知类型 | 否 | 自定义通知 |
| **SubagentStart** | 子代理启动 | 代理类型名称 | 否 | 子代理设置 |
| **SubagentStop** | 子代理完成 | 代理类型名称 | 是 | 子代理验证 |
| **Stop** | Claude 完成响应 | (无) | 是 | 任务完成检查 |
| **StopFailure** | API 错误结束回合 | (无) | 否 | 错误恢复、日志记录 |
| **TeammateIdle** | 代理团队成员空闲 | (无) | 是 | 团队成员协调 |
| **TaskCompleted** | 任务标记为完成 | (无) | 是 | 任务后操作 |
| **TaskCreated** | 通过 TaskCreate 创建任务 | (无) | 否 | 任务跟踪、日志记录 |
| **ConfigChange** | 配置文件更改 | (无) | 是（除策略外） | 对配置更新做出反应 |
| **CwdChanged** | 工作目录更改 | (无) | 否 | 目录特定设置 |
| **FileChanged** | 监视的文件更改 | (无) | 否 | 文件监控、重新构建 |
| **PreCompact** | 上下文压缩前 | 手动/自动 | 否 | 压缩前操作 |
| **PostCompact** | 压缩完成后 | (无) | 否 | 压缩后操作 |
| **WorktreeCreate** | 正在创建工作树 | (无) | 是（路径返回） | 工作树初始化 |
| **WorktreeRemove** | 正在移除工作树 | (无) | 否 | 工作树清理 |
| **Elicitation** | MCP 服务器请求用户输入 | (无) | 是 | 输入验证 |
| **ElicitationResult** | 用户响应请求 | (无) | 是 | 响应处理 |
| **SessionEnd** | 会话终止 | (无) | 否 | 清理、最终日志记录 |

> **PostToolUse 时长（v2.1.119）：** `PostToolUse` 和 `PostToolUseFailure` 钩子输入现在包含 `duration_ms` — 详见 [PostToolUse](#posttooluse) 部分。

### PreToolUse

在 Claude 创建工具参数之后、处理之前运行。用于验证或修改工具输入。

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ]
  }
}
```

**常用匹配器：** `Task`、`Bash`、`Glob`、`Grep`、`Read`、`Edit`、`Write`、`WebFetch`、`WebSearch`

**输出控制：**
- `permissionDecision`: `"allow"`、`"deny"` 或 `"ask"`
- `permissionDecisionReason`: 决策原因说明
- `updatedInput`: 修改后的工具输入参数

### PostToolUse

在工具完成后立即运行。用于验证、日志记录或向 Claude 提供上下文。

**配置：**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-scan.py"
          }
        ]
      }
    ]
  }
}
```

**输出控制：**
- `"block"` 决策向 Claude 提供反馈提示
- `additionalContext`: 为 Claude 添加的上下文

**附加输入字段（v2.1.119）：**

| 字段 | 类型 | 描述 |
|------|------|------|
| `duration_ms` | number | 工具执行时间（毫秒）。不包括权限提示和 PreToolUse 钩子执行所花费的时间。在 `PostToolUse` 和 `PostToolUseFailure` 钩子上均可用。 |

### UserPromptSubmit

当用户提交提示词时运行，在 Claude 处理之前。

**配置：**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-prompt.py"
          }
        ]
      }
    ]
  }
}
```

**输出控制：**
- `decision`: `"block"` 以阻止处理
- `reason`: 如果被阻止的原因说明
- `additionalContext`: 添加到提示词的上下文

### Stop 和 SubagentStop

当 Claude 完成响应（Stop）或子代理完成（SubagentStop）时运行。支持基于提示词的评估，用于智能任务完成检查。

**附加输入字段：** `Stop` 和 `SubagentStop` 钩子都会在其 JSON 输入中接收一个 `last_assistant_message` 字段，包含 Claude 或子代理在停止前的最后一条消息。这对于评估任务完成情况很有用。

**配置：**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude completed all requested tasks.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### SubagentStart

当子代理开始执行时运行。匹配器输入是代理类型名称，允许钩子针对特定的子代理类型。

**配置：**
```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "code-review",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/subagent-init.sh"
          }
        ]
      }
    ]
  }
}
```

### SessionStart

当会话启动或恢复时运行。可以持久化环境变量。

**匹配器：** `startup`、`resume`、`clear`、`compact`

**特殊功能：** 使用 `CLAUDE_ENV_FILE` 来持久化环境变量（在 `CwdChanged` 和 `FileChanged` 钩子中也可用）：

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

### SessionEnd

当会话结束时运行，以执行清理或最终日志记录。不能阻止终止。

**原因字段值：**
- `clear` - 用户清除了会话
- `logout` - 用户注销登录
- `prompt_input_exit` - 用户通过提示词输入退出
- `other` - 其他原因

**配置：**
```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-cleanup.sh\""
          }
        ]
      }
    ]
  }
}
```

### Notification Event

通知事件的更新匹配器：
- `permission_prompt` - 权限请求通知
- `idle_prompt` - 空闲状态通知
- `auth_success` - 认证成功
- `elicitation_dialog` - 向用户显示的对话框

## 组件作用域钩子

钩子可以附加到特定组件（技能、代理、命令）的 frontmatter 中：

**在 SKILL.md、agent.md 或 command.md 中：**

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true  # 每个会话只运行一次
---
```

**组件钩子支持的事件：** `PreToolUse`、`PostToolUse`、`Stop`

这允许直接在使用它们的组件中定义钩子，将相关代码保持在一起。

### 子代理 Frontmatter 中的钩子

当在子代理的 frontmatter 中定义了 `Stop` 钩子时，它会自动转换为针对该子代理的作用域的 `SubagentStop` 钩子。这确保 Stop 钩子仅在该特定子代理完成时触发，而不是在主会话停止时触发。

```yaml
---
name: code-review-agent
description: Automated code review subagent
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "Verify the code review is thorough and complete."
  # 上面的 Stop 钩子会自动转换为此子代理的 SubagentStop
---
```

## PermissionRequest 事件

使用自定义输出格式处理权限请求：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {},
      "message": "Custom message",
      "interrupt": false
    }
  }
}
```

## 钩子输入和输出

### JSON 输入（通过 stdin）

所有钩子都通过 stdin 接收 JSON 输入：

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.js",
    "content": "..."
  },
  "tool_use_id": "toolu_01ABC123...",
  "agent_id": "agent-abc123",
  "agent_type": "main",
  "worktree": "/path/to/worktree"
}
```

**常用字段：**

| 字段 | 描述 |
|------|------|
| `session_id` | 唯一会话标识符 |
| `transcript_path` | 对话转录文件路径 |
| `cwd` | 当前工作目录 |
| `hook_event_name` | 触发钩子的事件名称 |
| `agent_id` | 运行此钩子的代理标识符 |
| `agent_type` | 代理类型（`"main"`、子代理类型名称等） |
| `worktree` | Git 工作树路径（如果代理在工作树中运行） |

### 退出码

| 退出码 | 含义 | 行为 |
|--------|------|------|
| **0** | 成功 | 继续，解析 JSON stdout |
| **2** | 阻塞错误 | 阻止操作，stderr 显示为错误 |
| **其他** | 非阻塞错误 | 继续，stderr 在详细模式下显示 |

### JSON 输出（stdout，退出码 0）

```json
{
  "continue": true,
  "stopReason": "Optional message if stopping",
  "suppressOutput": false,
  "systemMessage": "Optional warning message",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "File is in allowed directory",
    "updatedInput": {
      "file_path": "/modified/path.js"
    }
  }
}
```

## 环境变量

| 变量 | 可用性 | 描述 |
|------|--------|------|
| `CLAUDE_PROJECT_DIR` | 所有钩子 | 项目根目录的绝对路径 |
| `CLAUDE_ENV_FILE` | SessionStart、CwdChanged、FileChanged | 用于持久化环境变量的文件路径 |
| `CLAUDE_CODE_REMOTE` | 所有钩子 | 如果在远程环境中运行则为 `"true"` |
| `${CLAUDE_PLUGIN_ROOT}` | 插件钩子 | 插件目录路径 |
| `${CLAUDE_PLUGIN_DATA}` | 插件钩子 | 插件数据目录路径 |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | SessionEnd 钩子 | SessionEnd 钩子的可配置超时时间（毫秒）（覆盖默认值） |

## 基于提示词的钩子

对于 `Stop` 和 `SubagentStop` 事件，可以使用基于 LLM 的评估：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review if all tasks are complete. Return your decision.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**LLM 响应模式：**
```json
{
  "decision": "approve",
  "reason": "All tasks completed successfully",
  "continue": false,
  "stopReason": "Task complete"
}
```

## 示例

### 示例 1：Bash 命令验证器（PreToolUse）

**文件：** `.claude/hooks/validate-bash.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED_PATTERNS = [
    (r"\brm\s+-rf\s+/", "Blocking dangerous rm -rf / command"),
    (r"\bsudo\s+rm", "Blocking sudo rm command"),
]

def main():
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = input_data.get("tool_input", {}).get("command", "")

    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            print(message, file=sys.stderr)
            sys.exit(2)  # 退出码 2 = 阻塞错误

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\""
          }
        ]
      }
    ]
  }
}
```

### 示例 2：安全扫描器（PostToolUse）

**文件：** `.claude/hooks/security-scan.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

SECRET_PATTERNS = [
    (r"password\s*=\s*['\"][^'\"]+['\"]", "Potential hardcoded password"),
    (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Potential hardcoded API key"),
]

def main():
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    content = tool_input.get("content", "") or tool_input.get("new_string", "")
    file_path = tool_input.get("file_path", "")

    warnings = []
    for pattern, message in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            warnings.append(message)

    if warnings:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"Security warnings for {file_path}: " + "; ".join(warnings)
            }
        }
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 示例 3：自动格式化代码（PostToolUse）

**文件：** `.claude/hooks/format-code.sh`

```bash
#!/bin/bash

# 从 stdin 读取 JSON
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_name', ''))")
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('file_path', ''))")

if [ "$TOOL_NAME" != "Write" ] && [ "$TOOL_NAME" != "Edit" ]; then
  exit 0
fi

# 根据文件扩展名进行格式化
case "$FILE_PATH" in
    *.js|*.jsx|*.ts|*.tsx|*.json)
        command -v prettier &>/dev/null && prettier --write "$FILE_PATH" 2>/dev/null
        ;;
    *.py)
        command -v black &>/dev/null && black "$FILE_PATH" 2>/dev/null
        ;;
    *.go)
        command -v gofmt &>/dev/null && gofmt -w "$FILE_PATH" 2>/dev/null
        ;;
esac

exit 0
```

### 示例 4：提示词验证器（UserPromptSubmit）

**文件：** `.claude/hooks/validate-prompt.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED_PATTERNS = [
    (r"delete\s+(all\s+)?database", "Dangerous: database deletion"),
    (r"rm\s+-rf\s+/", "Dangerous: root deletion"),
]

def main():
    input_data = json.load(sys.stdin)
    prompt = input_data.get("user_prompt", "") or input_data.get("prompt", "")

    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            output = {
                "decision": "block",
                "reason": f"Blocked: {message}"
            }
            print(json.dumps(output))
            sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 示例 5：智能停止钩子（基于提示词）

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review if Claude completed all requested tasks. Check: 1) Were all files created/modified? 2) Were there unresolved errors? If incomplete, explain what's missing.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 示例 6：上下文使用跟踪器（钩子对）

使用 `UserPromptSubmit`（消息前）和 `Stop`（响应后）钩子一起跟踪每次请求的 Token 消耗量。

**文件：** `.claude/hooks/context-tracker.py`

```python
#!/usr/bin/env python3
"""
上下文使用跟踪器 - 跟踪每次请求的 Token 消耗量。

使用 UserPromptSubmit 作为"消息前"钩子和 Stop 作为"响应后"钩子
来计算每次请求的 Token 使用增量。

Token 计数方法：
1. 字符估算（默认）：约每 4 个字符 1 个 Token，无依赖
2. tiktoken（可选）：更准确（~90-95%），需要：pip install tiktoken
"""
import json
import os
import sys
import tempfile

# 配置
CONTEXT_LIMIT = 128000  # Claude 的上下文窗口（根据您的模型调整）
USE_TIKTOKEN = False    # 如果安装了 tiktoken 则设为 True 以获得更好的准确性


def get_state_file(session_id: str) -> str:
    """获取用于存储消息前 Token 计数的临时文件路径，按会话隔离。"""
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")


def count_tokens(text: str) -> int:
    """
    统计文本中的 Token 数。

    如果可用，使用 tiktoken 的 p50k_base 编码（~90-95% 准确率），
    否则回退到字符估算（~80-90% 准确率）。
    """
    if USE_TIKTOKEN:
        try:
            import tiktoken
            enc = tiktoken.get_encoding("p50k_base")
            return len(enc.encode(text))
        except ImportError:
            pass  # 回退到估算

    # 基于字符的估算：英文约每 4 个字符 1 个 Token
    return len(text) // 4


def read_transcript(transcript_path: str) -> str:
    """读取并连接转录文件中的所有内容。"""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    content = []
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                # 从各种消息格式中提取文本内容
                if "message" in entry:
                    msg = entry["message"]
                    if isinstance(msg.get("content"), str):
                        content.append(msg["content"])
                    elif isinstance(msg.get("content"), list):
                        for block in msg["content"]:
                            if isinstance(block, dict) and block.get("type") == "text":
                                content.append(block.get("text", ""))
            except json.JSONDecodeError:
                continue

    return "\n".join(content)


def handle_user_prompt_submit(data: dict) -> None:
    """消息前钩子：在请求前保存当前 Token 计数。"""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 保存到临时文件以便后续比较
    state_file = get_state_file(session_id)
    with open(state_file, "w") as f:
        json.dump({"pre_tokens": current_tokens}, f)


def handle_stop(data: dict) -> None:
    """响应后钩子：计算并报告 Token 增量。"""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 加载消息前计数
    state_file = get_state_file(session_id)
    pre_tokens = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
                pre_tokens = state.get("pre_tokens", 0)
        except (json.JSONDecodeError, IOError):
            pass

    # 计算增量
    delta_tokens = current_tokens - pre_tokens
    remaining = CONTEXT_LIMIT - current_tokens
    percentage = (current_tokens / CONTEXT_LIMIT) * 100

    # 报告使用情况
    method = "tiktoken" if USE_TIKTOKEN else "estimated"
    print(f"Context ({method}): ~{current_tokens:,} tokens ({percentage:.1f}% used, ~{remaining:,} remaining)", file=sys.stderr)
    if delta_tokens > 0:
        print(f"This request: ~{delta_tokens:,} tokens", file=sys.stderr)


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        handle_user_prompt_submit(data)
    elif event == "Stop":
        handle_stop(data)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

**配置：**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-tracker.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-tracker.py\""
          }
        ]
      }
    ]
  }
}
```

**工作原理：**
1. `UserPromptSubmit` 在您的提示词被处理之前触发 — 保存当前 Token 计数
2. `Stop` 在 Claude 响应后触发 — 计算增量并报告使用情况
3. 每个会话通过临时文件名中的 `session_id` 进行隔离

**Token 计数方法：**

| 方法 | 准确率 | 依赖项 | 速度 |
|------|--------|--------|------|
| 字符估算 | ~80-90% | 无 | <1ms |
| tiktoken (p50k_base) | ~90-95% | `pip install tiktoken` | <10ms |

> **注意：** Anthropic 尚未发布官方的离线分词器。两种方法都是近似值。转录内容包括用户提示词、Claude 的响应和工具输出，但不包括系统提示词或内部上下文。

### 示例 7：种子自动模式权限（一次性设置脚本）

一次性设置脚本，向 `~/.claude/settings.json` 种植约 67 条安全权限规则，相当于 Claude Code 的自动模式基线 — 不需要任何钩子，不需要记住未来的选择。只需运行一次；可以安全地重复运行（跳过已存在的规则）。

**文件：** `09-advanced-features/setup-auto-mode-permissions.py`

```bash
# 预览将要添加的内容
python3 09-advanced-features/setup-auto-mode-permissions.py --dry-run

# 应用
python3 09-advanced-features/setup-auto-mode-permissions.py
```

**添加的内容：**

| 类别 | 示例 |
|------|------|
| 内置工具 | `Read(*)`、`Edit(*)`、`Write(*)`、`Glob(*)`、`Grep(*)`、`Agent(*)`、`WebSearch(*)` |
| Git 读取 | `Bash(git status:*)`、`Bash(git log:*)`、`Bash(git diff:*)` |
| Git 写入（本地） | `Bash(git add:*)`、`Bash(git commit:*)`、`Bash(git checkout:*)` |
| 包管理器 | `Bash(npm install:*)`、`Bash(pip install:*)`、`Bash(cargo build:*)` |
| 构建和测试 | `Bash(make:*)`、`Bash(pytest:*)`、`Bash(go test:*)` |
| 常用 Shell | `Bash(ls:*)`、`Bash(cat:*)`、`Bash(find:*)`、`Bash(cp:*)`、`Bash(mv:*)` |
| GitHub CLI | `Bash(gh pr view:*)`、`Bash(gh pr create:*)`、`Bash(gh issue list:*)` |

**有意排除的内容**（此脚本永远不会添加）：
- `rm -rf`、`sudo`、强制推送、`git reset --hard`
- `DROP TABLE`、`kubectl delete`、`terraform destroy`
- `npm publish`、`curl | bash`、生产环境部署

### 示例 8：学习进度记录器（SessionEnd）

在每个 Claude Code 会话结束时记录您学习的模块。进度存储在 `~/.claude-howto-progress.json` 中 — 位于仓库之外，因此在 `git pull` 时不会被覆盖。

**为什么使用 `SessionEnd` 而不是 `Stop`？**
`Stop` 在每次 Claude 响应后都触发。`SessionEnd` 在会话终止时仅触发一次 — 这正是您需要的会话结束日记条目。

**为什么使用 `/dev/tty` 进行输入？**
钩子脚本通过 `stdin` 接收钩子 JSON 数据，因此交互式 `read` 必须直接使用 `/dev/tty` 来访问终端。

**文件：** `06-hooks/session-end.sh`

```bash
#!/bin/env bash
# SessionEnd 钩子：提示用户输入工作的模块，然后将会话记录
# 追加到 ~/.claude-howto-progress.json 以实现持久化的学习进度跟踪。

PROGRESS_FILE="$HOME/.claude-howto-progress.json"

# 保护：仅在此仓库内运行
if [[ "$CLAUDE_PROJECT_DIR" != *"claude-howto"* ]] && [[ "$PWD" != *"claude-howto"* ]]; then
  exit 0
fi

if [ ! -f "$PROGRESS_FILE" ]; then
  echo '{"sessions":[]}' > "$PROGRESS_FILE"
fi

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")

echo ""
echo " 您在哪些模块上工作过？（例如 06,07 或按 Enter 跳过）"
echo " 01=Slash  02=Memory  03=Skills  04=Subagents  05=MCP"
echo " 06=Hooks  07=Plugins 08=Checkpoints 09=Advanced 10=CLI"
printf " > "
read -r INPUT </dev/tty

if [ -z "$INPUT" ] || [ "$INPUT" = "skip" ]; then
  exit 0
fi

MODULES_JSON=$(echo "$INPUT" | tr ',' '\n' | tr -d ' ' | while read -r m; do
  case "$m" in
    01) echo '"01-slash-commands"' ;;
    02) echo '"02-memory"' ;;
    03) echo '"03-skills"' ;;
    04) echo '"04-subagents"' ;;
    05) echo '"05-mcp"' ;;
    06) echo '"06-hooks"' ;;
    07) echo '"07-plugins"' ;;
    08) echo '"08-checkpoints"' ;;
    09) echo '"09-advanced-features"' ;;
    10) echo '"10-cli"' ;;
    *)  echo "\"$m\"" ;;
  esac
done | paste -sd ',' -)

printf " 备注？（可选，按 Enter 跳过）："
read -r NOTES </dev/tty

# 将 NOTES 作为单独的参数传递，让 Python 处理 JSON 转义 —
# 避免当备注包含引号或反斜杠时产生损坏的 JSON。
python3 - "$PROGRESS_FILE" "$DATE" "$TIME" "$MODULES_JSON" "$NOTES" <<'PYEOF'
import sys, json

path, date, time_str, modules_raw, notes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

new_session = {
    "date": date,
    "time": time_str,
    "modules": json.loads(f"[{modules_raw}]") if modules_raw else [],
    "notes": notes,
}

with open(path, 'r') as f:
    data = json.load(f)

data.setdefault('sessions', []).append(new_session)

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
PYEOF

echo " 已保存到 $PROGRESS_FILE"
```

**安装** — 将脚本复制到项目的钩子目录中，以便 `settings.json` 中的路径能够正确解析：

```bash
mkdir -p .claude/hooks
cp 06-hooks/session-end.sh .claude/hooks/
chmod +x .claude/hooks/session-end.sh
```

**配置**（在 `.claude/settings.json` 中）：

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh\""
          }
        ]
      }
    ]
  }
}
```

**输出 — `~/.claude-howto-progress.json`：**

```json
{
  "sessions": [
    {
      "date": "2026-04-18",
      "time": "14:32",
      "modules": ["06-hooks", "07-plugins"],
      "notes": "Installed first hook, tried pre-commit example"
    }
  ]
}
```

**演示的关键模式：**

| 模式 | 为什么重要 |
|------|------------|
| `SessionEnd` 事件 | 退出时仅触发一次 — 不像 `Stop` 那样每次响应后都触发 |
| `read -r INPUT </dev/tty` | 钩子拥有自己的 `stdin`（JSON 数据）；使用 `/dev/tty` 进行用户输入 |
| `$CLAUDE_PROJECT_DIR` | 可移植路径 — 永远不要硬编码 `/Users/yourname/...` |
| 顶部的保护子句 | 防止钩子在全局安装时在不相关的项目中运行 |
| 存储在仓库外部 | `~/` 路径在 `git pull` 时不会被覆盖您的数据 |

**配套工具：可视化进度跟踪器**

对于涵盖所有 10 个模块的基于复选框的完整 UI，请在浏览器中打开包含的跟踪器：

```bash
open local-progress/index.html
```

进度存储在浏览器的 `localStorage` 中（永远不会写入仓库内的磁盘）。使用 **导出** 按钮将快照保存为 JSON，使用 **导入** 按钮恢复它。

## 插件钩子

插件可以在其 `hooks/hooks.json` 文件中包含钩子：

**文件：** `plugins/hooks/hooks.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

**插件钩子中的环境变量：**
- `${CLAUDE_PLUGIN_ROOT}` - 插件目录路径
- `${CLAUDE_PLUGIN_DATA}` - 插件数据目录路径

这允许插件包含自定义验证和自动化钩子。

## MCP 工具钩子

MCP 工具遵循模式 `mcp__<server>__<tool>`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"systemMessage\": \"Memory operation logged\"}'"
          }
        ]
      }
    ]
  }
}
```

## 安全性考虑

### 免责声明

**风险自担**：钩子执行任意 Shell 命令。您需独自负责：
- 您配置的命令
- 文件访问/修改权限
- 可能的数据丢失或系统损坏
- 在生产环境使用前在安全环境中测试钩子

### 安全性说明

- **工作区信任必需：** `statusLine` 和 `fileSuggestion` 钩子输出命令现在需要工作区信任接受才能生效。
- **HTTP 钩子和环境变量：** HTTP 钩子需要显式的 `allowedEnvVars` 列表才能在 URL 中使用环境变量插值。这防止敏感环境变量意外泄露到远程端点。
- **托管设置层次结构：** `disableAllHooks` 设置现在尊重托管设置层次结构，意味着组织级别的设置可以强制禁用钩子，个别用户无法覆盖。
- **PowerShell 自动批准（v2.1.119）：** PowerShell 工具命令可以在权限模式中自动批准，与 Bash 保持一致。这为使用 PowerShell 支持 Shell 工具的 Windows 用户带来了对等性。

### 最佳实践

| 做 | 不要做 |
|----|--------|
| 验证并清理所有输入 | 盲目信任输入数据 |
| 引用 Shell 变量：`"$VAR"` | 使用未引用的：`$VAR` |
| 阻止路径遍历（`..`） | 允许任意路径 |
| 使用带有 `$CLAUDE_PROJECT_DIR` 的绝对路径 | 硬编码路径 |
| 跳过敏感文件（`.env`、`.git/`、密钥） | 处理所有文件 |
| 先独立测试钩子 | 部署未经测试的钩子 |
| 为 HTTP 钩子使用显式的 `allowedEnvVars` | 将所有环境变量暴露给 webhook |

## 调试

### 启用调试模式

使用调试标志运行 Claude 以查看详细的钩子日志：

```bash
claude --debug
```

### 详细模式

在 Claude Code 中使用 `Ctrl+O` 启用详细模式并查看钩子执行进度。

### 独立测试钩子

```bash
# 使用示例 JSON 输入进行测试
echo '{"tool_name": "Bash", "tool_input": {"command": "ls -la"}}' | python3 .claude/hooks/validate-bash.py

# 检查退出码
echo $?
```

## 完整配置示例

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh\"",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/security-scan.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-prompt.py\""
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-init.sh\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify all tasks are complete before stopping.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 钩子执行详情

| 方面 | 行为 |
|------|------|
| **超时** | 默认 60 秒，可按命令配置 |
| **并行化** | 所有匹配的钩子并行运行 |
| **去重** | 相同的钩子命令会被去重 |
| **环境** | 在当前目录中使用 Claude Code 的环境运行 |

## 故障排除

### 钩子未执行
- 验证 JSON 配置语法是否正确
- 检查匹配器模式是否匹配工具名称
- 确保脚本存在且可执行：`chmod +x script.sh`
- 运行 `claude --debug` 查看钩子执行日志
- 验证钩子是否从 stdin 读取 JSON（而非命令行参数）

### 钩子意外阻塞
- 使用示例 JSON 测试钩子：`echo '{"tool_name": "Write", ...}' | ./hook.py`
- 检查退出码：应该为 0 表示允许，2 表示阻止
- 检查 stderr 输出（在退出码 2 时显示）

### JSON 解析错误
- 始终从 stdin 读取，而非命令行参数
- 使用正确的 JSON 解析（而非字符串操作）
- 优雅地处理缺失字段

## 安装

### 步骤 1：创建钩子目录
```bash
mkdir -p ~/.claude/hooks
```

### 步骤 2：复制示例钩子
```bash
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

### 步骤 3：在设置中配置
编辑 `~/.claude/settings.json` 或 `.claude/settings.json`，添加上面显示的钩子配置。

## 相关概念

- **[检查点和回退](../08-checkpoints/)** - 保存和恢复对话状态
- **[斜杠命令](../01-slash-commands/)** - 创建自定义斜杠命令
- **[技能](../03-skills/)** - 可重用的自主能力
- **[子代理](../04-subagents/)** - 委托任务执行
- **[插件](../07-plugins/)** - 打包的扩展包
- **[高级功能](../09-advanced-features/)** - 探索 Claude Code 的高级功能

## 附加资源

- **[官方钩子文档](https://docs.anthropic.com/en/docs/claude-code/hooks)** - 完整的钩子参考
- **[CLI 参考](https://docs.anthropic.com/en/docs/claude-code/cli)** - 命令行接口文档
- **[记忆指南](../02-memory/)** - 持久化上下文配置

---

**最后更新**: 2026年4月24日
**Claude Code 版本**: 2.1.119
**来源**:
- https://docs.anthropic.com/en/docs/claude-code/hooks
- https://docs.anthropic.com/en/docs/claude-code/changelog
- https://github.com/anthropics/claude-code/releases/tag/v2.1.118
- https://github.com/anthropics/claude-code/releases/tag/v2.1.119
**兼容模型**: Claude Sonnet 4.6, Claude Opus 4.7, Claude Haiku 4.5
