# 课时测验 — 题库

每门课程 10 道题。每道题包含：类别、问题文本、选项（3-4 个）、正确答案、解析和复习指向。

---

## 第 01 课：Slash Commands（斜杠命令）

### Q1
- **类别**：概念类
- **问题**：Claude Code 中斜杠命令有哪四种类型？
- **选项**：A) 内置、技能、插件命令、MCP 提示词 | B) 内置、自定义、钩子命令、API 提示词 | C) 系统、用户、插件、终端命令 | D) 核心、扩展、宏、脚本命令
- **正确**：A
- **解析**：Claude Code 有内置命令（如 /help、/compact）、技能（SKILL.md 文件）、插件命令（带 plugin-name:command 命名空间）和 MCP 提示词（/mcp__server__prompt）。
- **复习**：斜杠命令类型章节

### Q2
- **类别**：实践类
- **问题**：如何将用户提供的所有参数传递给技能？
- **选项**：A) 使用 `${args}` | B) 使用 `$ARGUMENTS` | C) 使用 `$@` | D) 使用 `$INPUT`
- **正确**：B
- **解析**：`$ARGUMENTS` 捕获命令名称后的所有文本。对于位置参数，使用 `$0`、`$1` 等。
- **复习**：参数处理章节

### Q3
- **类别**：概念类
- **问题**：当技能（.claude/skills/name/SKILL.md）和传统命令（.claude/commands/name.md）同名时，哪个优先？
- **选项**：A) 传统命令 | B) 技能 | C) 先创建的那个 | D) Claude 让用户选择
- **正确**：B
- **解析**：技能优先于同名的传统命令。技能系统取代了旧的命令系统。
- **复习**：技能优先级章节

### Q4
- **类别**：实践类
- **问题**：如何将实时 Shell 输出注入到技能的提示中？
- **选项**：A) 使用 `$(command)` 语法 | B) 使用 `!`command``（带 ! 的反引号）语法 | C) 使用 `@shell:command` 语法 | D) 使用 `{command}` 语法
- **正确**：B
- **解析**：`!`command`` 语法运行 Shell 命令并将其输出注入到技能提示中，Claude 看到它之前就已执行完毕。
- **复习**：动态上下文注入章节

### Q5
- **类别**：概念类
- **问题**：技能 frontmatter 中的 `disable-model-invocation: true` 有什么作用？
- **选项**：A) 完全阻止技能运行 | B) 仅允许用户手动调用（Claude 不能自动调用）| C) 将其从 /help 菜单隐藏 | D) 禁用技能的 AI 处理
- **正确**：B
- **解析**：`disable-model-invocation: true` 表示只有用户可以通过 `/command-name` 触发该命令。Claude 永远不会自动调用它，适用于有副作用的技能（如部署）。
- **复习**：控制调用章节

### Q6
- **类别**：实践类
- **问题**：你想创建一个只有 Claude 能自动调用的技能（对用户 / 菜单隐藏）。应设置哪个 frontmatter 字段？
- **选项**：A) `disable-model-invocation: true` | B) `user-invocable: false` | C) `hidden: true` | D) `auto-only: true`
- **正确**：B
- **解析**：`user-invocable: false` 将技能从用户的斜杠菜单中隐藏，但允许 Claude 根据上下文自动调用它。
- **复习**：调用控制矩阵章节

### Q7
- **类别**：实践类
- **问题**：名为 "deploy" 的新自定义技能的正确目录结构是什么？
- **选项**：A) `.claude/commands/deploy.md` | B) `.claude/skills/deploy/SKILL.md` | C) `.claude/skills/deploy.md` | D) `.claude/deploy/SKILL.md`
- **正确**：B
- **解析**：技能位于 `.claude/skills/` 下的目录中，内部有一个 `SKILL.md` 文件。目录名与命令名匹配。
- **复习**：技能类型与位置章节

### Q8
- **类别**：概念类
- **问题**：插件命令如何避免与用户命令的命名冲突？
- **选项**：A) 它们使用 `plugin-name:command-name` 命名空间 | B) 它们有特殊的 .plugin 扩展名 | C) 它们以 `p/` 为前缀 | D) 它们自动覆盖用户命令
- **正确**：A
- **解析**：插件命令使用类似 `pr-review:check-security` 的命名空间来避免与独立用户命令冲突。
- **复习**：插件命令章节

### Q9
- **类别**：实践类
- **问题**：你想限制一个技能可以使用的工具。应在 frontmatter 中添加哪个字段？
- **选项**：A) `tools: [Read, Grep]` | B) `allowed-tools: [Read, Grep]` | C) `permissions: [Read, Grep]` | D) `restrict-tools: [Read, Grep]`
- **正确**：B
- **解析**：SKILL.md frontmatter 中的 `allowed-tools` 字段限定命令可调用的工具范围。
- **复习**：Frontmatter 字段参考章节

### Q10
- **类别**：概念类
- **问题**：技能中的 `@file` 语法有什么用途？
- **选项**：A) 导入另一个技能 | B) 引用一个文件以将其内容包含到提示中 | C) 创建符号链接 | D) 设置文件权限
- **正确**：B
- **解析**：技能中的 `@path/to/file` 语法将引用文件的内容包含到提示中，允许技能引入模板或上下文文件。
- **复习**：文件引用章节

---

## 第 02 课：Memory（记忆）

