<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 示例 — 完整索引

本文档提供按功能类型组织的所有示例文件的完整索引。

## 汇总统计

- **总文件数**：100+ 个文件
- **分类数**：10 个功能类别
- **插件**：3 个完整插件
- **技能**：6 个完整技能
- **钩子**：8 个示例钩子
- **即用状态**：所有示例

---

## 01. 斜杠命令（10 个文件）

用户调用的常用工作流快捷命令。

| 文件 | 描述 | 用途 |
|------|------|------|
| `optimize.md` | 代码优化分析器 | 发现性能问题 |
| `pr.md` | Pull Request 准备 | PR 工作流自动化 |
| `generate-api-docs.md` | API 文档生成器 | 生成 API 文档 |
| `commit.md` | 提交信息助手 | 标准化提交 |
| `setup-ci-cd.md` | CI/CD 流水线配置 | DevOps 自动化 |
| `push-all.md` | 推送所有更改 | 快速推送工作流 |
| `unit-test-expand.md` | 扩展单元测试覆盖率 | 测试自动化 |
| `doc-refactor.md` | 文档重构 | 文档改进 |
| `pr-slash-command.png` | 截图示例 | 视觉参考 |
| `README.md` | 文档 | 安装和使用指南 |

**安装路径**：`.claude/commands/`

**用法**：`/optimize`、`/pr`、`/generate-api-docs`、`/commit`、`/setup-ci-cd`、`/push-all`、`/unit-test-expand`、`/doc-refactor`

---

## 02. 记忆（6 个文件）

持久化上下文和项目标准。

| 文件 | 描述 | 范围 | 位置 |
|------|------|------|------|
| `project-CLAUDE.md` | 团队项目标准 | 项目级 | `./CLAUDE.md` |
| `directory-api-CLAUDE.md` | API 特定规则 | 目录级 | `./src/api/CLAUDE.md` |
| `personal-CLAUDE.md` | 个人偏好 | 用户级 | `~/.claude/CLAUDE.md` |
| `memory-saved.png` | 截图：记忆已保存 | - | 视觉参考 |
| `memory-ask-claude.png` | 截图：询问 Claude | - | 视觉参考 |
| `README.md` | 文档 | - | 参考资料 |

**安装方式**：复制到对应位置

**用法**：由 Claude 自动加载

---

## 03. 技能（28 个文件）

自动调用的能力，包含脚本和模板。

### 代码审查技能（5 个文件）
```
code-review/
├── SKILL.md                          # 技能定义
├── scripts/
│   ├── analyze-metrics.py            # 代码指标分析器
│   └── compare-complexity.py         # 复杂度对比工具
└── templates/
    ├── review-checklist.md           # 审查检查清单
    └── finding-template.md           # 问题记录模板
```

**用途**：全面的代码审查，含安全、性能和质量分析

**自动触发时机**：审查代码时

---

### 品牌语调技能（4 个文件）
```
brand-voice/
├── SKILL.md                          # 技能定义
├── templates/
│   ├── email-template.txt            # 邮件格式模板
│   └── social-post-template.txt      # 社交媒体格式模板
└── tone-examples.md                  # 语调示例消息
```

**用途**：确保沟通中的品牌语调一致性

**自动触发时机**：创建营销文案时

---

### 文档生成器技能（2 个文件）
```
doc-generator/
├── SKILL.md                          # 技能定义
└── generate-docs.py                  # Python 文档提取器
```

**用途**：从源代码生成全面的 API 文档

**自动触发时机**：创建/更新 API 文档时

---

### 重构技能（5 个文件）
```
refactor/
├── SKILL.md                          # 技能定义
├── scripts/
│   ├── analyze-complexity.py         # 复杂度分析器
│   └── detect-smells.py              # 代码异味检测器
├── references/
│   ├── code-smells.md                # 代码异味目录
│   └── refactoring-catalog.md        # 重构手法目录
└── templates/
    └── refactoring-plan.md           # 重构计划模板
```

**用途**：系统化代码重构，含复杂度分析

**自动触发时机**：重构代码时

---

### CLAUDE.md 管理技能（1 个文件）
```
claude-md/
└── SKILL.md                          # 技能定义
```

**用途**：管理和优化 CLAUDE.md 文件

---

