<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# MCP (Model Context Protocol)

本文件夹包含 MCP 服务器配置和与 Claude Code 配合使用的综合文档及示例。

## 概览

MCP (Model Context Protocol) 是 Claude 访问外部工具、API 和实时数据源的标准化方式。与 Memory 不同,MCP 提供对变化数据的实时访问。

核心特性:
- 对外部服务的实时访问
- 实时数据同步
- 可扩展架构
- 安全认证
- 基于工具的交互

## MCP 架构

```mermaid
graph TB
    A["Claude"]
    B["MCP Server"]
    C["External Service"]

    A -->|Request: list_issues| B
    B -->|Query| C
    C -->|Data| B
    B -->|Response| A

    A -->|Request: create_issue| B
    B -->|Action| C
    C -->|Result| B
    B -->|Response| A

```

## MCP 生态系统

```mermaid
graph TB
    A["Claude"] -->|MCP| B["Filesystem MCP Server"]
    A -->|MCP| C["GitHub MCP Server"]
    A -->|MCP| D["Database MCP Server"]
    A -->|MCP| E["Slack MCP Server"]
    A -->|MCP| F["Google Docs MCP Server"]

    B -->|File I/O| G["Local Files"]
    C -->|API| H["GitHub Repos"]
    D -->|Query| I["PostgreSQL/MySQL"]
    E -->|Messages| J["Slack Workspace"]
    F -->|Docs| K["Google Drive"]

```

## MCP 安装方法

Claude Code 支持多种传输协议用于 MCP 服务器连接:

### HTTP 传输(推荐)

```bash
# 基本 HTTP 连接
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 带认证头的 HTTP
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Stdio 传输(本地)

用于本地运行的 MCP 服务器:

```bash
# 本地 Node.js 服务器
claude mcp add --transport stdio myserver -- npx @myorg/mcp-server

# 带环境变量
claude mcp add --transport stdio myserver --env KEY=value -- npx server
```

### SSE 传输(已弃用)

Server-Sent Events 传输已被弃用,推荐使用 `http`,但仍支持:

```bash
claude mcp add --transport sse legacy-server https://example.com/sse
```

### WebSocket 传输

用于持久化双向连接的 WebSocket 传输:

```bash
claude mcp add --transport ws realtime-server wss://example.com/mcp
```

### Windows 特殊说明

在原生 Windows(非 WSL)上,对 npx 命令使用 `cmd /c`:

```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

### OAuth 2.0 认证

Claude Code 支持需要 OAuth 2.0 的 MCP 服务器。当连接到启用了 OAuth 的服务器时,Claude Code 会处理整个认证流程:

```bash
# 连接到启用 OAuth 的 MCP 服务器(交互式流程)
claude mcp add --transport http my-service https://my-service.example.com/mcp

# 为非交互式设置预配置 OAuth 凭据
claude mcp add --transport http my-service https://my-service.example.com/mcp \
  --client-id "your-client-id" \
  --client-secret "your-client-secret" \
  --callback-port 8080
```

| 功能 | 说明 |
|------|------|
| **交互式 OAuth** | 使用 `/mcp` 触发基于浏览器的 OAuth 流程 |
| **预配置 OAuth 客户端** | 为 Notion、Stripe 等常见服务内置 OAuth 客户端(v2.1.30+) |
| **预配置凭据** | `--client-id`、`--client-secret`、`--callback-port` 标志用于自动化设置 |
| **Token 存储** | Token 安全存储在你的系统密钥链中 |
| **升级认证** | 支持特权操作的升级认证 |
| **发现缓存** | OAuth 发现元数据被缓存以加速重连 |
| **元数据覆盖** | `.mcp.json` 中的 `oauth.authServerMetadataUrl` 用于覆盖默认 OAuth 元数据发现 |

#### 覆盖 OAuth 元数据发现

