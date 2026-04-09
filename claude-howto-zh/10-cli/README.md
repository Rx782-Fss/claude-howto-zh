<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# CLI 参考手册

## 概览

Claude Code CLI（命令行界面）是与 Claude Code 交互的主要方式。它提供了运行查询、管理会话、配置模型以及将 Claude 集成到开发工作流中的强大选项。

## 架构

```mermaid
graph TD
    A["用户终端"] -->|"claude [选项] [查询]"| B["Claude Code CLI"]
    B -->|交互模式| C["REPL 模式"]
    B -->|"--print"| D["打印模式 (SDK)"]
    B -->|"--resume"| E ["会话恢复"]
    C -->|对话| F["Claude API"]
    D -->|单次查询| F
    E -->|加载上下文| F
    F -->|响应| G["输出"]
    G -->|文本/json/流式JSON| H["终端/管道"]
```

## CLI 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `claude` | 启动交互式 REPL | `claude` |
| `claude "query"` | 带初始提示启动 REPL | `claude "解释这个项目"` |
| `claude -p "query"` | 打印模式——查询后退出 | `claude -p "解释这个函数"` |
| `cat file \| claude -p "query"` | 处理管道输入的内容 | `cat logs.txt \| claude -p "解释"` |
| `claude -c` | 继续最近的对话 | `claude -c` |
| `claude -c -p "query"` | 以打印模式继续 | `claude -c -p "检查类型错误"` |
| `claude -r "<session>" "query"` | 按 ID 或名称恢复会话 | `claude -r "auth-refactor" "完成这个 PR"` |
| `claude update` | 更新到最新版本 | `claude update` |
| `claude mcp` | 配置 MCP 服务器 | 参见 [MCP 文档](../05-mcp/) |
| `claude mcp serve` | 将 Claude Code 作为 MCP 服务器运行 | `claude mcp serve` |
| `claude agents` | 列出所有已配置的子代理 | `claude agents` |
| `claude auto-mode defaults` | 以 JSON 格式输出自动模式的默认规则 | `claude auto-mode defaults` |
| `claude remote-control` | 启动远程控制服务器 | `claude remote-control` |
| `claude plugin` | 管理插件（安装、启用、禁用） | `claude plugin install my-plugin` |
| `claude auth login` | 登录（支持 `--email`、`--sso`） | `claude auth login --email user@example.com` |
| `claude auth logout` | 登出当前账户 | `claude auth logout` |
| `claude auth status` | 检查认证状态（已登录返回 0，未登录返回 1） | `claude auth status` |

## 核心标志

| 标志 | 说明 | 示例 |
|------|------|------|
| `-p, --print` | 打印响应而不进入交互模式 | `claude -p "查询"` |
| `-c, --continue` | 加载最近的对话 | `claude --continue` |
| `-r, --resume` | 按 ID 或名称恢复特定会话 | `claude --resume auth-refactor` |
| `-v, --version` | 输出版本号 | `claude -v` |
| `-w, --worktree` | 在隔离的 git worktree 中启动 | `claude -w` |
| `-n, --name` | 会话显示名称 | `claude -n "auth-refactor"` |
| `--from-pr <编号>` | 恢复关联到 GitHub PR 的会话 | `claude --from-pr 42` |
| `--remote "task"` | 在 claude.ai 上创建 Web 会话 | `claude --remote "实现 API"` |
| `--remote-control, --rc` | 带远程控制的交互式会话 | `claude --rc` |
| `--teleport` | 本地恢复 Web 会话 | `claude --teleport` |
| `--teammate-mode` | Agent 团队显示模式 | `claude --teammate-mode tmux` |
| `--bare` | 最小化模式（跳过 hooks、skills、plugins、MCP、自动记忆、CLAUDE.md） | `claude --bare` |
| `--enable-auto-mode` | 解锁自动权限模式 | `claude --enable-auto-mode` |
| `--channels` | 订阅 MCP 频道插件 | `claude --channels discord,telegram` |
| `--chrome` / `--no-chrome` | 启用/禁用 Chrome 浏览器集成 | `claude --chrome` |
| `--effort` | 设置思考努力级别 | `claude --effort high` |
| `--init` / `--init-only` | 运行初始化 hooks | `claude --init` |
| `--maintenance` | 运行维护 hooks 后退出 | `claude --maintenance` |
| `--disable-slash-commands` | 禁用所有 skills 和斜杠命令 | `claude --disable-slash-commands` |
| `--no-session-persistence` | 禁用会话保存（打印模式） | `claude -p --no-session-persistence "查询"` |

