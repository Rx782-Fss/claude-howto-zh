# Claude Code 钩子 (Hooks)

> 钩子是在 Claude Code 会话期间响应特定事件而自动执行的脚本。它们实现自动化、验证、权限管理和自定义工作流。

**详细指南 → [[Claude 概念指南]]**

---

## 概述

钩子是自动化操作（Shell 命令、HTTP Webhook、LLM 提示词或子代理评估），在 Claude Code 中发生特定事件时自动执行。它们接收 JSON 输入，并通过退出码和 JSON 输出返回结果。

**核心特性:**
- 事件驱动自动化
- 基于 JSON 的输入/输出
- 支持 command、prompt、http 和 agent 四种钩子类型
- 支持工具级别的模式匹配

## 配置

钩子在设置文件中配置，具有特定结构：

- `~/.claude/settings.json` — 用户设置（所有项目）
- `.claude/settings.json` — 项目设置（可共享，可提交）
- `.claude/settings.local.json` — 本地项目设置（不提交）
- 托管策略 — 组织级设置
- 插件 `hooks/hooks.json` — 插件作用域钩子
- 技能/代理 frontmatter — 组件生命周期钩子

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

**关键字段:**

| 字段 | 描述 | 示例 |
|-------|-------------|---------|
| `matcher` | 匹配工具名的模式（区分大小写）| `"Write"`, `"Edit\|Write"`, `"*"` |
| `hooks` | 钩子定义数组 | `[{ "type": "command", ... }]` |
| `type` | 钩子类型: `"command"` (bash), `"prompt"` (LLM), `"http"` (webhook), 或 `"agent"` (子代理) | `"command"` |
| `command` | 要执行的 Shell 命令 | `"$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"` |
| `timeout` | 可选超时时间(秒)，默认 60 | `30` |
| `once` | 如果为 `true`，每会话只运行一次 | `true` |

### 匹配模式

| 模式 | 描述 | 示例 |
|---------|-------------|---------|
| 精确字符串 | 匹配特定工具 | `"Write"` |
| 正则表达式 | 匹配多个工具 | `"Edit\|Write"` |
| 通配符 | 匹配所有工具 | `"*"` 或 `""` |
| MCP 工具 | 服务器和工具模式 | `"mcp__memory__.*"` |

**InstructionsLoaded 匹配值:**

| 匹配值 | 描述 |
|---------------|-------------|
| `session_start` | 会话启动时加载指令 |
| `nested_traversal` | 嵌套目录遍历时加载指令 |
| `path_glob_match` | 通过路径 glob 模式匹配加载指令 |

## 钩子类型

Claude Code 支持四种钩子类型:

### Command 钩子 (命令)

默认钩子类型。执行 Shell 命令，通过 JSON stdin/stdout 和退出码通信。

```json
{
  "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py\"",
  "timeout": 60
}
```

### HTTP 钩子

> v2.1.63 新增。

远程 Webhook 端点，接收与 Command 钩子相同的 JSON 输入。HTTP 钩子向 URL POST JSON 并接收 JSON 响应。启用沙箱时 HTTP 钩子通过沙箱路由。URL 中的环境变量插值需要显式的 `allowedEnvVars` 列表以确保安全。

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

**关键属性:**
- `"type": "http"` — 标识为 HTTP 钩子
- `"url"` — Webhook 端点 URL
- 启用沙箱时通过沙箱路由
- URL 中使用环境变量插值需要显式 `allowedEnvVars` 列表

### Prompt 钩子 (提示)

LLM 评估型提示词，钩子内容是一个由 Claude 评估的提示词。主要用于 `Stop` 和 `SubagentStop` 事件进行智能任务完成检查。

```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude completed all requested tasks.",
  "timeout": 30
}
```

LLM 评估提示词并返回结构化决策。

### Agent 钩子 (代理)

基于子代理的验证钩子，启动专用代理来评估条件或执行复杂检查。与 Prompt 钩子（单轮 LLM 评估）不同，Agent 钩子可以使用工具并执行多步推理。

```json
{
  "type": "agent",
  "prompt": "Verify the code changes follow our architecture guidelines. Check the relevant design docs and compare.",
  "timeout": 120
}
```

**关键属性:**
- `"type": "agent"` — 标识为 Agent 钩子
- `"prompt"` — 子代理的任务描述
- 代理可以使用工具（Read、Grep、Bash 等）执行评估
- 返回与 Prompt 钩子类似的结构化决策

## 钩子事件

Claude Code 支持 **26 种钩子事件**：