如果你的 MCP 服务器在标准 OAuth 元数据端点(`/.well-known/oauth-authorization-server`)返回错误但暴露了一个可用的 OIDC 端点,你可以告诉 Claude Code 从特定 URL 获取 OAuth 元数据。在服务器配置的 `oauth` 对象中设置 `authServerMetadataUrl`:

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL 必须使用 `https://`。此选项需要 Claude Code v2.1.64 或更高版本。

### Claude.ai MCP 连接器

在你的 Claude.ai 账户中配置的 MCP 服务器在 Claude Code 中自动可用。这意味着你通过 Claude.ai Web 界面设置的任何 MCP 连接都无需额外配置即可访问。

Claude.ai MCP 连接器在 `--print` 模式下也可用(v2.1.83+),支持非交互化和脚本使用。

要在 Claude Code 中禁用 Claude.ai MCP 服务器,将 `ENABLE_CLAUDEAI_MCP_SERVERS` 环境变量设置为 `false`:

```bash
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

> **注意:** 此功能仅适用于使用 Claude.ai 账户登录的用户。

## MCP 设置流程

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Config as Config File
    participant Service as External Service

    User->>Claude: Type /mcp
    Claude->>Claude: List available MCP servers
    Claude->>User: Show options
    User->>Claude: Select GitHub MCP
    Claude->>Config: Update configuration
    Config->>Claude: Activate connection
    Claude->>Service: Test connection
    Service-->>Claude: Authentication successful
    Claude->>User: MCP connected!
```

## MCP 工具搜索

当 MCP 工具描述超过上下文窗口的 10% 时,Claude Code 会自动启用工具搜索以高效选择正确的工具而不会使模型上下文过载。

| 设置 | 值 | 说明 |
|------|-----|------|
| `ENABLE_TOOL_SEARCH` | `auto`(默认) | 当工具描述超过上下文的 10% 时自动启用 |
| `ENABLE_TOOL_SEARCH` | `auto:<N>` | 在自定义阈值 N 个工具时自动启用 |
| `ENABLE_TOOL_SEARCH` | `true` | 无论工具数量始终启用 |
| `ENABLE_TOOL_SEARCH` | `false` | 已禁用;所有工具描述完整发送 |

> **注意:** 工具搜索需要 Sonnet 4 或更高版本,或 Opus 4 或更高版本。Haiku 模型不支持工具搜索。

## 动态工具更新

Claude Code 支持 MCP `list_changed` 通知。当 MCP 服务器动态添加、删除或修改其可用工具时,Claude Code 会接收更新并自动调整其工具列表 -- 无需重新连接或重启。

## MCP 引导

MCP 服务器可以通过交互式对话框向用户请求结构化输入(v2.1.49+)。这允许 MCP 服务器在工作流中途请求额外信息 -- 例如,提示确认、从选项列表中选择或填写必填字段 -- 为 MCP 服务器交互增加交互性。

## 工具描述和指令限制

从 v2.1.84 起,Claude Code 对每个 MCP 服务器的工具描述和指令强制执行 **2 KB 限制**。这可以防止单个服务器因过于冗长的工具定义消耗过多上下文,减少上下文膨胀并保持交互高效。

## 作为斜杠命令的 MCP 提示词

MCP 服务器可以暴露在 Claude Code 中显示为斜杠命令的提示词。提示词可通过以下命名约定访问:

```
/mcp__<server>__<prompt>
```

例如,如果名为 `github` 的服务器暴露了一个名为 `review` 的提示词,你可以通过 `/mcp__github__review` 调用它。

## 服务器去重

当同一个 MCP 服务器在多个作用域(本地、项目、用户)中定义时,本地配置优先。这允许你使用本地自定义覆盖项目级或用户级 MCP 设置而不会产生冲突。

## 通过 @提及引用 MCP 资源

你可以在提示词中使用 `@` 提及语法直接引用 MCP 资源:

```
@server-name:protocol://resource/path
```

例如,引用特定的数据库资源:

```
@database:postgres://mydb/users
```

这允许 Claude 获取并将 MCP 资源内容内联包含作为对话上下文的一部分。

## MCP 作用域

