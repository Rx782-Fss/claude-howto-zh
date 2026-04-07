<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Agent Skills 指南

Agent Skills 是可复用的、基于文件系统的能力扩展，它们将领域专业知识、工作流和最佳实践打包成 Claude 在相关场景下自动使用的可发现组件。

## 概览

**Agent Skills** 是将通用代理转化为领域专家的模块化能力。与 Prompt（用于一次性任务的对话级指令）不同，Skills 按需加载，无需在多个对话中反复提供相同的指导。

### 核心优势

- **专业化定制**：为特定领域的任务量身定制能力
- **减少重复**：一次创建，跨对话自动使用
- **组合能力**：将多个 Skills 组合构建复杂工作流
- **规模化复用**：在多个项目和团队间共享 Skills
- **质量保障**：将最佳实践直接嵌入工作流

Skills 遵循 [Agent Skills](https://agentskills.io) 开放标准，该标准适用于多种 AI 工具。Claude Code 在标准基础上扩展了调用控制、子代理执行和动态上下文注入等附加功能。

> **注意**：自定义斜杠命令已合并到 Skills 中。`.claude/commands/` 文件仍然可用且支持相同的 frontmatter 字段。推荐新开发使用 Skills。当两者同时存在于同一路径时（如 `.claude/commands/review.md` 和 `.claude/skills/review/SKILL.md`），Skill 优先。

## Skills 工作原理：渐进式加载

Skills 采用**渐进式披露（Progressive Disclosure）**架构——Claude 按需分阶段加载信息，而非预先消耗全部上下文。这实现了高效的上下文管理，同时保持无限的可扩展性。

### 三级加载机制

```mermaid
graph TB
    subgraph "Level 1: Metadata"
        A["YAML Frontmatter"]
        A1["~100 tokens per skill"]
        A2["name + description"]
    end

    subgraph "Level 2: Instructions"
        B["SKILL.md Body"]
        B1["Under 5k tokens"]
        B2["Workflows and guidance"]
    end

    subgraph "Level 3: Resources"
        C["Bundled Files"]
        C1["Effectively unlimited"]
        C2["Scripts, templates, docs"]
    end

    A --> B
    B --> C
```

| 级别 | 加载时机 | Token 开销 | 内容 |
|------|----------|-----------|------|
| **Level 1: 元数据** | 始终（启动时） | 每个 Skill 约 100 tokens | YAML frontmatter 中的 `name` 和 `description` |
| **Level 2: 指令** | Skill 被触发时 | 不超过 5k tokens | SKILL.md 正文中的指令和指导 |
| **Level 3+: 资源** | 按需 | 实际上无限制 | 通过 bash 执行的捆绑文件，不加载内容到上下文 |

这意味着你可以安装大量 Skills 而不会产生上下文开销——在被实际触发之前，Claude 只知道每个 Skill 的存在和使用时机。

## Skill 加载流程

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude
    participant System as System
    participant Skill as Skill

    User->>Claude: "Review this code for security issues"
    Claude->>System: Check available skills - metadata
    System-->>Claude: Skill descriptions loaded at startup
    Claude->>Claude: Match request to skill description
    Claude->>Skill: bash read code-review-SKILL.md
    Skill-->>Claude: Instructions loaded into context
    Claude->>Claude: Determine need templates
    Claude->>Skill: bash read templates-checklist.md
    Skill-->>Claude: Template loaded
    Claude->>Claude: Execute skill instructions
    Claude->>User: Comprehensive code review
```

## Skill 类型与位置

| 类型 | 位置 | 作用域 | 是否共享 | 最适用于 |
|------|--------|-------|---------|----------|
| **企业级** | 托管设置 | 所有组织用户 | 是 | 组织范围的标准 |
| **个人级** | `~/.claude/skills/<skill-name>/SKILL.md` | 个人 | 否 | 个人工作流 |
| **项目级** | `.claude/skills/<skill-name>/SKILL.md` | 团队 | 是（通过 git） | 团队规范 |
| **插件级** | `<plugin>/skills/<skill-name>/SKILL.md` | 启用处 | 取决于插件 | 随插件捆绑 |

当不同层级存在同名 Skill 时，高优先级位置获胜：**企业 > 个人 > 项目**。Plugin Skills 使用 `plugin-name:skill-name` 命名空间，不会冲突。

### 自动发现

**嵌套目录**：当你在子目录中工作时，Claude Code 会自动从嵌套的 `.claude/skills/` 目录中发现技能。例如，如果你正在编辑 `packages/frontend/` 中的文件，Claude Code 也会在 `packages/frontend/.claude/skills/` 中查找技能。这支持 monorepo 中各包拥有自己技能的场景。

**`--add-dir` 目录**：通过 `--add-dir` 添加的目录中的技能会自动加载，并支持实时变更检测。对这些目录中技能文件的任何修改都会立即生效，无需重启 Claude Code。

**描述预算**：Skill 描述（Level 1 元数据）上限为**上下文窗口的 1%**（回退值：**8,000 字符**）。如果安装了很多 Skill，描述可能会被截断。所有 Skill 名称始终包含，但描述会被裁剪以适配预算。在描述中将关键使用场景前置。可通过 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量覆盖此预算。

## 创建自定义 Skills

### 基本目录结构

```
my-skill/
├── SKILL.md           # 主指令文件（必需）
├── template.md        # Claude 填写的模板
├── examples/
│   └── sample.md      # 展示预期格式的示例输出
└── scripts/
    └── validate.sh    # Claude 可执行的脚本
```

### SKILL.md 格式

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

### 必填字段

- **name**：仅允许小写字母、数字、连字符（最多 64 个字符）。不能包含 "anthropic" 或 "claude"。
- **description**：Skill 的功能以及何时使用它（最多 1024 个字符）。这对 Claude 知道何时激活 Skill 至关重要。

### 可选 Frontmatter 字段

```yaml
---
name: my-skill
description: What this skill does and when to use it
argument-hint: "[filename] [format]"        # 自动补全提示
disable-model-invocation: true              # 仅用户可调用
user-invocable: false                       # 从斜杠菜单隐藏
allowed-tools: Read, Grep, Glob             # 限制工具访问
model: opus                                 # 指定使用的模型
effort: high                                # 努力级别覆盖（low、medium、high、max）
context: fork                               # 在隔离子代理中运行
agent: Explore                              # 子代理类型（配合 context: fork）
shell: bash                                 # 命令使用的 Shell：bash（默认）或 powershell
hooks:                                      # Skill 级别的 hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
paths: "src/api/**/*.ts"               # 限制 Skill 自动激活的 Glob 模式
---
```

| 字段 | 说明 |
|------|------|
| `name` | 仅允许小写字母、数字、连字符（最多 64 字符）。不能包含 "anthropic" 或 "claude"。 |
| `description` | Skill 的功能以及何时使用它（最多 1024 字符）。对自动调用匹配至关重要。 |
| `argument-hint` | 在 `/` 自动补全菜单中显示的提示（如 `"[filename] [format]"`）。 |
| `disable-model-invocation` | `true` = 仅用户可通过 `/name` 调用。Claude 永远不会自动调用。 |
| `user-invocable` | `false` = 从 `/` 菜单中隐藏。仅 Claude 可自动调用。 |
| `allowed-tools` | 逗号分隔的工具列表，Skill 使用这些工具时无需权限确认。 |
| `model` | Skill 激活期间的模型覆盖（如 `opus`、`sonnet`）。 |
| `effort` | Skill 激活期间的努力级别覆盖：`low`、`medium`、`high` 或 `max`。 |
| `context` | `fork` 在分叉的子代理上下文中运行 Skill，拥有独立的上下文窗口。 |
| `agent` | 当 `context: fork` 时的子代理类型（如 `Explore`、`Plan`、`general-purpose`）。 |
| `shell` | 用于 `` !`command` `` 替换和脚本的 Shell：`bash`（默认）或 `powershell`。 |
| `hooks` | 限定于此 Skill 生命周期的 hooks（格式与全局 hooks 相同）。 |
| `paths` | 限制 Skill 自动激活时机的 Glob 模式。逗号分隔字符串或 YAML 列表。格式同路径特定规则。 |

## Skill 内容类型

Skills 可以包含两种类型的内容，各自适用于不同目的：

### 参考型内容

向 Claude 添加适用于当前工作的知识——约定、模式、风格指南、领域知识。与对话上下文内联运行。

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

### 任务型内容

特定操作的逐步指令。通常通过 `/skill-name` 直接调用。

```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

## 控制 Skill 调用

默认情况下，你和 Claude 都可以调用任何 Skill。两个 frontmatter 字段控制三种调用模式：

| Frontmatter | 用户可调用 | Claude 可调用 |
|---|---|---|
| （默认） | 是 | 是 |
| `disable-model-invocation: true` | 是 | 否 |
| `user-invocable: false` | 否 | 是 |

对有副作用的 workflow 使用 **`disable-model-invocation: true`**：`/commit`、`/deploy`、`/send-slack-message`。你不希望 Claude 因为觉得代码看起来就绪就自行部署。

对不可作为命令操作的后台知识使用 **`user-invocable: false`**。`legacy-system-context` 类型的 Skill 解释旧系统如何运作——对 Claude 有用，但对用户来说不是有意义的操作。

## 字符串替换

Skills 支持在内容发送给 Claude 之前解析的动态值：

| 变量 | 说明 |
|------|------|
| `$ARGUMENTS` | 调用 Skill 时传入的所有参数 |
| `$ARGUMENTS[N]` 或 `$N` | 按索引访问特定参数（从 0 开始） |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |
| `${CLAUDE_SKILL_DIR}` | 包含 SKILL.md 文件的目录 |
| `` !`command` `` | 动态上下文注入——运行 shell 命令并将输出内联 |

**示例：**

```yaml
---
name: fix-issue
description: Fix a GitHub issue
---

Fix GitHub issue $ARGUMENTS following our coding standards.
1. Read the issue description
2. Implement the fix
3. Write tests
4. Create a commit
```

运行 `/fix-issue 123` 会将 `$ARGUMENTS` 替换为 `123`。

## 注入动态上下文

`` !`command` `` 语法在 Skill 内容发送给 Claude 之前运行 shell 命令：

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

命令立即执行；Claude 只看到最终输出。默认情况下命令在 `bash` 中运行。在 frontmatter 中设置 `shell: powershell` 可改用 PowerShell。

## 在子代理中运行 Skills

添加 `context: fork` 可在隔离的子代理上下文中运行 Skill。Skill 内容成为专用子代理的任务，拥有自己的上下文窗口，保持主对话整洁。

`agent` 字段指定要使用的代理类型：

| 代理类型 | 最适用于 |
|---|---|
| `Explore` | 只读研究、代码库分析 |
| `Plan` | 创建实现方案 |
| `general-purpose` | 需要全部工具的广泛任务 |
| 自定义 agents | 配置中定义的专用代理 |

**示例 frontmatter：**

```yaml
---
context: fork
agent: Explore
---
```

**完整 Skill 示例：**

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

## 实战示例

### 示例 ①：代码审查 Skill

**目录结构：**

```
~/.claude/skills/code-review/
├── SKILL.md
├── templates/
│   ├── review-checklist.md
│   └── finding-template.md
└── scripts/
    ├── analyze-metrics.py
    └── compare-complexity.py
```

**文件：** `~/.claude/skills/code-review/SKILL.md`

```yaml
---
name: code-review-specialist
description: Comprehensive code review with security, performance, and quality analysis. Use when users ask to review code, analyze code quality, evaluate pull requests, or mention code review, security analysis, or performance optimization.
---

# Code Review Skill

This skill provides comprehensive code review capabilities focusing on:

1. **Security Analysis**
   - Authentication/authorization issues
   - Data exposure risks
   - Injection vulnerabilities
   - Cryptographic weaknesses

2. **Performance Review**
   - Algorithm efficiency (Big O analysis)
   - Memory optimization
   - Database query optimization
   - Caching opportunities

3. **Code Quality**
   - SOLID principles
   - Design patterns
   - Naming conventions
   - Test coverage

4. **Maintainability**
   - Code readability
   - Function size (should be < 50 lines)
   - Cyclomatic complexity
   - Type safety

## Review Template

For each piece of code reviewed, provide:

### Summary
- Overall quality assessment (1-5)
- Key findings count
- Recommended priority areas

### Critical Issues (if any)
- **Issue**: Clear description
- **Location**: File and line number
- **Impact**: Why this matters
- **Severity**: Critical/High/Medium
- **Fix**: Code example

For detailed checklists, see [templates/review-checklist.md](templates/review-checklist.md).
```

### 示例 ②：代码库可视化 Skill

生成交互式 HTML 可视化的 Skill：

**目录结构：**

```
~/.claude/skills/codebase-visualizer/
├── SKILL.md
└── scripts/
    └── visualize.py
```

**文件：** `~/.claude/skills/codebase-visualizer/SKILL.md`

````yaml
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view showing your project's file structure.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

捆绑的 Python 脚本负责繁重工作，Claude 负责编排。

### 示例 ③：部署 Skill（仅用户调用）

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
allowed-tools: Bash(npm *), Bash(git *)
---

Deploy $ARGUMENTS to production:

1. Run the test suite: `npm test`
2. Build the application: `npm run build`
3. Push to the deployment target
4. Verify the deployment succeeded
5. Report deployment status
```

### 示例 ④：品牌语调 Skill（后台知识）

```yaml
---
name: brand-voice
description: Ensure all communication matches brand voice and tone guidelines. Use when creating marketing copy, customer communications, or public-facing content.
user-invocable: false
---

## Tone of Voice
- **Friendly but professional** - approachable without being casual
- **Clear and concise** - avoid jargon
- **Confident** - we know what we're doing
- **Empathetic** - understand user needs

## Writing Guidelines
- Use "you" when addressing readers
- Use active voice
- Keep sentences under 20 words
- Start with value proposition

For templates, see [templates/](templates/).
```

### 示例 ⑤：CLAUDE.md 生成器 Skill

```yaml
---
name: claude-md
description: Create or update CLAUDE.md files following best practices for optimal AI agent onboarding. Use when users mention CLAUDE.md, project documentation, or AI onboarding.
---

## Core Principles

**LLMs are stateless**: CLAUDE.md is the only file automatically included in every conversation.

### The Golden Rules

1. **Less is More**: Keep under 300 lines (ideally under 100)
2. **Universal Applicability**: Only include information relevant to EVERY session
3. **Don't Use Claude as a Linter**: Use deterministic tools instead
4. **Never Auto-Generate**: Craft it manually with careful consideration

## Essential Sections

- **Project Name**: Brief one-line description
- **Tech Stack**: Primary language, frameworks, database
- **Development Commands**: Install, test, build commands
- **Critical Conventions**: Only non-obvious, high-impact conventions
- **Known Issues / Gotchas**: Things that trip up developers
```

### 示例 ⑥：带脚本的重构 Skill

**目录结构：**

```
refactor/
├── SKILL.md
├── references/
│   ├── code-smells.md
│   └── refactoring-catalog.md
├── templates/
│   └── refactoring-plan.md
└── scripts/
    ├── analyze-complexity.py
    └── detect-smells.py
```

**文件：** `refactor/SKILL.md`

```yaml
---
name: code-refactor
description: Systematic code refactoring based on Martin Fowler's methodology. Use when users ask to refactor code, improve code structure, reduce technical debt, or eliminate code smells.
---

# Code Refactoring Skill

A phased approach emphasizing safe, incremental changes backed by tests.

## Workflow

Phase 1: Research and Analysis -> Phase 2: Test Coverage Assessment ->
Phase 3: Code Smell Identification -> Phase 4: Refactoring Plan Creation ->
Phase 5: Incremental Implementation -> Phase 6: Review and Iteration

## Core Principles

1. **Behavior Preservation**: External behavior must remain unchanged
2. **Small Steps**: Make tiny, testable changes
3. **Test-Driven**: Tests are the safety net
4. **Continuous**: Refactoring is ongoing, not a one-time event

For code smell catalog, see [references/code-smells.md](references/code-smells.md).
For refactoring techniques, see [references/refactoring-catalog.md](references/refactoring-catalog.md).
```

## 辅助文件

Skills 可以在目录中包含除 `SKILL.md` 外的多个文件。这些辅助文件（模板、示例、脚本、参考文档）让主 Skill 文件保持精简，同时为 Claude 提供按需加载的额外资源。

```
my-skill/
├── SKILL.md              # 主指令文件（必需，保持在 500 行以内）
├── templates/            # Claude 填写的模板
│   └── output-format.md
├── examples/             # 展示预期格式的示例输出
│   └── sample-output.md
├── references/           # 领域知识和规格说明
│   └── api-spec.md
└── scripts/              # Claude 可执行的脚本
    └── validate.sh
```

辅助文件编写指南：

- 保持 `SKILL.md` 在 **500 行以内**。将详细的参考资料、大型示例和规格说明移至单独文件。
- 从 `SKILL.md` 中使用**相对路径**引用额外文件（如 `[API reference](references/api-spec.md)`）。
- 辅助文件在 Level 3（按需）加载，因此在 Claude 实际读取之前不会消耗上下文。

## 管理 Skills

### 查看可用 Skills

直接询问 Claude：
```
What Skills are available?
```

或检查文件系统：
```bash
# 列出个人 Skills
ls ~/.claude/skills/

# 列出项目 Skills
ls .claude/skills/
```

### 测试 Skill

两种测试方式：

**让 Claude 自动调用**——提出与描述匹配的问题：
```
Can you help me review this code for security issues?
```

**或直接调用**——使用 Skill 名称：
```
/code-review src/auth/login.ts
```

### 更新 Skill

直接编辑 `SKILL.md` 文件。更改在下次 Claude Code 启动时生效。

```bash
# 个人 Skill
code ~/.claude/skills/my-skill/SKILL.md

# 项目 Skill
code .claude/skills/my-skill/SKILL.md
```

### 限制 Claude 的 Skill 访问

三种控制 Claude 可调用哪些 Skill 的方式：

**在 `/permissions` 中禁用所有 Skills**：
```
# Add to deny rules:
Skill
```

**允许或拒绝特定 Skills**：
```
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

**隐藏单个 Skill**——在其 frontmatter 中添加 `disable-model-invocation: true`。

## 最佳实践

### ① 让描述具体化

- **差（模糊）**："Helps with documents"
- **好（具体）**："Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

### ② 保持 Skill 聚焦

- 一个 Skill = 一种能力
- ✅ "PDF form filling"
- ❌ "Document processing"（太宽泛）

### ③ 包含触发词

在描述中添加匹配用户请求的关键词：
```yaml
description: Analyze Excel spreadsheets, generate pivot tables, create charts. Use when working with Excel files, spreadsheets, or .xlsx files.
```

### ④ 保持 SKILL.md 在 500 行以内

将详细参考资料移至单独文件，由 Claude 按需加载。

### ⑤ 引用辅助文件

```markdown
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

### 应该做的

- 使用清晰、描述性的名称
- 包含全面的指令
- 添加具体的示例
- 打包相关的脚本和模板
- 用真实场景测试
- 记录依赖关系

### 不应该做的

- 不要为一次性任务创建 Skills
- 不要重复已有功能
- 不要让 Skill 太宽泛
- 不要跳过 description 字段
- 不要未经审计就从不受信任的来源安装 Skills

## 故障排查

### 快速参考

| 问题 | 解决方案 |
|------|----------|
| Claude 不使用 Skill | 让描述更具体，加入触发词 |
| Skill 文件未找到 | 验证路径：`~/.claude/skills/name/SKILL.md` |
| YAML 错误 | 检查 `---` 标记、缩进、不要用 Tab |
| Skills 冲突 | 在描述中使用不同的触发词 |
| 脚本无法运行 | 检查权限：`chmod +x scripts/*.py` |
| Claude 看不到所有 Skills | Skills 太多；检查 `/context` 是否有警告 |

### Skill 未被触发

如果 Claude 在预期时没有使用你的 Skill：

1. 检查描述是否包含用户自然会说出的关键词
2. 验证询问 "What skills are available?" 时 Skill 是否出现
3. 尝试重新表述请求以匹配描述
4. 用 `/skill-name` 直接调用进行测试

### Skill 触发过于频繁

如果 Claude 在不需要时使用了你的 Skill：

1. 让描述更具体
2. 添加 `disable-model-invocation: true` 限制为仅手动调用

### Claude 看不到所有 Skills

Skill 描述加载上限为**上下文窗口的 1%**（回退值：**8,000 字符**）。无论预算多少，每条目上限 250 字符。运行 `/context` 检查是否有关于被排除 Skills 的警告。可通过 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量覆盖此预算。

## 安全注意事项

**只使用来自可信来源的 Skills。** Skills 通过指令和代码为 Claude 提供能力——恶意 Skill 可能引导 Claude 以有害方式调用工具或执行代码。

**关键安全考量：**
- **彻底审计**：审查 Skill 目录中的所有文件
- **外部来源有风险**：从外部 URL 获取的 Skill 可能被篡改
- **工具滥用**：恶意 Skill 可能以有害方式调用工具
- **视同安装软件**：只使用来自可信来源的 Skills

## Skills 与其他功能对比

| 功能 | 调用方式 | 最适用于 |
|------|---------|----------|
| **Skills** | 自动或 `/name` | 可复用的专业知识、工作流 |
| **斜杠命令** | 用户发起 `/name` | 快捷方式（已合并到 Skills） |
| **子代理** | 自动委派 | 隔离任务执行 |
| **记忆（CLAUDE.md）** | 始终加载 | 持久化项目上下文 |
| **MCP** | 实时 | 外部数据/服务访问 |
| **Hooks** | 事件驱动 | 自动化副作用 |

## 内置 Skills

Claude Code 附带了几个无需安装即可始终使用的内置 Skill：

| Skill | 说明 |
|-------|------|
| `/simplify` | 审查变更文件的复用性、质量和效率；启动 3 个并行审查代理 |
| `/batch <instruction>` | 使用 git worktree 在代码库中进行大规模并行变更编排 |
| `/debug [description]` | 通过读取调试日志排查当前会话问题 |
| `/loop [interval] <prompt>` | 按间隔重复执行提示（如 `/loop 5m check the deploy`） |
| `/claude-api` | 加载 Claude API/SDK 参考；在 `anthropic`/`@anthropic-ai/sdk` 导入时自动激活 |

这些内置 Skill 开箱即用，无需安装或配置。它们遵循与自定义 Skill 相同的 SKILL.md 格式。

## 分享 Skills

### 项目 Skills（团队共享）

1. 在 `.claude/skills/` 中创建 Skill
2. 提交到 git
3. 团队成员拉取变更——Skills 立即可用

### 个人 Skills

```bash
# 复制到个人目录
cp -r my-skill ~/.claude/skills/

# 使脚本可执行
chmod +x ~/.claude/skills/my-skill/scripts/*.py
```

### 插件分发

将 Skills 打包到插件的 `skills/` 目录中以进行更广泛的分发。

## 进阶资源：Skill 合集与 Skill 管理器

当你开始认真构建 Skills 后，两件事变得至关重要：一个经过验证的 Skill 库和一个管理工具。

**[luongnv89/skills](https://github.com/luongnv89/skills)** —— 我在几乎所有项目中日常使用的 Skill 合集。亮点包括 `logo-designer`（即时生成项目 logo）和 `ollama-optimizer`（针对你的硬件调优本地 LLM 性能）。如果你想要现成可用的 Skills，这是很好的起点。

**[luongnv89/asm](https://github.com/luongnv89/asm)** —— Agent Skill Manager。处理 Skill 开发、重复检测和测试。`asm link` 命令让你在任何项目中测试 Skill 而无需复制文件——当你拥有超过少量 Skills 时必不可少。

## 更多资源

- [官方 Skills 文档](https://code.claude.com/docs/en/skills)
- [Agent Skills 架构博客](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [Skills 仓库](https://github.com/luongnv89/skills) —— 即用型 Skill 合集
- [斜杠命令指南](../01-slash-commands/) —— 用户发起的快捷方式
- [子代理指南](../04-subagents/) —— 委托 AI 代理
- [记忆指南](../02-memory/) —— 持久化上下文
- [MCP（模型上下文协议）](../05-mcp/) —— 实时外部数据
- [Hooks 指南](../06-hooks/) —— 事件驱动自动化

---

*属于 [Claude How To](../) 指南系列*

---
**最后更新**: 2026 年 4 月
**Claude Code 版本**: 2.1+
**兼容模型**: Claude Sonnet 4.6, Claude Opus 4.6, Claude Haiku 4.5