### 交互模式 vs 打印模式

```mermaid
graph LR
    A["claude"] -->|默认| B["交互式 REPL"]
    A -->|"-p 标志"| C["打印模式"]
    B -->|特性| D["多轮对话 Tab 补全 历史记录 斜杠命令"]
    C -->|特性| E["单次查询 可脚本化 支持管道 JSON 输出"]
```

**交互模式**（默认）：
```bash
# 启动交互会话
claude

# 带初始提示启动
claude "解释认证流程"
```

**打印模式**（非交互式）：
```bash
# 单次查询，然后退出
claude -p "这个函数做什么?"

# 处理文件内容
cat error.log | claude -p "解释这个错误"

# 与其他工具链式组合
claude -p "列出所有待办事项" | grep "紧急"
```

## 模型与配置

| 标志 | 说明 | 示例 |
|------|------|------|
| `--model` | 设置模型（sonnet、opus、haiku 或完整名称） | `claude --model opus` |
| `--fallback-model` | 过载时自动回退模型 | `claude -p --fallback-model sonnet "查询"` |
| `--agent` | 指定会话使用的 agent | `claude --agent my-custom-agent` |
| `--agents` | 通过 JSON 定义自定义子代理 | 参见 [Agent 配置](#agent-配置) |
| `--effort` | 设置努力级别（low、medium、high、max） | `claude --effort high` |

### 模型选择示例

```bash
# 使用 Opus 4.6 处理复杂任务
claude --model opus "设计缓存策略"

# 使用 Haiku 4.5 快速处理简单任务
claude --model haiku -p "格式化此 JSON"

# 完整模型名
claude --model claude-sonnet-4-6-20250929 "审查这段代码"

# 配合回退模型提高可靠性
claude -p --model opus --fallback-model sonnet "分析架构"

# 使用 opusplan（Opus 规划，Sonnet 执行）
claude --model opusplan "设计并实现缓存层"
```

## 系统提示词自定义

| 标志 | 说明 | 示例 |
|------|------|------|
| `--system-prompt` | 替换整个默认系统提示词 | `claude --system-prompt "你是一位 Python 专家"` |
| `--system-prompt-file` | 从文件加载提示词（仅打印模式） | `claude -p --system-prompt-file ./prompt.txt "查询"` |
| `--append-system-prompt` | 追加到默认系统提示词末尾 | `claude --append-system-prompt "始终使用 TypeScript"` |

### 系统提示词示例

```bash
# 完整自定义角色
claude --system-prompt "你是一位高级安全工程师。专注于漏洞分析。"

# 追加特定指令
claude --append-system-prompt "代码示例必须包含单元测试"

# 从文件加载复杂提示词
claude -p --system-prompt-file ./prompts/code-reviewer.txt "审查 main.py"
```

### 系统提示词标志对比

| 标志 | 行为 | 交互模式 | 打印模式 |
|------|------|---------|---------|
| `--system-prompt` | 替换整个默认系统提示词 | ✅ | ✅ |
| `--system-prompt-file` | 用文件内容替换 | ❌ | ✅ |
| `--append-system-prompt` | 追加到默认系统提示词 | ✅ | ✅ |

> **注意**：`--system-prompt-file` 仅在打印模式下可用。交互模式请使用 `--system-prompt` 或 `--append-system-prompt`。

## 工具与权限管理

| 标志 | 说明 | 示例 |
|------|------|------|
| `--tools` | 限制可用的内置工具 | `claude -p --tools "Bash,Edit,Read" "查询"` |
| `--allowedTools` | 无需确认即可执行的工具 | `"Bash(git log:*)" "Read"` |
| `--disallowedTools` | 从上下文中移除的工具 | `"Bash(rm:*)" "Edit"` |
| `--dangerously-skip-permissions` | 跳过所有权限确认提示 | `claude --dangerously-skip-permissions` |
| `--permission-mode` | 以指定权限模式启动 | `claude --permission-mode auto` |
| `--permission-prompt-tool` | 用于权限处理的 MCP 工具 | `claude -p --permission-prompt-tool mcp_auth "查询"` |
| `--enable-auto-mode` | 解锁自动权限模式 | `claude --enable-auto-mode` |

### 权限示例

```bash
# 只读模式进行代码审查
claude --permission-mode plan "审查此代码库"

# 仅允许安全工具
claude --tools "Read,Grep,Glob" -p "找出所有 TODO 注释"

# 允许特定 git 命令无需确认
claude --allowedTools "Bash(git status:*)" "Bash(git log:*)"

# 阻止危险操作
claude --disallowedTools "Bash(rm -rf:*)" "Bash(git push --force:*)"
```

## 输出与格式

| 标志 | 说明 | 可选值 | 示例 |
|------|------|--------|------|
| `--output-format` | 指定输出格式（仅打印模式） | `text`、`json`、`stream-json` | `claude -p --output-format json "查询"` |
| `--input-format` | 指定输入格式（仅打印模式） | `text`、`stream-json` | `claude -p --input-format stream-json` |
| `--verbose` | 启用详细日志 | | `claude --verbose` |
| `--include-partial-messages` | 包含流式事件 | 需配合 `stream-json` | `claude -p --output-format stream-json --include-partial-messages "查询"` |
| `--json-schema` | 获取符合 schema 的验证 JSON | | `claude -p --json-schema '{"type":"object"}' "查询"` |
| `--max-budget-usd` | 打印模式最大消费金额 | | `claude -p --max-budget-usd 5.00 "查询"` |

### 输出格式示例

```bash
# 纯文本（默认）
claude -p "解释这段代码"

# JSON 格式用于程序化处理
claude -p --output-format json "列出 main.py 中所有函数"

# 流式 JSON 用于实时处理
claude -p --output-format stream-json "生成一份长报告"

# 带 schema 验证的结构化输出
claude -p --json-schema '{"type":"object","properties":{"bugs":{"type":"array"}}}' \
  "找出此代码中的 bug 并以 JSON 返回"
```

## 工作区与目录

| 标志 | 说明 | 示例 |
|------|------|------|
| `--add-dir` | 添加额外的工作目录 | `claude --add-dir ../apps ../lib` |
| `--setting-sources` | 逗号分隔的设置来源 | `claude --setting-sources user,project` |
| `--settings` | 从文件或 JSON 加载设置 | `claude --settings ./settings.json` |
| `--plugin-dir` | 从目录加载插件（可重复使用） | `claude --plugin-dir ./my-plugin` |

### 多目录示例

```bash
# 跨多个项目目录工作
claude --add-dir ../frontend ../backend ../shared "找出所有 API 端点"

# 加载自定义设置
claude --settings '{"model":"opus","verbose":true}' "复杂任务"
```

## MCP 配置

| 标志 | 说明 | 示例 |
|------|------|------|
| `--mcp-config` | 从 JSON 加载 MCP 服务器配置 | `claude --mcp-config ./mcp.json` |
| `--strict-mcp-config` | 仅使用指定的 MCP 配置 | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--channels` | 订阅 MCP 频道插件 | `claude --channels discord,telegram` |

### MCP 示例

```bash
# 加载 GitHub MCP 服务器
claude --mcp-config ./github-mcp.json "列出开放的 PR"

# 严格模式——仅使用指定的服务器
claude --strict-mcp-config --mcp-config ./production-mcp.json "部署到预发布环境"
```

## 会话管理

| 标志 | 说明 | 示例 |
|------|------|------|
| `--session-id` | 使用指定的会话 ID（UUID） | `claude --session-id "550e8400-..."` |
| `--fork-session` | 恢复时创建新会话 | `claude --resume abc123 --fork-session` |

### 会话示例

```bash
# 继续最近的对话
claude -c

# 恢复命名会话
claude -r "feature-auth" "继续实现登录功能"

# 分叉会话用于实验
claude --resume feature-auth --fork-session "尝试替代方案"

# 使用指定会话 ID
claude --session-id "550e8400-e29b-41d4-a716-446655440000" "继续"
```

### 会话分叉

从现有会话创建分支用于实验：

```bash
# 分叉会话尝试不同方案
claude --resume abc123 --fork-session "尝试替代实现"

# 分叉并附带自定义消息
claude -r "feature-auth" --fork-session "测试不同的架构"
```

**适用场景：**
- 尝试替代实现而不影响原始会话
- 并行实验不同方案
- 从成功的工作中创建变体分支
- 测试破坏性变更而不影响主会话

原始会话保持不变，分叉出的会话成为独立的新会话。

## 高级特性

| 标志 | 说明 | 示例 |
|------|------|------|
| `--chrome` | 启用 Chrome 浏览器集成 | `claude --chrome` |
| `--no-chrome` | 禁用 Chrome 浏览器集成 | `claude --no-chrome` |
| `--ide` | 自动连接可用 IDE | `claude --ide` |
| `--max-turns` | 限制 Agent 轮次（非交互模式） | `claude -p --max-turns 3 "查询"` |
| `--debug` | 启用带过滤的调试模式 | `claude --debug "api,mcp"` |
| `--enable-lsp-logging` | 启用详细 LSP 日志 | `claude --enable-lsp-logging` |
| `--betas` | API 请求的 Beta 功能头 | `claude --betas interleaved-thinking` |
| `--plugin-dir` | 从目录加载插件（可重复） | `claude --plugin-dir ./my-plugin` |
| `--enable-auto-mode` | 解锁自动权限模式 | `claude --enable-auto-mode` |
| `--effort` | 设置思考努力级别 | `claude --effort high` |
| `--bare` | 最小化模式（跳过 hooks、skills、plugins、MCP、自动记忆、CLAUDE.md） | `claude --bare` |
| `--channels` | 订阅 MCP 频道插件 | `claude --channels discord` |
| `--tmux` | 为 worktree 创建 tmux 会话 | `claude --tmux` |
| `--fork-session` | 恢复时创建新会话 ID | `claude --resume abc --fork-session` |
| `--max-budget-usd` | 最大消费金额（打印模式） | `claude -p --max-budget-usd 5.00 "查询"` |
| `--json-schema` | 验证 JSON 输出 | `claude -p --json-schema '{"type":"object"}' "q"` |

### 高级示例

```bash
# 限制自主行动轮次
claude -p --max-turns 5 "重构此模块"

# 调试 API 调用
claude --debug "api" "测试查询"

# 启用 IDE 集成
claude --ide "帮我处理此文件"
```

## Agent 配置

`--agents` 标志接受一个 JSON 对象，用于定义会话的自定义子代理。

### Agent JSON 格式

```json
{
  "agent-name": {
    "description": "必填: 何时调用此 agent",
    "prompt": "必填: agent 的系统提示词",
    "tools": ["可选", "工具", "数组"],
    "model": "可选: sonnet|opus|haiku"
  }
}
```

**必填字段：**
- `description`——何时使用此 agent 的自然语言描述
- `prompt`——定义 agent 角色和行为的系统提示词

**可选字段：**
- `tools`——可用工具数组（省略则继承全部）
  - 格式：`["Read", "Grep", "Glob", "Bash"]`
- `model`——使用的模型：`sonnet`、`opus` 或 `haiku`

### 完整 Agent 示例

```json
{
  "code-reviewer": {
    "description": "专家级代码审查员。代码变更后主动调用。",
    "prompt": "你是一位高级代码审查员。关注代码质量、安全和最佳实践。",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "错误和测试失败的调试专家。",
    "prompt": "你是一位调试专家。分析错误，定位根因并提供修复方案。",
    "tools": ["Read", "Edit", "Bash", "Grep"],
    "model": "opus"
  },
  "documenter": {
    "description": "生成指南文档的专家。",
    "prompt": "你是一位技术写作者。创建清晰全面的文档。",
    "tools": ["Read", "Write"],
    "model": "haiku"
  }
}
```

### Agent 命令示例

```bash
# 内联定义自定义 agent
claude --agents '{
  "security-auditor": {
    "description": "漏洞分析安全专家",
    "prompt": "你是一位安全专家。发现漏洞并提出修复建议。",
    "tools": ["Read", "Grep", "Glob"],
    "model": "opus"
  }
}' "审计此代码库的安全问题"