MCP 配置可以存储在不同的作用域中,具有不同的共享级别:

| 作用域 | 位置 | 说明 | 共享对象 | 需要批准 |
|--------|------|------|----------|----------|
| **Local**(默认) | `~/.claude.json`(项目路径下) | 仅当前用户、当前项目私有(旧版本称为 `project`) | 仅你自己 | 否 |
| **Project** | `.mcp.json` | 纳入 git 版本控制 | 团队成员 | 是(首次使用) |
| **User** | `~/.claude.json` | 在所有项目中可用(旧版本称为 `global`) | 仅你自己 | 否 |

### 使用项目作用域

在 `.mcp.json` 中存储项目特定的 MCP 配置:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp"
    }
  }
}
```

团队成员首次使用项目 MCP 时会看到批准提示。

## MCP 配置管理

### 添加 MCP 服务器

```bash
# 添加基于 HTTP 的服务器
claude mcp add --transport http github https://api.github.com/mcp

# 添加本地 stdio 服务器
claude mcp add --transport stdio database -- npx @company/db-server

# 列出所有 MCP 服务器
claude mcp list

# 获取特定服务器的详细信息
claude mcp get github

# 移除 MCP 服务器
claude mcp remove github

# 重置项目特定的批准选择
claude mcp reset-project-choices

# 从 Claude Desktop 导入
claude mcp add-from-claude-desktop
```

## 可用 MCP 服务器表

| MCP 服务器 | 用途 | 常用工具 | 认证 | 实时 |
|------------|------|----------|------|------|
| **Filesystem** | 文件操作 | read, write, delete | OS 权限 | 是 |
| **GitHub** | 仓库管理 | list_prs, create_issue, push | OAuth | 是 |
| **Slack** | 团队通信 | send_message, list_channels | Token | 是 |
| **Database** | SQL 查询 | query, insert, update | 凭据 | 是 |
| **Google Docs** | 文档访问 | read, write, share | OAuth | 是 |
| **Asana** | 项目管理 | create_task, update_status | API Key | 是 |
| **Stripe** | 支付数据 | list_charges, create_invoice | API Key | 是 |
| **Memory** | 持久化记忆 | store, retrieve, delete | 本地 | 否 |

## 实际示例

### 示例 1:GitHub MCP 配置

**文件:** `.mcp.json`(项目根目录)

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

**可用的 GitHub MCP 工具:**

#### Pull Request 管理
- `list_prs` - 列出仓库中的所有 PR
- `get_pr` - 获取 PR 详情(含 diff)
- `create_pr` - 创建新 PR
- `update_pr` - 更新 PR 描述/标题
- `merge_pr` - 将 PR 合并到主分支
- `review_pr` - 添加审查评论

**示例请求:**
```
/mcp__github__get_pr 456

# 返回:
Title: Add dark mode support
Author: @alice
Description: Implements dark theme using CSS variables
Status: OPEN
Reviewers: @bob, @charlie
```

#### Issue 管理
- `list_issues` - 列出所有 issues
- `get_issue` - 获取 issue 详情
- `create_issue` - 创建新 issue
- `close_issue` - 关闭 issue
- `add_comment` - 向 issue 添加评论

#### 仓库信息
- `get_repo_info` - 仓库详情
- `list_files` - 文件树结构
- `get_file_content` - 读取文件内容
- `search_code` - 在代码库中搜索

#### Commit 操作
- `list_commits` - Commit 历史
- `get_commit` - 特定 commit 详情
- `create_commit` - 创建新 commit

**设置:**
```bash
export GITHUB_TOKEN="your_github_token"
# 或使用 CLI 直接添加:
claude mcp add --transport stdio github -- npx @modelcontextprotocol/server-github
```

### 配置中的环境变量扩展

MCP 配置支持带默认回退值的环境变量扩展。`${VAR}` 和 `${VAR:-default}` 语法可用于以下字段:`command`、`args`、`env`、`url` 和 `headers`。

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}",
        "X-Custom-Header": "${CUSTOM_HEADER:-default-value}"
      }
    },
    "local-server": {
      "command": "${MCP_BIN_PATH:-npx}",
      "args": ["${MCP_PACKAGE:-@company/mcp-server}"],
      "env": {
        "DB_URL": "${DATABASE_URL:-postgresql://localhost/dev}"
      }
    }
  }
}
```

