<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg" width="120">
</picture>

<p align="center">
  <a href="https://github.com/trending">
    <img src="https://img.shields.io/badge/GitHub-🔥%20中文翻译-purple?style=for-the-badge&logo=github"/>
  </a>
</p>

[![原项目 Stars](https://img.shields.io/github/stars/luongnv89/claude-howto?style=flat&color=gold)](https://github.com/luongnv89/claude-howto/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![翻译版本](https://img.shields.io/badge/version-v2.2.0-brightgreen)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-2.1+-purple)](https://code.claude.com)

# Claude How To — 中文翻译版

> **基于** [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto) 的完整中文翻译
>
> **v2.2.0** · **与官方结构 1:1 对齐**

**[15 分钟快速开始](#快速开始)** | [**找到你的水平**](#不确定从哪里开始)** | [**浏览功能目录**](CATALOG.md)**

---

## 目录

- [简介](#简介)
- [为什么需要这个翻译版？](#为什么需要这个翻译版)
- [如何使用](#如何使用)
- [不确定从哪里开始？](#不确定从哪里开始)
- [快速开始](#快速开始)
- [你能用它做什么？](#你能用它做什么)
- [翻译范围](#翻译范围)
- [常见问题](#常见问题)

---

## 简介

你安装了 Claude Code，跑了几条命令，然后呢？

- **官方文档描述了功能 —— 但没告诉你怎么组合使用。** 你知道斜杠命令存在，但不知道怎么把它和钩子、记忆、子代理组合成真正能省时间的工作流。
- **没有清晰的学习路径。** 应该先学 MCP 还是先学 Hooks？Skills 在 Subagents 前面还是后面？结果你什么都略读了一遍，什么都没精通。
- **示例太基础。** 一个 "hello world" 斜杠命令帮不了你搭建一个能自动做代码审查、安全扫描的生产级流水线。

你在浪费 Claude Code 90% 的能力 —— 而你自己还不知道。

---

## 为什么需要这个翻译版？

| | 官方文档 | 本指南（中文） |
|--|---------|---------------|
| **格式** | 参考文档 | 含 Mermaid 图表的可视化教程 |
| **深度** | 功能描述 | 内部原理 + 工作机制 |
| **示例** | 基础代码片段 | 可直接使用的生产级模板 |
| **结构** | 按功能组织 | 渐进式学习路径（入门→高级） |
| **引导方式** | 自行探索 | 有路线图 + 时间估算 + 自测 |
| **语言** | 英文 | **中文 + 专业术语英文注释** |

### 你将获得：

- **10 大教程模块**，覆盖 Claude Code 每个功能 —— 从斜杠命令到自定义 Agent 团队
- **开箱即用的配置模板** —— 斜杠命令、CLAUDE.md 模板、钩子脚本、MCP 配置、子代理定义、完整插件包
- **Mermaid 图表** 展示每个功能的内部工作原理，让你不仅知其然更知其所以然
- **渐进式学习路径**，带你从入门到高手（11-13 小时）
- **内置自评测验** —— 直接在 Claude Code 中运行 `/self-assessment` 或 `/lesson-quiz` 找到知识盲区

**[开始学习 →](LEARNING-ROADMAP.md)**

---

## 如何使用

### 1. 确定你的水平

运行自评测验或在 Claude Code 中执行 `/self-assessment`，获取基于你当前水平的个性化路线图。

### 2. 按引导路径学习

按顺序完成 10 个模块 —— 每个模块建立在前一个之上。边学边把模板直接复制到你的项目中。

### 3. 组合功能为工作流

真正的威力在于组合功能。学会把斜杠命令 + 记忆 + 子代理 + 钩子串成自动化流水线，处理代码审查、部署和文档生成。

### 4. 验证理解

每个模块后运行 `/lesson-quiz [主题]`。测验会精准定位你的知识盲区，帮你快速补全。

**[15 分钟快速开始 →](#快速开始)**

---

## 不确定从哪里开始？

做个自评或选择你的水平：

| 水平 | 你已经可以... | 从这里开始 | 时间 |
|------|-------------|----------|------|
| **初学者** | 刚安装好 Claude Code，能对话 | [斜杠命令](01-slash-commands/) | ~2.5 小时 |
| **中级** | 会用 CLAUDE.md 和自定义命令 | [技能](03-skills/) | ~3.5 小时 |
| **高级** | 能配置 MCP 服务器和钩子 | [高级功能](09-advanced-features/) | ~5 小时 |

**完整学习路径（全部 10 个模块）：**

| 序号 | 模块 | 水平 | 时间 |
|------|------|------|------|
| 1 | [斜杠命令](01-slash-commands/) | 入门 | 30 分钟 |
| 2 | [记忆系统](02-memory/) | 入门+ | 45 分钟 |
| 3 | [检查点](08-checkpoints/) | 中级 | 45 分钟 |
| 4 | [CLI 参考](10-cli/) | 入门+ | 30 分钟 |
| 5 | [技能](03-skills/) | 中级 | 1 小时 |
| 6 | [钩子](06-hooks/) | 中级 | 1 小时 |
| 7 | [MCP](05-mcp/) | 中级+ | 1 小时 |
| 8 | [子代理](04-subagents/) | 中级+ | 1.5 小时 |
| 9 | [高级功能](09-advanced-features/) | 高级 | 2-3 小时 |
| 10 | [插件](07-plugins/) | 高级 | 2 小时 |

**[查看完整学习路线图 →](LEARNING-ROADMAP.md)**

---

## 快速开始

```bash
# 1. 克隆本仓库
git clone https://github.com/Rx782-Fss/claude-howto-zh.git
cd claude-howto-zh

# 2. 复制你的第一个斜杠命令
mkdir -p /path/to/your-project/.claude/commands
cp 01-slash-commands/optimize.md /path/to/your-project/.claude/commands/

# 3. 试试看 —— 在 Claude Code 中输入：
# /optimize

# 4. 准备好更多了？设置项目记忆：
cp 02-memory/project-CLAUDE.md /path/to/your-project/CLAUDE.md

# 5. 安装一个技能：
cp -r 03-skills/code-review ~/.claude/skills/
```

想要完整配置？这是 **1 小时核心配置**：

```bash
# 斜杠命令（15 分钟）
cp 01-slash-commands/*.md .claude/commands/

# 项目记忆（15 分钟）
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 安装一个技能（15 分钟）
cp -r 03-skills/code-review ~/.claude/skills/

# 周末目标：添加钩子、子代理、MCP 和插件
# 按照学习路径引导配置
```

**[查看完整安装参考](#快速开始)**

---

## 你能用它做什么？

| 用例 | 你会组合的功能 |
|------|---------------|
| **自动化代码审查** | 斜杠命令 + 子代理 + 记忆 + MCP |
| **团队新人引导** | 记忆 + 斜杠命令 + 插件 |
| **CI/CD 自动化** | CLI 参考 + 钩子 + 后台任务 |
| **文档生成** | 技能 + 子代理 + 插件 |
| **安全审计** | 子代理 + 技能 + 钩子（只读模式） |
| **DevOps 流水线** | 插件 + MCP + 钩子 + 后台任务 |
| **复杂重构** | 检查点 + 规划模式 + 钩子 |

---

## 翻译范围

| 模块 | 内容 | 文件数 |
|------|------|--------|
| [01 斜杠命令](01-slash-commands/) | Slash Commands 参考 | 9 |
| [02 记忆系统](02-memory/) | Memory / CLAUDE.md | 6 |
| [03 技能](03-skills/) | Skills 系统（7 个子技能） | 22 |
| [04 子代理](04-subagents/) | Subagents | 9 |
| [05 MCP](05-mcp/) | Model Context Protocol | 5 |
| [06 钩子](06-hooks/) | Hooks 系统 | 9 |
| [07 插件](07-plugins/) | Plugins 架构（3 个示例） | 39 |
| [08 检查点](08-checkpoints/) | Checkpoints | 2 |
| [09 高级功能](09-advanced-features/) | Advanced Features | 4 |
| [10 CLI 参考](10-cli/) | CLI Reference | 1 |

### 辅助文档

- 📖 [学习路线图](LEARNING-ROADMAP.md) — Level 1→3 渐进式路径（6 个里程碑）
- ⚡ [快速参考卡](QUICK_REFERENCE.md) — 全功能速查表
- 📋 [功能目录](CATALOG.md) — 99 个内置功能索引
- 📚 [文件总索引](INDEX.md) — 完整文件清单
- 📝 [更新日志](CHANGELOG.md) — v2.0 → v2.2.0 变更记录

---

## 翻译规范

- ✅ 专业术语首次出现保留 **英文 + 中文注释**
- ✅ 代码逻辑不翻译，仅翻译注释和描述
- ✅ Mermaid 图表文本已翻译
- ✅ JSON 的 `description` 字段已翻译
- ✅ Shell `#` 注释已翻译
- ✅ Python docstring / `#` 注释已翻译
- ✅ 结构与原项目 **1:1 对齐**

---

## 常见问题

**这是免费的吗？**
是的。MIT 许可证，永久免费。个人项目、工作、团队中使用均可 —— 只需包含许可声明即可。

**翻译质量如何？**
所有文件由 AI 辅助人工校对翻译，专业术语保持中英对照，技术内容准确无误。如发现翻译问题欢迎提 Issue 或 PR。

**和原项目有区别吗？**
内容上完全一致（1:1 对齐），区别在于语言（中文）和部分本地化适配。建议配合原项目英文版交叉参考。

**支持离线阅读吗？**
可以。整个仓库就是纯 Markdown 文件，克隆到本地即可用任何 Markdown 阅读器打开。

**如何跟踪原项目更新？**
本项目通过 GitHub 与原项目独立维护。当原项目发布新版本时，可使用更新工具检测差异并增量翻译。详见原项目 [CHANGELOG.md](CHANGELOG.md)。

**我可以贡献吗？**
欢迎！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。我们欢迎新的示例、Bug 修复、文档改进和社区模板。

**有 Obsidian 版本吗？**
有的！翻译内容已同步整理为 Obsidian 知识库格式，包含 Frontmatter 和双向链接，可在 Obsidian 中直接使用。

---

## 原项目

- **GitHub**: https://github.com/luongnv89/claude-howto
- **Star**: 5,900+
- **License**: MIT
- **Claude Code**: ≥ 2.1

---

*翻译完成于 2026-04-05 · 基于 v2.2.0 · 由 Rx782-Fss 翻译*
