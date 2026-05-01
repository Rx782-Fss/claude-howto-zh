<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# 高级功能（Advanced Features）

Claude Code 高级功能完整指南，涵盖规划模式（Planning Mode）、扩展思考（Extended Thinking）、自动模式（Auto Mode）、后台任务（Background Tasks）、权限模式（Permission Modes）、打印模式/非交互式模式（Print Mode）、会话管理（Session Management）、交互功能（Interactive Features）、通道（Channels）、语音听写（Voice Dictation）、远程控制（Remote Control）、Web 会话（Web Sessions）、桌面应用（Desktop App）、任务列表（Task List）、提示建议（Prompt Suggestions）、Git 工作树（Git Worktrees）、沙箱隔离（Sandboxing）、托管设置（Managed Settings）以及配置管理（Configuration）等内容。

## 目录

1. [概述](#概述)
2. [规划模式](#规划模式)
3. [Ultraplan (云端计划草稿)](#ultraplan-云端计划草稿)
4. [扩展思考](#扩展思考)
5. [自动模式](#自动模式)
6. [后台任务](#后台任务)
7. [Monitor 工具（事件驱动流）](#monitor-工具事件驱动流)
8. [定时任务](#定时任务)
9. [权限模式](#权限模式)
10. [无头模式](#无头模式)
11. [会话管理](#会话管理)
12. [交互功能](#交互功能)
13. [TUI 模式（全屏）](#tui-模式全屏)
14. [语音听写](#语音听写)
15. [通道](#通道)
16. [Chrome 集成](#chrome-集成)
17. [远程控制](#远程控制)
18. [Web 会话](#web-会话)
19. [桌面应用](#桌面应用)
20. [任务列表](#任务列表)
21. [提示建议](#提示建议)
22. [Git 工作树](#git-工作树)
23. [沙箱隔离](#沙箱隔离)
24. [托管设置（企业版）](#托管设置企业版)
25. [配置与设置](#配置与设置)
26. [代理团队](#代理团队)
27. [最佳实践](#最佳实践)
28. [附加资源](#附加资源)

---

## 概述

Claude Code 的高级功能通过规划、推理、自动化和控制机制扩展了核心能力。这些功能支持复杂开发任务、代码审查、自动化和多会话管理的精细化工作流程。

**主要高级功能包括：**
- **规划模式（Planning Mode）**：在编码前创建详细的实现计划
- **扩展思考（Extended Thinking）**：对复杂问题进行深度推理
- **自动模式（Auto Mode）**：后台安全分类器在执行前审查每个操作（研究预览版）
- **后台任务（Background Tasks）**：运行长时间操作而不阻塞对话
- **权限模式（Permission Modes）**：控制 Claude 可以执行的操作（`default`、`acceptEdits`、`plan`、`auto`、`dontAsk`、`bypassPermissions`）
- **打印模式（Print Mode）**：以非交互方式运行 Claude Code，用于自动化和 CI/CD（`claude -p`）
- **会话管理（Session Management）**：管理工作会话
- **交互功能（Interactive Features）**：键盘快捷键、多行输入和命令历史
- **语音听写（Voice Dictation）**：支持 20 种语言的按住说话语音输入
- **通道（Channels）**：MCP 服务器将消息推送到正在运行的会话中（研究预览版）
- **远程控制（Remote Control）**：从 Claude.ai 或 Claude 应用程序控制 Claude Code
- **Web 会话（Web Sessions）**：在浏览器中的 claude.ai/code 上运行 Claude Code
- **桌面应用（Desktop App）**：独立应用程序，用于可视化差异审查和多会话管理
- **任务列表（Task List）**：跨上下文压缩的持久化任务跟踪
- **提示建议（Prompt Suggestions）**：基于上下文的智能命令建议
- **Git 工作树（Git Worktrees）**：用于并行工作的隔离工作树分支
- **沙箱隔离（Sandboxing）**：操作系统级别的文件系统和网络隔离
- **托管设置（Managed Settings）**：通过 plist、Registry 或托管文件进行企业部署
- **配置（Configuration）**：使用 JSON 配置文件自定义行为

---

## 规划模式（Planning Mode）

规划模式允许 Claude 在实现之前仔细思考复杂任务，创建一个你可以审查和批准的详细计划。

### 什么是规划模式？

规划模式采用两阶段方法：
1. **规划阶段（Planning Phase）**：Claude 分析任务并创建详细的实现计划
2. **实现阶段（Implementation Phase）**：批准后，Claude 执行计划

### 何时使用规划模式

✅ **适用场景：**
- 复杂的多文件重构
- 新功能实现
- 架构变更
- 数据库迁移
- 主要 API 重设计

❌ **不适用场景：**
- 简单的错误修复
- 格式调整
- 单文件编辑
- 快速查询

### 激活规划模式

**斜杠命令：**
```bash
/plan 实现用户认证系统
```

**CLI 标志：**
```bash
claude --permission-mode plan
```

**设为默认值：**
```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

**键盘快捷键：**
- `Shift + Tab` - 切换权限模式（包括 plan 模式）
- `Alt + M` - 切换权限模式（Windows/Linux）

### 规划模式的优势

- **结构化的实现方法**：详细的实现步骤分解
- **审查和批准**：在执行前批准或调整计划
- **风险识别**：在实现前识别潜在问题
- **清晰的阶段**：有组织的实现阶段和里程碑

### 示例：功能实现

```
用户: /plan 添加实时通知系统

Claude: 我将为实施实时通知系统创建一个计划。

## 实施计划

### 阶段 1: 基础设施搭建
1. 安装 WebSocket 库 (socket.io)
2. 设置 WebSocket 服务器
3. 配置连接管理

### 阶段 2: 后端实现
4. 创建通知服务
5. 实现通知队列
6. 添加通知数据库表结构
7. 创建 API 端点

### 阶段 3: 前端集成
8. 设置 WebSocket 客户端
9. 创建通知 UI 组件
10. 实现通知状态管理
11. 添加通知权限设置

### 阶段 4: 测试与部署
12. 编写单元测试
13. 编写集成测试
14. 更新文档
15. 部署到预发布环境

预计时间: 3-4 小时
需修改文件: 12 个
需新建文件: 8 个

准备继续吗？(yes/no/modify plan)

用户: yes

Claude: [按照计划开始实施]
```

### 计划修改

```
用户: 修改计划 - 先跳过队列功能，我们稍后再添加

Claude: 已更新计划:
[显示移除队列后的修改后计划]

用户: 看起来不错，继续

Claude: [执行修改后的计划]
```

### 规划模式配置

规划模式可通过 CLI 标志或斜杠命令激活：

```bash
# 通过 CLI 激活规划模式
claude --permission-mode plan

# 或在 REPL 内使用 /plan 斜杠命令
/plan 实现用户认证系统
```

**用于规划的模型别名**：使用 `opusplan` 作为模型别名，让 Opus 进行规划，Sonnet 执行实现：

```bash
claude --model opusplan "设计和实现新 API"
```

**外部编辑计划**：按 `Ctrl+G` 在外部编辑器中打开当前计划以进行详细修改。

> **v2.1.112 更新**：计划文件现在根据生成计划的提示词命名（而不是随机单词），使其更容易浏览和复用。

---

## Ultraplan (云端计划草稿)

> **v2.1.101 新功能**：Ultraplan 现在会在首次调用时自动创建一个 Web 云端环境的 Claude Code——无需手动设置，无需等待容器预热即可开始起草计划。

> **注意**：Ultraplan 是一个研究预览功能，需要 Claude Code v2.1.91 或更高版本。

`/ultraplan` 将规划任务从本地 CLI 交给运行在规划模式的 Web 会话中的 Claude Code。Claude 在云端起草计划，同时你的终端保持空闲可用于其他工作，然后你在浏览器中审查草稿并选择执行位置——在同一云端会话中或传送回你的终端。

### 何时使用 Ultraplan

- 你想要比终端更丰富的审查界面：内联注释、emoji 反应、大纲侧边栏和历史记录
- 你想在本地继续编码的同时进行无人值守的起草——云端会话研究仓库并编写计划而不阻塞你的 CLI
- 计划需要在执行前经过利益相关者审查——可共享的 Web URL 胜过粘贴终端滚动回溯

### 要求

- 一个 Claude Code on the Web 账户
- 一个 GitHub 仓库（云端会话克隆你的仓库以针对真实代码起草计划）
- **不适用于** Amazon Bedrock、Google Cloud Vertex AI 或 Microsoft Foundry

### 三种启动方式

- **命令**：`/ultraplan <prompt>` — 显式调用
- **关键词**：在任何正常提示词中包含单词 `ultraplan`，Claude 会将请求路由到云端
- **从本地计划**：Claude 在本地完成计划后，在批准对话框中选择"否，在 Claude Code on the Web 上用 Ultraplan 完善"将草稿提交给更深入的研究

### 使用示例

```bash
/ultraplan 将认证服务从 sessions 迁移到 JWTs
```

Claude 确认后启动云环境（在 v2.1.101+ 中首次运行时自动创建），并返回一个你可以在浏览器中打开的会话链接。

### 状态指示器

| 状态 | 含义 |
|------|------|
| `◇ ultraplan` | Claude 正在研究你的代码库并起草计划 |
| `◇ ultraplan needs your input` | Claude 有一个澄清问题；打开会话链接回应 |
| `◆ ultraplan ready` | 计划已准备好在浏览器中审查 |

### 执行选项

一旦计划准备好，你有两条执行路径。在浏览器中批准计划以在同一云端会话中执行——Claude 远程实现更改并通过 Web UI 打开拉取请求。或者选择"批准计划并传送到终端"以在本地实现。终端传送对话框提供三个选择：

- **在此处实现（Implement here）** — 在当前终端会话中运行已批准的计划
- **启动新会话（Start new session）** — 在同一工作目录中打开新会话并在那里实现
- **取消（Cancel）** — 将计划保存到文件以便稍后继续

> **警告**：当 Ultraplan 启动时远程控制会断开连接。两个功能共享 claude.ai/code 界面，因此同一时间只能激活其中一个。

---

## 扩展思考（Extended Thinking）

扩展思考允许 Claude 在提供解决方案之前花费更多时间对复杂问题进行推理。

### 什么是扩展思考？

扩展思考是一个深思熟虑的、逐步推理过程，Claude 在此过程中：
- 分解复杂问题
- 考虑多种方法
- 评估权衡取舍
- 推理边缘情况

### 激活扩展思考

**键盘快捷键：**
- `Option + T` (macOS) / `Alt + T` (Windows/Linux) - 切换扩展思考

**自动激活：**
- 默认对所有模型启用（Opus 4.7、Sonnet 4.6、Haiku 4.5）
- Opus 4.7：自适应推理，支持推理级别（effort levels）：`low` (○)、`medium` (◐)、`high` (●)、`xhigh`（仅 Opus 4.7，自 Opus 4.7 发布以来（2026-04-16）在 Claude Code 上为默认值）、`max`。Opus 4.6 和 Sonnet 4.6 也支持 `low`、`medium`、`high`、`max`（无 `xhigh`）。Opus 4.7 具有 1M-token 原生上下文窗口（1M 上下文修复在 v2.1.117 中落地——在此之前，`/context` 错误地将 Opus 4.7 按 200K 窗口计算并触发过早的自动压缩）。
- Pro/Max 订阅者在 Opus 4.6 / Sonnet 4.6 上的默认推理级别在 v2.1.117 中从 `medium` 提升到 `high`。
- 其他模型：固定预算最多 31,999 tokens

**配置方法：**
- 切换：`Alt+T` / `Option+T`，或通过 `/config`
- 查看推理过程：`Ctrl+O`（详细模式）
- 设置推理级别：`/effort` 命令或 `--effort` 标志

**自定义预算：**
```bash
export MAX_THINKING_TOKENS=1024
```

**推理级别（Effort Level）**（Opus 4.7、Opus 4.6 和 Sonnet 4.6 支持）：
```bash
export CLAUDE_CODE_EFFORT_LEVEL=xhigh   # low (○), medium (◐), high (●), xhigh (仅 Opus 4.7, 默认), 或 max
```

**CLI 标志：**
```bash
claude --effort high "复杂的架构审查"
```

**斜杠命令：**
```
/effort high
```

> **注意**：提示词中的关键词 "ultrathink" 会激活深度推理模式。推理级别 `low`、`medium`、`high` 和 `max` 在 Opus 4.7、Opus 4.6 和 Sonnet 4.6 上受支持。`xhigh`（Opus 4.7 上的默认值）仅限 Opus 4.7。

### 扩展思考的优势

- **深度推理**：花费更多时间思考复杂问题
- **更好的架构决策**：通过全面评估做出明智的选择
- **考虑边缘情况**：彻底思考潜在问题和场景
- **透彻分析**：结构化的复杂问题解决方法

### 示例：架构决策

```
用户: /think 我们应该为电商平台使用微服务还是单体架构？

Claude: 让我仔细思考这个架构决策...

<extended_thinking>
## 上下文分析
- 团队规模: 5 名开发者
- 预期流量: 初期 10,000 日活跃用户
- 需要扩展到 100,000+ 用户
- DevOps 资源有限
- 6 个月的时间线到 MVP

## 方案 1: 微服务架构
优点:
+ 独立扩展
+ 技术灵活性
+ 团队独立性
+ 故障隔离

缺点:
- 运维复杂性
- 网络开销
- 需要分布式追踪
- 需要 DevOps 专业知识
- 初始开发速度较慢

## 方案 2: 单体架构
优点:
+ 部署更简单
+ 初始开发更快
+ 调试更容易
+ 运维开销更低
+ 单一代码库

缺点:
- 后期扩展挑战
- 全有或全无部署
- 技术锁定
- 可能产生紧耦合

## 决策因素
1. 团队规模 (5 人) → 倾向于单体
2. DevOps 资源 (有限) → 倾向于单体
3. 时间线 (6 个月) → 倾向于单体
4. 未来规模 (10 万用户) → 单体 + 缓存可实现
5. 复杂度预算 → 有限

## 建议
从**模块化单体（modular monolith）**开始：
- 单个部署单元
- 清晰的模块边界
- 模块间接口清晰
- 为将来提取微服务做好准备

这给你带来：
✓ 初始开发速度快
✓ 运维复杂度低
✓ 以后可提取服务的选项
✓ 架构清晰

迁移路径：当你达到 50,000+ 用户或特定模块需要独立扩展时，将这些模块提取为微服务。
</extended_thinking>

**建议**：实施具有清晰模块边界的模块化单体架构。

这种方法平衡了你当前的约束条件（团队规模、时间线、DevOps 资源）与未来的可扩展性需求。以后当有明确的业务需求时，你可以将特定模块迁移到微服务。
```

### 扩展思考配置

扩展思考通过环境变量、键盘快捷键和 CLI 标志进行控制：

```bash
# 设置思考 token 预算
export MAX_THINKING_TOKENS=16000

# 设置推理级别 (Opus 4.7, Opus 4.6, Sonnet 4.6): low (○), medium (◐), high (●), xhigh (仅 Opus 4.7, 默认), 或 max
export CLAUDE_CODE_EFFORT_LEVEL=xhigh
```

在会话中使用 `Alt+T` / `Option+T` 切换，使用 `/effort` 设置级别，或通过 `/config` 配置。

---

## 自动模式（Auto Mode）

自动模式是一个研究预览权限模式（2026 年 3 月），它使用后台安全分类器在执行前审查每个操作。它允许 Claude 自主工作，同时阻止危险操作。

### 要求

- **计划（Plan）**：Team、Enterprise 或 API 计划（Pro 或 Max 计划不可用）
- **模型**：Claude Sonnet 4.6 或 Opus 4.7
- **提供商（Provider）**：仅 Anthropic API（不支持 Bedrock、Vertex 或 Foundry）
- **分类器（Classifier）**：运行在 Claude Sonnet 4.6 上（增加额外的 token 成本）

### 启用自动模式

```bash
# 使用 CLI 标志解锁自动模式（对于 Opus 4.7 上的 Max 订阅者不再需要——可直接访问）
claude --enable-auto-mode

# 然后在 REPL 中使用 Shift+Tab 循环切换到它
```

> **v2.1.112 更新**：自动模式不再需要 `--enable-auto-mode` 标志。Max 订阅者可在 Opus 4.7 上直接访问。

或将其设置为默认权限模式：

```bash
claude --permission-mode auto
```

通过配置设置：
```json
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

### 分类器如何工作

后台分类器使用以下决策顺序评估每个操作：

1. **允许/拒绝规则（Allow/deny rules）** -- 首先检查显式权限规则
2. **只读/编辑自动批准（Read-only/edits auto-approved）** -- 文件读取和编辑自动通过
3. **分类器（Classifier）** -- 后台分类器审查操作
4. **回退（Fallback）** -- 在连续 3 次或总共 20 次阻止后回退到提示用户

### 默认阻止的操作

自动模式默认阻止以下操作：

| 阻止的操作 | 示例 |
|-----------|------|
| 管道到 shell 的安装 | `curl \| bash` |
| 向外发送敏感数据 | 通过网络发送 API 密钥、凭证 |
| 生产环境部署 | 针对生产环境的部署命令 |
| 大规模删除 | 对大型目录执行 `rm -rf` |
| IAM 变更 | 权限和角色修改 |
| 强制推送到 main | `git push --force origin main` |

### 默认允许的操作

| 允许的操作 | 示例 |
|-----------|------|
| 本地文件操作 | 读取、写入、编辑项目文件 |
| 声明的依赖安装 | 从清单文件执行 `npm install`、`pip install` |
| 只读 HTTP | 使用 `curl` 获取文档 |
| 推送到当前分支 | `git push origin feature-branch` |

### 配置自动模式

**将默认规则打印为 JSON**：
```bash
claude auto-mode defaults
```

**通过 `autoMode.environment` 托管设置配置受信任的基础设施**，用于企业部署。这允许管理员定义受信任的 CI/CD 环境、部署目标和基础设施模式。

#### 使用 `"$defaults"` 扩展默认规则（v2.1.118）

自 v2.1.118 起，`autoMode.allow`、`autoMode.soft_deny` 和 `autoMode.environment` 接受 `"$defaults"` 令牌，该令牌将你的规则**追加**到内置列表而不是替换它。在 v2.1.118 之前，任何用户定义的数组都会静默覆盖内置规则。

**之前（替换内置规则 —— v2.1.118 之前的行为）：**

```json
{
  "autoMode": {
    "allow": ["Bash(gh pr list:*)"]
  }
}
```

**之后（扩展内置规则 —— v2.1.118+）：**

```json
{
  "autoMode": {
    "allow": ["$defaults", "Bash(gh pr list:*)"],
    "soft_deny": ["$defaults", "Bash(kubectl delete:*)"],
    "environment": ["$defaults", "trusted-ci.internal"]
  }
}
```

使用 `"$defaults"` 在保留出厂默认规则的同时，在其上叠加组织或项目特定的添加项。

### 回退行为

当分类器不确定时，自动模式会回退到提示用户：
- 在**连续 3 次**分类器阻止后
- 在会话中总共**20 次**分类器阻止后

这确保当分类器无法自信地批准操作时，用户始终保留控制权。

### 种子自动模式等效权限（无需 Team 计划）

如果你没有 Team 计划或想要没有后台分类器的更简单方法，你可以用一组保守的安全权限规则作为基线来填充你的 `~/.claude/settings.json`。该脚本从只读和本地检查规则开始，然后仅在你需要时才允许你选择加入编辑、测试、本地 git 写入、包安装和 GitHub 写操作。

**文件**：`09-advanced-features/setup-auto-mode-permissions.py`

```bash
# 预览将添加的内容（不会写入更改）
python3 09-advanced-features/setup-auto-mode-permissions.py --dry-run

# 应用保守基线
python3 09-advanced-features/setup-auto-mode-permissions.py

# 仅在需要时添加更多能力
python3 09-advanced-features/setup-auto-mode-permissions.py --include-edits --include-tests
python3 09-advanced-features/setup-auto-mode-permissions.py --include-git-write --include-packages
```

该脚本跨以下类别添加规则：

| 类别 | 示例 |
|------|------|
| 核心只读工具 | `Read(*)`、`Glob(*)`、`Grep(*)`、`Agent(*)`、`WebSearch(*)`、`WebFetch(*)` |
| 本地检查 | `Bash(git status:*)`、`Bash(git log:*)`、`Bash(git diff:*)`、`Bash(cat:*)` |
| 可选编辑 | `Edit(*)`、`Write(*)`、`NotebookEdit(*)` |
| 可选测试/构建 | `Bash(pytest:*)`、`Bash(python3 -m pytest:*)`、`Bash(cargo test:*)` |
| 可选 git 写入 | `Bash(git add:*)`、`Bash(git commit:*)`、`Bash(git stash:*)` |
| Git（本地写入） | `Bash(git add:*)`、`Bash(git commit:*)`、`Bash(git checkout:*)` |
| 包管理器 | `Bash(npm install:*)`、`Bash(pip install:*)`、`Bash(cargo build:*)` |
| 构建与测试 | `Bash(make:*)`、`Bash(pytest:*)`、`Bash(go test:*)` |
| 常用 shell | `Bash(ls:*)`、`Bash(cat:*)`、`Bash(find:*)`、`Bash(cp:*)`、`Bash(mv:*)` |
| GitHub CLI | `Bash(gh pr view:*)`、`Bash(gh pr create:*)`、`Bash(gh issue list:*)` |

危险操作（`rm -rf`、`sudo`、强制推送、`DROP TABLE`、`terraform destroy` 等）被有意排除在外。该脚本是幂等的——运行两次不会重复规则。

---

## 后台任务（Background Tasks）

后台任务允许长时间运行的操作在不阻塞对话的情况下执行。

### 什么是后台任务？

后台任务异步运行，同时你可以继续工作：
- 大型测试套件
- 构建过程
- 数据库迁移
- 部署脚本
- 分析工具

**基本用法：**
```bash
用户: 在后台运行测试

Claude: 已启动任务 bg-1234

/task list           # 显示所有任务
/task status bg-1234 # 检查进度
/task show bg-1234   # 查看输出
/task cancel bg-1234 # 取消任务
```

### 启动后台任务

```
用户: 在后台运行完整的测试套件

Claude: 正在后台启动测试（任务 ID: bg-1234）
测试运行时你可以继续工作。

[你可以继续对话]

用户: 同时，让我们重构认证模块

Claude: [测试在后台运行时处理认证模块]

[稍后，当测试完成时]

Claude: 📢 后台任务 bg-1234 已完成：
✅ 245 个测试通过
❌ 3 个测试失败
查看结果: /task show bg-1234
```

### 管理后台任务

**列出活动任务：**
```
用户: /task list

活动后台任务:
1. [bg-1234] 运行测试（已完成 50%，剩余 2 分钟）
2. [bg-1235] 构建 Docker 镜像（已完成 25%，剩余 8 分钟）
3. [bg-1236] 部署到预发布环境（已完成 90%，剩余 30 秒）
```

**检查任务状态：**
```
用户: /task status bg-1234

任务 bg-1234: 运行测试
状态: 进行中
进度: 120/245 测试（49%）
启动时间: 2025-11-08 10:30:15
预计完成时间: 2025-11-08 10:34:22
```

**查看任务输出：**
```
用户: /task show bg-1234

[显示测试运行的实时输出]
```

**取消任务：**
```
用户: /task cancel bg-1234

已取消后台任务 bg-1234
```

### 示例：并行开发

```
用户: 在后台运行构建

Claude: 正在启动构建...（任务 ID: bg-5001）

用户: 同时在后台运行 linter

Claude: 正在启动 linter...（任务 ID: bg-5002）

用户: 当这些运行时，让我们实现新的 API 端点

Claude: [构建和 linter 运行时实现 API 端点]

[10 分钟后]

Claude: 📢 构建成功完成（bg-5001）
📢 Linter 发现 12 个问题（bg-5002）

用户: 给我看看 linter 的问题

Claude: [显示来自 bg-5002 的 linter 输出]
```

### 配置

```json
{
  "backgroundTasks": {
    "enabled": true,
    "maxConcurrentTasks": 5,
    "notifyOnCompletion": true,
    "autoCleanup": true,
    "logOutput": true
  }
}
```

---

## Monitor 工具（事件驱动流）

> **v2.1.98 新功能**：Monitor 工具让 Claude 监视后台命令的 stdout 并在匹配的事件出现时立即做出反应——替代轮询循环和 `sleep` 来等待长时间运行的进程。

Monitor 附加到任何向 stdout 写入的 shell 命令。命令的每一行 stdout 都成为一个唤醒会话的通知。Claude 指定命令；harness 流式传输输出并在事件触发时交付它们。有关启动底层进程的信息，请参阅相关的[后台任务](#后台任务)部分。

### 为什么重要

使用 `/loop` 或 `sleep` 进行轮询每个周期都会消耗一次完整的 API 往返，无论是否有任何更改。Monitor 保持静默直到事件触发，在命令安静期间消耗**零 token**。当事件确实发生时，Claude 立即反应——无需等待下一个轮询周期的延迟发现。对于运行时间超过几分钟的任何事情，这既比轮循循环更便宜又更快。

### 两种常见模式

**流过滤器（Stream filters）**监视来自长时间运行源的持续输出。命令永远运行；每个匹配的行都是一个事件。

```bash
tail -f /var/log/app.log | grep --line-buffered "ERROR"
```

**轮询并发射过滤器（Poll-and-emit filters）**定期检查源，仅在发生变化时发出信号。将此用于 API、数据库或任何没有原生流的资源。

```bash
last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
while true; do
  gh api "repos/owner/repo/issues/123/comments?since=$last" || true
  last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  sleep 30
done
```

### 具体示例

"启动我的开发服务器并监视错误。"Claude 将服务器作为后台任务启动，附加一个 Monitor 过滤器（`tail -F server.log | grep --line-buffered -E "ERROR|FATAL"`），然后会话进入静默状态。当日志中出现错误行的那一刻，Claude 被唤醒，读取错误，并可以做出反应——重启服务器、修复 bug 或向你展示——而无需你去检查。

> **警告**：当管道传输到 `grep` 时，**务必**使用 `grep --line-buffered`。如果没有它，grep 会以 4KB 块缓冲 stdout，这在低流量流上可能会延迟事件数分钟。这是 Monitor 在实践中失效的第一大原因——如果你的过滤器在不应该沉默时看起来沉默了，首先检查 `--line-buffered` 标志。

---

## 定时任务（Scheduled Tasks）

定时任务让你可以按重复计划或一次性提醒的方式自动运行提示词。任务是会话作用域的——它们在 Claude Code 活动时运行，并在会话结束时清除。自 v2.1.72+ 起可用。

### `/loop` 命令

```bash
# 显式间隔
/loop 5m 检查部署是否完成

# 自然语言
/loop 每 30 分钟检查构建状态
```

也支持标准的 5 字段 cron 表达式用于精确调度。

### 一次性提醒

设置在特定时间触发一次的提醒：

```
下午 3 点提醒我推送发布分支
45 分钟后，运行集成测试
```

### 管理定时任务

| 工具 | 说明 |
|------|------|
| `CronCreate` | 创建新的定时任务 |
| `CronList` | 列出所有活动定时任务 |
| `CronDelete` | 删除定时任务 |

**限制和行为：**
- 每个会话最多 **50 个定时任务**
- 会话作用域——会话结束时清除
- 重复任务在 **3 天**后自动过期
- 任务仅在 Claude Code 运行时触发——不补发错过的触发

### 行为详情

| 方面 | 详情 |
|------|------|
| **重复抖动（Recurring jitter）** | 间隔的最多 10%（最多 15 分钟） |
| **一次性抖动（One-shot jitter）** | :00/:30 边界上最多 90 秒 |
| **错过触发（Missed fires）** | 不补发——如果 Claude Code 未运行则跳过 |
| **持久性（Persistence）** | 不跨重启持久化 |

### 云端定时任务

使用 `/schedule` 创建在 Anthropic 基础设施上运行的云端定时任务：

```
/schedule 每天 上午 9 点运行测试套件并报告失败
```

云端定时任务跨重启持久化，不需要 Claude Code 在本地运行。

### 禁用定时任务

```bash
export CLAUDE_CODE_DISABLE_CRON=1
```

### 示例：监控部署

```
/loop 5m 检查预发布环境的部署状态。
        如果部署成功，通知我并停止循环。
        如果失败，显示错误日志。
```

> **提示**：定时任务是会话作用域的。对于在重启后存活的持久化自动化，请改用 CI/CD 流水线、GitHub Actions 或桌面应用定时任务。

---

## 权限模式（Permission Modes）

权限模式控制 Claude 无需明确批准即可执行的操作。

### 可用的权限模式

| 模式 | 行为 |
|------|------|