变量在运行时展开:
- `${VAR}` - 使用环境变量,未设置时报错
- `${VAR:-default}` - 使用环境变量,未设置时使用默认值

### 示例 2:数据库 MCP 设置

**配置:**

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

**示例用法:**

```markdown
User: Fetch all users with more than 10 orders

Claude: I'll query your database to find that information.

# Using MCP database tool:
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING COUNT(o.id) > 10
ORDER BY order_count DESC;

# Results:
- Alice: 15 orders
- Bob: 12 orders
- Charlie: 11 orders
```

**设置:**
```bash
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
# 或使用 CLI 直接添加:
claude mcp add --transport stdio database -- npx @modelcontextprotocol/server-database
```

### 示例 3:多 MCP 工作流

**场景:每日报告生成**

```markdown
# Daily Report Workflow using Multiple MCPs

## Setup
1. GitHub MCP - fetch PR metrics
2. Database MCP - query sales data
3. Slack MCP - post report
4. Filesystem MCP - save report

## Workflow

### Step 1: Fetch GitHub Data
/mcp__github__list_prs completed:true last:7days

Output:
- Total PRs: 42
- Average merge time: 2.3 hours
- Review turnaround: 1.1 hours

### Step 2: Query Database
SELECT COUNT(*) as sales, SUM(amount) as revenue
FROM orders
WHERE created_at > NOW() - INTERVAL '1 day'

Output:
- Sales: 247
- Revenue: $12,450

### Step 3: Generate Report
Combine data into HTML report

### Step 4: Save to Filesystem
Write report.html to /reports/

### Step 5: Post to Slack
Send summary to #daily-reports channel

Final Output:
Report generated and posted
47 PRs merged this week
$12,450 in daily sales
```

**设置:**
```bash
export GITHUB_TOKEN="your_github_token"
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
export SLACK_TOKEN="your_slack_token"
# 通过 CLI 添加每个 MCP 服务器或在 .mcp.json 中配置它们
```

### 示例 4:文件系统 MCP 操作

**配置:**

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

**可用操作:**

| 操作 | 命令 | 用途 |
|------|------|------|
| 列出文件 | `ls ~/projects` | 显示目录内容 |
| 读取文件 | `cat src/main.ts` | 读取文件内容 |
| 写入文件 | `create docs/api.md` | 创建新文件 |
| 编辑文件 | `edit src/app.ts` | 修改文件 |
| 搜索 | `grep "async function"` | 在文件中搜索 |
| 删除 | `rm old-file.js` | 删除文件 |

**设置:**
```bash
# 使用 CLI 直接添加:
claude mcp add --transport stdio filesystem -- npx @modelcontextprotocol/server-filesystem /home/user/projects
```

## MCP vs Memory:决策矩阵

```mermaid
graph TD
    A["Need external data"]
    A -->|No| B["Use Memory"]
    A -->|Yes| C["Does it change frequently"]
    C -->|No/Rarely| B
    C -->|Yes/Often| D["Use MCP"]

    B -->|Stores| E["Preferences Context History"]
    D -->|Accesses| F["Live APIs Databases Services"]

```

## 请求/响应模式

```mermaid
sequenceDiagram
    participant App as Claude
    participant MCP as MCP Server
    participant DB as Database

    App->>MCP: Request: "SELECT * FROM users WHERE id=1"
    MCP->>DB: Execute query
    DB-->>MCP: Result set
    MCP-->>App: Return parsed data
    App->>App: Process result
    App->>App: Continue task

    Note over MCP,DB: Real-time access No caching
```

## 环境变量

在环境变量中存储敏感凭据:

