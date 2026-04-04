<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Subagents（子代理）— 完整参考指南

Subagents 是 Claude Code 可以委派任务给它的专用 AI 助手。每个子代理都有特定用途，使用独立于主对话的上下文窗口，并可配置特定的工具和自定义系统提示词。

## 概览

Subagents 通过以下方式实现 Claude Code 中的委派式任务执行：

- 创建具有**独立上下文窗口**的隔离 AI 助手
- 提供用于**专业化能力的定制系统提示词**
- 强制执行**工具访问控制**以限制能力
- 防止复杂任务造成的**上下文污染**
- 实现**多个专业任务的并行执行**

每个子代理以干净的状态独立运行，仅接收其任务所需的特定上下文，然后将结果返回给主代理进行综合。

**快速开始**：使用 `/agents` 命令以交互方式创建、查看、编辑和管理你的子代理。

## 核心优势

| 优势 | 说明 |
|------|------|
| **上下文隔离** | 在独立的上下文中运行，避免污染主对话 |
| **专业化能力** | 针对特定领域微调，成功率更高 |
| **可复用性** | 跨不同项目使用并与团队共享 |
| **灵活权限** | 不同子代理类型可配置不同的工具访问级别 |
| **可扩展性** | 多个代理可同时处理不同方面的工作 |

## 文件位置

子代理文件可存储在多个位置，对应不同的作用域：

| 优先级 | 类型 | 位置 | 作用域 |
|--------|------|--------|-------|
| 1（最高） | **CLI 定义** | 通过 `--agents` 标志（JSON 格式） | 仅当前会话 |
| 2 | **项目子代理** | `.claude/agents/` | 当前项目 |
| 3 | **用户子代理** | `~/.claude/agents/` | 所有项目 |
| 4（最低） | **插件代理** | 插件的 `agents/` 目录 | 通过插件 |

当存在重名时，高优先级的源优先。

## 配置

### 文件格式

子代理通过 YAML frontmatter 定义元数据，后跟 Markdown 格式的系统提示词：

```yaml
---
name: your-sub-agent-name
description: 该子代理被调用场景的描述
tools: tool1, tool2, tool3  # 可选 - 省略时继承所有工具
disallowedTools: tool4  # 可选 - 明确禁止的工具
model: sonnet  # 可选 - sonnet, opus, haiku, 或继承当前模型
permissionMode: default  # 可选 - 权限模式
maxTurns: 20  # 可选 - 限制代理轮次
skills: skill1, skill2  # 可选 - 预加载到上下文的技能
mcpServers: server1  # 可选 - 使其可用的 MCP 服务器
memory: user  # 可选 - 持久化记忆范围（user, project, local）
background: false  # 可选 - 作为后台任务运行
effort: high  # 可选 - 推理努力级别（low, medium, high, max）
---

# 系统提示词
你是一个专业的 [角色描述]...

## 你的职责
...
```

### 配置字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 子代理标识符 |
| `description` | string | 功能描述（用于自动匹配委派） |
| `model` | string | 模型覆盖（如 `haiku-4.5`） |
| `tools` | array | 允许使用的工具列表 |
| `disallowedTools` | array | 明确禁止的工具列表 |
| `effort` | string | 推理努力级别：`low`、`medium`、`high`、`max` |
| `initialPrompt` | string | 代理启动时注入的系统提示词 |
| `maxTurns` | number | 最大轮次限制 |

## 内置子代理

Claude Code 内置了 6 个预配置子代理：

| 代理 | 说明 | 工具 | 模型 | 适用场景 |
|------|--------|------|------|----------|
| **general-purpose** | 多步骤任务、研究 | 全部工具 | 继承当前模型 | 复杂研究、多文件任务 |
| **Plan** | 实现规划 | Read, Glob, Grep, Bash | 继承当前模型 | 架构设计、规划方案 |
| **Explore** | 代码库探索 | Read, Glob, Grep | Haiku 4.5 | 快速搜索、理解代码 |
| **Bash** | 命令执行 | Bash | 继承当前模型 | Git 操作、终端任务 |
| **statusline-setup** | 状态栏配置 | Bash, Read, Write | Sonnet 4.6 | 配置状态栏显示 |
| **Claude Code Guide** | 帮助和文档 | Read, Glob, Grep | Haiku 4.5 | 获取帮助、学习功能 |

## 使用子代理

### 自动委派

Claude 会根据请求内容自动选择合适的子代理。你可以通过描述来触发委派：

```markdown
用户: "审查这段代码的安全性"
→ Claude 委派给 code-reviewer 子代理

用户: "为这个 API 编写测试"
→ Claude 委派给 test-engineer 子代理
```

### 手动指定

你也可以明确指定使用某个子代理：
```markdown
用户: "让 debugger 代理分析这个错误"
```

## 最佳实践

✅ **推荐做法**：
- 为每个子代理编写清晰的 description 以便正确匹配
- 使用 `disallowedTools` 限制敏感操作（如安全审查者不应有 Write 权限）
- 合理使用 `model` 字段——简单任务用 Haiku 节省成本
- 利用 `memory` 字段控制子代理的上下文范围

❌ **避免事项**：
- 不要创建功能重叠的子代理
- 不要忽略 `maxTurns` 设置——防止无限循环
- 不要在子代理中放入过多上下文

> 💡 **中文开发者提示**：子代理是处理复杂任务的利器。最实用的组合是：主代理负责协调 → code-reviewer 负责代码质量 → test-engineer 负责测试策略 → documentation-writer 负责文档输出。这种"流水线"式的委派模式可以大幅提升工作效率。

---

**最后更新**：2026 年 3 月