| 事件 | 触发时机 | 匹配输入 | 可阻塞 | 常见用途 |
|-------|---------------|---------------|-----------|------------|
| **SessionStart** | 会话开始/恢复/清除/压缩 | startup/resume/clear/compact | 否 | 环境初始化 |
| **InstructionsLoaded** | CLAUDE.md 或规则文件加载后 | (无) | 否 | 修改/过滤指令 |
| **UserPromptSubmit** | 用户提交提示词 | (无) | 是 | 验证提示词 |
| **PreToolUse** | 工具执行前 | 工具名 | 是 (允许/拒绝/询问) | 验证、修改输入 |
| **PermissionRequest** | 权限对话框显示 | 工具名 | 是 | 自动批准/拒绝 |
| **PermissionDenied** | 用户拒绝权限请求 | 工具名 | 否 | 日志记录、分析、策略执行 |
| **PostToolUse** | 工具成功后 | 工具名 | 否 | 添加上下文、反馈 |
| **PostToolUseFailure** | 工具执行失败 | 工具名 | 否 | 错误处理、日志 |
| **Notification** | 发送通知 | 通知类型 | 否 | 自定义通知 |
| **SubagentStart** | 子代理启动 | 代理类型名 | 否 | 子代理初始化 |
| **SubagentStop** | 子代理完成 | 代理类型名 | 是 | 子代理验证 |
| **Stop** | Claude 完成响应 | (无) | 是 | 任务完成检查 |
| **StopFailure** | API 错误结束回合 | (无) | 否 | 错误恢复、日志 |
| **TeammateIdle** | Agent Team 队友空闲 | (无) | 是 | 队友协调 |
| **TaskCompleted** | 任务标记完成 | (无) | 是 | 任务后操作 |
| **TaskCreated** | 通过 TaskCreate 创建任务 | (无) | 否 | 任务跟踪、日志 |
| **ConfigChange** | 配置文件变更 | (none) | 是 (除策略外) | 响应配置更新 |
| **CwdChanged** | 工作目录变更 | (none) | 否 | 目录特定初始化 |
| **FileChanged** | 监控文件变更 | (none) | 否 | 文件监控、重建 |
| **PreCompact** | 上下文压缩前 | manual/auto | 否 | 压缩前操作 |
| **PostCompact** | 压缩完成后 | (none) | 否 | 压缩后操作 |
| **WorktreeCreate** | Worktree 创建中 | (none) | 是 (路径返回) | Worktree 初始化 |
| **WorktreeRemove** | Worktree 移除中 | (none) | 否 | Worktree 清理 |
| **Elicitation** | MCP 服务器请求用户输入 | (none) | 是 | 输入验证 |
| **ElicitationResult** | 用户响应 Elicitation | (none) | 是 | 响应处理 |
| **SessionEnd** | 会话终止 | (none) | 否 | 清理、最终日志 |

### PreToolUse

在 Claude 创建工具参数后、处理之前运行。用于验证或修改工具输入。

**配置:**
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

**常用匹配器:** `Task`, `Bash`, `Glob`, `Grep`, `Read`, `Edit`, `Write`, `WebFetch`, `WebSearch`

**输出控制:**
- `permissionDecision`: `"allow"`, `"deny"`, 或 `"ask"`
- `permissionDecisionReason`: 决策说明
- `updatedInput`: 修改后的工具输入参数

### PostToolUse

在工具完成后立即运行。用于验证、日志记录或向 Claude 提供上下文。

**配置:**
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

**输出控制:**
- `"block"` 决策向 Claude 反馈信息
- `additionalContext`: 为 Claude 添加的上下文

### Stop 和 SubagentStop

当 Claude 完成响应 (Stop) 或子代理完成 (SubagentStop) 时运行。支持基于 Prompt 的智能任务完成检查。

**额外输入字段:** `Stop` 和 `SubagentStop` 钩子的 JSON 输入中都包含 `last_assistant_message` 字段，包含 Claude 或子代理停止前的最后消息。

### SessionStart

会话启动或恢复时运行。可以持久化环境变量。

**匹配器:** `startup`, `resume`, `clear`, `compact`

**特殊功能:** 使用 `CLAUDE_ENV_FILE` 持久化环境变量（同样适用于 `CwdChanged` 和 `FileChanged` 钩子）:

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

### SessionEnd

会话结束时运行以执行清理或最终日志。不能阻止终止。

**原因字段值:**
- `clear` - 用户清除会话
- `logout` - 用户登出
- `prompt_input_exit` - 用户通过提示输入退出
- `other` - 其他原因

## 组件作用域钩子

钩子可以附加到特定组件（技能、代理、命令）的 frontmatter 中：

**在 SKILL.md、agent.md 或 command.md 中:**

```yaml
---
name: secure-operations
description: 执行带安全检查的操作
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true  # 每会话仅运行一次
---
```

**组件钩子支持的事件:** `PreToolUse`, `PostToolUse`, `Stop`

这允许将钩子直接定义在使用它的组件中，保持相关代码在一起。

