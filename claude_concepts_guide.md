<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude 概念完全指南

一份全面的参考指南，涵盖斜杠命令、子代理、记忆、MCP 协议和代理技能，包含表格、图表和实用示例。

---

## 目录

1. [斜杠命令](#斜杠命令)
2. [子代理](#子代理)
3. [记忆](#记忆)
4. [MCP 协议](#mcp-协议)
5. [代理技能](#代理技能)
6. [插件](#claude-code-插件)
7. [钩子](#钩子)
8. [检查点与回退](#检查点与回退)
9. [高级功能](#高级功能)
10. [比较与集成](#比较与集成)

---

## 斜杠命令

### 概述

斜杠命令（Slash Commands）是用户调用的快捷方式，以 Markdown 文件形式存储，Claude Code 可以执行它们。它们使团队能够标准化常用的提示词和工作流。

### 架构

```mermaid
graph TD
    A["用户输入: /command-name"] -->|触发| B["搜索 .claude/commands/"]
    B -->|找到| C["command-name.md"]
    C -->|加载| D["Markdown 内容"]
    D -->|执行| E["Claude 处理提示词"]
    E -->|返回| F["上下文中的结果"]
```

### 文件结构

```mermaid
graph LR
    A["项目根目录"] -->|包含| B[".claude/commands/"]
    B -->|包含| C["optimize.md"]
    B -->|包含| D["test.md"]
    B -->|包含| E["docs/"]
    E -->|包含| F["generate-api-docs.md"]
    E -->|包含| G["generate-readme.md"]
```

### 命令组织表

| 位置 | 范围 | 可用性 | 用例 | Git 跟踪 |
|------|------|--------|------|----------|
| `.claude/commands/` | 项目特定 | 团队成员 | 团队工作流、共享标准 | ✅ 是 |
| `~/.claude/commands/` | 个人 | 单个用户 | 跨项目的个人快捷方式 | ❌ 否 |
| 子目录 | 命名空间化 | 基于父目录 | 按类别组织 | ✅ 是 |

### 功能与能力

| 功能 | 示例 | 支持 |
|------|------|------|
| Shell 脚本执行 | `bash scripts/deploy.sh` | ✅ 是 |
| 文件引用 | `@path/to/file.js` | ✅ 是 |
| Bash 集成 | `$(git log --oneline)` | ✅ 是 |
| 参数 | `/pr --verbose` | ✅ 是 |
| MCP 命令 | `/mcp__github__list_prs` | ✅ 是 |

### 实用示例

#### 示例 1：代码优化命令

**文件：** `.claude/commands/optimize.md`

```markdown
---
name: 代码优化
description: 分析代码的性能问题并建议优化
tags: performance, analysis
---

# 代码优化

按优先级顺序审查以下问题：

1. **性能瓶颈** - 识别 O(n²) 操作、低效循环
2. **内存泄漏** - 查找未释放的资源、循环引用
3. **算法改进** - 建议更好的算法或数据结构
4. **缓存机会** - 识别重复计算
5. **并发问题** - 查找竞态条件或线程问题

格式化你的响应：
- 问题严重程度（Critical/High/Medium/Low）
- 代码中的位置
- 解释说明
- 建议修复方案及代码示例
```

**用法：**
```bash
# 用户在 Claude Code 中输入
/optimize

# Claude 加载提示词并等待代码输入
```

#### 示例 2：Pull Request 辅助命令

**文件：** `.claude/commands/pr.md`

```markdown
---
name: 准备 Pull Request
description: 清理代码、暂存更改并准备 Pull Request
tags: git, workflow
---

# Pull Request 准备清单

在创建 PR 之前，执行以下步骤：

1. 运行代码检查：`prettier --write .`
2. 运行测试：`npm test`
3. 审查 git diff：`git diff HEAD`
4. 暂存更改：`git add .`
5. 创建符合 conventional commits 规范的提交信息：
   - `fix:` 用于 Bug 修复
   - `feat:` 用于新功能
   - `docs:` 用于文档更新
   - `refactor:` 用于代码重构
   - `test:` 用于测试补充
   - `chore:` 用于维护工作

6. 生成 PR 摘要，包括：
   - 变更内容
   - 变更原因
   - 执行的测试
   - 潜在影响
```

**用法：**
```bash
/pr

# Claude 运行清单并准备 PR
```

#### 示例 3：分层文档生成器

**文件：** `.claude/commands/docs/generate-api-docs.md`

```markdown
---
name: 生成 API 文档
description: 从源代码创建全面的 API 文档
tags: documentation, api
---

# API 文档生成器

通过以下步骤生成 API 文档：

1. 扫描 `/src/api/` 中的所有文件
2. 提取函数签名和 JSDoc 注释
3. 按端点/模块组织
4. 创建带示例的 Markdown
5. 包含请求/响应模式
6. 添加错误文档

输出格式：
- `/docs/api.md` 中的 Markdown 文件
- 为所有端点包含 curl 示例
- 添加 TypeScript 类型
```

### 命令生命周期图

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant FS as FileSystem
    participant CLI as Shell/Bash

    User->>Claude: 输入 /optimize
    Claude->>FS: 搜索 .claude/commands/
    FS-->>Claude: 返回 optimize.md
    Claude->>Claude: 加载 Markdown 内容
    Claude->>User: 显示提示词上下文
    User->>Claude: 提供要分析的代码
    Claude->>CLI: (可能执行脚本)
    CLI-->>Claude: 结果
    Claude->>User: 返回分析结果
```

### 最佳实践

| ✅ 推荐 | ❌ 不推荐 |
|---------|----------|
| 使用清晰、面向动作的命名 | 为一次性任务创建命令 |
| 在 description 中记录触发词 | 在命令中构建复杂逻辑 |
| 保持命令专注于单一任务 | 创建冗余命令 |
| 对项目命令进行版本控制 | 硬编码敏感信息 |
| 在子目录中组织相关文件 | 创建过长的命令列表 |
| 使用简单、可读的提示词 | 使用缩写或晦涩的措辞 |

---

## 子代理

### 概述

子代理（Subagents）是具有隔离上下文窗口和自定义系统提示词的专业 AI 助手。它们支持委托任务执行，同时保持清晰的关注点分离。

### 架构图

```mermaid
graph TB
    User[" 用户"]
    Main["[OK] 主代理 (协调者)"]
    Reviewer["[OK] 代码审查者 子代理"]
    Tester["[OK] 测试工程师 子代理"]
    Docs[" 文档编写 子代理"]

    User -->|请求| Main
    Main -->|委托| Reviewer
    Main -->|委托| Tester
    Main -->|委托| Docs
    Reviewer -->|返回结果| Main
    Tester -->|返回结果| Main
    Docs -->|返回结果| Main
    Main -->|综合| User
```

### 子代理生命周期

```mermaid
sequenceDiagram
    participant User
    participant MainAgent as MainAgent
    participant CodeReviewer as CodeReviewer 子代理
    participant Context as IsolatedContext

    User->>MainAgent: "构建新的认证功能"
    MainAgent->>MainAgent: 分析任务
    MainAgent->>CodeReviewer: "审查这段代码"
    CodeReviewer->>Context: 初始化干净上下文
    Context->>CodeReviewer: 加载审查指令
    CodeReviewer->>CodeReviewer: 执行审查
    CodeReviewer-->>MainAgent: 返回发现
    MainAgent->>MainAgent: 整合结果
    MainAgent-->>User: 提供综合分析
```

### 子代理配置表

| 配置项 | 类型 | 用途 | 示例 |
|--------|------|------|------|
| `name` | 字符串 | 代理标识符 | `code-reviewer` |
| `description` | 字符串 | 用途与触发术语 | `Comprehensive code quality analysis` |
| `tools` | 列表/字符串 | 允许的能力 | `read, grep, diff, lint_runner` |
| `system_prompt` | Markdown | 行为指令 | 自定义指南 |

### 工具访问层级

```mermaid
graph TD
    A["子代理配置"] -->|选项 1| B["继承主线程 的所有工具"]
    A -->|选项 2| C["指定单个工具"]
    B -->|包含| B1["文件操作"]
    B -->|包含| B2["Shell 命令"]
    B -->|包含| B3["MCP 工具"]
    C -->|显式列表| C1["read, grep, diff"]
    C -->|显式列表| C2["Bash(npm:*), Bash(test:*)"]
```

### 实用示例

#### 示例 1：完整的子代理设置

**文件：** `.claude/agents/code-reviewer.md`

```yaml
---
name: code-reviewer
description: 全面的代码质量和可维护性分析
tools: read, grep, diff, lint_runner
---

# 代码审查代理

你是一位专家级代码审查员，专长于：

- 性能优化
- 安全漏洞
- 代码可维护性
- 测试覆盖率
- 设计模式

## 审查优先级（按顺序）

1. **安全问题** - 认证、授权、数据泄露
2. **性能问题** - O(n²) 操作、内存泄漏、低效查询
3. **代码质量** - 可读性、命名、文档
4. **测试覆盖率** - 缺失测试、边界情况
5. **设计模式** - SOLID 原则、架构

## 审查输出格式

对每个问题：
- **严重程度**：Critical / High / Medium / Low
- **类别**：Security / Performance / Quality / Testing / Design
- **位置**：文件路径和行号
- **问题描述**：哪里有问题以及原因
- **建议修复**：代码示例
- **影响**：对系统的影响

## 审查示例

### 问题：N+1 查询问题
- **严重程度**：高
- **类别**：性能
- **位置**：src/user-service.ts:45
- **问题**：循环在每次迭代中执行数据库查询
- **修复**：使用 JOIN 或批量查询
```

**文件：** `.claude/agents/test-engineer.md`

```yaml
---
name: test-engineer
description: 测试策略、覆盖率分析和自动化测试
tools: read, write, bash, grep
---

# 测试工程师代理

你的专长：

- 编写全面的测试套件
- 确保高代码覆盖率（>80%）
- 测试边界情况和错误场景
- 性能基准测试
- 集成测试

## 测试策略

1. **单元测试** - 单个函数/方法
2. **集成测试** - 组件交互
3. **端到端测试** - 完整工作流
4. **边界情况** - 边界条件
5. **错误场景** - 故障处理

## 测试输出要求

- 对 JavaScript/TypeScript 使用 Jest
- 为每个测试包含 setup/teardown
- Mock 外部依赖
- 记录测试目的
- 在相关时包含性能断言

## 覆盖率要求

- 最低 80% 代码覆盖率
- 关键路径 100% 覆盖率
- 报告缺失覆盖率区域
```

**文件：** `.claude/agents/documentation-writer.md`

```yaml
---
name: documentation-writer
description: 技术文档、API 文档和用户指南
tools: read, write, grep
---

# 文档编写代理

你创建：

- 带示例的 API 文档
- 用户指南和教程
- 架构文档
- 更新日志条目
- 代码注释改进

## 文档标准

1. **清晰度** - 使用简单、清晰的语言
2. **示例** - 包含实用的代码示例
3. **完整性** - 覆盖所有参数和返回值
4. **结构** - 使用一致的格式
5. **准确性** - 对照实际代码验证

## 文档章节

### 针对 API
- 描述
- 参数（带类型）
- 返回值（带类型）
- 可能抛出的异常（可能的错误）
- 示例（curl、JavaScript、Python）
- 相关端点

### 针对功能
- 概述
- 前置条件
- 分步说明
- 预期结果
- 故障排除
- 相关主题
```

#### 示例 2：子代理委托实战

```markdown
# 场景：构建支付功能

## 用户请求
"构建一个安全的支付处理功能，集成 Stripe"

## 主代理流程

1. **规划阶段**
   - 理解需求
   - 确定所需任务
   - 规划架构

2. **委托给代码审查子代理**
   - 任务："审查支付处理实现的安全性"
   - 上下文：认证、API 密钥、Token 处理
   - 审查内容：SQL 注入、密钥暴露、HTTPS 强制执行

3. **委托给测试工程师子代理**
   - 任务："为支付流程创建全面测试"
   - 上下文：成功场景、失败场景、边界情况
   - 创建测试：有效支付、拒绝卡片、网络故障、Webhook

4. **委托给文档编写子代理**
   - 任务："记录支付 API 端点"
   - 上下文：请求/响应模式
   - 产出：带 curl 示例的 API 文档、错误码

5. **综合**
   - 主代理收集所有输出
   - 整合发现
   - 向用户返回完整解决方案
```

#### 示例 3：工具权限范围控制

**限制性设置 — 仅限特定命令**

```yaml
---
name: secure-reviewer
description: 最小权限的安全焦点代码审查
tools: read, grep
---

# 安全代码审查者

仅审查安全漏洞。

此代理：
- ✅ 读取文件进行分析
- ✅ 搜索模式
- ❌ 不能执行代码
- ❌ 不能修改文件
- ❌ 不能运行测试

这确保审查者不会意外破坏任何东西。
```

**扩展设置 — 实现的全功能**

```yaml
---
name: implementation-agent
description: 功能开发的完整实现能力
tools: read, write, bash, grep, edit, glob
---

# 实现代理

从规格说明构建功能。

此代理：
- ✅ 读取规格说明
- ✅ 编写新代码文件
- ✅ 运行构建命令
- ✅ 搜索代码库
- ✅ 编辑现有文件
- ✅ 查找匹配模式的文件
```

### 子代理上下文管理

```mermaid
graph TB
    A["主代理上下文 50,000 tokens"]
    B["子代理 1 上下文 20,000 tokens"]
    C["子代理 2 上下文 20,000 tokens"]
    D["子代理 3 上下文 20,000 tokens"]

    A -->|干净状态| B
    A -->|干净状态| C
    A -->|干净状态| D

    B -->|仅结果| A
    C -->|仅结果| A
    D -->|仅结果| A

    style A fill:#e1f5ff
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
```

### 何时使用子代理

| 场景 | 使用子代理 | 原因 |
|------|-----------|------|
| 多步骤复杂功能 | ✅ 是 | 分离关注点，防止上下文污染 |
| 快速代码审查 | ❌ 否 | 无必要开销 |
| 并行任务执行 | ✅ 是 | 每个子代理有自己的上下文 |
| 需要专业知识 | ✅ 是 | 自定义系统提示词 |
| 长时间运行的分析 | ✅ 是 | 防止主上下文耗尽 |
| 单一任务 | ❌ 否 | 不必要地增加延迟 |

### 代理团队

代理团队协调多个代理处理相关任务。不同于一次委托一个子代理，代理团队允许主代理编排一组协作、共享中间结果并朝着共同目标工作的代理。这对于大规模任务非常有用，例如全栈功能开发中前端代理、后端代理和测试代理并行工作的情况。

---

## 记忆

### 概述

记忆使 Claude 能够跨会话和对话保留上下文。它存在两种形式：claude.ai 中的自动合成，以及 Claude Code 中基于文件系统的 CLAUDE.md。

### 记忆架构

```mermaid
graph TB
    A["Claude 会话"]
    B["用户输入"]
    C["记忆系统"]
    D["记忆存储"]

    B -->|用户提供信息| C
    C -->|每 24 小时合成| D
    D -->|自动加载| A
    A -->|使用上下文| C
```

### Claude Code 中的记忆层级（7 层）

Claude Code 从 7 个层级加载记忆，按从高到低的优先级排列：

```mermaid
graph TD
    A["1. 托管策略 企业管理员策略"] --> B["2. 项目记忆 ./CLAUDE.md"]
    B --> C["3. 项目规则 .claude/rules/*.md"]
    C --> D["4. 用户记忆 ~/.claude/CLAUDE.md"]
    D --> E["5. 用户规则 ~/.claude/rules/*.md"]
    E --> F["6. 本地记忆 .claude/local/CLAUDE.md"]
    F --> G["7. 自动记忆 自动捕获的偏好设置"]

    style A fill:#fce4ec,stroke:#333,color:#333
    style B fill:#e1f5fe,stroke:#333,color:#333
    style C fill:#e1f5fe,stroke:#333,color:#333
    style D fill:#f3e5f5,stroke:#333,color:#333
    style E fill:#f3e5f5,stroke:#333,color:#333
    style F fill:#e8f5e9,stroke:#333,color:#333
    style G fill:#fff3e0,stroke:#333,color:#333
```

### 记忆位置表

| 层级 | 位置 | 范围 | 优先级 | 共享 | 适用场景 |
|------|------|------|--------|------|----------|
| 1. 托管策略 | 企业管理员 | 组织 | 最高 | 所有组织用户 | 合规、安全策略 |
| 2. 项目 | `./CLAUDE.md` | 项目 | 高 | 团队（Git） | 团队标准、架构 |
| 3. 项目规则 | `.claude/rules/*.md` | 项目 | 高 | 团队（Git） | 模块化的项目约定 |
| 4. 用户 | `~/.claude/CLAUDE.md` | 个人 | 中等 | 个人 | 个人偏好 |
| 5. 用户规则 | `~/.claude/rules/*.md` | 个人 | 中等 | 个人 | 个人规则模块 |
| 6. 本地 | `.claude/local/CLAUDE.md` | 本地 | 低 | 不共享 | 特定机器设置 |
| 7. 自动记忆 | 自动 | 会话 | 最低 | 个人 | 学习到的偏好、模式 |

### 自动记忆

自动记忆自动捕获会话期间观察到的用户偏好和模式。Claude 从交互中学习并记住：

- 编码风格偏好
- 你常做的修正
- 框架和工具选择
- 通信风格偏好

自动记忆在后台运行，无需手动配置。

### 记忆更新生命周期

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Editor as FileSystem
    participant Memory as CLAUDE.md

    User->>Claude: "记住:使用 async/await"
    Claude->>User: "保存到哪个记忆文件?"
    User->>Claude: "项目记忆"
    Claude->>Editor: 打开 ~/.claude/settings.json
    Claude->>Memory: 写入 ./CLAUDE.md
    Memory-->>Claude: 文件已保存
    Claude->>Claude: 加载更新的记忆
    Claude-->>User: "记忆已保存!"
```

### 实用示例

#### 示例 1：项目记忆结构

**文件：** `./CLAUDE.md`

```markdown
# 项目配置

## 项目概览
- **名称**：电商平台
- **技术栈**：Node.js、PostgreSQL、React 18、Docker
- **团队规模**：5 名开发者
- **截止日期**：2025 年第四季度

## 架构
@docs/architecture.md
@docs/api-standards.md
@docs/database-schema.md

## 开发标准

### 代码风格
- 使用 Prettier 格式化
- 使用 ESLint 配置 airbnb 规则
- 最大行长：100 字符
- 使用 2 空格缩进

### 命名规范
- **文件**：kebab-case（user-controller.js）
- **类**：PascalCase（UserService）
- **函数/变量**：camelCase（getUserById）
- **常量**：UPPER_SNAKE_CASE（API_BASE_URL）
- **数据库表**：snake_case（user_accounts）

### Git 工作流
- 分支名称：`feature/description` 或 `fix/description`
- 提交信息：遵循 Conventional Commits
- 合并前需要 PR
- 所有 CI/CD 检查必须通过
- 至少需要 1 人批准

### 测试要求
- 最低 80% 代码覆盖率
- 所有关键路径必须有测试
- 单元测试使用 Jest
- 端到端测试使用 Cypress
- 测试文件名：`*.test.ts` 或 `*.spec.ts`

### API 标准
- 仅 RESTful 端点
- JSON 请求/响应
- 正确使用 HTTP 状态码
- 版本化 API 端点：`/api/v1/`
- 用示例文档化所有端点

### 数据库
- 使用迁移进行 Schema 变更
- 绝不硬编码凭据
- 使用连接池
- 开发环境启用查询日志
- 定期备份

### 部署
- 基于 Docker 的部署
- Kubernetes 编排
- 蓝/绿部署策略
- 失败时自动回滚
- 部署前运行数据库迁移

## 常用命令
| 命令 | 用途 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm test` | 运行测试套件 |
| `npm run lint` | 检查代码风格 |
| `npm run build` | 生产构建 |
| `npm run migrate` | 运行数据库迁移 |

## 团队联系人
- 技术负责人：Sarah Chen (@sarah.chen)
- 产品经理：Mike Johnson (@mike.j)
- DevOps：Alex Kim (@alex.k)

## 已知问题和解决方案
- PostgreSQL 连接池高峰时段限制为 20
- 解决方案：实现查询队列
- Safari 14 与 async generators 存在兼容性问题
- 解决方案：使用 Babel 转译器

## 相关项目
- 分析面板：`/projects/analytics`
- 移动应用：`/projects/mobile`
- 管理后台：`/projects/admin`
```

#### 示例 2：目录特定的记忆

**文件：** `./src/api/CLAUDE.md`

~~~~markdown
# API 模块标准

此文件覆盖 /src/api/ 中所有内容的根 CLAUDE.md

## API 特定标准

### 请求验证
- 使用 Zod 进行 Schema 验证
- 始终验证输入
- 返回 400 及验证错误详情
- 包含字段级别的错误信息

### 认证
- 所有端点需要 JWT Token
- Token 在 Authorization 头中
- Token 24 小时后过期
- 实现 Token 刷新机制

### 响应格式

所有响应必须遵循此结构：

```json
{
  "success": true,
  "data": { /* 实际数据 */ },
  "timestamp": "2025-11-06T10:30:00Z",
  "version": "1.0"
}
```

### 错误响应：
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "用户消息",
    "details": { /* 字段错误 */ }
  },
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### 分页
- 使用基于游标的分页（非偏移量）
- 包含 `hasMore` 布尔值
- 最大页大小限制为 100
- 默认页大小：20

### 速率限制
- 认证用户每小时 1000 次请求
- 公开端点每小时 100 次请求
- 超出时返回 429
- 包含 retry-after 头

### 缓存
- 使用 Redis 进行会话缓存
- 默认缓存时长：5 分钟
- 写操作时失效
- 用资源类型标记缓存键
~~~~

#### 示例 3：个人记忆

**文件：** `~/.claude/CLAUDE.md`

~~~~markdown
# 我的开发偏好

## 关于我
- **经验水平**：8 年全栈开发
- **首选语言**：TypeScript、Python
- **沟通风格**：直接，附带示例
- **学习风格**：可视化图表 + 代码

## 代码偏好

### 错误处理
我倾向于使用 try-catch 块进行显式错误处理，附带有意义的错误消息。避免通用错误。始终记录错误以便调试。

### 注释
注释用于解释 WHY，而非 WHAT。代码应该自文档化。注释应解释业务逻辑或不明显的决策。

### 测试
我倾向于 TDD（测试驱动开发）。先写测试，再写实现。关注行为而非实现细节。

### 架构
我倾向于模块化、松耦合设计。使用依赖注入提高可测试性。分离关注点（控制器、服务、仓库）。

## 调试偏好
- 使用 console.log 并加前缀：`[DEBUG]`
- 包含上下文：函数名、相关变量
- 可用时使用堆栈跟踪
- 日志始终包含时间戳

## 沟通
- 用图表解释复杂概念
- 先展示具体示例再解释理论
- 包含修改前后的代码片段
- 最后总结要点

## 项目组织
我的项目组织方式如下：
```
project/
  ├── src/
  │   ├── api/
  │   ├── services/
  │   ├── models/
  │   └── utils/
  ├── tests/
  ├── docs/
  └── docker/
```

## 工具链
- **IDE**：VS Code + vim 快捷键
- **终端**：Zsh + Oh-My-Zsh
- **格式化**：Prettier（100 字符行宽）
- **Linter**：ESLint + airbnb 配置
- **测试框架**：Jest + React Testing Library
~~~~

#### 示例 4：会话中的记忆更新

**会话交互：**

```markdown
用户：记住我更喜欢对所有新组件使用 React Hooks 而不是类组件

Claude：我会把这个添加到你的记忆中。应该保存到哪个记忆文件？
        1. 项目记忆（./CLAUDE.md）
        2. 个人记忆（~/.claude/CLAUDE.md）

用户：项目记忆

Claude：✅ 记忆已保存！

已添加到 ./CLAUDE.md：
---

### 组件开发
- 使用带 React Hooks 的函数式组件
- Hooks 优于类组件
- 自定义 Hook 用于可复用逻辑
- 事件处理器使用 useCallback
- 昂贵计算使用 useMemo
```

### Claude Web/Desktop 中的记忆

#### 记忆合成时间线

```mermaid
graph LR
    A["第 1 天:用户 对话"] -->|24 小时| B["第 2 天:记忆 合成"]
    B -->|自动| C["记忆已更新 摘要"]
    C -->|加载到| D["第 2-N 天: 新对话"]
    D -->|添加到| E["记忆"]
    E -->|24 小时后| F["记忆刷新"]
```

**示例记忆摘要：**

```markdown## Claude 对用户的记忆

### 专业背景
- 8 年经验的高级全栈开发者
- 专注 TypeScript/Node.js 后端和 React 前端
- 活跃的开源贡献者
- 对 AI 和机器学习感兴趣

### 项目背景
- 当前正在构建电商平台
- 技术栈：Node.js、PostgreSQL、React 18、Docker
- 与 5 名开发者组成的团队合作
- 使用 CI/CD 和蓝绿部署

### 沟通偏好
- 偏好直接、简洁的解释
- 喜欢可视化和示例
- 欣赏代码片段
- 在注释中解释业务逻辑

### 当前目标
- 提高 API 性能
- 将测试覆盖率提升至 90%
- 实现缓存策略
- 文档化架构
```

### 记忆功能对比

| 功能 | Claude Web/Desktop | Claude Code (CLAUDE.md) |
|------|-------------------|------------------------|
| 自动合成 | ✅ 每 24h | ❌ 手动 |
| 跨项目 | ✅ 共享 | ❌ 项目特定 |
| 团队访问 | ✅ 共享项目 | ✅ Git 跟踪 |
| 可搜索 | ✅ 内置 | ✅ 通过 `/memory` |
| 可编辑 | ✅ 聊天内 | ✅ 直接编辑文件 |
| 导入/导出 | ✅ 是 | ✅ 复制/粘贴 |
| 持久性 | ✅ 24h+ | ✅ 无限期 |

---

## MCP 协议

### 概述

MCP（Model Context Protocol，模型上下文协议）是 Claude 访问外部工具、API 和实时数据源的标准化方式。与记忆不同，MCP 提供对变化数据的实时访问。

### MCP 架构

```mermaid
graph TB
    A["Claude"]
    B["MCP 服务器"]
    C["外部服务"]

    A -->|请求: list_issues| B
    B -->|查询| C
    C -->|数据| B
    B -->|响应| A

    A -->|请求: create_issue| B
    B -->|操作| C
    C -->|结果| B
    B -->|响应| A
```

### MCP 生态系统

```mermaid
graph TB
    A["Claude"] -->|MCP| B["文件系统 MCP 服务器"]
    A -->|MCP| C["GitHub MCP 服务器"]
    A -->|MCP| D["数据库 MCP 服务器"]
    A -->|MCP| E["Slack MCP 服务器"]
    A -->|MCP| F["Google Docs MCP 服务器"]

    B -->|文件 I/O| G["本地文件"]
    C -->|API| H["GitHub 仓库"]
    D -->|查询| I["PostgreSQL/MySQL"]
    E -->|消息| J["Slack 工作区"]
    F -->|文档| K["Google Drive"]
```

### MCP 设置流程

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Config as Config文件
    participant Service as ExternalService

    User->>Claude: 输入 /mcp
    Claude->>Claude: 列出可用 MCP 服务器
    Claude->>User: 显示选项
    User->>Claude: 选择 GitHub MCP
    Claude->>Config: 更新配置
    Config->>Claude: 激活连接
    Claude->>Service: 测试连接
    Service-->>Claude: 认证成功
    Claude->>User: [OK] MCP 已连接!
```

### 可用 MCP 服务器表

| MCP 服务器 | 用途 | 常见工具 | 认证 | 实时 |
|------------|------|----------|------|------|
| **文件系统** | 文件操作 | read, write, delete | 操作系统权限 | ✅ 是 |
| **GitHub** | 仓库管理 | list_prs, create_issue, push | OAuth | ✅ 是 |
| **Slack** | 团队通信 | send_message, list_channels | Token | ✅ 是 |
| **数据库** | SQL 查询 | query, insert, update | 凭据 | ✅ 是 |
| **Google Docs** | 文档访问 | read, write, share | OAuth | ✅ 是 |
| **Asana** | 项目管理 | create_task, update_status | API Key | ✅ 是 |
| **Stripe** | 支付数据 | list_charges, create_invoice | API Key | ✅ 是 |
| **Memory** | 持久化记忆 | store, retrieve, delete | 本地 | ❌ 否 |

### 实用示例

#### 示例 1：GitHub MCP 配置

**文件：** `.mcp.json`（项目范围）或 `~/.claude.json`（用户范围）

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**可用 GitHub MCP 工具：**

~~~~markdown
# GitHub MCP 工具

## Pull Request 管理
- `list_prs` - 列出仓库中的所有 PR
- `get_pr` - 获取 PR 详情（含 diff）
- `create_pr` - 创建新 PR
- `update_pr` - 更新 PR 描述/标题
- `merge_pr` - 将 PR 合并到 main 分支
- `review_pr` - 添加审查评论

示例请求：
```
/mcp__github__get_pr 456

# 返回：
标题：Add dark mode support
作者：@alice
描述：使用 CSS 变量实现深色主题
状态：OPEN
审查者：@bob, @charlie
```

## Issue 管理
- `list_issues` - 列出所有 Issue
- `get_issue` - 获取 Issue 详情
- `create_issue` - 创建新 Issue
- `close_issue` - 关闭 Issue
- `add_comment` - 给 Issue 添加评论

## 仓库信息
- `get_repo_info` - 仓库详情
- `list_files` - 文件树结构
- `get_file_content` - 读取文件内容
- `search_code` - 跨代码库搜索

## Commit 操作
- `list_commits` - 提交历史
- `get_commit` - 特定 commit 详情
- `create_commit` - 创建新 commit
~~~~

#### 示例 2：数据库 MCP 设置

**配置：**

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-database"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/mydb"
      }
    }
  }
}
```

**示例用法：**

```markdown
用户：获取所有订单数超过 10 的用户

Claude：我来查询数据库找到这些信息。

# 使用 MCP 数据库工具：
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING COUNT(o.id) > 10
ORDER BY order_count DESC;

# 结果：
- Alice: 15 orders
- Bob: 12 orders
- Charlie: 11 orders
```

#### 示例 3：多 MCP 工作流

**场景：每日报告生成**

```markdown
# 使用多个 MCP 的每日报告工作流

## 设置
1. GitHub MCP - 获取 PR 指标
2. 数据库 MCP - 查询销售数据
3. Slack MCP - 发布报告
4. 文件系统 MCP - 保存报告

## 工作流

### 步骤 1：获取 GitHub 数据
/mcp__github__list_prs completed:true last:7days

输出：
- 总 PR 数：42
- 平均合并时间：2.3 小时
- 审查周转时间：1.1 小时

### 步骤 2：查询数据库
SELECT COUNT(*) as sales, SUM(amount) as revenue
FROM orders
WHERE created_at > NOW() - INTERVAL '1 day'

输出：
- 销售额：247
- 收入：$12,450

### 步骤 3：生成报告
将数据组合为 HTML 报告

### 步骤 4：保存到文件系统
写入 report.html 到 /reports/

### 步骤 5：发布到 Slack
发送摘要到 #daily-reports 频道

最终输出：
✅ 报告已生成并发布
📊 本周合并了 47 个 PR
💰 日销售额 $12,450
```

#### 示例 4：文件系统 MCP 操作

**配置：**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    }
  }
}
```

**可用操作：**

| 操作 | 命令 | 用途 |
|------|------|------|
| 列出文件 | `ls ~/projects` | 显示目录内容 |
| 读取文件 | `cat src/main.ts` | 读取文件内容 |
| 写入文件 | `create docs/api.md` | 创建新文件 |
| 编辑文件 | `edit src/app.ts` | 修改文件 |
| 搜索 | `grep "async function"` | 在文件中搜索 |
| 删除 | `rm old-file.js` | 删除文件 |

### MCP vs 记忆：决策矩阵

```mermaid
graph TD
    A["需要外部数据?"]
    A -->|否| B["使用记忆"]
    A -->|是| C["是否频繁变化?"]
    C -->|否/很少| B
    C -->|是/经常| D["使用 MCP"]

    B -->|存储| E["偏好 上下文 历史"]
    D -->|访问| F["实时 API 数据库 服务"]

    style B fill:#e1f5ff
    style D fill:#fff9c4
```

### 请求/响应模式

```mermaid
sequenceDiagram
    participant App as Claude
    participant MCP as MCP 服务器
    participant DB as Database

    App->>MCP: 请求:"SELECT * FROM users WHERE id=1"
    MCP->>DB: 执行查询
    DB-->>MCP: 结果集
    MCP-->>App: 返回解析后的数据
    App->>App: 处理结果
    App->>App: 继续任务

    Note over MCP,DB: 实时访问 无缓存
```

---

## 代理技能

### 概述

代理技能（Agent Skills）是可复用的、模型调用能力，以文件夹形式打包，包含指令、脚本和资源。Claude 自动检测并使用相关技能。

### 技能架构

```mermaid
graph TB
    A["技能目录"]
    B["SKILL.md"]
    C ["YAML 元数据"]
    D["指令"]
    E["脚本"]
    F["模板"]

    A --> B
    B --> C
    B --> D
    E --> A
    F --> A
```

### 技能加载流程

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude
    participant System as System
    participant Skill as SkillSystem

    User->>Claude: "创建 Excel 报告"
    Claude->>System: 扫描可用技能
    System->>System: 加载技能元数据
    Claude->>Claude: 匹配用户请求与技能
    Claude->>Skill: 加载 xlsx 技能 SKILL.md
    Skill-->>Claude: 返回指令 + 工具
    Claude->>Claude: 执行技能
    Claude->>User: 生成 Excel 文件
```

### 技能类型与位置表

| 类型 | 位置 | 范围 | 共享 | 同步 | 适用场景 |
|------|------|------|------|------|----------|
| 预构建 | 内置 | 全局 | 所有用户 | 自动 | 文档创建 |
| 个人 | `~/.claude/skills/` | 个人 | 否 | 手动 | 个人自动化 |
| 项目 | `.claude/skills/` | 团队 | 是 | Git | 团队标准 |
| 插件 | 通过插件安装 | 可变 | 取决于插件 | 自动 | 集成功能 |

### 预构建技能

```mermaid
graph TB
    A["预构建技能"]
    B["PowerPoint (pptx)"]
    C["Excel (xlsx)"]
    D["Word (docx)"]
    E["PDF"]

    A --> B
    A --> C
    A --> D
    A --> E

    B --> B1["创建演示文稿"]
    B --> B2["编辑幻灯片"]
    C --> C1["创建电子表格"]
    C --> C2["分析数据"]
    D --> D1["创建文档"]
    D --> D2["格式化文本"]
    E --> E1["生成 PDF"]
    E --> E2["填写表单"]
```

### 内置技能

Claude Code 现在包含 5 个内置技能，开箱即用：

| 技能 | 命令 | 用途 |
|------|------|------|
| **Simplify** | `/simplify` | 简化复杂的代码或解释 |
| **Batch** | `/batch` | 跨多个文件或项运行操作 |
| **Debug** | `/debug` | 带根因分析的系统化调试 |
| **Loop** | `/loop` | 按定时器调度重复任务 |
| **Claude API** | `/claude-api` | 直接与 Anthropic API 交互 |

这些内置技能始终可用，无需安装或配置。

### 实用示例

#### 示例 1：自定义代码审查技能

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
name: 代码审查专家
description: 全面代码审查，包含安全、性能和质量分析
version: "1.0.0"
tags:
  - code-review
  - quality
  - security
when_to_use: 当用户要求审查代码、分析代码质量或评估 PR 时
effort: high
shell: bash
---

# 代码审查技能

本技能提供全面的代码审查能力，重点关注：

1. **安全分析**
   - 认证/授权问题
   - 数据泄露风险
   - 注入漏洞
   - 密码学弱点
   - 敏感数据日志

2. **性能审查**
   - 算法效率（Big O 分析）
   - 内存优化
   - 数据库查询优化
   - 缓存机会
   - 并发问题

3. **代码质量**
   - SOLID 原则
   - 设计模式
   - 命名规范
   - 文档
   - 测试覆盖率

4. **可维护性**
   - 代码可读性
   - 函数大小（应 < 50 行）
   - 圈复杂度
   - 依赖管理
   - 类型安全

## 审查模板

对每段被审查的代码，提供：

### 总结
- 整体质量评估（1-5）
- 发现数量
- 推荐的优先领域

### 关键问题（如有）
- **问题**：清晰描述
- **位置**：文件和行号
- **影响**：为什么重要
- **严重程度**：Critical/High/Medium
- **修复**：代码示例

### 分类发现

#### 安全（如有问题）
列出安全漏洞及示例

#### 性能（如有问题）
列出性能问题及复杂度分析

#### 质量（如有问题）
列出代码质量问题及重构建议

#### 可维护性（如有问题）
列出可维护性问题及改进方案
```

## Python 脚本：analyze-metrics.py

```python
#!/usr/bin/env python3
import re
import sys

def analyze_code_metrics(code):
    """分析代码的常见指标。"""

    # 统计函数数量
    functions = len(re.findall(r'^def\s+\w+', code, re.MULTILINE))

    # 统计类数量
    classes = len(re.findall(r'^class\s+\w+', code, re.MULTILINE))

    # 平均行长
    lines = code.split('\n')
    avg_length = sum(len(l) for l in lines) / len(lines) if lines else 0

    # 估算复杂度
    complexity = len(re.findall(r'\b(if|elif|else|for|while|and|or)\b', code))

    return {
        'functions': functions,
        'classes': classes,
        'avg_line_length': avg_length,
        'complexity_score': complexity
    }

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    metrics = analyze_code_metrics(code)
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")
```

## Python 脚本：compare-complexity.py

```python
#!/usr/bin/env python3
"""
比较变更前后代码的圈复杂度。
帮助确定重构是否真正简化了代码结构。
"""

import re
import sys
from typing import Dict, Tuple

class ComplexityAnalyzer:
    """分析代码复杂度指标。"""

    def __init__(self, code: str):
        self.code = code
        self.lines = code.split('\n')

    def calculate_cyclomatic_complexity(self) -> int:
        """
        使用 McCabe 方法计算圈复杂度。
        统计决策点：if, elif, else, for, while, except, and, or
        """
        complexity = 1  # 基础复杂度

        # 统计决策点
        decision_patterns = [
            r'\bif\b',
            r'\belif\b',
            r'\bfor\b',
            r'\bwhile\b',
            r'\bexcept\b',
            r'\band\b(?!$)',
            r'\bor\b(?!$)'
        ]

        for pattern in decision_patterns:
            matches = re.findall(pattern, self.code)
            complexity += len(matches)

        return complexity

    def calculate_cognitive_complexity(self) -> int:
        """
        认知复杂度 — 理解起来有多难？
        基于嵌套深度和控制流。
        """
        cognitive = 0
        nesting_depth = 0

        for line in self.lines:
            # 跟踪嵌套深度
            if re.search(r'^\s*(if|for|while|def|class|try)\b', line):
                nesting_depth += 1
                cognitive += nesting_depth
            elif re.search(r'^\s*(elif|else|except|finally)\b', line):
                cognitive += nesting_depth

            # 缩进减少时降低嵌套
            if line and not line[0].isspace():
                nesting_depth = 0

        return cognitive

    def calculate_maintainability_index(self) -> float:
        """
        可维护性指数范围为 0-100。
        > 85: 优秀
        > 65: 良好
        > 50: 一般
        < 50: 较差
        """
        lines = len(self.lines)
        cyclomatic = self.calculate_cyclomatic_complexity()
        cognitive = self.calculate_cognitive_complexity()

        # 简化的 MI 计算
        mi = 171 - 5.2 * (cyclomatic / lines) - 0.23 * (cognitive) - 16.2 * (lines / 1000)

        return max(0, min(100, mi))

    def get_complexity_report(self) -> Dict:
        """生成全面的复杂度报告。"""
        return {
            'cyclomatic_complexity': self.calculate_cyclomatic_complexity(),
            'cognitive_complexity': self.calculate_cognitive_complexity(),
            'maintainability_index': round(self.calculate_maintainability_index(), 2),
            'lines_of_code': len(self.lines),
            'avg_line_length': round(sum(len(l) for l in self.lines) / len(self.lines), 2) if self.lines else 0
        }


def compare_files(before_file: str, after_file: str) -> None:
    """比较两个代码版本之间的复杂度指标。"""

    with open(before_file, 'r') as f:
        before_code = f.read()

    with open(after_file, 'r') as f:
        after_code = f.read()

    before_analyzer = ComplexityAnalyzer(before_code)
    after_analyzer = ComplexityAnalyzer(after_code)

    before_metrics = before_analyzer.get_complexity_report()
    after_metrics = after_analyzer.get_complexity_report()

    print("=" * 60)
    print("CODE COMPLEXITY COMPARISON")
    print("=" * 60)

    print("\nBEFORE:")
    print(f"  Cyclomatic Complexity:    {before_metrics['cyclomatic_complexity']}")
    print(f"  Cognitive Complexity:     {before_metrics['cognitive_complexity']}")
    print(f"  Maintainability Index:    {before_metrics['maintainability_index']}")
    print(f"  Lines of Code:            {before_metrics['lines_of_code']}")
    print(f"  Avg Line Length:          {before_metrics['avg_line_length']}")

    print("\nAFTER:")
    print(f"  Cyclomatic Complexity:    {after_metrics['cyclomatic_complexity']}")
    print(f"  Cognitive Complexity:     {after_metrics['cognitive_complexity']}")
    print(f"  Maintainability Index:    {after_metrics['maintainability_index']}")
    print(f"  Lines of Code:            {after_metrics['lines_of_code']}")
    print(f"  Avg Line Length:          {after_metrics['avg_line_length']}")

    print("\nCHANGES:")
    cyclomatic_change = after_metrics['cyclomatic_complexity'] - before_metrics['cyclomatic_complexity']
    cognitive_change = after_metrics['cognitive_complexity'] - before_metrics['cognitive_complexity']
    mi_change = after_metrics['maintainability_index'] - before_metrics['maintainability_index']
    loc_change = after_metrics['lines_of_code'] - before_metrics['lines_of_code']

    print(f"  Cyclomatic Complexity:    {cyclomatic_change:+d}")
    print(f"  Cognitive Complexity:     {cognitive_change:+d}")
    print(f"  Maintainability Index:    {mi_change:+.2f}")
    print(f"  Lines of Code:            {loc_change:+d}")

    print("\nASSESSMENT:")
    if mi_change > 0:
        print("  ✅ Code is MORE maintainable")
    elif mi_change < 0:
        print("  ⚠️  Code is LESS maintainable")
    else:
        print("  ➡️  Maintainability unchanged")

    if cyclomatic_change < 0:
        print("  ✅ Complexity DECREASED")
    elif cyclomatic_change > 0:
        print("  ⚠️  Complexity INCREASED")
    else:
        print("  ➡️  Complexity unchanged")

    print("=" * 60)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python compare-complexity.py <before_file> <after_file>")
        sys.exit(1)

    compare_files(sys.argv[1], sys.argv[2])
```

## 模板：review-checklist.md

```markdown
# 代码审查清单

## 安全检查清单
- [ ] 无硬编码凭据或密钥
- [ ] 所有用户输入都有验证
- [ ] SQL 注入防护（参数化查询）
- [ ] 状态变更操作的 CSRF 防护
- [ ] 正确转义的 XSS 防护
- [ ] 受保护端点的认证检查
- [ ] 资源的授权检查
- [ ] 安全密码哈希（bcrypt、argon2）
- [ ] 日志中无敏感数据
- [ ] 强制 HTTPS

## 性能检查清单
- [ ] 无 N+1 查询
- [ ] 适当使用索引
- [ ] 有益处时实现了缓存
- [ ] 主线程无阻塞操作
- [ ] async/await 正确使用
- [ ] 大数据集分页
- [ ] 数据库连接池
- [ ] 正则表达式优化
- [ ] 无不必要的对象创建
- [ ] 已防止内存泄漏

## 质量检查清单
- [ ] 函数 < 50 行
- [ ] 清晰的变量命名
- [ ] 无重复代码
- [ ] 适当的错误处理
- [ ] 注释解释 WHY 而非 WHAT
- [ ] 生产环境无 console.log
- [ ] 类型检查（TypeScript/JSDoc）
- [ ] 遵循 SOLID 原则
- [ ] 正确应用设计模式
- [ ] 自文档化代码

## 测试检查清单
- [ ] 已编写单元测试
- [ ] 覆盖边界情况
- [ ] 已测试错误场景
- [ ] 存在集成测试
- [ ] 覆盖率 > 80%
- [ ] 无不稳定测试
- [ ] Mock 外部依赖
- [ ] 清晰的测试名称
```

## 模板：finding-template.md

~~~~markdown
# 代码审查发现模板

在代码审查中发现每个问题时使用此模板。

---

## Issue: [标题]

### 严重程度
- [ ] Critical（阻止部署）
- [ ] High（合并前应修复）
- [ ] Medium（应尽快修复）
- [ ] Low（可选改进）

### 类别
- [ ] Security
- [ ] Performance
- [ ] Code Quality
- [ ] Maintainability
- [ ] Testing
- [ ] Design Pattern
- [ ] Documentation

### 位置
**文件：** `src/components/UserCard.tsx`

**行号：** 45-52

**函数/方法：** `renderUserDetails()`

### 问题描述

**是什么：** 描述问题所在。

**为什么重要：** 解释影响以及为何需要修复。

**当前行为：** 展示有问题的代码或行为。

**预期行为：** 描述应该发生什么。

### 代码示例

#### 当前（有问题）

```typescript
// 展示 N+1 查询问题
const users = fetchUsers();
users.forEach(user => {
  const posts = fetchUserPosts(user.id); // 每个用户一次查询！
  renderUserPosts(posts);
});
```

#### 建议修复

```typescript
// 使用 JOIN 查询优化
const usersWithPosts = fetchUsersWithPosts();
usersWithPosts.forEach(({ user, posts }) => {
  renderUserPosts(posts);
});
```

### 影响分析

| 方面 | 影响 | 严重程度 |
|------|------|----------|
| 性能 | 20 个用户产生 100+ 次查询 | High |
| 用户体验 | 页面加载缓慢 | High |
| 可扩展性 | 大规模时崩溃 | Critical |
| 可维护性 | 难以调试 | Medium |

### 相关问题

- `AdminUserList.tsx` 第 120 行存在类似问题
- 相关 PR：#456
- 相关 Issue：#789

### 其他资源

- [N+1 查询问题](https://en.wikipedia.org/wiki/N%2B1_problem)
- [数据库 Join 文档](https://docs.example.com/joins)

### 审查备注

- 这是代码库中的常见模式
- 考虑将其添加到代码风格指南
- 可能值得创建辅助函数

### 作者反馈（待填写）

*由代码作者填写：*

- [ ] 修复已在 commit `abc123` 中实现
- [ ] 修复状态：Complete / In Progress / Needs Discussion
- [ ] 问题或疑虑：（描述）

---

## 发现统计（供审查者使用）

审查多个问题时，跟踪：

- **总发现问题数**：X
- **Critical**：X
- **High**：X
- **Medium**：X
- **Low**：X

**建议**：✅ Approve / ⚠️ Request Changes / 🔄 Needs Discussion

**整体代码质量**：1-5 星
~~~~

## 用法示例

~~~~markdown
用户：审查这段 React 组件代码

Claude：我将使用代码审查技能进行全面审查。

[加载 SKILL.md]
[根据清单分析代码]
[运行 Python 指标脚本]
[应用模板]

## 代码审查结果

### 总结
质量评分：3.5/5
关键发现：7 项
优先领域：性能优化、错误处理

### 关键问题：1

**Issue**：N+1 查询问题
**位置**：UserComponent.tsx，第 45-52 行
**影响**：20 个用户列表渲染 100+ 次数据库查询
**严重程度**：高
**修复**：
```javascript
// Before: N+1 queries
const users = fetchUsers();
users.forEach(user => fetchUserPosts(user.id)); // 20+ queries

// After: Single query with JOIN
const users = fetchUsersWithPosts(); // 1 query
```

### 性能发现
- 大列表缺少分页
- 建议：对列表项使用 React.memo()
- 数据库查询：可通过索引优化

### 质量发现
- 第 20 行的函数有 127 行（最大：50）
- 缺少错误边界
- Props 应该有 TypeScript 类型
~~~~

#### 示例 2：品牌语调技能

**目录结构：**

```
.claude/skills/brand-voice/
├── SKILL.md
├── brand-guidelines.md
├── tone-examples.md
└── templates/
    ├── email-template.txt
    ├── social-post-template.txt
    └── blog-post-template.md
```

**文件：** `.claude/skills/brand-voice/SKILL.md`

```yaml
---
name: 品牌语调一致性
description: 确保所有沟通都符合品牌语调和风格指南
tags:
  - brand
  - writing
  - consistency
when_to_use: 创建营销文案、客户沟通或面向公众的内容时
---

# 品牌语调技能

## 概述
本技能确保所有沟通保持一致的品牌语调、语气和信息传递。

## 品牌身份

### 使命
帮助团队用 AI 自动化开发工作流

### 价值观
- **简约**：让复杂的事情变简单
- **可靠性**：坚如磐石的执行力
- **赋能**：激发人类创造力

### 语调
- **友好但专业** — 易接近但不随意
- **清晰简洁** — 避免行话，简单解释技术概念
- **自信** — 我们知道自己在做什么
- **共情** — 理解用户需求和痛点

## 写作指南

### 推荐 ✅
- 称呼读者时使用"你"
- 使用主动语态："Claude 生成报告"而非"报告由 Claude 生成"
- 以价值主张开头
- 使用具体示例
- 保持句子在 20 词以内
- 使用列表增强清晰度
- 包含行动号召

### 避免 ❌
- 不要使用企业黑话
- 不要居高临下或过度简化
- 不要使用"我们相信"或"我们认为"
- 不要全大写（除非强调）
- 不要创建大段文字墙
- 不要假设读者有技术知识

## 词汇

### ✅ 推荐用语
- Claude（而非 "the Claude AI"）
- 代码生成（而非 "auto-coding"）
- Agent（而非 "bot"）
- 简化流程（而非 "revolutionize"）
- 集成（而非 "synergize"）

### ❌ 避免用语
- "Cutting-edge"（过度使用）
- "Game-changer"（模糊）
- "Leverage"（企业腔）
- "Utilize"（请用 "use"）
- "Paradigm shift"（不清晰）
```

## 示例

### ✅ 好的示例
"Claude 自动化你的代码审查流程。无需手动检查每个 PR，Claude 自动审查安全性、性能和质量——每周为你节省数小时。"

为什么有效：价值清晰、具体好处、面向行动

### ❌ 差的示例
"Claude 利用尖端 AI 提供全面的软件开发解决方案。"

为什么无效：模糊、企业黑话、没有具体价值

## 模板：邮件

```
Subject: [清晰、利益驱动的主题]

Hi [Name],

[开头：对他们有什么价值]

[正文：如何运作 / 他们能得到什么]

[具体示例或好处]

[行动号召：明确的下一步]

Best regards,
[Name]
```

## 模板：社交媒体

```
[Hook：首行抓住注意力]
[2-3 行：价值或有趣事实]
[行动号召：链接、问题或互动]
[Emoji：最多 1-2 个增加视觉兴趣]
```

## 文件：tone-examples.md
```
激动人心的公告：
"每周节省 8 小时代码审查时间。Claude 自动审查你的 PR。"

共情支持：
"我们知道部署可能很有压力。Claude 处理测试，让你不必担心。"

自信的产品功能：
"Claude 不只是建议代码。它理解你的架构并保持一致性。"

教育博客文章：
"让我们探索代理如何改善代码审查工作流。这是我们学到的……"
```

#### 示例 3：文档生成器技能

**文件：** `.claude/skills/doc-generator/SKILL.md`

~~~~yaml
---
name: API 文档生成器
description: 从源代码生成全面、准确的 API 文档
version: "1.0.0"
tags:
  - documentation
  - api
  - automation
when_to_use: 创建或更新 API 文档时
---

# API 文档生成器技能

## 生成内容

- OpenAPI/Swagger 规范
- API 端点文档
- SDK 使用示例
- 集成指南
- 错误码参考
- 认证指南

## 文档结构

### 对每个端点

```markdown
## GET /api/v1/users/:id

### 描述
简要解释此端点的功能

### 参数

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | string | 是 | 用户 ID |

### 响应

**200 成功**
```json
{
  "id": "usr_123",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**404 未找到**
```json
{
  "error": "USER_NOT_FOUND",
  "message": "用户不存在"
}
```

### 示例

**cURL**
```bash
curl -X GET "https://api.example.com/api/v1/users/usr_123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**JavaScript**
```javascript
const user = await fetch('/api/v1/users/usr_123', {
  headers: { 'Authorization': 'Bearer token' }
}).then(r => r.json());
```

**Python**
```python
response = requests.get(
    'https://api.example.com/api/v1/users/usr_123',
    headers={'Authorization': 'Bearer token'}
)
user = response.json()
```
```

## Python 脚本：generate-docs.py

```python
#!/usr/bin/env python3
import ast
import json
from typing import Dict, List

class APIDocExtractor(ast.NodeVisitor):
    """从 Python 源代码提取 API 文档。"""

    def __init__(self):
        self.endpoints = []

    def visit_FunctionDef(self, node):
        """提取函数文档。"""
        if node.name.startswith('get_') or node.name.startswith('post_'):
            doc = ast.get_docstring(node)
            endpoint = {
                'name': node.name,
                'docstring': doc,
                'params': [arg.arg for arg in node.args.args],
                'returns': self._extract_return_type(node)
            }
            self.endpoints.append(endpoint)
        self.generic_visit()

    def _extract_return_type(self, node):
        """从函数注解提取返回类型。"""
        if node.returns:
            return ast.unparse(node.returns)
        return "Any"


def generate_markdown_docs(endpoints: List[Dict]) -> str:
    """从端点生成 Markdown 文档。"""
    docs = "# API Documentation\n\n"

    for endpoint in endpoints:
        docs += f"## {endpoint['name']}\n\n"
        docs += f"{endpoint['docstring']}\n\n"
        docs += f"**Parameters**: {', '.join(endpoint['params'])}\n\n"
        docs += f"**Returns**: {endpoint['returns']}\n\n"
        docs += "---\n\n"

    return docs


if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as f:
        tree = ast.parse(f.read())

    extractor = APIDocExtractor()
    extractor.visit(tree)

    markdown = generate_markdown_docs(extractor.endpoints)
    print(markdown)
~~~~

### 技能发现与调用

```mermaid
graph TD
    A["用户请求"] --> B["Claude 分析"]
    B -->|扫描| C["可用技能"]
    C -->|元数据检查| D["描述匹配?"]
    D -->|是| E["加载 SKILL.md"]
    D -->|否| F["尝试下一个技能"]
    F -->|还有技能?| D
    F -->|没有了| G["使用通用知识"]
    E --> H["提取指令"]
    H --> I["执行技能"]
    I --> J["返回结果"]
```

### 技能与其他功能的对比

```mermaid
graph TB
    A["扩展 Claude 能力"]
    B["斜杠命令"]
    C["子代理"]
    D["记忆"]
    E["MCP"]
    F["技能"]

    A --> B
    A --> C
    A --> D
    A --> E
    A --> F

    B -->|用户调用| G["快速快捷方式"]
    C -->|自动委托| H["隔离上下文"]
    D -->|持久化| I["跨会话上下文"]
    E -->|实时| J["外部数据访问"]
    F -->|自动调用| K["自主执行"]
```

---

## Claude Code 插件

### 概述

Claude Code 插件（Plugins）是定制化集合包（斜杠命令、子代理、MCP 服务器和钩子），通过单条命令安装。它们代表最高级的扩展机制——将多种功能整合为内聚的、可共享的包。

### 架构

```mermaid
graph TB
    A["插件"]
    B["斜杠命令"]
    C["子代理"]
    D["MCP 服务器"]
    E["钩子"]
    F["配置"]

    A -->|打包| B
    A -->|打包| C
    A -->|打包| D
    A -->|打包| E
    A -->|打包| F
```

### 插件加载流程

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Plugin as Plugin市场
    participant Install as Installer
    participant SlashCmds as SlashCommands
    participant Subagents as Subagents
    participant MCPServers as MCP 服务器
    participant Hooks as HooksSystem
    participant Tools as ConfiguredTools

    User->>Claude: /plugin install pr-review
    Claude->>Plugin: 下载插件清单
    Plugin-->>Claude: 返回插件定义
    Claude->>Install: 提取组件
    Install->>SlashCmds: 配置
    Install->>Subagents: 配置
    Install->>MCPServers: 配置
    Install->>Hooks: 配置
    SlashCmds-->>Tools: 就绪
    Subagents-->>Tools: 就绪
    MCPServers-->>Tools: 就绪
    Hooks-->>Tools: 就绪
    Tools-->>Claude: 插件已安装 [OK]
```

### 插件类型与分发

| 类型 | 范围 | 共享 | 权威来源 | 示例 |
|------|------|------|----------|------|
| 官方 | 全局 | 所有用户 | Anthropic | PR 审查、安全指导 |
| 社区 | 公开 | 所有用户 | 社区 | DevOps、数据科学 |
| 组织 | 内部 | 团队成员 | 公司 | 内部标准、工具 |
| 个人 | 个人 | 单个用户 | 开发者 | 自定义工作流 |

### 插件定义结构

```yaml
---
name: plugin-name
version: "1.0.0"
description: "此插件的功能"
author: "Your Name"
license: MIT

# 插件元数据
tags:
  - category
  - use-case

# 需求
requires:
  - claude-code: ">=1.0.0"

# 打包的组件
components:
  - type: commands
    path: commands/
  - type: agents
    path: agents/
  - type: mcp
    path: mcp/
  - type: hooks
    path: hooks/

# 配置
config:
  auto_load: true
  enabled_by_default: true
---
```

### 插件结构

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── task-1.md
│   ├── task-2.md
│   └── workflows/
├── agents/
│   ├── specialist-1.md
│   ├── specialist-2.md
│   └── configs/
├── skills/
│   ├── skill-1.md
│   └── skill-2.md
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
├── settings.json
├── templates/
│   └── issue-template.md
├── scripts/
│   ├── helper-1.sh
│   └── helper-2.py
├── docs/
│   ├── README.md
│   └── USAGE.md
└── tests/
    └── plugin.test.js
```

### 实用示例

#### 示例 1：PR 审查插件

**文件：** `.claude-plugin/plugin.json`

```json
{
  "name": "pr-review",
  "version": "1.0.0",
  "description": "完整的 PR 审查工作流，包含安全、测试和文档检查",
  "author": {
    "name": "Anthropic"
  },
  "license": "MIT"
}
```

**文件：** `commands/review-pr.md`

```markdown
---
name: Review PR
description: 启动全面 PR 审查，包含安全和测试检查
---

# PR Review

此命令启动完整的 Pull Request 审查，包括：

1. 安全分析
2. 测试覆盖率验证
3. 文档更新
4. 代码质量检查
5. 性能影响评估
```

**文件：** `agents/security-reviewer.md`

```yaml
---
name: security-reviewer
description: 安全焦点的代码审查
tools: read, grep, diff
---

# Security Reviewer

专长于查找安全漏洞：
- 认证/授权问题
- 数据泄露
- 注入攻击
- 安全配置
```

**安装：**

```bash
/plugin install pr-review

# 结果：
# ✅ 3 个斜杠命令已安装
# ✅ 3 个子代理已配置
# ✅ 2 个 MCP 服务器已连接
# ✅ 4 个钩子已注册
# ✅ 就绪可用！
```

#### 示例 2：DevOps 插件

**组件：**

```
devops-automation/
├── commands/
│   ├── deploy.md
│   ├── rollback.md
│   ├── status.md
│   └── incident.md
├── agents/
│   ├── deployment-specialist.md
│   ├── incident-commander.md
│   └── alert-analyzer.md
├── mcp/
│   ├── github-config.json
│   ├── kubernetes-config.json
│   └── prometheus-config.json
├── hooks/
│   ├── pre-deploy.js
│   ├── post-deploy.js
│   └── on-error.js
└── scripts/
    ├── deploy.sh
    ├── rollback.sh
    └── health-check.sh
```

#### 示例 3：文档插件

**打包组件：**

```
documentation/
├── commands/
│   ├── generate-api-docs.md
│   ├── generate-readme.md
│   ├── sync-docs.md
│   └── validate-docs.md
├── agents/
│   ├── api-documenter.md
│   ├── code-commentator.md
│   └── example-generator.md
├── mcp/
│   ├── github-docs-config.json
│   └── slack-announce-config.json
└── templates/
    ├── api-endpoint.md
    ├── function-docs.md
    └── adr-template.md
```

### 插件市场

```mermaid
graph TB
    A["插件市场"]
    B["官方 Anthropic"]
    C["社区 市场"]
    D["企业 注册中心"]

    A --> B
    A --> C
    A --> D

    B -->|分类| B1["开发"]
    B -->|分类| B2["DevOps"]
    B -->|分类| B3["文档"]

    C -->|搜索| C1["DevOps 自动化"]
    C -->|搜索| C2["移动开发"]
    C -->|搜索| C3["数据科学"]

    D -->|内部| D1["公司标准"]
    D -->|内部| D2["遗留系统"]
    D -->|内部| D3["合规"]
```

### 插件安装与生命周期

```mermaid
graph LR
    A["发现"] -->|浏览| B["市场"]
    B -->|选择| C["插件页面"]
    C -->|查看| D["组件"]
    D -->|安装| E["/plugin install"]
    E -->|提取| F["配置"]
    F -->|激活| G["使用"]
    G -->|检查| H["更新"]
    H -->|有可用| G
    G -->|完成| I["禁用"]
    I -->|稍后| J["启用"]
    J -->|返回| G
```

### 插件功能对比

| 功能 | 斜杠命令 | 技能 | 子代理 | 插件 |
|------|---------|------|--------|------|
| **安装** | 手动复制 | 手动复制 | 手动配置 | 一条命令 |
| **设置时间** | 5 分钟 | 10 分钟 | 15 分钟 | 2 分钟 |
| **打包** | 单文件 | 单文件 | 单文件 | 多个 |
| **版本管理** | 手动 | 手动 | 手动 | 自动 |
| **团队共享** | 复制文件 | 复制文件 | 复制文件 | 安装 ID |
| **更新** | 手动 | 手动 | 手动 | 自动通知 |
| **依赖** | 无 | 无 | 无 | 可包含 |
| **市场** | 无 | 无 | 无 | 有 |
| **分发** | 仓库 | 仓库 | 仓库 | 市场 |

### 插件用例

| 用例 | 建议 | 原因 |
|------|------|------|
| **团队入职** | ✅ 使用插件 | 即时设置，全部配置 |
| **框架搭建** | ✅ 使用插件 | 打包框架专用命令 |
| **企业标准** | ✅ 使用插件 | 集中分发、版本控制 |
| **快速任务自动化** | ❌ 使用命令 | 过度复杂 |
| **单一领域专业** | ❌ 使用技能 | 太重，改用技能 |
| **专业化分析** | ❌ 使用子代理 | 手动创建或使用技能 |
| **实时数据访问** | ❌ 使用 MCP | 独立，不要捆绑 |

### 何时创建插件

```mermaid
graph TD
    A["我应该创建插件吗?"]
    A -->|需要多个组件| B["多个命令 或子代理 或 MCP?"]
    B -->|是| C["[OK] 创建插件"]
    B -->|否| D["使用单个功能"]
    A -->|团队工作流| E["需要与 团队共享?"]
    E -->|是| C
    E -->|否| F["保留为本地设置"]
    A -->|复杂设置| G["需要自动 配置?"]
    G -->|是| C
    G -->|否| D
```

### 发布插件

**发布步骤：**

1. 创建包含所有组件的插件结构
2. 编写 `.claude-plugin/plugin.json` 清单
3. 创建带文档的 `README.md`
4. 使用 `/plugin install ./my-plugin` 本地测试
5. 提交到插件市场
6. 审核并批准
7. 发布到市场
8. 用户可以一条命令安装

**示例提交：**

~~~~markdown
# PR 审查插件

## 描述
完整的 PR 审查工作流，包含安全、测试和文档检查。

## 包含内容
- 3 个不同类型的斜杠命令
- 3 个专业化子代理
- GitHub 和 CodeQL MCP 集成
- 自动安全扫描钩子

## 安装
```bash
/plugin install pr-review
```

## 功能
✅ 安全分析
✅ 测试覆盖率检查
✅ 文档验证
✅ 代码质量评估
✅ 性能影响分析

## 用法
```bash
/review-pr
/check-security
/check-tests
```

## 要求
- Claude Code 1.0+
- GitHub 访问权限
- CodeQL（可选）
~~~~

### 插件 vs 手动配置

**手动配置（2+ 小时）：**
- 逐一安装斜杠命令
- 单独创建子代理
- 分别配置 MCP
- 手动设置钩子
- 文档化所有内容
- 与团队共享（希望他们正确配置）

**使用插件（2 分钟）：**
```bash
/plugin install pr-review
# ✅ 一切已安装和配置
# ✅ 立即可用
# ✅ 团队可以精确复现设置
```

---

## 比较与集成

### 功能对比矩阵

| 功能 | 调用方式 | 持久性 | 范围 | 用例 |
|------|---------|--------|------|------|
| **斜杠命令** | 手动 (`/cmd`) | 仅会话 | 单个命令 | 快捷方式 |
| **子代理** | 自动委托 | 隔离上下文 | 专业任务 | 任务分发 |
| **记忆** | 自动加载 | 跨会话 | 用户/团队上下文 | 长期学习 |
| **MCP 协议** | 自动查询 | 实时外部 | 实时数据访问 | 动态信息 |
| **技能** | 自动调用 | 基于文件系统 | 可复用的专业知识 | 自动化工作流 |

### 交互时间线

```mermaid
graph LR
    A["会话开始"] -->|加载| B["记忆 (CLAUDE.md)"]
    B -->|发现| C["可用技能"]
    C -->|注册| D["斜杠命令"]
    D -->|连接| E["MCP 服务器"]
    E -->|就绪| F["用户交互"]

    F -->|输入 /cmd| G["斜杠命令"]
    F -->|请求| H["技能自动调用"]
    F -->|查询| I["MCP 数据"]
    F -->|复杂任务| J["委托给子代理"]

    G -->|使用| B
    H -->|使用| B
    I -->|使用| B
    J -->|使用| B
```

### 实用集成示例：客户支持自动化

#### 架构

```mermaid
graph TB
    Customer["客户邮件"] -->|接收| Router["支持路由器"]

    Router -->|分析| Memory["记忆 客户历史"]
    Router -->|查询| MCP1["MCP: 客户数据库 过往工单"]
    Router -->|检查| MCP2["MCP: Slack 团队状态"]

    Router -->|路由复杂| Sub1["子代理: 技术支持 上下文: 技术问题"]
    Router -->|路由简单| Sub2["子代理: 计费 上下文: 支付问题"]
    Router -->|路由紧急| Sub3["子代理: 升级处理 上下文: 优先级处理"]

    Sub1 -->|格式化| Skill1["技能: 响应生成器 品牌语调一致"]
    Sub2 -->|格式化| Skill2["技能: 响应生成器"]
    Sub3 -->|格式化| Skill3["技能: 响应生成器"]

    Skill1 -->|生成| Output["格式化响应"]
    Skill2 -->|生成| Output
    Skill3 -->|生成| Output

    Output -->|发布| MCP3["MCP: Slack 通知团队"]
    Output -->|发送| Reply["客户回复"]
```

#### 请求流程

```markdown
## 客户支持请求流程

### 1. 收到邮件
"上传文件时遇到 500 错误。这阻塞了我的工作流！"

### 2. 记忆查询
- 加载带支持标准的 CLAUDE.md
- 检查客户历史：VIP 客户，本月第 3 次

### 3. MCP 查询
- GitHub MCP：列出开放 Issue（找到相关 Bug 报告）
- 数据库 MCP：检查系统状态（未报告中断）
- Slack MCP：检查工程团队是否知情

### 4. 技能检测与加载
- 请求匹配"技术支持"技能
- 从技能加载支持响应模板

### 5. 子代理委托
- 路由到技术支持子代理
- 提供上下文：客户历史、错误详情、已知问题
- 子代理拥有完整访问权：read、bash、grep 工具

### 6. 子代理处理
技术支持子代理：
- 在代码库中搜索文件上传的 500 错误
- 在 commit 8f4a2c 中找到最近变更
- 创建临时解决方案文档

### 7. 技能执行
响应生成器技能：
- 使用品牌语调指南
- 以共情格式化响应
- 包含临时解决步骤
- 链接到相关文档

### 8. MCP 输出
- 发布更新到 #support Slack 频道
- 标记工程团队
- 在 Jira MCP 中更新工单

### 9. 响应
客户收到：
- 共情确认
- 原因解释
- 临时解决方案
- 永久修复时间线
- 相关 Issue 链接
```

### 完整功能编排

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Memory as Memory CLAUDE.md
    participant MCP as MCP 服务器
    participant Skills as SkillSystem
    participant SubAgent as Subagents

    User->>Claude: 请求:"构建认证系统"
    Claude->>Memory: 加载项目标准
    Memory-->>Claude: 认证标准、团队实践
    Claude->>MCP: 查询 GitHub 获取类似实现
    MCP-->>Claude: 代码示例、最佳实践
    Claude->>Skills: 检测匹配的技能
    Skills-->>Claude: 安全审查技能 + 测试技能
    Claude->>SubAgent: 委托实现
    SubAgent->>SubAgent: 构建功能
    Claude->>Skills: 应用安全审查技能
    Skills-->>Claude: 安全清单结果
    Claude->>SubAgent: 委托测试
    SubAgent-->>Claude: 测试结果
    Claude->>User: 交付完整系统
```

### 何时使用各功能

```mermaid
graph TD
    A["新任务"] --> B["任务类型"]

    B -->|重复工作流| C["斜杠命令"]
    B -->|需要实时数据| D["MCP 协议"]
    B -->|下次还要记住| E["记忆"]
    B -->|专业子任务| F["子代理"]
    B -->|特定领域工作| G["技能"]

    C --> C1["[OK] 团队快捷方式"]
    D --> D1["[OK] 实时 API 访问"]
    E --> E1["[OK] 持久化上下文"]
    F --> F1["[OK] 并行执行"]
    G --> G1["[OK] 自动调用专业知识"]
```

### 选择决策树

```mermaid
graph TD
    Start["需要扩展 Claude?"]

    Start -->|快速重复任务| A["手动 or 自动?"]
    A -->|手动| B["斜杠命令"]
    A -->|自动| C["技能"]

    Start -->|需要外部数据| D["实时?"]
    D -->|是| E["MCP 协议"]
    D -->|否/跨会话| F["记忆"]

    Start -->|复杂项目| G["多个角色?"]
    G -->|是| H["子代理"]
    G -->|否| I["技能 + 记忆"]

    Start -->|长期上下文| J["记忆"]
    Start -->|团队工作流| K["斜杠命令 + 记忆"]
    Start -->|全自动化| L["技能 + 子代理 + MCP"]
```

---

## 汇总表

| 方面 | 斜杠命令 | 子代理 | 记忆 | MCP | 技能 | 插件 |
|------|---------|--------|------|-----|------|------|
| **设置难度** | 简单 | 中等 | 简单 | 中等 | 中等 | 简单 |
| **学习曲线** | 低 | 中等 | 低 | 中等 | 中等 | 低 |
| **团队收益** | 高 | 高 | 中等 | 高 | 高 | 很高 |
| **自动化水平** | 低 | 高 | 中等 | 高 | 高 | 很高 |
| **上下文管理** | 单次会话 | 隔离 | 持久化 | 实时 | 持久化 | 全部功能 |
| **维护负担** | 低 | 中等 | 低 | 中等 | 中等 | 低 |
| **可扩展性** | 良好 | 优秀 | 良好 | 优秀 | 优秀 | 优秀 |
| **可分享性** | 一般 | 一般 | 良好 | 良好 | 良好 | 优秀 |
| **版本管理** | 手动 | 手动 | 手动 | 手动 | 手动 | 自动 |
| **安装** | 手动复制 | 手动配置 | N/A | 手动配置 | 手动复制 | 一条命令 |

---

## 快速入门指南

### 第 1 周：从简单开始
- 为常见任务创建 2-3 个斜杠命令
- 在设置中启用记忆
- 在 CLAUDE.md 中记录团队标准

### 第 2 周：添加实时访问
- 设置 1 个 MCP（GitHub 或数据库）
- 使用 `/mcp` 配置
- 在工作流中查询实时数据

### 第 3 周：分发工作
- 为特定角色创建第一个子代理
- 使用 `/agents` 命令
- 用简单任务测试委托

### 第 4 周：自动化一切
- 为重复自动化创建第一个技能
- 使用技能市场或自行构建
- 组合所有功能实现完整工作流

### 持续进行
- 每月审查和更新记忆
- 随着模式出现添加新技能
- 优化 MCP 查询
- 完善子代理提示词

---

## 钩子

### 概述

钩子（Hooks）是事件驱动的 Shell 命令，响应 Claude Code 事件自动执行。它们支持自动化、验证和自定义工作流，无需人工干预。

### 钩子事件

Claude Code 支持 **25 种钩子事件**，分为四种钩子类型（command、http、prompt、agent）：

| 钩子事件 | 触发时机 | 用例 |
|----------|---------|------|
| **SessionStart** | 会话开始/恢复/清除/压缩时 | 环境设置、初始化 |
| **InstructionsLoaded** | CLAUDE.md 或规则文件加载时 | 验证、转换、增强 |
| **UserPromptSubmit** | 用户提交提示词时 | 输入验证、提示词过滤 |
| **PreToolUse** | 任何工具运行之前 | 验证、审批门控、日志 |
| **PermissionRequest** | 显示权限对话框时 | 自动批准/拒绝流程 |
| **PostToolUse** | 工具成功执行之后 | 自动格式化、通知、清理 |
| **PostToolUseFailure** | 工具执行失败时 | 错误处理、日志 |
| **Notification** | 发送通知时 | 告警、外部集成 |
| **SubagentStart** | 子代理启动时 | 上下文注入、初始化 |
| **SubagentStop** | 子代理完成时 | 结果验证、日志 |
| **Stop** | Claude 完成响应时 | 摘要生成、清理任务 |
| **StopFailure** | API 错误结束回合时 | 错误恢复、日志 |
| **TeammateIdle** | 代理团队成员空闲时 | 工作分发、协调 |
| **TaskCompleted** | 标记任务完成时 | 任务后处理 |
| **TaskCreated** | 通过 TaskCreate 创建任务时 | 任务跟踪、日志 |
| **ConfigChange** | 配置文件变更时 | 验证、传播 |
| **CwdChanged** | 工作目录变更时 | 目录特定设置 |
| **FileChanged** | 监控文件变更时 | 文件监控、重建触发 |
| **PreCompact** | 上下文压缩之前 | 状态保存 |
| **PostCompact** | 压缩完成后 | 压缩后操作 |
| **WorktreeCreate** | 创建 worktree 时 | 环境设置、依赖安装 |
| **WorktreeRemove** | 移除 worktree 时 | 清理、资源释放 |
| **Elicitation** | MCP 服务器请求用户输入时 | 输入验证 |
| **ElicitationResult** | 用户回应 elicitation 时 | 响应处理 |
| **SessionEnd** | 会话终止时 | 清理、最终日志 |

### 常用钩子

钩子在 `~/.claude/settings.json`（用户级别）或 `.claude/settings.json`（项目级别）中配置：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATH"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "eslint $CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

### 钩子环境变量

- `$CLAUDE_FILE_PATH` - 正在被编辑/写入的文件路径
- `$CLAUDE_TOOL_NAME` - 正在使用的工具名称
- `$CLAUDE_SESSION_ID` - 当前会话标识符
- `$CLAUDE_PROJECT_DIR` - 项目目录路径

### 最佳实践

✅ **推荐：**
- 保持钩子快速（< 1 秒）
- 使用钩子进行验证和自动化
- 优雅地处理错误
- 使用绝对路径

❌ **不推荐：**
- 让钩子变成交互式的
- 使用钩子执行长时间运行的任务
- 硬编码凭据

**详见**：[06-hooks/](06-hooks/) 获取详细示例

---

## 检查点与回退

### 概述

检查点（Checkpoints）允许你保存对话状态并回退到之前的点，实现安全实验和多方案探索。

### 关键概念

| 概念 | 描述 |
|------|------|
| **检查点** | 包含消息、文件和上下文的对话状态快照 |
| **回退** | 返回之前的检查点，丢弃后续变更 |
| **分支点** | 从中探索多个方案的检查点 |

### 访问检查点

检查点在每个用户提示词时自动创建。要回退：

```bash
# 按 Esc 两次打开检查点浏览器
Esc + Esc

# 或使用 /rewind 命令
/rewind
```

选择检查点时，你有五个选项：
1. **恢复代码和对话** — 两者都还原到该点
2. **恢复对话** — 回退消息，保留当前代码
3. **恢复代码** — 还原文件，保留对话
4. **从此处总结** — 将对话压缩为摘要
5. **算了** — 取消

### 用例

| 场景 | 工作流 |
|------|------|
| **探索方案** | 保存 → 尝试方案 A → 保存 → 回退 → 尝试方案 B → 比较 |
| **安全重构** | 保存 → 重构 → 测试 → 如果失败：回退 |
| **A/B 测试** | 保存 → 设计 A → 保存 → 回退 → 设计 B → 比较 |
| **错误恢复** | 发现问题 → 回退到最后一个良好状态 |

### 配置

```json
{
  "autoCheckpoint": true
}
```

**详见**：[08-checkpoints/](08-checkpoints/) 获取详细示例

---

## 高级功能

### 规划模式（Planning Mode）

在编码之前创建详细的实施计划。

**激活：**
```bash
/plan Implement user authentication system
```

**优势：**
- 带时间估算的清晰路线图
- 风险评估
- 系统化的任务分解
- 审查和修改机会

### 扩展思考（Extended Thinking）

针对复杂问题的深度推理。

**激活：**
- 在会话中切换 `Alt+T`（macOS 上为 `Option+T`）
- 设置 `MAX_THINKING_TOKENS` 环境变量进行程序化控制

```bash
# 通过环境变量启用扩展思考
export MAX_THINKING_TOKENS=50000
claude -p "我们应该使用微服务还是单体架构？"
```

**优势：**
- 权衡取舍的透彻分析
- 更好的架构决策
- 边界情况考虑
- 系统化评估

### 后台任务

运行长时间操作而不阻塞对话。

**用法：**
```bash
用户：在后台运行测试

Claude：已启动任务 bg-1234

/task list           # 显示所有任务
/task status bg-1234 # 检查进度
/task show bg-1234   # 查看输出
/task cancel bg-1234 # 取消任务
```

### 权限模式

控制 Claude 可以做什么。

| 模式 | 描述 | 用例 |
|------|------|------|
| **default** | 标准权限，敏感操作需确认 | 通用开发 |
| **acceptEdits** | 自动接受文件编辑，无需确认 | 受信任的编辑工作流 |
| **plan** | 仅分析和规划，不修改文件 | 代码审查、架构规划 |
| **auto** | 自动批准安全操作，仅对风险操作提示 | 平衡自主性与安全性 |
| **dontAsk** | 执行所有操作无需确认提示 | 有经验的用户、自动化 |
| **bypassPermissions** | 完全不受限访问，无安全检查 | CI/CD 流水线、受信任脚本 |

**用法：**
```bash
claude --permission-mode plan          # 只读分析
claude --permission-mode acceptEdits   # 自动接受编辑
claude --permission-mode auto          # 自动批准安全操作
claude --permission-mode dontAsk       # 无确认提示
```

### 无头模式（Headless Mode / Print Mode）

使用 `-p`（print）标志在没有交互输入的情况下运行 Claude Code，适用于自动化和 CI/CD。

**用法：**
```bash
# 运行特定任务
claude -p "Run all tests"

# 通过管道输入进行分析
cat error.log | claude -p "explain this error"

# CI/CD 集成（GitHub Actions）
- name: AI Code Review
  run: claude -p "Review PR changes and report issues"

# JSON 输出用于脚本
claude -p --output-format json "list all functions in src/"
```

### 定时任务

使用 `/loop` 命令按计划重复运行任务。

**用法：**
```bash
/loop every 30m "Run tests and report failures"
/loop every 2h "Check for dependency updates"
/loop every 1d "Generate daily summary of code changes"
```

定时任务在后台运行，完成后报告结果。适用于持续监控、定期检查和自动化维护工作流。

### Chrome 集成

Claude Code 可以与 Chrome 浏览器集成以实现 Web 自动化任务。这支持在开发工作流中直接导航网页、填写表单、截图和从网站提取数据等功能。

### 会话管理

管理多个工作会话。

**命令：**
```bash
/resume                # 恢复之前的对话
/rename "Feature"      # 命名当前会话
/fork                  # 分叉到新会话
claude -c              # 继续最近的对话
claude -r "Feature"    # 按名称/ID 恢复会话
```

### 交互功能

**键盘快捷键：**
- `Ctrl + R` - 搜索命令历史
- `Tab` - 自动补全
- `↑ / ↓` - 命令历史
- `Ctrl + L` - 清屏

**多行输入：**
```bash
用户: \
> 长而复杂的提示词
> 跨越多行
> \end
```

### 配置

完整配置示例：

```json
{
  "planning": {
    "autoEnter": true,
    "requireApproval": true
  },
  "extendedThinking": {
    "enabled": true,
    "showThinkingProcess": true
  },
  "backgroundTasks": {
    "enabled": true,
    "maxConcurrentTasks": 5
  },
  "permissions": {
    "mode": "default"
  }
}
```

**详见**：[09-advanced-features/](09-advanced-features/) 获取完整指南

---

## 资源

- [Claude Code 文档](https://code.claude.com/docs/en/overview)
- [Anthropic 文档](https://docs.anthropic.com)
- [MCP GitHub 服务器](https://github.com/modelcontextprotocol/servers)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

---

*最后更新：2026 年 3 月*
*适用于 Claude Haiku 4.5、Sonnet 4.6 和 Opus 4.6*
*现在包含：钩子、检查点、规划模式、扩展思考、后台任务、权限模式（6 种）、无头模式、会话管理、自动记忆、代理团队、定时任务、Chrome 集成、频道、语音听写和内置技能*