```bash
# ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
export SLACK_TOKEN="xoxb-xxxxxxxxxxxxx"
```

然后在 MCP 配置中引用它们:

```json
{
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

## Claude 作为 MCP 服务器 (`claude mcp serve`)

Claude Code 本身可以作为其他应用程序的 MCP 服务器。这使得外部工具、编辑器和自动化系统能够通过标准 MCP 协议利用 Claude 的能力。

```bash
# 将 Claude Code 作为 stdio 上的 MCP 服务器启动
claude mcp serve
```

然后其他应用程序可以像连接任何基于 stdio 的 MCP 服务器一样连接到此服务器。例如,在另一个 Claude Code 实例中将 Claude Code 添加为 MCP 服务器:

```bash
claude mcp add --transport stdio claude-agent -- claude mcp serve
```

这对于构建多代理工作流很有用,其中一个 Claude 实例编排另一个实例。

## 托管 MCP 配置(企业版)

对于企业部署,IT 管理员可以通过 `managed-mcp.json` 配置文件强制执行 MCP 服务器策略。该文件提供对整个组织范围内允许或阻止哪些 MCP 服务器的独占控制。

**位置:**
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux: `~/.config/ClaudeCode/managed-mcp.json`
- Windows: `%APPDATA%\ClaudeCode\managed-mcp.json`

**功能:**
- `allowedMcpServers` -- 允许的服务器白名单
- `deniedMcpServers` -- 禁止的服务器黑名单
- 支持按服务器名称、命令和 URL 模式匹配
- 组织范围的 MCP 策略在用户配置之前强制执行
- 防止未经授权的服务器连接

**示例配置:**

```json
{
  "allowedMcpServers": [
    {
      "serverName": "github",
      "serverUrl": "https://api.github.com/mcp"
    },
    {
      "serverName": "company-internal",
      "serverCommand": "company-mcp-server"
    }
  ],
  "deniedMcpServers": [
    {
      "serverName": "untrusted-*"
    },
    {
      "serverUrl": "http://*"
    }
  ]
}
```

> **注意:** 当 `allowedMcpServers` 和 `deniedMcpServers` 同时匹配一个服务器时,拒绝规则优先。

## 插件提供的 MCP 服务器

插件可以捆绑自己的 MCP 服务器,使其在插件安装时自动可用。插件提供的 MCP 服务器可以通过两种方式定义:
1. **独立的 `.mcp.json`** -- 在插件根目录放置 `.mcp.json` 文件
2. **内联于 `plugin.json`** -- 在插件清单中直接定义 MCP 服务器

使用 `${CLAUDE_PLUGIN_ROOT}` 变量引用相对于插件安装目录的路径:

```json
{
  "mcpServers": {
    "plugin-tools": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/dist/mcp-server.js"],
      "env": {
        "CONFIG_PATH": "${CLAUDE_PLUGIN_ROOT}/config.json"
      }
    }
  }
}
```

## 子代理作用域的 MCP

可以使用 `mcpServers:` 键在 agent frontmatter 中内联定义 MCP 服务器,将其作用于特定子代理而非整个项目。当某个代理需要访问工作流中其他代理不需要的特定 MCP 服务器时,这非常有用。

```yaml
---
mcpServers:
  my-tool:
    type: http
    url: https://my-tool.example.com/mcp
---