# 从文件加载 agent
claude --agents "$(cat ~/.claude/agents.json)" "审查认证模块"

# 与其他标志组合使用
claude -p --agents "$(cat agents.json)" --model sonnet "分析性能"
```

### Agent 优先级

当存在多个 agent 定义时，按以下优先级顺序加载：

① **CLI 定义**（`--agents` 标志）——会话级别
② **用户级别**（`~/.claude/agents/`）——所有项目
③ **项目级别**（`.claude/agents/`）——当前项目

CLI 定义的 agent 在当前会话中覆盖用户和项目级别的 agent。

---

## 高价值使用场景

### ① CI/CD 集成

在 CI/CD 流水线中使用 Claude Code 进行自动化代码审查、测试和文档生成。

**GitHub Actions 示例：**

```yaml
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p --output-format json \
            --max-turns 1 \
            "Review the changes in this PR for:
            - Security vulnerabilities
            - Performance issues
            - Code quality
            Output as JSON with 'issues' array" > review.json

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review.json', 'utf8'));
            // Process and post review comments
```

**Jenkins Pipeline：**

```groovy
pipeline {
    agent any
    stages {
        stage('AI Review') {
            steps {
                sh '''
                    claude -p --output-format json \
                      --max-turns 3 \
                      "Analyze test coverage and suggest missing tests" \
                      > coverage-analysis.json
                '''
            }
        }
    }
}
```

### ② 脚本管道处理

通过 Claude 处理文件、日志和数据进行分析。

**日志分析：**

```bash
# 分析错误日志
tail -1000 /var/log/app/error.log | claude -p "总结这些错误并提出修复建议"