### 子代理 Frontmatter 中的钩子

当子代理的 frontmatter 中定义了 `Stop` 钩子时，它会自动转换为该子代理专属的 `SubagentStop` 钩子。确保停止钩子仅在特定子代理完成时触发，而不是主会话停止时触发。

```yaml
---
name: code-review-agent
description: 自动代码审查子代理
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "验证代码审查是否彻底完整。"
  # 以上 Stop 钩子会自动转换为该子代理的 SubagentStop
---
```

## 权限请求事件

使用自定义输出格式处理权限请求：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {},
      "message": "自定义消息",
      "interrupt": false
    }
  }
}
```

## 钩子输入和输出

### JSON 输入 (通过 stdin)

所有钩子通过 stdin 接收 JSON 输入：

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

**常用字段:**

| 字段 | 描述 |
|-------|-------------|
| `session_id` | 唯一会话标识符 |
| `transcript_path` | 对话转录文件路径 |
| `cwd` | 当前工作目录 |
| `hook_event_name` | 触发钩子的事件名称 |
| `agent_id` | 运行此钩子的代理标识符 |
| `agent_type` | 代理类型 (`"main"`, 子代理类型名等) |
| `worktree` | Git worktree 路径（如果代理在 worktree 中运行）|

### 退出码

| 退出码 | 含义 | 行为 |
|-----------|---------|----------|
| **0** | 成功 | 继续，解析 JSON stdout |
| **2** | 阻塞性错误 | 阻止操作，stderr 显示为错误 |
| **其他** | 非阻塞性错误 | 继续，verbose 模式下显示 stderr |

### JSON 输出 (stdout, 退出码 0)

```json
{
  "continue": true,
  "stopReason": "可选的停止原因消息",
  "suppressOutput": false,
  "systemMessage": "可选警告消息",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "文件在允许目录中",
    "updatedInput": {
      "file_path": "/modified/path.js"
    }
  }
}
```

## 环境变量

| 变量 | 可用性 | 描述 |
|----------|-------------|-------------|
| `CLAUDE_PROJECT_DIR` | 所有钩子 | 项目根目录绝对路径 |
| `CLAUDE_ENV_FILE` | SessionStart, CwdChanged, FileChanged | 用于持久化环境变量的文件路径 |
| `CLAUDE_CODE_REMOTE` | 所有钩子 | 远程环境运行为 `"true"` |
| `${CLAUDE_PLUGIN_ROOT}` | 插件钩子 | 插件目录路径 |
| `${CLAUDE_PLUGIN_DATA}` | 插件钩子 | 插件数据目录路径 |

## 基于 Prompt 的钩子

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

**LLM 响应模式:**
```json
{
  "decision": "approve",
  "reason": "All tasks completed successfully",
  "continue": false,
  "stopReason": "Task complete"
}
```

## 示例

### 示例 1: Bash 命令验证器 (PreToolUse)

**文件:** `.claude/hooks/validate-bash.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED_PATTERNS = [
    (r"\brm\s+-rf\s+/", "阻止危险的 rm -rf / 命令"),
    (r"\bsudo\s+rm", "阻止 sudo rm 命令"),
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
            sys.exit(2)  # 退出码 2 = 阻塞性错误
    
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 示例 2: 安全扫描器 (PostToolUse)

**文件:** `.claude/hooks/security-scan.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

SECRET_PATTERNS = [
    (r"password\s*=\s*['\"][^'\"]+['\"]", "可能存在硬编码密码"),
    (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "可能存在硬编码 API 密钥"),
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
                "additionalContext": f"{file_path} 的安全警告: " + "; ".join(warnings)
            }
        }
        print(json.dumps(output))
    
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 示例 3: 自动格式化代码 (PostToolUse)

**文件:** `.claude/hooks/format-code.sh`

```bash
#!/bin/bash

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_name', ''))")
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('file_path', ''))")

if [ "$TOOL_NAME" != "Write" ] && [ "$TOOL_NAME" != "Edit" ]; then
    exit 0
fi

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

### 示例 4: 提示词验证器 (UserPromptSubmit)

**文件:** `.claude/hooks/validate-prompt.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED_PATTERNS = [
    (r"delete\s+(all\s+)?database", "危险: 数据库删除操作"),
    (r"rm\s+-rf\s+/", "危险: 根目录删除操作"),
]

def main():
    input_data = json.load(sys.stdin)
    prompt = input_data.get("user_prompt", "") or input_data.get("prompt", "")
    
    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            output = {
                "decision": "block",
                "reason": f"已阻止: {message}"
            }
            print(json.dumps(output))
            sys.exit(0)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 示例 5: 智能 Stop 钩子 (基于 Prompt)

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

### 示例 6: 上下文用量跟踪器 (钩子对)

使用 `UserPromptSubmit` (消息前) 和 `Stop` (响应后) 钩子对来跟踪每次请求的 Token 消耗。

**文件:** `.claude/hooks/context-tracker.py`

```python
#!/usr/bin/env python3
"""
上下文用量跟踪器 - 跟踪每次请求的 Token 消耗。

使用 UserPromptSubmit 作为"消息前"钩子和 Stop 作为"响应后"钩子
来计算每次请求的 Token 用量差值。
"""
import json
import os
import sys
import tempfile