### 博客草稿技能（3 个文件）
```
blog-draft/
├── SKILL.md                          # 技能定义
└── templates/
    ├── draft-template.md             # 博客草稿模板
    └── outline-template.md           # 博客大纲模板
```

**用途**：以一致的结构起草博客文章

此外还有：`README.md` — 技能概览和使用指南

**安装路径**：`~/.claude/skills/` 或 `.claude/skills/`

---

## 04. 子代理（9 个文件）

具有自定义能力的专业化 AI 助手。

| 文件 | 描述 | 工具 | 用途 |
|------|------|------|------|
| `code-reviewer.md` | 代码质量分析 | read, grep, diff, lint_runner | 全面审查 |
| `test-engineer.md` | 测试覆盖率分析 | read, write, bash, grep | 测试自动化 |
| `documentation-writer.md` | 文档创建 | read, write, grep | 文档生成 |
| `secure-reviewer.md` | 安全审查（只读）| read, grep | 安全审计 |
| `implementation-agent.md` | 完整实现 | read, write, bash, grep, edit, glob | 功能开发 |
| `debugger.md` | 调试专家 | read, bash, grep | Bug 调查 |
| `data-scientist.md` | 数据分析专家 | read, write, bash | 数据工作流 |
| `clean-code-reviewer.md` | 代码整洁标准 | read, grep | 代码质量 |
| `README.md` | 文档 | - | 安装和使用指南 |

**安装路径**：`.claude/agents/`

**用法**：由主代理自动委派

---

## 05. MCP 协议（5 个文件）

外部工具和 API 集成。

| 文件 | 描述 | 集成对象 | 用途 |
|------|------|----------|------|
| `github-mcp.json` | GitHub 集成 | GitHub API | PR/Issue 管理 |
| `database-mcp.json` | 数据库查询 | PostgreSQL/MySQL | 实时数据查询 |
| `filesystem-mcp.json` | 文件操作 | 本地文件系统 | 文件管理 |
| `multi-mcp.json` | 多服务器 | GitHub + DB + Slack | 完整集成 |
| `README.md` | 文档 | - | 安装和使用指南 |

**安装路径**：`.mcp.json`（项目级）或 `~/.claude.json`（用户级）

**用法**：`/mcp__github__list_prs` 等

---

## 06. 钩子（9 个文件）

事件驱动的自动化脚本，自动执行。

| 文件 | 描述 | 事件 | 用途 |
|------|------|------|------|
| `format-code.sh` | 自动格式化代码 | PreToolUse:Write | 代码格式化 |
| `pre-commit.sh` | 提交前运行测试 | PreToolUse:Bash | 测试自动化 |
| `security-scan.sh` | 安全扫描 | PostToolUse:Write | 安全检查 |
| `log-bash.sh` | 记录 Bash 命令 | PostToolUse:Bash | 命令日志 |
| `validate-prompt.sh` | 验证提示词 | PreToolUse | 输入验证 |
| `notify-team.sh` | 发送通知 | Notification | 团队通知 |
| `context-tracker.py` | 追踪上下文窗口使用量 | PostToolUse | 上下文监控 |
| `context-tracker-tiktoken.py` | 基于 Token 的上下文追踪 | PostToolUse | 精确 Token 计数 |
| `README.md` | 文档 | - | 安装和使用指南 |

**安装路径**：在 `~/.claude/settings.json` 中配置

**用法**：在设置中配置，自动执行

**钩子类型**（4 种类型，25 个事件）：
- 工具钩子：PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest
- 会话钩子：SessionStart, SessionEnd, Stop, StopFailure, SubagentStart, SubagentStop
- 任务钩子：UserPromptSubmit, TaskCompleted, TaskCreated, TeammateIdle
- 生命周期钩子：ConfigChange, CwdChanged, FileChanged, PreCompact, PostCompact, WorktreeCreate, WorktreeRemove, Notification, InstructionsLoaded, Elicitation, ElicitationResult

---

## 07. 插件（3 个完整插件，40 个文件）

打包的功能集合。

### PR 审查插件（10 个文件）
```
pr-review/
├── .claude-plugin/
│   └── plugin.json                   # 插件清单
├── commands/
│   ├── review-pr.md                  # 全面审查
│   ├── check-security.md             # 安全检查
│   └── check-tests.md                # 测试覆盖率检查
├── agents/
│   ├── security-reviewer.md          # 安全专家
│   ├── test-checker.md               # 测试专家
│   └── performance-analyzer.md       # 性能专家
├── mcp/
│   └── github-config.json            # GitHub 集成
├── hooks/
│   └── pre-review.js                 # 审查前验证
└── README.md                         # 插件文档
```

