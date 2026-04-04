<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# MCP（Model Context Protocol，模型上下文协议）

MCP 是一个开放标准，允许 Claude Code 连接外部工具、数据源和 API。它将 Claude 从一个代码助手转变为可以访问实时数据、数据库、API 和第三方服务的完整开发平台。

## 概览

**MCP（Model Context Protocol，模型上下文协议）** 是一种开放标准，使 AI 工具能够连接外部数据源和服务。在 Claude Code 中，MCP 服务器作为桥梁，让 Claude 能够：

- **查询实时数据** — 访问 GitHub Issues/PR、数据库记录、实时指标
- **执行操作** — 创建 PR、发送消息、管理资源
- **集成 API** — 连接 Stripe、Slack、Google Docs 等服务
- **扩展能力** — 超出内置工具范围的自定义功能

## MCP 工作原理

```mermaid
graph LR
    A["Claude Code"] -->|"MCP 客户端"| B["MCP 服务器"]
    B --> C["GitHub API"]
    B --> D["PostgreSQL"]
    B --> E["文件系统"]
    B --> F["自定义 API"]
```

### 核心概念

| 概念 | 说明 |
|------|------|
| **MCP Server（MCP 服务器）** | 提供特定能力的程序（如 GitHub 集成） |
| **Tool（工具）** | 服务器暴露的每个可调用函数 |
| **Resource（资源）** | 服务器提供的数据（文件、URL 等） |
| **Transport（传输层）** | 客户端与服务器之间的通信方式 |

## 配置 MCP 服务器

### 方法一：使用 CLI 命令

```bash
# 添加 GitHub MCP 服务器
export GITHUB_TOKEN="your_token"
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# 添加数据库 MCP 服务器
claude mcp add db -- npx -y @modelcontextprotocol/server-postgres \
  "postgresql://user:pass@localhost:5432/mydb"
```

### 方法二：编辑配置文件

**项目级配置** (`.mcp.json`)：
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**用户级配置** (`~/.claude.json`)：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  }
}
```

### 配置字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `command` | string | 启动服务器的命令 |
| `args` | array | 传递给命令的参数 |
| `env` | object | 环境变量 |
| `transport` | string | 可选：`stdio`（默认）或 `sse` / `websocket` |

## 使用 MCP 工具

配置完成后，MCP 工具会自动出现在 Claude 的可用工具列表中：

```markdown
用户: 查看 #42 这个 PR 的状态
Claude: [自动使用 mcp__github__get_pull_request]
PR #42 的状态如下：
- 标题：修复认证 Token 过期问题
- 状态：Open
- 作者：@alice
- 审查者：@bob（已批准）
```

### 工具命名规范

MCP 工具统一使用以下命名格式：`mcp__<server>__<tool_name>`

例如：
- `mcp__github__list_pull_requests`
- `mcp__db__query`
- `mcp__filesystem__read_file`

## 安全注意事项

⚠️ **重要安全提醒**：
- MCP 服务器以你的权限运行——确保只安装可信的服务器
- 不要在配置中硬编码敏感信息——使用环境变量引用
- 定期审查已安装的 MCP 服务器列表

> 💡 **中文开发者提示**：MCP 是 Claude Code 最强大的扩展机制之一。国内开发者可能需要配置代理才能正常访问 npm 包。建议从 GitHub MCP 开始尝试，这是最实用也最容易上手的 MCP 服务器。

---

**最后更新**：2026 年 3 月
