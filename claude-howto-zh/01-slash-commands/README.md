<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# 斜杠命令(Slash Commands)

## 概述

斜杠命令(Slash Commands)是在交互式会话中控制 Claude 行为的快捷方式。它们分为以下几种类型:

- **内置命令(Built-in commands)**:由 Claude Code 提供(`/help`、`/clear`、`/model`)
- **技能(Skills)**:用户创建的 `SKILL.md` 文件形式的命令(`/optimize`、`/pr`)
- **插件命令(Plugin commands)**:来自已安装插件的命令(`/frontend-design:frontend-design`)
- **MCP 提示词(MCP prompts)**:来自 MCP 服务器的命令(`/mcp__github__list_prs`)

> **注意**:自定义斜杠命令已合并到技能系统中。`.claude/commands/` 中的文件仍然可用,但技能(`.claude/skills/`)现在是推荐的方式。两者都会创建 `/command-name` 快捷方式。完整参考请参阅 [技能指南](../03-skills/)。

## 内置命令参考

内置命令是常见操作的快捷方式。共有 **55+ 个内置命令**和 **5 个内置技能**可用。在 Claude Code 中输入 `/` 查看完整列表,或输入 `/` 后跟字母进行筛选。

| 命令 | 用途 |
|------|------|
| `/add-dir <path>` | 添加工作目录 |
| `/agents` | 管理代理配置 |
| `/branch [name]` | 将对话分支到新会话(别名:`/fork`)。注意:v2.1.77 中 `/fork` 已重命名为 `/branch` |
| `/btw <question>` | 侧边提问,不添加到历史记录 |
| `/chrome` | 配置 Chrome 浏览器集成 |
| `/clear` | 清除对话(别名:`/reset`、`/new`) |
| `/color [color\|default]` | 设置提示栏颜色 |
| `/compact [instructions]` | 压缩对话,可选聚焦指令 |
| `/config` | 打开设置(别名:`/settings`) |
| `/context` | 以彩色网格可视化上下文使用情况 |
| `/copy [N]` | 将助手响应复制到剪贴板;`w` 写入文件 |
| `/cost` | 显示 Token 使用统计 |
| `/desktop` | 在桌面应用中继续(别名:`/app`) |
| `/diff` | 未提交更改的交互式差异查看器 |
| `/doctor` | 诊断安装健康状况 |
| `/effort [low\|medium\|high\|max\|auto]` | 设置努力程度级别。`max` 需要 Opus 4.6 |
| `/exit` | 退出 REPL(别名:`/quit`) |
| `/export [filename]` | 将当前对话导出到文件或剪贴板 |
| `/extra-usage` | 配置额外使用量以应对速率限制 |
| `/fast [on\|off]` | 切换快速模式 |
| `/feedback` | 提交反馈(别名:`/bug`) |
| `/help` | 显示帮助 |
| `/hooks` | 查看钩子配置 |
| `/ide` | 管理 IDE 集成 |
| `/init` | 初始化 `CLAUDE.md`。设置 `CLAUDE_CODE_NEW_INIT=true` 启用交互流程 |
| `/insights` | 生成会话分析报告 |
| `/install-github-app` | 设置 GitHub Actions 应用 |
| `/install-slack-app` | 安装 Slack 应用 |
| `/keybindings` | 打开快捷键配置 |
| `/login` | 切换 Anthropic 账户 |
| `/logout` | 从 Anthropic 账户登出 |
| `/mcp` | 管理 MCP 服务器和 OAuth |
| `/memory` | 编辑 `CLAUDE.md`,切换自动记忆 |
| `/mobile` | 移动应用二维码(别名:`/ios`、`/android`) |
| `/model [model]` | 选择模型,使用左右箭头调整努力程度 |
| `/passes` | 分享 Claude Code 免费周 |
| `/permissions` | 查看/更新权限(别名:`/allowed-tools`) |
| `/plan [description]` | 进入规划模式 |
| `/plugin` | 管理插件 |
| `/pr-comments [PR]` | 获取 GitHub PR 评论 |
| `/privacy-settings` | 隐私设置(仅 Pro/Max) |
| `/release-notes` | 查看更新日志 |
| `/reload-plugins` | 重新加载活动插件 |
| `/remote-control` | 从 claude.ai 远程控制(别名:`/rc`) |
| `/remote-env` | 配置默认远程环境 |
| `/rename [name]` | 重命名会话 |
| `/resume [session]` | 恢复对话(别名:`/continue`) |
| `/review` | **已弃用** -- 请安装 `code-review` 插件替代 |
| `/rewind` | 回退对话和/或代码(别名:`/checkpoint`) |
| `/sandbox` | 切换沙箱模式 |
| `/schedule [description]` | 创建/管理定时任务 |
| `/security-review` | 分析分支的安全漏洞 |
| `/skills` | 列出可用技能 |
| `/stats` | 可视化每日使用情况、会话数、连续天数 |
| `/status` | 显示版本、模型、账户信息 |
| `/statusline` | 配置状态栏 |
| `/tasks` | 列出/管理后台任务 |
| `/terminal-setup` | 配置终端快捷键 |
| `/theme` | 更改颜色主题 |
| `/vim` | 切换 Vim/普通模式 |
| `/voice` | 切换按住说话语音输入 |

