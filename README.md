<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

<p align="center">
  <a href="https://github.com/trending">
    <img src="https://img.shields.io/badge/GitHub-🔥%20%231%20Trending-purple?style=for-the-badge&logo=github"/>
  </a>
</p>

[![GitHub Stars](https://img.shields.io/github/stars/luongnv89/claude-howto?style=flat&color=gold)](https://github.com/luongnv89/claude-howto/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/luongnv89/claude-howto?style=flat)](https://github.com/luongnv89/claude-howto/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.2.0-brightgreen)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-2.1+-purple)](https://code.claude.com)

# 周末精通 Claude Code

从只会输入 `claude` 到熟练编排 agents(代理)、hooks(钩子)、skills(技能)和 MCP servers(服务器)----通过可视化教程、即拷即用的模板和引导式学习路径,助你快速进阶。

**[15 分钟快速上手](#15-分钟快速上手)** | **[找到你的水平](#不确定从哪里开始)** | **[浏览功能目录](CATALOG.md)**

---

## 目录

- [问题所在](#问题所在)
- [本指南如何解决这些问题](#本指南如何解决这些问题)
- [工作原理](#工作原理)
- [不确定从哪里开始?](#不确定从哪里开始)
- [15 分钟快速上手](#15-分钟快速上手)
- [你能用它构建什么?](#你能用它构建什么)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 问题所在

你安装了 Claude Code,试了几个 prompt,然后呢?

- **官方文档描述了各项功能----但没有告诉你如何组合使用。** 你知道 Slash Commands(斜杠命令)的存在,却不知道如何将它们与 hooks、memory 和 subagents 串联成真正能节省数小时的工作流。
- **没有清晰的学习路径。** 应该先学 MCP 还是 hooks?Skills 还是 subagents?结果你什么都浏览了一遍,什么都没精通。
- **示例太基础了。** 一个 "hello world" 级别的 slash command 帮不了你构建一个生产级的代码审查流水线----那种能利用 memory、委派给专用 agent、并自动运行安全扫描的流水线。

你正在浪费 Claude Code **90% 的能力**----而你甚至不知道自己不知道什么。

---

## 本指南如何解决这些问题

这不是又一份功能参考文档。这是一份**结构化的、可视化的、以示例驱动的指南**,它教你使用每一个 Claude Code 功能,并提供可直接复制到你项目中的真实模板。

| | 官方文档 | 本指南 |
|--|---------------|------------|
| **格式** | 参考文档 | 含 Mermaid 图表的可视化教程 |
| **深度** | 功能描述 | 内部工作原理 |
| **示例** | 基础代码片段 | 可直接使用的生产级模板 |
| **结构** | 按功能组织 | 渐进式学习路径(入门到高级) |
| **引导方式** | 自行探索 | 含时间估算的引导式路线图 |
| **自评机制** | 无 | 交互式测验,发现知识盲区并定制个性化路径 |

### 你将获得:

- **10 个教程模块**,覆盖所有 Claude Code 功能----从 Slash Commands 到自定义 Agent 团队
- **即拷即用的配置**----slash commands、CLAUDE.md 模板、hook 脚本、MCP 配置、subagent 定义以及完整的插件包
- **Mermaid 图表**展示每个功能的内部工作机制,让你不仅知道*怎么做*,更理解*为什么*
- **引导式学习路径**,在 11-13 小时内带你从新手成长为高手
- **内置自评机制**----在 Claude Code 中直接运行 `/self-assessment` 或 `/lesson-quiz` 来发现知识盲区

**[开始学习路径 →](LEARNING-ROADMAP.md)**

---

## 工作原理

### 1. 确定你的水平

参加[自评测验](LEARNING-ROADMAP.md#-find-your-level)或在 Claude Code 中运行 `/self-assessment`,根据你已有的知识获取个性化路线图。

### 2. 沿着引导路径学习

按顺序完成 10 个模块----每个模块都建立在前一个的基础上。边学边将模板直接复制到你的项目中。

### 3. 将功能组合为工作流

真正的力量在于组合功能。学会将 slash commands + memory + subagents + hooks 串联成自动化流水线,处理代码审查、部署和文档生成等任务。

### 4. 验证你的理解

每个模块完成后运行 `/lesson-quiz [主题]`。测验会精准定位你遗漏的知识点,帮你快速补齐短板。

**[15 分钟快速上手](#15-分钟快速上手)**

---

## 深受 5,900+ 开发者信赖

- **5,900+ GitHub Stars**----来自日常使用 Claude Code 的开发者们
- **690+ Forks**----各团队正在将此指南适配到自己的工作流中
- **积极维护**----与每次 Claude Code 发布同步更新(最新:v2.2.0,2026 年 3 月)
- **社区驱动**----来自开发者们分享的真实配置贡献

[![Star History Chart](https://api.star-history.com/svg?repos=luongnv89/claude-howto&type=Date)](https://star-history.com/#luongnv89/claude-howto&Date)

---

## 不确定从哪里开始?

参加自评测试或选择你的水平:

| 水平 | 你已经可以... | 从这里开始 | 所需时间 |
|-------|-----------|------------|------|
| **初学者(Beginner)** | 启动 Claude Code 并对话 | [Slash Commands(斜杠命令)](01-slash-commands/) | 约 2.5 小时 |
| **中级(Intermediate)** | 使用 CLAUDE.md 和自定义命令 | [Skills(技能)](03-skills/) | 约 3.5 小时 |
| **高级(Advanced)** | 配置 MCP servers 和 hooks | [Advanced Features(高级功能)](09-advanced-features/) | 约 5 小时 |

**包含全部 10 个模块的完整学习路径:**

| 序号 | 模块 | 难度 | 时间 |
|-------|--------|-------|------|
| 1 | [Slash Commands(斜杠命令)](01-slash-commands/) | 初学者 | 30 分钟 |
| 2 | [Memory(记忆)](02-memory/) | 初学者+ | 45 分钟 |
| 3 | [Checkpoints(检查点)](08-checkpoints/) | 中级 | 45 分钟 |
| 4 | [CLI Basics(命令行基础)](10-cli/) | 初学者+ | 30 分钟 |
| 5 | [Skills(技能)](03-skills/) | 中级 | 1 小时 |
| 6 | [Hooks(钩子)](06-hooks/) | 中级 | 1 小时 |
| 7 | [MCP(模型上下文协议)](05-mcp/) | 中级+ | 1 小时 |
| 8 | [Subagents(子代理)](04-subagents/) | 中级+ | 1.5 小时 |
| 9 | [Advanced Features(高级功能)](09-advanced-features/) | 高级 | 2-3 小时 |
| 10 | [Plugins(插件)](07-plugins/) | 高级 | 2 小时 |

**[完整学习路线图 →](LEARNING-ROADMAP.md)**

---

## 15 分钟快速上手

```bash
# 1. 克隆本指南
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# 2. 复制你的第一个斜杠命令
mkdir -p /path/to/your-project/.claude/commands
cp 01-slash-commands/optimize.md /path/to/your-project/.claude/commands/

# 3. 试试看----在 Claude Code 中输入:
# /optimize

# 4. 想要更多?设置项目记忆:
cp 02-memory/project-CLAUDE.md /path/to/your-project/CLAUDE.md

# 5. 安装一个技能:
cp -r 03-skills/code-review ~/.claude/skills/
```

想要完整设置?这是 **1 小时核心配置**:

```bash
# 斜杠命令(15 分钟)
cp 01-slash-commands/*.md .claude/commands/

# 项目记忆(15 分钟)
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 安装一个技能(15 分钟)
cp -r 03-skills/code-review ~/.claude/skills/

# 周末目标:添加 hooks、subagents、MCP 和 plugins
# 按照学习路径进行引导式配置
```

**[查看完整安装参考](#15-分钟快速上手)**

---

## 你能用它构建什么?

| 使用场景 | 你需要组合的功能 |
|----------|------------------------|
| **自动化代码审查** | Slash Commands + Subagents + Memory + MCP |
| **团队入职引导** | Memory + Slash Commands + Plugins |
| **CI/CD 自动化** | CLI Reference + Hooks + Background Tasks |
| **文档自动生成** | Skills + Subagents + Plugins |
| **安全审计** | Subagents + Skills + Hooks(只读模式) |
| **DevOps 流水线** | Plugins + MCP + Hooks + Background Tasks |
| **复杂重构** | Checkpoints + Planning Mode + Hooks |

---

## 常见问题

**这个项目免费吗?**
是的。MIT 许可证授权,永久免费。可用于个人项目、工作中或团队内部----唯一的要求是保留许可声明。

**这个项目还在维护吗?**
是的,积极维护中。本指南与每次 Claude Code 发布同步更新。当前版本:v2.2.0(2026 年 3 月),兼容 Claude Code 2.1+。

**它和官方文档有什么区别?**
官方文档是功能参考手册。本指南是包含图表、生产级模板和渐进式学习路径的教程。两者互为补充----从这里开始学习,需要具体细节时查阅官方文档。

**学完所有内容需要多长时间?**
完整路径需要 11-13 小时。但你在 15 分钟内就能获得实际价值----只需复制一个 slash command 模板试试看。

**我可以在 Claude Sonnet / Haiku / Opus 上使用吗?**
可以。所有模板均兼容 Claude Sonnet 4.6、Claude Opus 4.6 和 Claude Haiku 4.5。

**我可以参与贡献吗?**
当然!请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。我们欢迎新示例、Bug 修复、文档改进和社区模板。

**我可以离线阅读吗?**
可以。运行 `uv run scripts/build_epub.py` 即可生成包含所有内容和已渲染图表的 EPUB 电子书。

---

## 今天就开始精通 Claude Code

你已经安装了 Claude Code。阻碍你实现 10 倍效率提升的,只是不知道如何使用它而已。本指南为你提供结构化的路径、可视化的解释和即拷即用的模板,助你达成目标。

MIT 许可证授权。永久免费。克隆它、Fork 它、让它成为你自己的。

**[开始学习路径 →](LEARNING-ROADMAP.md)** | **[浏览功能目录](CATALOG.md)** | **[15 分钟快速上手](#15-分钟快速上手)**

---

<details>
<summary>快速导航 ---- 全部功能</summary>

| 功能 | 说明 | 目录 |
|---------|-------------|--------|
| **功能目录** | 包含安装命令的完整参考 | [CATALOG.md](CATALOG.md) |
| **Slash Commands(斜杠命令)** | 用户手动触发的快捷命令 | [01-slash-commands/](01-slash-commands/) |
| **Memory(记忆)** | 持久化上下文 | [02-memory/](02-memory/) |
| **Skills(技能)** | 可复用的能力 | [03-skills/](03-skills/) |
| **Subagents(子代理)** | 专用 AI 助手 | [04-subagents/](04-subagents/) |
| **MCP Protocol(模型上下文协议)** | 访问外部工具 | [05-mcp/](05-mcp/) |
| **Hooks(钩子)** | 事件驱动自动化 | [06-hooks/](06-hooks/) |
| **Plugins(插件)** | 打包的功能集合 | [07-plugins/](07-plugins/) |
| **Checkpoints(检查点)** | 会话快照与回退 | [08-checkpoints/](08-checkpoints/) |
| **Advanced Features(高级功能)** | 规划、思考、后台任务 | [09-advanced-features/](09-advanced-features/) |
| **CLI Reference(命令行参考)** | 命令、标志和选项 | [10-cli/](10-cli/) |
| **博客文章** | 真实使用案例 | [博客文章](https://medium.com/@luongnv89) |

</details>

<details>
<summary>功能对比</summary>

| 功能 | 触发方式 | 持久性 | 最适用场景 |
|---------|-----------|------------|----------|
| **Slash Commands(斜杠命令)** | 手动 (`/cmd`) | 仅当前会话 | 快捷操作 |
| **Memory(记忆)** | 自动加载 | 跨会话 | 长期学习积累 |
| **Skills(技能)** | 自动调用 | 文件系统 | 自动化工作流 |
| **Subagents(子代理)** | 自动委派 | 隔离上下文 | 任务分发 |
| **MCP Protocol(模型上下文协议)** | 自动查询 | 实时 | 实时数据访问 |
| **Hooks(钩子)** | 事件触发 | 已配置 | 自动化与校验 |
| **Plugins(插件)** | 一条命令 | 全部功能 | 完整解决方案 |
| **Checkpoints(检查点)** | 手动/自动 | 基于会话 | 安全实验 |
| **Planning Mode(规划模式)** | 手动/自动 | 规划阶段 | 复杂实现 |
| **Background Tasks(后台任务)** | 手动 | 任务周期 | 长时间运行的操作 |
| **CLI Reference(命令行参考)** | 终端命令 | 会话/脚本 | 自动化与脚本编程 |

</details>

<details>
<summary>安装快速参考</summary>

```bash
# Slash Commands(斜杠命令)
cp 01-slash-commands/*.md .claude/commands/

# Memory(记忆)
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# Skills(技能)
cp -r 03-skills/code-review ~/.claude/skills/

# Subagents(子代理)
cp 04-subagents/*.md .claude/agents/

# MCP(模型上下文协议)
export GITHUB_TOKEN="token"
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Hooks(钩子)
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# Plugins(插件)
/plugin install pr-review

# Checkpoints(检查点)(默认启用,在 settings 中配置)
# 详细说明参见 08-checkpoints/README.md

# Advanced Features(高级功能)(在 settings 中配置)
# 详细说明参见 09-advanced-features/config-examples.json

# CLI Reference(命令行参考)(无需安装)
# 使用示例参见 10-cli/README.md
```

</details>

<details>
<summary>01. Slash Commands(斜杠命令)</summary>

**位置**:[01-slash-commands/](01-slash-commands/)

**是什么**:存储为 Markdown 文件的用户手动触发的快捷命令

**示例**:
- `optimize.md` - 代码优化分析
- `pr.md` - Pull Request 准备
- `generate-api-docs.md` - API 文档生成器

**安装**:
```bash
cp 01-slash-commands/*.md /path/to/project/.claude/commands/
```

**使用方法**:
```
/optimize
/pr
/generate-api-docs
```

**了解更多**:[探索 Claude Code 斜杠命令](https://medium.com/@luongnv89/discovering-claude-code-slash-commands-cdc17f0dfb29)

</details>

<details>
<summary>02. Memory(记忆)</summary>

**位置**:[02-memory/](02-memory/)

**是什么**:跨会话持久化的上下文信息

**示例**:
- `project-CLAUDE.md` - 团队级别的项目规范
- `directory-api-CLAUDE.md` - 特定目录的规则
- `personal-CLAUDE.md` - 个人偏好设置

**安装**:
```bash
# 项目级记忆
cp 02-memory/project-CLAUDE.md /path/to/project/CLAUDE.md

# 目录级记忆
cp 02-memory/directory-api-CLAUDE.md /path/to/project/src/api/CLAUDE.md

# 个人级记忆
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

**使用方法**:由 Claude 自动加载

</details>

<details>
<summary>03. Skills(技能)</summary>

**位置**:[03-skills/](03-skills/)

**是什么**:可复用、自动调用的能力,包含指令和脚本

**示例**:
- `code-review/` - 带脚本的全面代码审查
- `brand-voice/` - 品牌语调一致性检查
- `doc-generator/` - API 文档生成器

**安装**:
```bash
# 个人技能
cp -r 03-skills/code-review ~/.claude/skills/

# 项目技能
cp -r 03-skills/code-review /path/to/project/.claude/skills/
```

**使用方法**:在相关场景下自动调用

</details>

<details>
<summary>04. Subagents(子代理)</summary>

**位置**:[04-subagents/](04-subagents/)

**是什么**:具有隔离上下文和自定义提示词的专用 AI 助手

**示例**:
- `code-reviewer.md` - 全面的代码质量分析
- `test-engineer.md` - 测试策略与覆盖率
- `documentation-writer.md` - 技术文档撰写
- `secure-reviewer.md` - 安全专项审查(只读模式)
- `implementation-agent.md` - 完整功能实现

**安装**:
```bash
cp 04-subagents/*.md /path/to/project/.claude/agents/
```

**使用方法**:由主 agent 自动委派任务

</details>

<details>
<summary>05. MCP Protocol(模型上下文协议)</summary>

**位置**:[05-mcp/](05-mcp/)

**是什么**:用于访问外部工具和 API 的 Model Context Protocol(模型上下文协议)

**示例**:
- `github-mcp.json` - GitHub 集成
- `database-mcp.json` - 数据库查询
- `filesystem-mcp.json` - 文件操作
- `multi-mcp.json` - 多个 MCP 服务器

**安装**:
```bash
# 设置环境变量
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 通过 CLI 添加 MCP server
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# 或手动添加到项目的 .mcp.json(示例参见 05-mcp/)
```

**使用方法**:配置完成后,MCP 工具对 Claude 自动可用

</details>

<details>
<summary>06. Hooks(钩子)</summary>

**位置**:[06-hooks/](06-hooks/)

**是什么**:响应 Claude Code 事件而自动执行的事件驱动型 Shell 命令

**示例**:
- `format-code.sh` - 写入代码前自动格式化
- `pre-commit.sh` - 提交前运行测试
- `security-scan.sh` - 安全问题扫描
- `log-bash.sh` - 记录所有 bash 命令
- `validate-prompt.sh` - 校验用户输入
- `notify-team.sh` - 事件发生时发送通知

**安装**:
```bash
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

在 `~/.claude/settings.json` 中配置 hooks:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write",
      "hooks": ["~/.claude/hooks/format-code.sh"]
    }],
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": ["~/.claude/hooks/security-scan.sh"]
    }]
  }
}
```

**使用方法**:Hooks 在事件触发时自动执行

**Hook 类型**(4 大类,25 种事件):
- **Tool Hooks(工具钩子)**:`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`
- **Session Hooks(会话钩子)**:`SessionStart`、`SessionEnd`、`Stop`、`StopFailure`、`SubagentStart`、`SubagentStop`
- **Task Hooks(任务钩子)**:`UserPromptSubmit`、`TaskCompleted`、`TaskCreated`、`TeammateIdle`
- **Lifecycle Hooks(生命周期钩子)**:`ConfigChange`、`CwdChanged`、`FileChanged`、`PreCompact`、`PostCompact`、`WorktreeCreate`、`WorktreeRemove`、`Notification`、`InstructionsLoaded`、`Elicitation`、`ElicitationResult`

</details>

<details>
<summary>07. Plugins(插件)</summary>

**位置**:[07-plugins/](07-plugins/)

**是什么**:打包集合的 commands、agents、MCP 和 hooks

**示例**:
- `pr-review/` - 完整的 PR 审查工作流
- `devops-automation/` - 部署与监控
- `documentation/` - 文档生成

**安装**:
```bash
/plugin install pr-review
/plugin install devops-automation
/plugin install documentation
```

**使用方法**:使用捆绑的 slash commands 和功能

</details>

<details>
<summary>08. Checkpoints 与 Rewind(检查点与回退)</summary>

**位置**:[08-checkpoints/](08-checkpoints/)

**是什么**:保存对话状态并回退到之前的节点,以便探索不同的实现方案

**核心概念**:
- **Checkpoint(检查点)**:对话状态的快照
- **Rewind(回退)**:返回到之前的检查点
- **Branch Point(分支点)**:从同一检查点探索多种方案

**使用方法**:
```
# 每次用户输入时会自动创建检查点
# 要回退,按两次 Esc 或使用:
/rewind

# 然后从五个选项中选择:
# 1. 恢复代码和对话
# 2. 仅恢复对话
# 3. 仅恢复代码
# 4. 从此处总结
# 5. 算了
```

**适用场景**:
- 尝试不同的实现方案
- 从错误中恢复
- 安全地进行实验
- 对比替代方案
- 不同设计的 A/B 测试

</details>

<details>
<summary>09. Advanced Features(高级功能)</summary>

**位置**:[09-advanced-features/](09-advanced-features/)

**是什么**:用于复杂工作流和自动化场景的高级能力

**包括**:
- **Planning Mode(规划模式)** -- 编码前创建详细的实现计划
- **Extended Thinking(扩展思考)** -- 复杂问题的深度推理(使用 `Alt+T` / `Option+T` 切换)
- **Background Tasks(后台任务)** -- 运行长时间操作而不阻塞
- **Permission Modes(权限模式)** -- `default`、`acceptEdits`、`plan`、`dontAsk`、`bypassPermissions`
- **Headless Mode(无头模式)** -- 在 CI/CD 中运行 Claude Code:`claude -p "Run tests and generate report"`
- **Session Management(会话管理)** -- `/resume`、`/rename`、`/fork`、`claude -c`、`claude -r`
- **Configuration(配置)** -- 在 `~/.claude/settings.json` 中自定义行为

完整配置请参考 [config-examples.json](09-advanced-features/config-examples.json)。

</details>

<details>
<summary>10. CLI Reference(命令行参考)</summary>

**位置**:[10-cli/](10-cli/)

**是什么**:Claude Code 完整的命令行界面参考

**快速示例**:
```bash
# 交互模式
claude "explain this project"

# 打印模式(非交互式)
claude -p "review this code"

# 处理文件内容
cat error.log | claude -p "explain this error"

# JSON 格式输出(用于脚本)
claude -p --output-format json "list functions"

# 恢复会话
claude -r "feature-auth" "continue implementation"
```

**适用场景**:CI/CD 流水线集成、脚本自动化、批处理、多会话工作流、自定义 agent 配置

</details>

<details>
<summary>示例工作流</summary>

### 完整代码审查工作流

```markdown
# 使用功能:Slash Commands + Subagents + Memory + MCP

用户: /review-pr

Claude:
1. 加载项目记忆(编码规范)
2. 通过 GitHub MCP 获取 PR 信息
3. 委派给 code-reviewer 子代理
4. 委派给 test-engineer 子代理
5. 综合分析结果
6. 提供全面的审查报告
```

### 自动化文档生成

```markdown
# 使用功能:Skills + Subagents + Memory

用户: "Generate API documentation for the auth module"

Claude:
1. 加载项目记忆(文档标准)
2. 检测到文档生成请求
3. 自动调用 doc-generator 技能
4. 委派给 api-documenter 子代理
5. 创建带示例的完整文档
```

### DevOps 部署

```markdown
# 使用功能:Plugins + MCP + Hooks

用户: /deploy production

Claude:
1. 运行部署前 hook(验证环境)
2. 委派给 deployment-specialist 子代理
3. 通过 Kubernetes MCP 执行部署
4. 监控进度
5. 运行部署后 hook(健康检查)
6. 报告状态
```

</details>

<details>
<summary>目录结构</summary>

```
├── 01-slash-commands/
│   ├── optimize.md
│   ├── pr.md
│   ├── generate-api-docs.md
│   └── README.md
├── 02-memory/
│   ├── project-CLAUDE.md
│   ├── directory-api-CLAUDE.md
│   ├── personal-CLAUDE.md
│   └── README.md
├── 03-skills/
│   ├── code-review/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── templates/
│   ├── brand-voice/
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── doc-generator/
│   │   ├── SKILL.md
│   │   └── generate-docs.py
│   └── README.md
├── 04-subagents/
│   ├── code-reviewer.md
│   ├── test-engineer.md
│   ├── documentation-writer.md
│   ├── secure-reviewer.md
│   ├── implementation-agent.md
│   └── README.md
├── 05-mcp/
│   ├── github-mcp.json
│   ├── database-mcp.json
│   ├── filesystem-mcp.json
│   ├── multi-mcp.json
│   └── README.md
├── 06-hooks/
│   ├── format-code.sh
│   ├── pre-commit.sh
│   ├── security-scan.sh
│   ├── log-bash.sh
│   ├── validate-prompt.sh
│   ├── notify-team.sh
│   └── README.md
├── 07-plugins/
│   ├── pr-review/
│   ├── devops-automation/
│   ├── documentation/
│   └── README.md
├── 08-checkpoints/
│   ├── checkpoint-examples.md
│   └── README.md
├── 09-advanced-features/
│   ├── config-examples.json
│   ├── planning-mode-examples.md
│   └── README.md
├── 10-cli/
│   └── README.md
└── README.md(本文件)
```

</details>

<details>
<summary>最佳实践</summary>

### 推荐做法
- 从简单的 slash commands 开始
- 逐步增量地添加功能
- 用 memory 来管理团队规范
- 先在本地测试配置
- 记录自定义实现
- 对项目配置进行版本控制
- 与团队共享 plugins

### 避免事项
- 不要创建冗余功能
- 不要硬编码凭证
- 不要跳过文档编写
- 不要把简单任务复杂化
- 不要忽视安全最佳实践
- 不要提交敏感数据

</details>

<details>
<summary>故障排除</summary>

### 功能未加载
1. 检查文件位置和命名
2. 验证 YAML frontmatter 语法
3. 检查文件权限
4. 确认 Claude Code 版本兼容性

### MCP 连接失败
1. 验证环境变量
2. 检查 MCP server 是否正确安装
3. 测试凭证是否有效
4. 检查网络连接

### Subagent 未被委派任务
1. 检查工具权限
2. 验证 agent 描述是否清晰
3. 审查任务复杂度
4. 独立测试 agent

</details>

<details>
<summary>测试</summary>

本项目包含全面的自动化测试:

- **单元测试**:使用 pytest 的 Python 测试(Python 3.10、3.11、3.12)
- **代码质量**:使用 Ruff 进行代码检查和格式化
- **安全扫描**:使用 Bandit 进行漏洞扫描
- **类型检查**:使用 mypy 进行静态类型分析
- **构建验证**:EPUB 生成测试
- **覆盖率跟踪**:Codecov 集成

```bash
# 安装开发依赖
uv pip install -r requirements-dev.txt

# 运行所有单元测试
pytest scripts/tests/ -v

# 运行测试并生成覆盖率报告
pytest scripts/tests/ -v --cov=scripts --cov-report=html

# 运行代码质量检查
ruff check scripts/
ruff format --check scripts/

# 运行安全扫描
bandit -c pyproject.toml -r scripts/ --exclude scripts/tests/

# 运行类型检查
mypy scripts/ --ignore-missing-imports
```

测试会在每次推送到 `main`/`develop` 分支以及每个向 `main` 提交的 PR 上自动运行。详细信息请参阅 [TESTING.md](.github/TESTING.md)。

</details>

<details>
<summary>EPUB 电子书生成</summary>

想离线阅读本指南?生成 EPUB 电子书:

```bash
uv run scripts/build_epub.py
```

这将创建 `claude-howto-guide.epub`,包含所有内容和已渲染的 Mermaid 图表。

更多选项请参阅 [scripts/README.md](scripts/README.md)。

</details>

<details>
<summary>贡献指南</summary>

发现了问题或想贡献示例?我们需要你的帮助!

**请详细阅读 [CONTRIBUTING.md](CONTRIBUTING.md),了解以下内容:**
- 贡献类型(示例、文档、功能、Bug 反馈等)
- 如何搭建开发环境
- 目录结构和如何添加内容
- 编写指南和最佳实践
- Commit 和 PR 流程

**我们的社区准则:**
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - 社区行为准则
- [SECURITY.md](SECURITY.md) - 安全政策和漏洞报告流程

### 报告安全问题

如果你发现了安全漏洞,请负责任地报告:

1. **使用 GitHub 私有漏洞报告**:https://github.com/luongnv89/claude-howto/security/advisories
2. **或阅读** [.github/SECURITY_REPORTING.md](.github/SECURITY_REPORTING.md) 获取详细指引
3. **切勿**就安全漏洞公开提 Issue

快速起步:
1. Fork 并克隆仓库
2. 创建有意义的分支(`add/feature-name`、`fix/bug`、`docs/improvement`)
3. 按照指南进行修改
4. 提交清晰的 PR 描述

**需要帮助?** 提出 Issue 或讨论,我们会引导你完成整个流程。

</details>

<details>
<summary>补充资源</summary>

- [Claude Code 官方文档](https://code.claude.com/docs/en/overview)
- [MCP 协议规范](https://modelcontextprotocol.io)
- [Skills 技能仓库](https://github.com/luongnv89/skills) - 即用型技能合集
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Boris Cherny 的 Claude Code 工作流](https://x.com/bcherny/status/2007179832300581177) - Claude Code 创建者分享的系统化工作流:并行 agents、共享 CLAUDE.md、Plan 模式、slash commands、subagents 以及用于自主长时间运行的验证 hooks。

</details>

---

## 贡献指南

我们欢迎贡献!详情请参阅我们的[贡献指南](CONTRIBUTING.md)。

## 贡献者

感谢每一位为本项目做出贡献的人!

| 贡献者 | PR |
|-------------|-----|
| [wjhrdy](https://github.com/wjhrdy) | [#1 - 添加 EPUB 生成工具](https://github.com/luongnv89/claude-howto/pull/1) |
| [VikalpP](https://github.com/VikalpP) | [#7 - 修复文档:概念指南中嵌套代码块使用波浪线围栏](https://github.com/luongnv89/claude-howto/pull/7) |

---

## 许可证

MIT 许可证----详见 [LICENSE](LICENSE)。可自由使用、修改和分发。唯一要求是保留许可声明。

---

**最后更新**:2026 年 3 月
**Claude Code 版本**:2.1+
**兼容模型**:Claude Sonnet 4.6、Claude Opus 4.6、Claude Haiku 4.5