You are an agent with access to my-tool for specialized operations.
```

子代理作用域的 MCP 服务器仅在该代理的执行上下文中可用,不会与父代理或兄弟代理共享。

## MCP 输出限制

Claude Code 对 MCP 工具输出强制执行限制以防止上下文溢出:

| 限制 | 阈值 | 行为 |
|------|------|------|
| **警告** | 10,000 tokens | 显示输出过大的警告 |
| **默认最大值** | 25,000 tokens | 输出超出此限制时被截断 |
| **磁盘持久化** | 50,000 字符 | 超过 50K 字符的工具结果被持久化到磁盘 |

最大输出限制可通过 `MAX_MCP_OUTPUT_TOKENS` 环境变量配置:

```bash
# 将最大输出增加到 50,000 tokens
export MAX_MCP_OUTPUT_TOKENS=50000
```

## 使用代码执行解决上下文膨胀

随着 MCP 采用规模的扩大,连接到具有数百或数千个工具的数十个服务器带来了重大挑战:**上下文膨胀**。这可以说是 MCP 规模化的最大问题,Anthropic 工程团队提出了一个优雅的解决方案 -- 使用代码执行代替直接工具调用。

> **来源:** [Code Execution with MCP: Building More Efficient Agents](https://www.anthropic.com/engineering/code-execution-with-mcp) -- Anthropic Engineering Blog

### 问题:Token 浪费的两个来源

**1. 工具定义使上下文窗口过载**

大多数 MCP 客户端预先加载所有工具定义。当连接到数千个工具时,模型必须在甚至读取用户请求之前处理数十万个 token。

**2. 中间结果消耗额外的 token**

每个中间工具结果都会经过模型的上下文。考虑将会议记录从 Google Drive 传输到 Salesforce -- 完整记录会流经上下文**两次**:一次是读取时,另一次是写入目标时。一个 2 小时的会议记录可能意味着 50,000+ 额外的 token。

```mermaid
graph LR
    A["Model"] -->|"Tool Call: getDocument"| B["MCP Server"]
    B -->|"Full transcript (50K tokens)"| A
    A -->|"Tool Call: updateRecord (re-sends full transcript)"| B
    B -->|"Confirmation"| A

```

### 解决方案:作为代码 API 的 MCP 工具

不是通过上下文窗口传递工具定义和结果,而是代理**编写代码**来调用 MCP 工具作为 API。代码在沙箱执行环境中运行,只有最终结果返回给模型。

```mermaid
graph LR
    A["Model"] -->|"Writes code"| B["Code Execution Environment"]
    B -->|"Calls tools directly"| C["MCP Servers"]
    C -->|"Data stays in execution env"| B
    B -->|"Only final result (minimal tokens)"| A

```

#### 工作原理

MCP 工具作为类型化函数的文件树呈现:

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
└── ...
```

每个工具文件包含类型化包装器:

```typescript
// ./servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

interface GetDocumentInput {
  documentId: string;
}

interface GetDocumentResponse {
  content: string;
}

export async function getDocument(
  input: GetDocumentInput
): Promise<GetDocumentResponse> {
  return callMCPTool<GetDocumentResponse>(
    'google_drive__get_document', input
  );
}
```

然后代理编写代码来编排这些工具:

```typescript
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

// 数据直接在工具之间流动 -- 从不经过模型
const transcript = (
  await gdrive.getDocument({ documentId: 'abc123' })
).content;

await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});
```

**结果:Token 使用量从约 150,000 降至约 2,000 -- 减少 98.7%。**

### 主要优势

| 优势 | 说明 |
|------|------|
| **渐进式披露** | 代理浏览文件系统只加载它需要的工具定义,而不是预先加载所有工具 |
| **上下文高效的结果** | 数据在返回模型之前在执行环境中进行过滤/转换 |
| **强大的控制流** | 循环、条件语句和错误处理在代码中运行而无需往返模型 |
| **隐私保护** | 中间数据(PII、敏感记录)保留在执行环境中;从不进入模型上下文 |
| **状态持久化** | 代理可以将中间结果保存到文件并构建可复用的技能函数 |

#### 示例:过滤大型数据集

```typescript
// 不使用代码执行 -- 所有 10,000 行流经上下文
// TOOL CALL: gdrive.getSheet(sheetId: 'abc123')
//   -> returns 10,000 rows in context

// 使用代码执行 -- 在执行环境中过滤
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(
  row => row["Status"] === 'pending'
);
console.log(`Found ${pendingOrders.length} pending orders`);
console.log(pendingOrders.slice(0, 5)); // 只有 5 行到达模型
```

#### 示例:无需往返的循环