**功能**：安全分析、测试覆盖率、性能影响评估

**命令**：`/review-pr`、`/check-security`、`/check-tests`

**安装**：`/plugin install pr-review`

---

### DevOps 自动化插件（15 个文件）
```
devops-automation/
├── .claude-plugin/
│   └── plugin.json                   # 插件清单
├── commands/
│   ├── deploy.md                     # 部署
│   ├── rollback.md                   # 回滚
│   ├── status.md                     # 系统状态
│   └── incident.md                   # 事件响应
├── agents/
│   ├── deployment-specialist.md      # 部署专家
│   ├── incident-commander.md         # 事件协调指挥官
│   └── alert-analyzer.md             # 系统健康分析器
├── mcp/
│   └── kubernetes-config.json        # Kubernetes 集成
├── hooks/
│   ├── pre-deploy.js                 # 部署前检查
│   └── post-deploy.js                # 部署后任务
├── scripts/
│   ├── deploy.sh                     # 部署自动化脚本
│   ├── rollback.sh                   # 回滚自动化脚本
│   └── health-check.sh               # 健康检查工具
└── README.md                         # 插件文档
```

**功能**：Kubernetes 部署、回滚、监控、事件响应

**命令**：`/deploy`、`/rollback`、`/status`、`/incident`

**安装**：`/plugin install devops-automation`

---

### 文档插件（14 个文件）
```
documentation/
├── .claude-plugin/
│   └── plugin.json                   # 插件清单
├── commands/
│   ├── generate-api-docs.md          # API 文档生成
│   ├── generate-readme.md            # README 创建
│   ├── sync-docs.md                  # 文档同步
│   └── validate-docs.md              # 文档验证
├── agents/
│   ├── api-documenter.md             # API 文档专家
│   ├── code-commentator.md           # 代码注释专家
│   └── example-generator.md          # 示例创建专家
├── mcp/
│   └── github-docs-config.json       # GitHub 集成
├── templates/
│   ├── api-endpoint.md               # API 端点模板
│   ├── function-docs.md              # 函数文档模板
│   └── adr-template.md               # ADR 模板
└── README.md                         # 插件文档
```

**功能**：API 文档、README 生成、文档同步、验证

**命令**：`/generate-api-docs`、`/generate-readme`、`/sync-docs`、`/validate-docs`

**安装**：`/plugin install documentation`

此外还有：`README.md` — 插件概览和使用指南

---

## 08. 检查点与回退（2 个文件）

保存对话状态并探索替代方案。

| 文件 | 描述 | 内容 |
|------|------|------|
| `README.md` | 文档 | 全面的检查点指南 |
| `checkpoint-examples.md` | 真实案例 | 数据库迁移、性能优化、UI 迭代、调试 |

**核心概念**：
- **检查点（Checkpoint）**：对话状态的快照
- **回退（Rewind）**：返回到之前的检查点
- **分支点（Branch Point）**：探索多种方案

**用法**：
```
# 每次用户输入时自动创建检查点
# 要回退：按 Esc 键两次或使用：
/rewind
# 然后选择：恢复代码和对话、仅恢复对话、仅恢复代码、
# 从此处摘要、或取消
```

**使用场景**：
- 尝试不同的实现方式
- 从错误中恢复
- 安全实验
- 对比解决方案
- A/B 测试

---

## 09. 高级功能（3 个文件）

用于复杂工作流的高级能力。

| 文件 | 描述 | 功能 |
|------|------|------|
| `README.md` | 完整指南 | 所有高级功能的文档 |
| `config-examples.json` | 配置示例 | 10+ 种特定场景的配置 |
| `planning-mode-examples.md` | 规划模式示例 | REST API、数据库迁移、重构 |

**涵盖的高级功能**：

### 规划模式
- 创建详细的实施计划
- 时间估算和风险评估
- 系统化的任务分解

### 扩展思考
- 复杂问题的深度推理
- 架构决策分析
- 权衡评估

### 后台任务
- 不阻塞的长时间运行操作
- 并行开发工作流
- 任务管理和监控