### 内置技能(Bundled Skills)

这些技能随 Claude Code 一起提供,可以像斜杠命令一样调用:

| 技能 | 用途 |
|------|------|
| `/batch <instruction>` | 使用 worktree 编排大规模并行更改 |
| `/claude-api` | 加载项目语言的 Claude API 参考 |
| `/debug [description]` | 启用调试日志 |
| `/loop [interval] <prompt>` | 按间隔重复运行提示词 |
| `/simplify [focus]` | 审查更改文件的代码质量 |

### 已弃用的命令

| 命令 | 状态 |
|------|------|
| `/review` | 已弃用 -- 由 `code-review` 插件替代 |
| `/output-style` | 自 v2.1.73 起已弃用 |
| `/fork` | 已重命名为 `/branch`(别名仍可用,v2.1.77) |

### 近期变更

- `/fork` 已重命名为 `/branch`,`/fork` 保留为别名(v2.1.77)
- `/output-style` 已弃用(v2.1.73)
- `/review` 已弃用,推荐使用 `code-review` 插件
- 新增 `/effort` 命令,支持 `max` 级别(需要 Opus 4.6)
- 新增 `/voice` 命令,支持按住说话语音输入
- 新增 `/schedule` 命令,用于创建/管理定时任务
- 新增 `/color` 命令,用于提示栏自定义
- `/model` 选择器现在显示可读标签(如 "Sonnet 4.6"),而非原始模型 ID
- `/resume` 支持 `/continue` 别名
- MCP 提示词可作为 `/mcp__<server>__<prompt>` 命令使用(参见 [MCP 提示词作为命令](#mcp-prompts-as-commands))

## 自定义命令(现为技能)

自定义斜杠命令已**合并到技能系统**。两种方式都能创建可通过 `/command-name` 调用的命令:

| 方式 | 位置 | 状态 |
|------|------|------|
| **技能(推荐)** | `.claude/skills/<name>/SKILL.md` | 当前标准 |
| **旧版命令** | `.claude/commands/<name>.md` | 仍然可用 |

如果技能和命令同名,**技能优先**。例如,当 `.claude/commands/review.md` 和 `.claude/skills/review/SKILL.md` 同时存在时,将使用技能版本。

### 迁移路径

现有的 `.claude/commands/` 文件无需修改即可继续使用。要迁移到技能:

**迁移前(命令):**
```
.claude/commands/optimize.md
```

**迁移后(技能):**
```
.claude/skills/optimize/SKILL.md
```

### 为什么选择技能?

技能相比旧版命令提供额外的功能:

- **目录结构**:可打包脚本、模板和参考文件
- **自动调用**:Claude 可以在相关时自动触发技能
- **调用控制**:可选择用户、Claude 或两者是否可以调用
- **子代理执行**:可在隔离上下文中使用 `context: fork` 运行技能
- **渐进式加载**:仅在需要时加载附加文件

### 将自定义命令创建为技能

创建一个包含 `SKILL.md` 文件的目录:

```bash
mkdir -p .claude/skills/my-command
```

**文件:** `.claude/skills/my-command/SKILL.md`

```yaml
---
name: my-command
description: 此命令的功能以及何时使用它
---

# 我的命令

Claude 在调用此命令时应遵循的说明。

1. 第一步
2. 第二步
3. 第三步
```

### Frontmatter 参考表

| 字段 | 用途 | 默认值 |
|------|------|--------|
| `name` | 命令名称(变为 `/name`) | 目录名 |
| `description` | 简短描述(帮助 Claude 知道何时使用) | 第一段 |
| `argument-hint` | 用于自动补全的预期参数 | 无 |
| `allowed-tools` | 命令无需许可即可使用的工具 | 继承 |
| `model` | 要使用的特定模型 | 继承 |
| `disable-model-invocation` | 若为 `true`,仅用户可调用(非 Claude) | `false` |
| `user-invocable` | 若为 `false`,从 `/` 菜单中隐藏 | `true` |
| `context` | 设为 `fork` 以在隔离子代理中运行 | 无 |
| `agent` | 使用 `context: fork` 时的代理类型 | `general-purpose` |
| `hooks` | 技能作用域钩子(PreToolUse, PostToolUse, Stop) | 无 |

### 参数

命令可以接收参数:

**所有参数通过 `$ARGUMENTS`:**

```yaml
---
name: fix-issue
description: 按编号修复 GitHub Issue
---

按照我们的编码标准修复 #$ARGUMENTS Issue
```

用法:`/fix-issue 123` → `$ARGUMENTS` 变为 "123"

**独立参数通过 `$0`、`$1` 等:**

```yaml
---
name: review-pr
description: 按优先级审查 PR
---

审查 PR #$0,优先级 $1
```

用法:`/review-pr 456 high` → `$0`="456", `$1`="high"

### 通过 Shell 命令实现动态上下文

在提示词之前使用 `` !`command` `` 执行 bash 命令:

```yaml
---
name: commit
description: 创建带上下文的 git commit
allowed-tools: Bash(git *)
---

## 上下文

- 当前 git 状态:!`git status`
- 当前 git diff:!`git diff HEAD`
- 当前分支:!`git branch --show-current`
- 最近提交:!`git log --oneline -5`

## 你的任务

基于以上变更,创建一个 git commit。
```

### 文件引用

使用 `@` 包含文件内容:

```markdown
审查 @src/utils/helpers.js 中的实现
比较 @src/old-version.js 与 @src/new-version.js
```

## 插件命令

插件可以提供自定义命令:

```
/plugin-name:command-name
```

或在没有命名冲突时直接使用 `/command-name`。

**示例:**
```bash
/frontend-design:frontend-design
/commit-commands:commit
```

## MCP 提示词作为命令

MCP 服务器可以将提示词暴露为斜杠命令:

```
/mcp__<server-name>__<prompt-name> [arguments]
```

**示例:**
```bash
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug 标题" high
```

### MCP 权限语法

在权限中控制 MCP 服务器访问:

- `mcp__github` - 访问整个 GitHub MCP 服务器
- `mcp__github__*` - 通配符访问所有工具
- `mcp__github__get_issue` - 特定工具访问

## 命令架构

```mermaid
graph TD
    A["用户输入: /command-name"] --> B["命令类型"]
    B -->|内置| C["执行内置命令"]
    B -->|技能| D["加载 SKILL.md"]
    B -->|插件| E["加载插件命令"]
    B -->|MCP| F["执行 MCP 提示词"]

    D --> G["解析 Frontmatter"]
    G --> H["替换变量"]
    H --> I["执行 Shell 命令"]
    I --> J["发送给 Claude"]
    J --> K["返回结果"]
```

## 命令生命周期

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant FS as FileSystem
    participant CLI as Shell/Bash

    User->>Claude: 输入 /optimize
    Claude->>FS: 搜索 .claude/skills/ 和 .claude/commands/
    FS-->>Claude: 返回 optimize/SKILL.md
    Claude->>Claude: 解析 frontmatter
    Claude->>CLI: 执行 !`command` 替换
    CLI-->>Claude: 命令输出
    Claude->>Claude: 替换 $ARGUMENTS
    Claude->>User: 处理提示词
    Claude->>User: 返回结果
```

## 本文件夹中的可用命令

这些示例命令可以作为技能或旧版命令安装。

### 1. `/optimize` -- 代码优化

分析代码的性能问题、内存泄漏和优化机会。

**用法:**
```
/optimize
[粘贴你的代码]
```

### 2. `/pr` -- Pull Request 准备

引导完成 PR 准备清单,包括代码检查、测试和提交格式化。

**用法:**
```
/pr
```

**截图:**
![/pr](pr-slash-command.png)

### 3. `/generate-api-docs` -- API 文档生成器

从源代码生成全面的 API 文档。

**用法:**
```
/generate-api-docs
```

### 4. `/commit` -- 带上下文的 Git Commit

从你的仓库创建带动态上下文的 git commit。

**用法:**
```
/commit [可选消息]
```

### 5. `/push-all` -- 暂存、提交和推送

暂存所有变更、创建 commit 并推送到远程,附带安全检查。

**用法:**
```
/push-all
```

**安全检查:**
- 密钥:`.env*`、`*.key`、`*.pem`、`credentials.json`
- API Key:检测真实密钥与占位符
- 大文件:`>10MB` 且未使用 Git LFS
- 构建产物:`node_modules/`、`dist/`、`__pycache__/`

### 6. `/doc-refactor` -- 文档重构

重构项目文档以提高清晰度和可访问性。

**用法:**
```
/doc-refactor
```

### 7. `/setup-ci-cd` -- CI/CD 流水线搭建

实现预提交钩子和 GitHub Actions 以保证质量。

**用法:**
```
/setup-ci-cd
```

### 8. `/unit-test-expand` -- 测试覆盖率扩展

通过针对未测试的分支和边界情况来增加测试覆盖率。

**用法:**
```
/unit-test-expand
```

## 安装

### 作为技能安装(推荐)

复制到你的技能目录:

```bash
# 创建技能目录
mkdir -p .claude/skills

# 对每个命令文件,创建技能目录
for cmd in optimize pr commit; do
  mkdir -p .claude/skills/$cmd
  cp 01-slash-commands/$cmd.md .claude/skills/$cmd/SKILL.md
done
```

### 作为旧版命令安装

复制到你的命令目录:

```bash
# 项目范围(团队)
mkdir -p .claude/commands
cp 01-slash-commands/*.md .claude/commands/

# 个人使用
mkdir -p ~/.claude/commands
cp 01-slash-commands/*.md ~/.claude/commands/
```

## 创建你自己的命令

### 技能模板(推荐)

创建 `.claude/skills/my-command/SKILL.md`:

```yaml
---
name: my-command
description: 此命令的功能。[触发条件]时使用。
argument-hint: [可选参数]
allowed-tools: Bash(npm *), Read, Grep
---

# 命令标题

## 上下文

- 当前分支:!`git branch --show-current`
- 相关文件:@package.json

## 说明

1. 第一步
2. 第二步,带参数:$ARGUMENTS
3. 第三步

## 输出格式

- 如何格式化响应
- 包含什么内容
```

### 仅用户调用命令(无自动调用)

对于具有副作用且 Claude 不应自动触发的命令:

```yaml
---
name: deploy
description: 部署到生产环境
disable-model-invocation: true
allowed-tools: Bash(npm *), Bash(git *)
---

部署应用到生产环境:

1. 运行测试
2. 构建应用
3. 推送到部署目标
4. 验证部署
```

## 最佳实践

| ✅ 推荐 | ❌ 不推荐 |
|---------|----------|
| 使用清晰、面向动作的命名 | 为一次性任务创建命令 |
| 包含带触发条件的 `description` | 在命令中构建复杂逻辑 |
| 保持命令专注于单一任务 | 硬编码敏感信息 |
| 对副作用使用 `disable-model-invocation` | 跳过 description 字段 |
| 使用 `!` 前缀实现动态上下文 | 假设 Claude 知道当前状态 |
| 将相关文件组织在技能目录中 | 把所有内容放在一个文件中 |

## 故障排除

### 命令未找到

**解决方案:**
- 检查文件是否在 `.claude/skills/<name>/SKILL.md` 或 `.claude/commands/<name>.md`
- 验证 frontmatter 中的 `name` 字段与预期的命令名匹配
- 重启 Claude Code 会话
- 运行 `/help` 查看可用命令

### 命令未按预期执行

**解决方案:**
- 添加更具体的指令
- 在技能文件中包含示例
- 如果使用 bash 命令,检查 `allowed-tools`
- 先用简单输入测试

### 技能与命令冲突

如果两者同名,**技能优先**。删除其中一个或重命名。

## 相关指南

- **[技能](../03-skills/)** -- 技能完整参考(自动调用能力)
- **[记忆](../02-memory/)** -- 通过 CLAUDE.md 实现持久化上下文
- **[子代理](../04-subagents/)** -- 委托型 AI 代理
- **[插件](../07-plugins/)** -- 打包的命令集合
- **[钩子](../06-hooks/)** -- 事件驱动自动化

## 其他资源

- [官方交互模式文档](https://code.claude.com/docs/en/interactive-mode) -- 内置命令参考
- [官方技能文档](https://code.claude.com/docs/en/skills) -- 技能完整参考
- [CLI 参考](https://code.claude.com/docs/en/cli-reference) -- 命令行选项

---
*属于 [Claude How To](../) 指南系列的一部分*