```typescript
// 轮询部署通知 -- 完全在代码中运行
let found = false;
while (!found) {
  const messages = await slack.getChannelHistory({
    channel: 'C123456'
  });
  found = messages.some(
    m => m.text.includes('deployment complete')
  );
  if (!found) await new Promise(r => setTimeout(r, 5000));
}
console.log('Deployment notification received');
```

### 需要权衡的取舍

代码执行引入了自己的复杂性。运行代理生成的代码需要:

- 具有适当资源限制的**安全沙箱执行环境**
- 已执行代码的**监控和日志记录**
- 与直接工具调用相比额外的**基础设施开销**

好处 -- 降低 token 成本、降低延迟、改进工具组合 -- 应与这些实现成本相权衡。对于只有几个 MCP 服务器的代理,直接工具调用可能更简单。对于大规模代理(数十个服务器、数百个工具),代码执行是一个显著的改进。

### MCPorter:MCP 工具组合的运行时

[MCPorter](https://github.com/steipete/mcporter) 是一个 TypeScript 运行时和 CLI 工具包,使调用 MCP 服务器变得实用且无需样板代码 -- 并通过选择性工具暴露和类型化包装器帮助减少上下文膨胀。

**解决什么问题:** 不是预先加载来自所有 MCP 服务器的所有工具定义,MCPorter 让你按需发现、检查和调用特定工具 -- 保持你的上下文精简。

**主要功能:**

| 功能 | 说明 |
|------|------|
| **零配置发现** | 自动从 Cursor、Claude、Codex 或本地配置发现 MCP 服务器 |
| **类型化工具客户端** | `mcporter emit-ts` 生成 `.d.ts` 接口和即用型包装器 |
| **可组合 API** | `createServerProxy()` 将工具暴露为带有 `.text()`, `.json()`, `.markdown()` 辅助方法的驼峰命名方法 |
| **CLI 生成** | `mcporter generate-cli` 将任何 MCP 服务器转换为带有 `--include-tools` / `--exclude-tools` 过滤的独立 CLI |
| **参数隐藏** | 可选参数默认隐藏,减少模式冗长性 |

**安装:**

```bash
npx mcporter list          # 无需安装 -- 立即发现服务器
pnpm add mcporter          # 添加到项目
brew install steipete/tap/mcporter  # macOS via Homebrew
```

**示例 -- 在 TypeScript 中组合工具:**

```typescript
import { createRuntime, createServerProxy } from "mcporter";

const runtime = await createRuntime();
const gdrive = createServerProxy(runtime, "google-drive");
const salesforce = createServerProxy(runtime, "salesforce");

// 数据在工具之间流动而不经过模型上下文
const doc = await gdrive.getDocument({ documentId: "abc123" });
await salesforce.updateRecord({
  objectType: "SalesMeeting",
  recordId: "00Q5f000001abcXYZ",
  data: { Notes: doc.text() }
});
```

**示例 -- CLI 工具调用:**

```bash
# 直接调用特定工具
npx mcporter call linear.create_comment issueId:ENG-123 body:'Looks good!'

# 列出可用的服务器和工具
npx mcporter list
```

MCPorter 通过提供将 MCP 工具作为类型化 API 调用的运行时基础设施来补充上述代码执行方法 -- 使中间数据远离模型上下文变得简单明了。

## 最佳实践

### 安全注意事项

#### 应该做的 ✅
- 所有凭据使用环境变量
- 定期轮换 token 和 API 密钥(建议每月)
- 尽可能使用只读 token
- 将 MCP 服务器访问范围限制为最低要求
- 监控 MCP 服务器使用情况和访问日志
- 对外部服务尽可能使用 OAuth
- 对 MCP 请求实施速率限制
- 在生产使用前测试 MCP 连接
- 记录所有活动的 MCP 连接
- 保持 MCP 服务器包更新

#### 不应该做的 ❌
- 不要在配置文件中硬编码凭据
- 不要将 token 或秘密提交到 git
- 不要在团队聊天或邮件中分享 token
- 不要对团队项目使用个人 token
- 不要授予不必要的权限
- 不要忽略认证错误
- 不要公开暴露 MCP 端点
- 不要以 root/admin 权限运行 MCP 服务器
- 不要在日志中缓存敏感数据
- 不要禁用认证机制

### 配置最佳实践

1. **版本控制**:将 `.mcp.json` 保存在 git 中,但对机密信息使用环境变量
2. **最小权限原则**:为每个 MCP 服务器授予所需的最小权限
3. **隔离**:尽可能在不同进程中运行不同的 MCP 服务器
4. **监控**:记录所有 MCP 请求和错误以供审计跟踪
5. **测试**:在部署到生产环境之前测试所有 MCP 配置

### 性能技巧

- 在应用程序级别缓存频繁访问的数据
- 使用具体的 MCP 查询以减少数据传输
- 监控 MCP 操作的响应时间
- 考虑对外部 API 实施速率限制
- 执行多个操作时使用批处理

## 安装说明

### 先决条件
- Node.js 和 npm 已安装
- Claude Code CLI 已安装
- 外部服务的 API token/凭据

### 分步设置

1. **添加你的第一个 MCP 服务器** 使用 CLI(示例:GitHub):
```bash
claude mcp add --transport stdio github -- npx @modelcontextprotocol/server-github
```

   或在项目根目录创建 `.mcp.json` 文件:
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

2. **设置环境变量:**
```bash
export GITHUB_TOKEN="your_github_personal_access_token"
```

3. **测试连接:**
```bash
claude /mcp
```

4. **使用 MCP 工具:**
```bash
/mcp__github__list_prs
/mcp__github__create_issue "Title" "Description"
```

### 特定服务的安装

**GitHub MCP:**
```bash
npm install -g @modelcontextprotocol/server-github
```

**Database MCP:**
```bash
npm install -g @modelcontextprotocol/server-database
```

**Filesystem MCP:**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Slack MCP:**
```bash
npm install -g @modelcontextprotocol/server-slack
```

## 故障排除

### MCP 服务器未找到
```bash
# 验证 MCP 服务器已安装
npm list -g @modelcontextprotocol/server-github

# 如果缺失则安装
npm install -g @modelcontextprotocol/server-github
```

### 认证失败
```bash
# 验证环境变量已设置
echo $GITHUB_TOKEN

# 如需重新导出
export GITHUB_TOKEN="your_token"

# 验证 token 具有正确权限
# 在以下位置检查 GitHub token scopes: https://github.com/settings/tokens
```

### 连接超时
- 检查网络连通性:`ping api.github.com`
- 验证 API 端点可访问
- 检查 API 速率限制
- 尝试增加配置中的超时时间
- 检查防火墙或代理问题

### MCP 服务器崩溃
- 检查 MCP 服务器日志:`~/.claude/logs/`
- 验证所有环境变量已设置
- 确保正确的文件权限
- 尝试重新安装 MCP 服务器包
- 检查同一端口上是否有冲突的进程

## 相关概念

### Memory vs MCP
- **Memory**:存储持久不变的数据(偏好设置、上下文、历史)
- **MCP**:访问实时变化的数据(API、数据库、实时服务)

### 何时使用每种
- **使用 Memory** 用于:用户偏好、对话历史、学习到的上下文
- **使用 MCP** 用于:当前 GitHub issues、实时数据库查询、实时数据

### 与其他 Claude 功能的集成
- 结合 Memory 和 MCP 以获得丰富的上下文
- 在提示词中使用 MCP 工具以获得更好的推理
- 利用多个 MCP 进行复杂工作流

## 其他资源

- [Official MCP Documentation](https://code.claude.com/docs/en/mcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/specification)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol/servers)
- [Available MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCPorter](https://github.com/steipete/mcporter) -- TypeScript runtime & CLI for calling MCP servers without boilerplate
- [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) -- Anthropic's engineering blog on solving context bloat
- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Claude API Documentation](https://docs.anthropic.com)