CONTEXT_LIMIT = 128000  # Claude 上下文窗口大小
USE_TIKTOKEN = False

def get_state_file(session_id: str) -> str:
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")

def count_tokens(text: str) -> int:
    if USE_TIKTOKEN:
        try:
            import tiktoken
            enc = tiktoken.get_encoding("p50k_base")
            return len(enc.encode(text))
        except ImportError:
            pass
    return len(text) // 4

def read_transcript(transcript_path: str) -> str:
    if not transcript_path or not os.path.exists(transcript_path):
        return ""
    content = []
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
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
    session_id = data.get("session_id", "unknown")
    transcript_content = read_transcript(data.get("transcript_path", ""))
    current_tokens = count_tokens(transcript_content)
    with open(get_state_file(session_id), "w") as f:
        json.dump({"pre_tokens": current_tokens}, f)

def handle_stop(data: dict) -> None:
    session_id = data.get("session_id", "unknown")
    transcript_content = read_transcript(data.get("transcript_path", ""))
    current_tokens = count_tokens(transcript_content)
    
    pre_tokens = 0
    state_file = get_state_file(session_id)
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                pre_tokens = json.load(f).get("pre_tokens", 0)
        except (json.JSONDecodeError, IOError):
            pass
    
    delta_tokens = current_tokens - pre_tokens
    remaining = CONTEXT_LIMIT - current_tokens
    percentage = (current_tokens / CONTEXT_LIMIT) * 100
    
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

## 插件钩子

插件可以在其 `hooks/hooks.json` 文件中包含钩子：

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

**插件钩子中的环境变量:**
- `${CLAUDE_PLUGIN_ROOT}` — 插件目录路径
- `${CLAUDE_PLUGIN_DATA}` — 插件数据目录路径

## MCP 工具钩子

MCP 工具遵循 `mcp__<server>__<tool>` 模式：

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

## 安全注意事项

### 免责声明

**自行承担风险**: 钩子执行任意 Shell 命令。你需要自行负责：
- 你配置的命令
- 文件访问/修改权限
- 可能的数据丢失或系统损坏
- 在生产使用前在安全环境中测试钩子

### 最佳实践

| 应做 | 不应做 |
|-----|-------|
| 验证和清理所有输入 | 盲目信任输入数据 |
| 引用 Shell 变量: `"$VAR"` | 不加引号: `$VAR` |
| 阻止路径遍历 (`..`) | 允许任意路径 |
| 使用 `$CLAUDE_PROJECT_DIR` 的绝对路径 | 硬编码路径 |
| 跳过敏感文件 (`.env`, `.git/`, 密钥) | 处理所有文件 |
| 先隔离测试钩子 | 部署未测试的钩子 |

## 调试

### 启用调试模式

```bash
claude --debug
```

### 详细模式

在 Claude Code 中按 `Ctrl+O` 启用详细模式查看钩子执行进度。

### 独立测试钩子

```bash
# 用示例 JSON 输入测试
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

## 安装

### 第一步: 创建钩子目录
```bash
mkdir -p ~/.claude/hooks
```

### 第二步: 复制示例钩子
```bash
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

### 第三步: 在设置中配置
编辑 `~/.claude/settings.json` 或 `.claude/settings.json`，添加上述钩子配置。

## 相关概念

- **[检查点和回退](../08-checkpoints/)** — 保存和恢复对话状态
- **[斜杠命令](../01-slash-commands/)** — 创建自定义斜杠命令
- **[技能](../03-skills/)** — 可复用的自主能力
- **[子代理](../04-subagents/)** — 委派任务执行
- **[插件](../07-plugins/)** — 打包扩展包
- **[高级功能](../09-advanced-features/)** — 探索高级 Claude Code 功能

## 更多资源

- **[官方钩子文档](https://code.claude.com/docs/en/hooks)** — 完整钩子参考
- **[CLI 参考](https://code.claude.com/docs/en/cli-reference)** — 命令行接口文档
- **[记忆指南](../02-memory/)** — 持久化上下文配置

---

*最后更新: 2026 年 4 月*
*Claude Code 版本: 2.1.97*
*兼容模型: Claude Sonnet 4.6, Claude Opus 4.6, Claude Haiku 4.5*