# 发现访问日志中的异常模式
cat access.log | claude -p "识别可疑的访问模式"

# 分析 git 历史
git log --oneline -50 | claude -p "总结近期的开发活动"
```

**代码处理：**

```bash
# 审查单个文件
cat src/auth.ts | claude -p "审查此认证代码的安全问题"

# 生成文档
cat src/api/*.ts | claude -p "生成 markdown 格式的 API 文档"

# 找出 TODO 并按优先级排序
grep -r "TODO" src/ | claude -p "按重要性对这些 TODO 排序"
```

### ③ 多会话工作流

使用多个对话线程管理复杂项目。

```bash
# 启动一个功能分支会话
claude -r "feature-auth" "我们来实现用户认证"

# 之后继续该会话
claude -r "feature-auth" "添加密码重置功能"

# 分叉会话尝试替代方案
claude --resume feature-auth --fork-session "改用 OAuth"

# 切换到另一个功能会话
claude -r "feature-payments" "继续 Stripe 集成"
```

### ④ 自定义 Agent 配置

为团队工作流定义专用 agent。

```bash
# 将 agent 配置保存到文件
cat > ~/.claude/agents.json << 'EOF'
{
  "reviewer": {
    "description": "PR 审查用的代码审查员",
    "prompt": "审查代码的质量、安全性和可维护性。",
    "model": "opus"
  },
  "documenter": {
    "description": "文档专家",
    "prompt": "生成清晰全面的文档。",
    "model": "sonnet"
  },
  "refactorer": {
    "description": "代码重构专家",
    "prompt": "提出并实施整洁代码重构。",
    "tools": ["Read", "Edit", "Glob"]
  }
}
EOF

# 在会话中使用 agent
claude --agents "$(cat ~/.claude/agents.json)" "审查认证模块"
```

### ⑤ 批量处理

使用一致设置处理多个查询。

```bash
# 处理多个文件
for file in src/*.ts; do
  echo "Processing $file..."
  claude -p --model haiku "总结此文件: $(cat $file)" >> summaries.md
done

# 批量代码审查
find src -name "*.py" -exec sh -c '
  echo "## $1" >> review.md
  cat "$1" | claude -p "简短代码审查" >> review.md
' _ {} \;

# 为所有模块生成测试
for module in $(ls src/modules/); do
  claude -p "为 src/modules/$module 生成单元测试" > "tests/$module.test.ts"
done
```

### ⑥ 安全意识开发

使用权限控制确保安全运行。

```bash
# 只读安全审计
claude --permission-mode plan \
  --tools "Read,Grep,Glob" \
  "审计此代码库的安全漏洞"

# 阻止危险命令
claude --disallowedTools "Bash(rm:*)" "Bash(curl:*)" "Bash(wget:*)" \
  "帮我清理此项目"

# 受限自动化
claude -p --max-turns 2 \
  --allowedTools "Read" "Glob" \
  "找出所有硬编码的凭据"
```

### ⑦ JSON API 集成

结合 `jq` 解析将 Claude 用作可编程 API。

```bash
# 获取结构化分析结果
claude -p --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array"},"complexity":{"type":"string"}}}' \
  "分析 main.py 并返回函数列表及复杂度评级"

# 结合 jq 进行后处理
claude -p --output-format json "列出所有 API 端点" | jq '.endpoints[]'

# 在脚本中使用
RESULT=$(claude -p --output-format json "此代码是否安全? 以 {secure: boolean, issues: []} 回答" < code.py)
if echo "$RESULT" | jq -e '.secure == false' > /dev/null; then
  echo "发现安全问题!"
  echo "$RESULT" | jq '.issues[]'
fi
```

### jq 解析示例

使用 `jq` 解析和处理 Claude 的 JSON 输出：

```bash
# 提取特定字段
claude -p --output-format json "分析此代码" | jq '.result'

# 过滤数组元素
claude -p --output-format json "列出问题" | jq -r '.issues[] | select(.severity=="high")'

# 提取多个字段
claude -p --output-format json "描述此项目" | jq -r '.{name, version, description}'

# 转换为 CSV
claude -p --output-format json "列出函数" | jq -r '.functions[] | [.name, .lineCount] | @csv'

# 条件处理
claude -p --output-format json "检查安全性" | jq 'if .vulnerabilities | length > 0 then "UNSAFE" else "SAFE" end'

# 提取嵌套值
claude -p --output-format json "分析性能" | jq '.metrics.cpu.usage'

# 处理整个数组
claude -p --output-format json "找出待办事项" | jq '.todos | length'

# 转换输出格式
claude -p --output-format json "列出改进建议" | jq 'map({title: .title, priority: .priority})'
```

---

## 模型

Claude Code 支持多种具有不同能力的模型：

| 模型 | ID | 上下文窗口 | 说明 |
|------|-----|-----------|------|
| Opus 4.6 | `claude-opus-4-6` | 100 万 token | 最强能力，自适应努力级别 |
| Sonnet 4.6 | `claude-sonnet-4-6` | 100 万 token | 速度与能力的平衡 |
| Haiku 4.5 | `claude-haiku-4-5` | 100 万 token | 最快速度，适合快速任务 |

### 模型选择

```bash
# 使用简称
claude --model opus "复杂架构审查"
claude --model sonnet "实现此功能"
claude --model haiku -p "格式化此 JSON"

# 使用 opusplan 别名（Opus 规划，Sonnet 执行）
claude --model opusplan "设计并实现此 API"

# 会话内切换快速模式
/fast
```

### 努力级别（Opus 4.6）

Opus 4.6 支持自适应推理和努力级别：

```bash
# 通过 CLI 标志设置
claude --effort high "复杂审查"

# 通过斜杠命令设置
/effort high

# 通过环境变量设置
export CLAUDE_CODE_EFFORT_LEVEL=high   # low, medium, high, 或 max（仅 Opus 4.6）
```

提示词中的 `ultrathink` 关键字会激活深度推理。`max` 努力级别为 Opus 4.6 专属。

---

## 关键环境变量

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | API 认证密钥 |
| `ANTHROPIC_MODEL` | 覆盖默认模型 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | API 自定义模型选项 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | 覆盖默认 Opus 模型 ID |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 覆盖默认 Sonnet 模型 ID |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | 覆盖默认 Haiku 模型 ID |
| `MAX_THINKING_TOKENS` | 设置扩展思考的 token 预算 |
| `CLAUDE_CODE_EFFORT_LEVEL` | 设置努力级别（`low`/`medium`/`high`/`max`） |
| `CLAUDE_CODE_SIMPLE` | 最小化模式，由 `--bare` 标志设置 |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | 禁用自动更新 CLAUDE.md |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | 禁用后台任务执行 |
| `CLAUDE_CODE_DISABLE_CRON` | 禁用定时/计划任务 |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | 禁用 git 相关指令 |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` | 禁用终端标题更新 |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | 禁用 100 万 token 上下文窗口 |
| `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` | 禁用非流式回退 |
| `CLAUDE_CODE_ENABLE_TASKS` | 启用任务列表功能 |
| `CLAUDE_CODE_TASK_LIST_ID` | 跨会话共享的命名任务目录 |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | 切换提示建议（`true`/`false`） |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 启用实验性 Agent 团队 |
| `CLAUDE_CODE_NEW_INIT` | 使用新的初始化流程 |
| `CLAUDE_CODE_SUBAGENT_MODEL` | 子代理执行模型 |
| `CLAUDE_CODE_PLUGIN_SEED_DIR` | 插件种子文件目录 |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | 从子进程中清除的环境变量 |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | 覆盖自动压缩百分比 |
| `CLAUDE_STREAM_IDLE_TIMEOUT_MS` | 流空闲超时（毫秒） |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | 斜杠命令工具字符预算 |
| `ENABLE_TOOL_SEARCH` | 启用工具搜索能力 |
| `MAX_MCP_OUTPUT_TOKENS` | MCP 工具输出的最大 token 数 |

---

## 快速参考

### 最常用命令

```bash
# 交互会话
claude

# 快速提问
claude -p "如何..."

# 继续对话
claude -c

# 处理文件
cat file.py | claude -p "审查此文件"

# JSON 输出用于脚本
claude -p --output-format json "查询"
```

### 标志组合速查

| 使用场景 | 命令 |
|----------|------|
| 快速代码审查 | `cat file \| claude -p "审查"` |
| 结构化输出 | `claude -p --output-format json "查询"` |
| 安全探索 | `claude --permission-mode plan` |
| 自主运行+安全 | `claude --enable-auto-mode --permission-mode auto` |
| CI/CD 集成 | `claude -p --max-turns 3 --output-format json` |
| 恢复工作 | `claude -r "会话名称"` |
| 自定义模型 | `claude --model opus "复杂任务"` |
| 最小化模式 | `claude --bare "快速查询"` |
| 预算受限运行 | `claude -p --max-budget-usd 2.00 "分析代码"` |

---

## 故障排查

### 命令未找到

**问题：** `claude: command not found`

**解决方案：**
- 安装 Claude Code：`npm install -g @anthropic-ai/claude-code`
- 检查 PATH 是否包含 npm 全局 bin 目录
- 尝试完整路径运行：`npx claude`

### API 密钥问题

**问题：** 认证失败

**解决方案：**
- 设置 API 密钥：`export ANTHROPIC_API_KEY=your-key`
- 检查密钥有效且有足够额度
- 验证密钥对所请求模型的权限

### 会话未找到

**问题：** 无法恢复会话

**解决方案：**
- 列出可用会话找到正确的名称/ID
- 会话可能在长时间不活跃后过期
- 使用 `-c` 继续最近的会话

### 输出格式问题

**问题：** JSON 输出格式异常

**解决方案：**
- 使用 `--json-schema` 强制结构
- 在提示词中添加明确的 JSON 指令
- 使用 `--output-format json`（而非仅在提示词中要求 JSON）

### 权限被拒绝

**问题：** 工具执行被阻止

**解决方案：**
- 检查 `--permission-mode` 设置
- 审查 `--allowedTools` 和 `--disallowedTools` 标志
- 自动化场景谨慎使用 `--dangerously-skip-permissions`

---

## 更多资源

- **[官方 CLI 参考](https://code.claude.com/docs/en/cli-reference)** —— 完整命令参考
- **[无头模式文档](https://code.claude.com/docs/en/headless)** —— 自动化执行
- **[斜杠命令](../01-slash-commands/)** —— Claude 内部自定义快捷方式
- **[记忆指南](../02-memory/)** —— 通过 CLAUDE.md 持久化上下文
- **[MCP 协议](../05-mcp/)** —— 外部工具集成
- **[高级特性](../09-advanced-features/)** —— 规划模式、扩展思考
- **[子代理指南](../04-subagents/)** —— 委托任务执行

---

*属于 [Claude How To](../) 指南系列*

---
**最后更新: 2026 年 4 月 9 日
**Claude Code 版本: 2.1.97
**兼容模型**: Claude Sonnet 4.6, Claude Opus 4.6, Claude Haiku 4.5