### 权限模式
- **default**：对有风险的操作请求批准
- **acceptEdits**：自动接受文件编辑，其他操作请求批准
- **plan**：只读分析，不做修改
- **auto**：自动批准安全操作，对有风险操作进行提示
- **dontAsk**：接受除有风险操作外的所有操作
- **bypassPermissions**：接受所有操作（需要 `--dangerously-skip-permissions`）

### 无头模式（`claude -p`）
- CI/CD 集成
- 自动化任务执行
- 批处理

### 会话管理
- 多个工作会话
- 会话切换和保存
- 会话持久化

---

## 10. CLI 使用（1 个文件）

命令行界面使用模式和参考。

| 文件 | 描述 | 内容 |
|------|------|------|
| `README.md` | CLI 文档 | 标志、选项和使用模式 |

**核心 CLI 功能**：
- `claude` — 启动交互式会话
- `claude -p "prompt"` — 无头/非交互式模式
- `claude web` — 启动 Web 会话
- `claude --model` — 选择模型（Sonnet 4.6、Opus 4.6）
- `claude --permission-mode` — 设置权限模式
- `claude --remote` — 通过 WebSocket 启用远程控制

---

## 文档文件（13 个文件）

| 文件 | 位置 | 描述 |
|------|------|------|
| `README.md` | `/` | 主示例概览 |
| `INDEX.md` | `/` | 本完整索引 |
| `QUICK_REFERENCE.md` | `/` | 快速参考卡 |
| `README.md` | `/01-slash-commands/` | 斜杠命令指南 |
| `README.md` | `/02-memory/` | 记忆指南 |
| `README.md` | `/03-skills/` | 技能指南 |
| `README.md` | `/04-subagents/` | 子代理指南 |
| `README.md` | `/05-mcp/` | MCP 指南 |
| `README.md` | `/06-hooks/` | 钩子指南 |
| `README.md` | `/07-plugins/` | 插件指南 |
| `README.md` | `/08-checkpoints/` | 检查点指南 |
| `README.md` | `/09-advanced-features/` | 高级功能指南 |
| `README.md` | `/10-cli/` | CLI 指南 |

---

## 按使用场景快速开始

### 代码质量和审查
```bash
# 安装斜杠命令
cp 01-slash-commands/optimize.md .claude/commands/

# 安装子代理
cp 04-subagents/code-reviewer.md .claude/agents/

# 安装技能
cp -r 03-skills/code-review ~/.claude/skills/

# 或安装完整插件
/plugin install pr-review
```

### DevOps 与部署
```bash
# 安装插件（包含一切）
/plugin install devops-automation
```

### 文档
```bash
# 安装斜杠命令
cp 01-slash-commands/generate-api-docs.md .claude/commands/

# 安装子代理
cp 04-subagents/documentation-writer.md .claude/agents/

# 安装技能
cp -r 03-skills/doc-generator ~/.claude/skills/

# 或安装完整插件
/plugin install documentation
```

### 团队标准
```bash
# 设置项目记忆
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 编辑以匹配你团队的标准
```

### 外部集成
```bash
# 设置环境变量
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 安装 MCP 配置（项目级）
cp 05-mcp/multi-mcp.json .mcp.json
```

### 自动化与验证
```bash
# 安装钩子
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 在设置中配置钩子（~/.claude/settings.json）
# 参见 06-hooks/README.md
```

### 安全实验
```bash
# 每次用户输入时自动创建检查点
# 要回退：按 Esc+Esc 或使用 /rewind
# 然后从回退菜单中选择要恢复的内容

# 详细示例参见 08-checkpoints/README.md
```

### 高级工作流
```bash
# 配置高级功能
# 参见 09-advanced-features/config-examples.json

# 使用规划模式
/plan Implement feature X

# 使用权限模式
claude --permission-mode plan          # 用于代码审查（只读）
claude --permission-mode acceptEdits   # 自动接受编辑
claude --permission-mode auto          # 自动批准安全操作

# 以无头模式运行用于 CI/CD
claude -p "Run tests and report results"

# 运行后台任务
Run tests in background

# 完整指南参见 09-advanced-features/README.md
```

---

## 功能覆盖矩阵

