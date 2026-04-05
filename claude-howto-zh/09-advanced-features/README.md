<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Advanced Features(高级功能)

Claude Code 高级能力的综合指南,包括规划模式(Planning Mode)、扩展思考(Extended Thinking)、自动模式(Auto Mode)、后台任务(Background Tasks)、权限模式(Permission Modes)、打印模式(Print Mode)、会话管理(Session Management)、交互特性(Interactive Features)、语音听写(Voice Dictation)、频道(Channels)、远程控制(Remote Control)、Web 会话(Web Sessions)、桌面应用(Desktop App)、任务列表(Task List)、提示建议(Prompt Suggestions)、Git Worktrees、沙箱隔离(Sandboxing)、托管设置(Managed Settings)以及配置(Configuration)。

## 目录

1. [概览](#overview)
2. [Planning Mode(规划模式)](#planning-mode)
3. [Extended Thinking(扩展思考)](#extended-thinking)
4. [Auto Mode(自动模式)](#auto-mode)
5. [Background Tasks(后台任务)](#background-tasks)
6. [Scheduled Tasks(定时任务)](#scheduled-tasks)
7. [Permission Modes(权限模式)](#permission-modes)
8. [Headless Mode(无头模式)](#headless-mode)
9. [Session Management(会话管理)](#session-management)
10. [Interactive Features(交互特性)](#interactive-features)
11. [Voice Dictation(语音听写)](#voice-dictation)
12. [Channels(频道)](#channels)
13. [Chrome Integration(Chrome 集成)](#chrome-integration)
14. [Remote Control(远程控制)](#remote-control)
15. [Web Sessions(Web 会话)](#web-sessions)
16. [Desktop App(桌面应用)](#desktop-app)
17. [Task List(任务列表)](#task-list)
18. [Prompt Suggestions(提示建议)](#prompt-suggestions)
19. [Git Worktrees](#git-worktrees)
20. [Sandboxing(沙箱隔离)](#sandboxing)
21. [Managed Settings(企业托管设置)](#managed-settings-enterprise)
22. [Configuration and Settings(配置与设置)](#configuration-and-settings)
23. [Best Practices(最佳实践)](#best-practices)

---

## 概览

高级功能扩展了 Claude Code 的核心能力,提供了规划、推理、自动化和控制机制。这些功能支持复杂开发任务、代码审查、自动化和多会话管理的精细化工作流。

**主要高级功能包括**:
- **Planning Mode(规划模式)**:编码前创建详细的实现计划
- **Extended Thinking(扩展思考)**:复杂问题的深度推理
- **Auto Mode(自动模式)**:后台安全分类器在执行前审核每个操作(研究预览版)
- **Background Tasks(后台任务)**:运行长时间操作而不阻塞对话
- **Permission Modes(权限模式)**:控制 Claude 可以做什么(6 种模式)
- **Print Mode(打印模式)**:非交互式运行用于自动化和 CI/CD(`claude -p`)
- **Session Management(会话管理)**:管理工作会话
- **Interactive Features(交互特性)**:键盘快捷键、多行输入和命令历史
- **Voice Dictation(语音听写)**:支持 20 种语言的按住说话语音输入
- **Channels(频道)**:MCP 服务器向运行中的会话推送消息(研究预览版)
- **Remote Control(远程控制)**:从 Claude.ai 或 Claude 应用控制 Claude Code
- **Web Sessions(Web 会话)**:在浏览器中运行 Claude Code(claude.ai/code)
- **Desktop App(桌面应用)**:独立应用,支持可视化差异审查和多会话
- **Task List(任务列表)**:跨上下文压缩的持久化任务跟踪
- **Prompt Suggestions(提示建议)**:基于上下文的智能命令建议
- **Git Worktrees**:用于并行工作的隔离 Worktree 分支
- **Sandboxing(沙箱隔离)**:操作系统级别的文件系统和网络隔离
- **Managed Settings(托管设置)**:通过 plist、Registry 或托管文件进行企业部署
- **Configuration(配置)**:通过 JSON 配置文件自定义行为

---

## Planning Mode(规划模式)

规划模式允许 Claude 在实施之前仔细思考复杂任务,创建你可以审阅和批准的详细计划。

### 什么是规划模式?

规划模式采用两阶段方法:
1. **规划阶段**:分析任务并创建详细的实现计划
2. **实施阶段**:获得批准后,执行计划

### 何时使用规划模式?

✅ 适用于:
- 复杂的多文件重构
- 新功能实现
- 架构设计决策
- 影响多人的大规模变更

### 如何使用

```bash
# 进入规划模式
/plan Implement user authentication system

# 或使用标志启动
claude --permission-mode plan "design the API"
```

---

## Extended Thinking(扩展思考)

切换深度推理模式,用于处理需要仔细分析的复杂问题。

### 如何启用

按 **Alt+T**(macOS 上为 **Option+T**)在会话中切换扩展思考。

或使用标志:
```bash
claude --thinking "analyze this complex algorithm"
```

---

## Auto Mode(自动模式)

> ⚠️ **研究预览版功能(2026 年 3 月)**

自动模式下,后台安全分类器会在执行前审核每个操作。Claude 无需逐项确认即可自主运行。

### 如何启用

```bash
# 方式一:启动时指定
claude --enable-auto-mode

# 方式二:权限模式
claude --permission-mode auto

# 方式三:会话中切换
/permissions auto
```

---

## Background Tasks(后台任务)

运行长时间操作而不阻塞对话。

### 使用场景
- 编译大型项目
- 运行完整的测试套件
- 执行长时间的数据迁移
- 生成大型文档集

### 管理
```bash
/tasks              # 查看所有后台任务
/task <id>           # 查看特定任务详情
```

---

## Permission Modes(权限模式)

Claude Code 支持 **6 种权限模式**:

| 模式 | 说明 | 适用场景 |
|------|--------|----------|
| `default` | 每次工具调用时提示确认 | 标准交互式使用 |
| `acceptEdits` | 自动接受文件编辑,其他操作仍需提示 | 可信的编辑工作流 |
| `plan` | 只读工具,不允许写入 | 规划和探索阶段 |
| `auto` | 无需提示接受所有工具(研究预览版) | 全自主运行 |
| `dontAsk` | 跳过需要权限的工具 | 非交互式脚本编程 |
| `bypassPermissions` | 跳过所有权限检查 | CI/CD、无头环境 |

---

## Configuration(配置)

通过 JSON 配置文件自定义行为:

**用户级**:`~/.claude/settings.json`
**项目级**:`.claude/settings.json`

```json
{
  "model": "sonnet",
  "maxTurns": 50,
  "autoCheckpoint": true,
  "theme": "dark"
}
```

> 💡 **中文开发者提示**:高级功能是区分"会用 Claude Code"和"精通 Claude Code"的关键分水岭。建议按以下顺序学习:① Planning Mode → ② Permission Modes → ③ Extended Thinking → ④ Background Tasks → ⑤ Auto Mode。每一项都能显著提升你的工作效率。

---

**最后更新**:2026 年 3 月