### Q1
- **类别**：概念类
- **问题**：Claude Code 记忆层级有多少级，哪个优先级最高？
- **选项**：A) 5 级，用户记忆最高 | B) 7 级，托管策略最高 | C) 3 级，项目记忆最高 | D) 7 级，自动记忆最高
- **正确**：B
- **解析**：层级共有 7 级：托管策略 > 项目记忆 > 项目规则 > 用户记忆 > 用户规则 > 本地项目记忆 > 自动记忆。由管理员设置的托管策略优先级最高。
- **复习**：记忆层级章节

### Q2
- **类别**：实践类
- **问题**：如何在对话中快速向记忆添加新规则？
- **选项**：A) 输入 `/memory add "rule text"` | B) 用 `#` 作为消息前缀（例如 `# always use TypeScript`）| C) 输入 `/rule "rule text"` | D) 使用 `@add-memory "rule text"`
- **正确**：B
- **解析**：`#` 前缀模式允许在对话中快速添加单条规则。Claude 会询问要保存到哪个记忆级别。
- **复习**：快速记忆更新章节

### Q3
- **类别**：概念类
- **问题**：CLAUDE.md 中 `@path/to/file` 导入的最大深度是多少？
- **选项**：A) 3 层深 | B) 5 层深 | C) 10 层深 | D) 无限
- **正确**：B
- **解析**：`@import` 语法支持递归导入，最大深度为 5 层以防止无限循环。
- **复习**：导入语法章节

### Q4
- **类别**：实践类
- **问题**：如何将规则限定为仅应用于 `src/api/` 中的文件？
- **选项**：A) 将规则放在 `src/api/CLAUDE.md` | B) 在 `.claude/rules/*.md` 文件中添加 `paths: src/api/**` YAML frontmatter | C) 将文件命名为 `.claude/rules/api.md` | D) 在规则文件中使用 `@scope: src/api`
- **正确**：B
- **解析**：`.claude/rules/` 中的文件支持带有 glob 模式的 `paths:` frontmatter 字段来将规则限定到特定目录。
- **复习**：路径特定规则章节

### Q5
- **类别**：概念类
- **问题**：Auto Memory 的 MEMORY.md 在会话开始时加载多少行？
- **选项**：A) 所有行 | B) 前 100 行 | C) 前 200 行 | D) 前 500 行
- **正确**：C
- **解析**：MEMORY.md 的前 200 行在会话启动时自动加载到上下文中。从 MEMORY.md 引用的主题文件按需加载。
- **复习**：自动记忆章节

### Q6
- **类别**：实践类
- **问题**：你需要不提交到 git 的个人项目偏好设置。应使用哪个文件？
- **选项**：A) `~/.claude/CLAUDE.md` | B) `CLAUDE.local.md` | C) `.claude/rules/personal.md` | D) `.claude/memory/personal.md`
- **正确**：B
- **解析**：项目根目录下的 `CLAUDE.local.md` 用于个人项目专属偏好。应将其加入 git 忽略列表。
- **复习**：记忆位置对比章节

### Q7
- **类别**：概念类
- **问题**：`/init` 命令的作用是什么？
- **选项**：A) 从头初始化一个新的 Claude Code 项目 | B) 根据你的项目结构生成模板 CLAUDE.md | C) 重置所有记忆为默认值 | D) 创建一个新会话
- **正确**：B
- **解析**：`/init` 分析你的项目并生成包含建议规则和标准的模板 CLAUDE.md。这是一个一次性引导工具。
- **复习**：/init 命令章节

### Q8
- **类别**：实践类
- **问题**：如何完全禁用 Auto Memory？
- **选项**：A) 删除 ~/.claude/projects 目录 | B) 设置 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` | C) 在 CLAUDE.md 中添加 `auto-memory: false` | D) 使用 `/memory disable auto`
- **正确**：B
- **解析**：设置 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` 可禁用自动记忆。值为 0 时强制开启。不设置则默认开启。
- **复习**：自动记忆配置章节

### Q9
- **类别**：概念类
- **问题**：较低优先级的记忆层级能否覆盖较高优先级层级的规则？
- **选项**：A) 可以，最近的规则总是胜出 | B) 不可以，较高层级始终优先 | C) 可以，如果低层级使用了 `!important` 标记 | D) 取决于规则类型
- **正确**：B
- **解析**：记忆优先级从托管策略向下流动。较低层级（如自动记忆）不能覆盖较高层级（如项目记忆）。
- **复习**：记忆层级章节

### Q10
- **类别**：实践类
- **问题**：你在两个仓库工作，希望 Claude 加载两者的 CLAUDE.md。应使用哪个标志？
- **选项**：A) `--multi-repo` | B) `--add-dir /path/to/other` | C) `--include /path/to/other` | D) `--merge-context /path/to/other`
- **正确**：B
- **解析**：`--add-dir` 标志从额外目录加载 CLAUDE.md，允许多仓库上下文。
- **复习**：附加目录章节

---

> ⚠️ **注意**：第 03-10 课的题目遵循相同的格式结构（类别、问题、选项、正确答案、解析、复习指向）。完整的 100 题题库请参阅源文件 `references/question-bank.md`，其中包含 Skills、Subagents、MCP、Hooks、Plugins、Checkpoints、Advanced Features 和 CLI Reference 的全部题目。
>
> 每门课 10 道题，涵盖概念理解和实际操作两方面，确保全面评估你对每个功能领域的掌握程度。
