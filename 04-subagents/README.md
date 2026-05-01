<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# 子代理（Subagents）- 完整参考指南

子代理是 Claude Code 可以委托任务给的专业化 AI 助手。每个子代理都有特定的用途，使用独立于主对话的上下文窗口，并可以配置特定的工具和自定义系统提示词。

## 目录

1. [概览](#概览)
2. [核心优势](#核心优势)
3. [文件位置](#文件位置)
4. [配置](#配置)
5. [内置子代理](#内置子代理)
6. [管理子代理](#管理子代理)
7. [使用子代理](#使用子代理)
8. [可恢复代理（Resumable Agents）](#可恢复代理resumable-agents)
9. [链式子代理（Chaining Subagents）](#链式子代理chaining-subagents)
10. [子代理的持久化记忆（Persistent Memory）](#子代理的持久化记忆persistent-memory-for-subagents)
11. [后台子代理（Background Subagents）](#后台子代理background-subagents)
12. [工作树隔离（Worktree Isolation）](#工作树隔离worktree-isolation)
13. [限制可生成的子代理（Restrict Spawnable Subagents）](#限制可生成的子代理restrict-spawnable-subagents)
14. [`claude agents` CLI 命令](#claude-agents-cli-command)
15. [代理团队（实验性）](#代理团队experimental)
16. [插件子代理安全性](#插件子代理安全性)
17. [架构](#架构)
18. [上下文管理（Context Management）](#上下文管理context-management)
19. [何时使用子代理](#何时使用子代理)
20. [最佳实践](#最佳实践)
21. [本文件夹中的示例子代理](#本文件夹中的示例子代理)
22. [安装说明](#安装说明)
23. [相关概念](#相关概念)

---

## 概览

子代理通过以下方式在 Claude Code 中实现委托任务执行：

- 创建具有独立上下文窗口的**隔离 AI 助手**
- 提供用于专业化专业知识的**自定义系统提示词**
- 强制执行**工具访问控制**以限制能力
- 防止来自复杂任务的**上下文污染**
- 启用多个专业化任务的**并行执行**

每个子代理独立运行，从零开始，仅接收其任务所需的特定上下文，然后将结果返回给主代理进行综合。

**快速开始**：使用 `/agents` 命令以交互方式创建、查看、编辑和管理您的子代理。

---

## 核心优势

| 优势 | 描述 |
|------|------|
| **上下文保留** | 在独立的上下文中运行，防止主对话被污染 |
| **专业化专业知识** | 针对特定领域进行微调，具有更高的成功率 |
| **可重用性** | 可在不同项目中使用并与团队共享 |
| **灵活权限** | 不同子代理类型具有不同的工具访问级别 |
| **可扩展性** | 多个代理可以同时处理不同方面 |

---

## 文件位置

子代理文件可以存储在多个位置，具有不同的作用域：

| 优先级 | 类型 | 位置 | 作用域 |
|--------|------|------|--------|
| 1（最高） | **CLI 定义** | 通过 `--agents` 标志（JSON） | 仅会话 |
| 2 | **项目子代理** | `.claude/agents/` | 当前项目 |
| 3 | **用户子代理** | `~/.claude/agents/` | 所有项目 |
| 4（最低） | **插件代理** | 插件 `agents/` 目录 | 通过插件 |

当存在重复名称时，较高优先级的源优先。

---

## 配置

### 文件格式

子代理在 YAML frontmatter 中定义，后跟 Markdown 格式的系统提示词：

```yaml
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # 可选 - 如果省略则继承所有工具
disallowedTools: tool4  # 可选 - 明确禁止的工具
model: sonnet  # 可选 - sonnet, opus, haiku, 或 inherit
permissionMode: default  # 可选 - 权限模式
maxTurns: 20  # 可选 - 限制代理轮次
skills: skill1, skill2  # 可选 - 预加载到上下文的技能
mcpServers: server1  # 可选 - 可用的 MCP 服务器
memory: user  # 可选 - 持久化记忆作用域（user, project, local）
background: false  # 可选 - 作为后台任务运行
effort: high  # 可选 - 推理强度（low, medium, high, max）
isolation: worktree  # 可选 - git 工作树隔离
initialPrompt: "Start by analyzing the codebase"  # 可选 - 自动提交的第一轮
hooks:  # 可选 - 组件作用域钩子
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.
```

### 配置字段

| 字段 | 必需 | 描述 |
|------|------|------|
| `name` | 是 | 唯一标识符（小写字母和连字符） |
| `description` | 是 | 用途的自然语言描述。包含 "use PROACTIVELY" 以鼓励自动调用 |
| `tools` | 否 | 特定工具的逗号分隔列表。省略以继承所有工具。支持 `agent(agent_name)` 语法来限制可生成的子代理 |
| `disallowedTools` | 否 | 子代理不得使用的工具的逗号分隔列表 |
| `model` | 否 | 要使用的模型：`sonnet`、`opus`、`haiku`、完整模型 ID 或 `inherit`。默认为配置的子代理模型 |
| `permissionMode` | 否 | `default`、`acceptEdits`、`dontAsk`、`bypassPermissions`、`plan` |
| `maxTurns` | 否 | 子代理可以执行的最大代理轮次数 |
| `skills` | 否 | 预加载技能的逗号分隔列表。在启动时将完整的技能内容注入子代理的上下文中 |
| `mcpServers` | 否 | 对子代理可用的 MCP 服务器 |
| `hooks` | 否 | 组件作用域钩子（PreToolUse、PostToolUse、Stop） |
| `memory` | 否 | 持久化记忆目录作用域：`user`、`project` 或 `local` |
| `background` | 否 | 设置为 `true` 以始终将此子代理作为后台任务运行 |
| `effort` | 否 | 推理强度级别：`low`、`medium`、`high` 或 `max` |
| `isolation` | 否 | 设置为 `worktree` 以给予子代理自己的 git 工作树 |
| `initialPrompt` | 否 | 当子代理作为主代理运行时自动提交的第一轮 |

### 主线程代理 Frontmatter 支持（v2.1.117+/v2.1.119+）

当代理作为主线程代理调用时（通过 `claude --agent <name>` 或 `--print` 模式），支持以下 frontmatter 字段：

| 字段 | 版本 | 说明 |
|------|------|------|
| `mcpServers` | v2.1.117+ | 当通过 `claude --agent <name>` 作为主线程代理调用时加载 |
| `permissionMode` | v2.1.119+ | 通过 `--agent <name>` 为内置代理支持 |
| `tools` / `disallowedTools` | v2.1.119+ | 在 `--print` 模式下支持（非交互式/脚本化用法） |

**示例 — 具有 `mcpServers` 和 `permissionMode` 的代理：**

```yaml
---
name: secure-researcher
description: Research agent with scoped MCP access and restricted permissions
permissionMode: acceptEdits
mcpServers:
  notion:
    type: http
    url: https://mcp.notion.com/mcp
  github:
    type: http
    url: https://api.github.com/mcp
tools: Read, Grep, Glob
---

You are a research agent. You may query Notion and GitHub through the
configured MCP servers, and read local files, but you cannot write or
execute commands outside of accepted edits.
```

运行方式：

```bash
claude --agent secure-researcher
```

### 工具配置选项

**选项 1：继承所有工具（省略该字段）**
```yaml
---
name: full-access-agent
description: Agent with all available tools
---
```

**选项 2：指定单个工具**
```yaml
---
name: limited-agent
description: Agent with specific tools only
tools: Read, Grep, Glob, Bash
---
```

> **关于 Glob/Grep 的说明（v2.1.113+）：** 在原生 macOS/Linux 构建中，Glob 和 Grep 作为 `bfs`/`ugrep` 通过 Bash 工具提供，而不是作为单独的工具。Windows 和 npm-JS 构建仍将它们作为独立工具公开。作者仍然可以在 `allowedTools` 中引用 Glob/Grep；后端替换是透明的。

**选项 3：条件工具访问**
```yaml
---
name: conditional-agent
description: Agent with filtered tool access
tools: Read, Bash(npm:*), Bash(test:*)
---
```

### 基于 CLI 的配置

使用带有 JSON 格式的 `--agents` 标志为单个会话定义子代理：

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**`--agents` 标志的 JSON 格式：**

```json
{
  "agent-name": {
    "description": "Required: when to invoke this agent",
    "prompt": "Required: system prompt for the agent",
    "tools": ["Optional", "array", "of", "tools"],
    "model": "optional: sonnet|opus|haiku"
  }
}
```

**代理定义的优先级：**

代理定义按以下优先级顺序加载（第一个匹配的优先）：
1. **CLI 定义** - `--agents` 标志（仅会话，JSON）
2. **项目级别** - `.claude/agents/`（当前项目）
3. **用户级别** - `~/.claude/agents/`（所有项目）
4. **插件级别** - 插件 `agents/` 目录

这允许 CLI 定义在单个会话中覆盖所有其他源。

---

## 内置子代理

Claude Code 包含几个始终可用的内置子代理：

| 代理 | 模型 | 用途 |
|------|------|------|
| **general-purpose** | 继承 | 复杂的多步骤任务 |
| **Plan** | 继承 | 规划模式的研究 |
| **Explore** | Haiku | 只读代码库探索（快速/中等/非常彻底） |
| **Bash** | 继承 | 独立上下文中的终端命令 |
| **statusline-setup** | Sonnet | 配置状态栏 |
| **Claude Code Guide** | Haiku | 回答 Claude Code 功能问题 |

### 通用子代理

| 属性 | 值 |
|------|-----|
| **模型** | 从父级继承 |
| **工具** | 所有工具 |
| **用途** | 复杂研究任务、多步骤操作、代码修改 |

**使用时机**：需要既有探索又有修改且涉及复杂推理的任务。

### Plan 子代理

| 属性 | 值 |
|------|-----|
| **模型** | 从父级继承 |
| **工具** | Read、Glob、Grep、Bash |
| **用途** | 在规划模式中自动用于研究代码库 |

**使用时机**：当 Claude 需要在展示计划之前了解代码库时。

### Explore 子代理

| 属性 | 值 |
|------|-----|
| **模型** | Haiku（快速、低延迟） |
| **模式** | 严格只读 |
| **工具** | Glob、Grep、Read、Bash（仅只读命令） |
| **用途** | 快速代码库搜索和分析 |

**使用时机**：在不进行更改的情况下搜索/理解代码时。

**彻底程度级别** - 指定探索深度：
- **"quick"** - 快速搜索，最小探索，适合查找特定模式
- **"medium"** - 适度探索，平衡速度和彻底程度，默认方法
- **"very thorough"** - 跨多个位置和命名约定的全面分析，可能需要更长时间

### Bash 子代理

| 属性 | 值 |
|------|-----|
| **模型** | 从父级继承 |
| **工具** | Bash |
| **用途** | 在独立的上下文窗口中执行终端命令 |

**使用时机**：当运行受益于隔离上下文的 Shell 命令时。

### 状态栏设置子代理

| 属性 | 值 |
|------|-----|
| **模型** | Sonnet |
| **工具** | Read、Write、Bash |
| **用途** | 配置 Claude Code 状态栏显示 |

**使用时机**：在设置或自定义状态栏时。

### Claude Code 指南子代理

| 属性 | 值 |
|------|-----|
| **模型** | Haiku（快速、低延迟） |
| **工具** | 只读 |
| **用途** | 回答关于 Claude Code 功能和用法的问题 |

**使用时机**：当用户询问 Claude Code 如何工作或如何使用特定功能的问题时。

---

## 管理子代理

### 使用 `/agents` 命令（推荐）

```bash
/agents
```

这提供了一个交互式菜单来：
- 查看所有可用的子代理（内置、用户和项目）
- 通过引导设置创建新的子代理
- 编辑现有的自定义子代理和工具访问权限
- 删除自定义子代理
- 查看存在重复时哪些子代理处于活动状态

### 直接文件管理

```bash
# 创建一个项目子代理
mkdir -p .claude/agents
cat > .claude/agents/test-runner.md << 'EOF'
---
name: test-runner
description: Use proactively to run tests and fix failures
tools: Read, Write, Edit, Bash
---

You are a test runner agent. When executed, run the project's test suite,
identify any failures, analyze the root causes, and attempt to fix them.
Focus on providing clear explanations of what was fixed and why.
EOF
```

### 使用 Task 工具启动子代理

主代理可以使用 Task 工具将工作委托给子代理：

```python
# 主代理委托代码审查任务
Task(
    subagent_type="code-reviewer",
    description="Review the authentication module for security vulnerabilities",
    prompt="Focus on SQL injection, XSS, and authentication bypass vulnerabilities"
)
```

---

## 使用子代理

### 自动调用

当满足以下条件时，Claude 会自动调用子代理：
- 任务匹配子代理的描述
- 任务可以从主对话中受益于隔离
- 用户没有明确要求自己完成

### 手动调用

使用 `/agents` 命令或直接引用名称：

```bash
# 使用 Explore 子代理搜索代码库
Please use the Explore subagent to find all API endpoint definitions.

# 使用 Bash 子代理运行测试
Run the test suite using the Bash subagent.
```

### 参数传递

向子代理传递特定参数：

```bash
# 带有具体指令的 Explore 子代理
Use the Explore subagent to find all files that import from 'react-router'.
Focus on components that use useParams or useLocation hooks.
```

---

## 可恢复代理（Resumable Agents）

> 添加于 v2.0.38。

可恢复代理允许您从上次停止的地方继续代理会话，即使跨多个 Claude Code 会话也是如此。

### 启用恢复

通过在代理定义中添加 `resumable: true` 来启用恢复：

```yaml
---
name: researcher
description: Deep research agent with persistent state
resumable: true
memory: project
---

You are a research agent. Maintain detailed notes on findings and
always resume from where you left off.
```

### 恢复机制

1. **自动保存**：代理状态在每个轮次结束时保存到持久化存储
2. **会话恢复**：新会话检测到之前的未完成状态并自动恢复
3. **上下文连续性**：恢复的代理可以访问之前轮次的发现和推理

### 用例

- **长期研究**：跨越数天的研究任务
- **迭代开发**：需要多次会话的复杂功能实现
- **渐进式分析**：随时间推移的代码库分析

---

## 链式子代理（Chaining Subagents）

链式子代理允许一个子代理的输出成为另一个子代理的输入，创建复杂的工作流程。

### 基本链式

```python
# 主代理协调链式子代理
results = []

# 步骤 1: Explore 子代理收集信息
explore_result = Task(
    subagent_type="Explore",
    description="Find all API endpoints in the codebase"
)
results.append(explore_result)

# 步骤 2: Plan 子代理分析结果
plan_result = Task(
    subagent_type="Plan",
    description="Create optimization plan based on exploration",
    prompt=f"Based on these findings: {explore_result}"
)
results.append(plan_result)

# 步骤 3: General-purpose 子代理实施计划
implementation = Task(
    subagent_type="general-purpose",
    description="Implement the optimization plan",
    prompt=f"Follow this plan: {plan_result}"
)
results.append(implementation)
```

### 条件链式

根据中间结果路由到不同的子代理：

```python
# 根据审查结果条件性地选择下一个子代理
review_result = Task(
    subagent_type="code-reviewer",
    description="Review code quality"
)

if "security issues" in review_result.lower():
    # 路由到安全专家子代理
    next_step = Task(
        subagent_type="security-expert",
        description="Fix identified security issues",
        prompt=f"Address these issues: {review_result}"
    )
else:
    # 路径到性能优化子代理
    next_step = Task(
        subagent_type="performance-analyst",
        description="Optimize performance",
        prompt=f"Improve performance based on: {review_result}"
    )
```

### 并行执行

同时运行多个独立的子代理：

```python
import asyncio

# 并行运行多个探索任务
tasks = [
    Task(subagent_type="Explore", description="Analyze frontend code"),
    Task(subagent_type="Explore", description="Analyze backend code"),
    Task(subagent_type="Explore", description="Analyze infrastructure")
]

# 同时执行所有任务
results = await asyncio.gather(*tasks)

# 综合结果
synthesis = Task(
    subagent_type="general-purpose",
    description="Synthesize findings from all explorations",
    prompt=f"Combine these insights: {results}"
)
```

---

## 子代理的持久化记忆（Persistent Memory）

子代理可以维护跨会话持久化的专用记忆存储。

### 配置记忆

```yaml
---
name: analyst
description: Data analysis agent with persistent memory
memory: project  # user, project, or local
---

You are a data analyst. Store important findings in your memory
for future reference. Always check existing memory before starting
new analysis tasks.
```

### 记忆作用域

| 作用域 | 位置 | 持久性 |
|--------|------|--------|
| `user` | `~/.claude/agents/<name>/memory/` | 跨所有项目持久化 |
| `project` | `.claude/agents/<name>/memory/` | 特定于当前项目 |
| `local` | `.claude/agents/<name>/memory.local/` | 不提交到 Git |

### 记忆使用模式

1. **启动时加载**：子代理在开始时自动加载现有记忆
2. **轮次期间更新**：重要发现写入记忆存储
3. **上下文感知**：记忆帮助避免重复工作
4. **知识积累**：随时间推移构建专业知识库

---

## 后台子代理（Background Subagents）

后台子代理在独立的后台进程中运行，不会阻塞主对话。

### 配置后台运行

```yaml
---
name: indexer
description: Background codebase indexing agent
background: true
---

You are a codebase indexer. Scan and index all source files for
future fast retrieval. Work quietly in the background.
```

### 后台行为

- **非阻塞**：主对话立即继续
- **独立进程**：在自己的上下文窗口中运行
- **状态查询**：可以检查进度和结果
- **资源管理**：受超时和资源限制约束

### 监控后台子代理

```bash
# 检查后台子代理状态
/background status

# 获取特定子代理的结果
/background result indexer
```

---

## 工作树隔离（Worktree Isolation）

工作树隔离为子代理提供完全独立的 Git 工作目录，防止对主代码库的意外修改。

### 启用工作树隔离

```yaml
---
name: experimenter
description: Experimental feature developer
isolation: worktree
---

You are an experimentation agent. Make changes in your isolated
worktree without affecting the main codebase.
```

### 隔离的好处

- **安全实验**：可以在不影响主分支的情况下尝试破坏性更改
- **并行开发**：多个子代理可以在不同的功能上工作而不冲突
- **干净环境**：每个子代理从未修改的代码库状态开始
- **轻松清理**：可以丢弃工作树而不会影响任何内容

### 工作树生命周期

1. **创建**：子代理启动时自动创建
2. **修改**：子代理在其工作树中进行所有更改
3. **合并**：成功的更改可以合并回主分支
4. **清理**：工作树在子代理完成后可以删除

---

## 限制可生成的子代理（Restrict Spawnable Subagents）

您可以控制哪些子代理可以被其他代理生成。

### 限制生成

```yaml
---
name: restricted-agent
description: Agent with limited spawning capability
tools: Read, Grep, Glob, Bash, agent(code-reviewer), agent(test-runner)
---

You have limited ability to spawn other subagents. Only spawn
code-reviewer or test-runner when explicitly needed.
```

### 生成语法

- `agent(*)` - 允许生成所有子代理
- `agent(specific-name)` - 仅允许生成特定子代理
- 省略 - 不允许生成任何子代理（默认）

---

## `claude agents` CLI 命令

CLI 命令用于管理子代理：

```bash
# 列出所有可用的子代理
claude agents list

# 显示特定子代理的详细信息
claude agents show code-reviewer

# 创建新子代理
claude agents create my-agent --description "My custom agent"

# 编辑现有子代理
claude agents edit code-reviewer

# 删除子代理
claude agents delete old-agent

# 测试子代理
claude agents test code-reviewer --prompt "Review auth.js"
```

---

## 代理团队（实验性）

> 实验性功能 - 可能在未来版本中更改。

代理团队允许多个代理协同工作于复杂任务。

### 团队配置

```yaml
---
name: development-team
type: team
members:
  - role: lead-developer
    agent: senior-dev
  - role: code-reviewer
    agent: security-reviewer
  - role: tester
    agent: qa-specialist
coordination: sequential  # or parallel
---

You are coordinating a development team. Assign tasks appropriately
and ensure quality through peer review.
```

### 团队协调模式

| 模式 | 行为 |
|------|------|
| **sequential** | 成员按顺序工作，每个成员接收前一个的输出 |
| **parallel** | 成员同时工作，结果在最后综合 |
| **hierarchical** | 团队领导协调并将工作分配给其他成员 |

---

## 插件子代理安全性

插件提供的子代理遵循与用户定义的子代理相同的安全限制。

### 安全考虑

- **沙箱执行**：插件子代理在受限环境中运行
- **权限继承**：子代理从其父插件设置继承权限
- **工具限制**：可以进一步限制插件子代理可用的工具
- **审计日志**：所有子代理操作都记录用于安全审计

### 示例：受限插件子代理

```yaml
# 在插件内定义
name: plugin-helper
description: Plugin-specific helper agent
tools: Read, Grep  # 仅允许只读操作
permissionMode: plan  # 只能规划，不能执行更改
---

You are a helper agent for this plugin. Assist users with
configuration and troubleshooting, but never modify files directly.
```

---

## 架构

### 执行流程

```
User Request
    ↓
Main Agent (Claude)
    ↓
Task Analysis → Should delegate?
    ↓ Yes                    ↓ No
Subagent Selection      Direct Execution
    ↓
Context Isolation
    ↓
Subagent Execution
    ↓
Result Synthesis
    ↓
Response to User
```

### 上下文管理

每个子代理维护：
- **独立的上下文窗口**：与主对话分离
- **专用的工具访问**：仅配置的工具
- **自己的记忆存储**：如果已配置
- **隔离的文件系统视图**：如果使用工作树隔离

---

## 上下文管理（Context Management）

### 上下文窗口分配

| 代理类型 | 默认上下文大小 | 可配置 |
|----------|----------------|--------|
| Main Agent | 200K tokens | 是 |
| Subagent | 依模型而定 | 通过 `maxTurns` |
| Explore (Haiku) | 较小 | 否 |

### 上下文优化策略

1. **最小化提示词**：保持系统提示词简洁
2. **选择性工具**：仅包含必需的工具
3. **有效记忆**：使用记忆存储避免重复上下文
4. **轮次限制**：使用 `maxTurns` 防止无限循环

---

## 何时使用子代理

### ✅ 适用场景

- **代码审查**：隔离的审查过程，不会污染主对话上下文
- **研究任务**：大型代码库探索，不需要修改
- **测试执行**：长时间运行的测试套件
- **文档生成**：创建广泛的文档而不中断主要工作流
- **数据处理**：分析大型数据集或日志文件
- **实验**：尝试可能失败的方法

### ❌ 不适用场景

- **简单编辑**：单文件更改可以直接完成
- **快速问题**：可以用单个响应回答的问题
- **紧密耦合的任务**：需要在主上下文中完成的任务
- **实时协作**：需要立即反馈的任务

---

## 最佳实践

### 设计原则

1. **单一职责**：每个子代理应该有一个明确定义的用途
2. **清晰描述**：编写详细的描述以确保正确的自动调用
3. **最小权限**：仅授予完成任务所需的工具
4. **明确边界**：定义子代理应该做什么和不应该做什么

### 性能优化

```yaml
# 优化的子代理配置
---
name: optimized-scanner
description: Fast vulnerability scanner
tools: Read, Grep  # 最小工具集
maxTurns: 10       # 限制轮次
model: haiku        # 快速模型用于简单任务
effort: low         # 减少推理开销
---
```

### 错误处理

- **优雅降级**：设计子代理以处理部分失败
- **清晰报告**：返回结构化的错误信息
- **重试逻辑**：为瞬态故障实现重试
- **日志记录**：记录调试和审计的操作

---

## 本文件夹中的示例子代理

此目录包含几个可以学习和适应的即用型示例子代理：

| 文件 | 名称 | 用途 |
|------|------|------|
| `code-reviewer.md` | Code Reviewer | 具有安全焦点的自动化代码审查 |
| `test-runner.md` | Test Runner | 智能测试执行和修复 |
| `documentation-writer.md` | Documentation Writer | 从源代码生成文档 |
| `refactor-assistant.md` | Refactor Assistant | 安全的代码重构助手 |
| `security-auditor.md` | Security Auditor | 安全漏洞扫描器 |

### 使用示例

```bash
# 复制示例到您的代理目录
cp 04-subagents/code-reviewer.md ~/.claude/agents/

# 自定义以满足您的需求
# 编辑 ~/.claude/agents/code-reviewer.md

# 在 Claude Code 中使用
/code-reviewer Please review the authentication module for security issues.
```

---

## 安装说明

### 快速安装

```bash
# 1. 创建代理目录
mkdir -p ~/.claude/agents

# 2. 复制示例代理
cp 04-subagents/*.md ~/.claude/agents/

# 3. 开始使用！
# 在 Claude Code 中：/agents （查看和管理代理）
```

### 项目级安装

```bash
# 为特定项目安装代理
mkdir -p .claude/agents
cp 04-subagents/code-reviewer.md .claude/agents/
cp 04-subagents/test-runner.md .claude/agents/
```

### 自定义

1. **复制模板**：从最接近您需求的示例开始
2. **编辑配置**：调整 frontmatter 中的名称、描述和工具
3. **定制提示词**：修改系统提示词以匹配您的需求
4. **测试验证**：在实际场景中测试子代理

---

## 相关概念

- **[钩子](../06-hooks/)** - 子代理生命周期的自动化
- **[技能](../03-skills/)** - 可重用的能力包
- **[插件](../07-plugins/)** - 打包的扩展和代理
- **[MCP 服务器](../05-mcp/)** - 外部工具集成
- **[高级功能](../09-advanced-features/)** - 后台任务和并行执行
- **[检查点](../08-checkpoints/)** - 状态保存和恢复

---

**最后更新**: 2026年4月24日
**Claude Code 版本**: 2.1.119
**来源**:
- https://docs.anthropic.com/en/docs/claude-code/subagents
- https://docs.anthropic.com/en/docs/claude-code/agents-cli
- https://github.com/anthropics/claude-code/releases/tag/v2.1.119
**兼容模型**: Claude Sonnet 4.6, Claude Opus 4.7, Claude Haiku 4.5