| 类别 | 命令 | 代理 | MCP | 钩子 | 脚本 | 模板 | 文档 | 图片 | 总计 |
|------|------|------|-----|-------|---------|-----------|------|--------|-------|
| **01 斜杠命令** | 8 | - | - | - | - | - | 1 | 1 | **10** |
| **02 记忆** | - | - | - | - | - | 3 | 1 | 2 | **6** |
| **03 技能** | - | - | - | - | 5 | 9 | 1 | - | **28** |
| **04 子代理** | - | 8 | - | - | - | - | 1 | - | **9** |
| **05 MCP** | - | - | 4 | - | - | - | 1 | - | **5** |
| **06 钩子** | - | - | - | 8 | - | - | 1 | - | **9** |
| **07 插件** | 11 | 9 | 3 | 3 | 3 | 3 | 4 | - | **40** |
| **08 检查点** | - | - | - | - | - | - | 1 | 1 | **2** |
| **09 高级功能** | - | - | - | - | - | - | 1 | 2 | **3** |
| **10 CLI** | - | - | - | - | - | - | 1 | - | **1** |

---

## 学习路径

### 入门阶段（第 1 周）
1. ✅ 阅读 `README.md`
2. ✅ 安装 1-2 个斜杠命令
3. ✅ 创建项目记忆文件
4. ✅ 尝试基本命令

### 进阶阶段（第 2-3 周）
1. ✅ 设置 GitHub MCP
2. ✅ 安装一个子代理
3. ✅ 尝试委派任务
4. ✅ 安装一个技能

### 高级阶段（第 4 周+）
1. ✅ 安装完整插件
2. ✅ 创建自定义斜杠命令
3. ✅ 创建自定义子代理
4. ✅ 创建自定义技能
5. ✅ 构建你自己的插件

### 专家阶段（第 5 周+）
1. ✅ 设置钩子实现自动化
2. ✅ 使用检查点进行实验
3. ✅ 配置规划模式
4. ✅ 有效使用权限模式
5. ✅ 为 CI/CD 设置无头模式
6. ✅ 掌握会话管理

---

## 按关键词搜索

### 性能相关
- `01-slash-commands/optimize.md` — 性能分析
- `04-subagents/code-reviewer.md` — 性能审查
- `03-skills/code-review/` — 性能指标
- `07-plugins/pr-review/agents/performance-analyzer.md` — 性能专家

### 安全相关
- `04-subagents/secure-reviewer.md` — 安全审查
- `03-skills/code-review/` — 安全分析
- `07-plugins/pr-review/` — 安全检查

### 测试相关
- `04-subagents/test-engineer.md` — 测试工程师
- `07-plugins/pr-review/commands/check-tests.md` — 测试覆盖率

### 文档相关
- `01-slash-commands/generate-api-docs.md` — API 文档命令
- `04-subagents/documentation-writer.md` — 文档编写代理
- `03-skills/doc-generator/` — 文档生成器技能
- `07-plugins/documentation/` — 完整文档插件

### 部署相关
- `07-plugins/devops-automation/` — 完整 DevOps 方案

### 自动化相关
- `06-hooks/` — 事件驱动自动化
- `06-hooks/pre-commit.sh` — 提交前自动化
- `06-hooks/format-code.sh` — 自动格式化
- `09-advanced-features/` — CI/CD 用的无头模式

### 实验相关
- `08-checkpoints/` — 利用回退的安全实验
- `08-checkpoints/checkpoint-examples.md` — 真实案例

### 规划相关
- `09-advanced-features/planning-mode-examples.md` — 规划模式示例
- `09-advanced-features/README.md` — 扩展思考

### 配置相关
- `09-advanced-features/config-examples.json` — 配置示例

---

## 备注

- 所有示例均可直接使用
- 根据你的具体需求修改
- 示例遵循 Claude Code 最佳实践
- 每个类别都有详细的 README 说明
- 脚本包含完善的错误处理
- 模板可自由定制

---

## 如何贡献

想添加更多示例？遵循以下结构：
1. 创建适当的子目录
2. 包含带使用说明的 README.md
3. 遵循命名规范
4. 充分测试
5. 更新本索引

---

**最后更新时间**：2026 年 3 月
**示例总数**：100+ 个文件
**分类数**：10 个功能类别
**钩子数**：8 个自动化脚本
**配置示例**：10+ 种场景
**可用状态**：全部就绪
