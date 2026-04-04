---
name: lesson-quiz
version: 1.0.0
description: Claude Code 教程交互式课时测验。通过 8-10 道混合概念和实践知识的问题测试对特定课程（01-10）的理解。可在课前用于预测试、课中用于进度检查或课后用于验证掌握程度。当用户说"quiz me on hooks"（给我出道钩子的测验）、"test my knowledge of lesson 3"（测试我对第3课的知识）、"lesson quiz"（课时测验）、"practice quiz for MCP"（MCP 练习测验）或 "do I understand skills"（我理解技能了吗）时使用。
---

# 课时测验

交互式测验工具，通过 8-10 道问题测试你对特定 Claude Code 课程的理解，提供逐题反馈并指出需要复习的领域。

## 指令

### 步骤 1：确定课程

如果用户提供了课程参数（例如 `/lesson-quiz hooks` 或 `/lesson-quiz 03`），将其映射到课程目录：

**课程映射：**
- `01`、`slash-commands`、`commands` → 01-slash-commands
- `02`、`memory` → 02-memory
- `03`、`skills` → 03-skills
- `04`、`subagents`、`agents` → 04-subagents
- `05`、`mcp` → 05-mcp
- `06`、`hooks` → 06-hooks
- `07`、`plugins` → 07-plugins
- `08`、`checkpoints`、`checkpoint` → 08-checkpoints
- `09`、`advanced`、`advanced-features` → 09-advanced-features
- `10`、`cli` → 10-cli

如果未提供参数，使用 AskUserQuestion 展示选择提示：

**问题 1**（标题："Lesson"）：
"你想测试哪门课程？"
选项：
1. "Slash Commands (01)" — 自定义命令、技能、frontmatter、参数
2. "Memory (02)" — CLAUDE.md、记忆层级、规则、自动记忆
3. "Skills (03)" — 渐进式加载、自动调用、SKILL.md
4. "Subagents (04)" — 任务委派、代理配置、隔离

**问题 2**（标题："Lesson"）：
"你想测试哪门课程？（续）"
选项：
1. "MCP (05)" — 外部集成、传输协议、服务器、Tool Search
2. "Hooks (06)" — 事件自动化、PreToolUse、退出码、JSON I/O
3. "Plugins (07)" — 打包解决方案、市场、plugin.json
4. "More lessons..." — Checkpoints、Advanced Features、 CLI

如果选择了 "More lessons..."：

**问题 3**（标题："Lesson"）：
"请选择你的课程："
选项：
1. "Checkpoints (08)" — 回退、恢复、安全实验
2. "Advanced Features (09)" — 规划、权限、打印模式、思考
3. "CLI Reference (10)" — 标志、输出格式、脚本化、管道

### 步骤 2：读取课程内容

读取课程 README.md 文件以刷新上下文：
- 读取文件：`<课程目录>/README.md`

然后使用 `references/question-bank.md` 中该课程的题库。题库为每门课程提供 10 道预编写的问题及正确答案和解析。

### 步骤 3：呈现测验

询问用户的测验时机：

使用 AskUserQuestion（标题："Timing"）：
"你相对于这门课程在什么阶段参加此测验？"
选项：
1. "课前（预测试）" — 我还没读过这门课，测试我的先验知识
2. "课中（进度检查）" — 我正在学习这门课的过程中
3. "课后（掌握验证）" — 我已完成这门课并想验证理解程度

此上下文影响结果呈现方式（见步骤 5）。

### 步骤 4：分轮次呈现问题

从题库中呈现 10 道问题，每轮 2 道（共 5 轮）。每道题使用 AskUserQuestion 配合问题文本和 3-4 个答案选项。

**重要提示**：AskUserQuestion 每题最多支持 4 个选项，每轮 2 题。

对于每轮，展示 2 道题。全部 5 轮完成后进入评分。

**每轮题目格式：**

题库中的每道题包含：
- `question`：问题文本
- `options`：3-4 个答案选项（一个正确，在题库中标注）
- `correct`：正确答案标签
- `explanation`：为什么该答案是正确的
- `category`："conceptual"（概念类）或 "practical"（实践类）

使用 AskUserQuestion 呈现每道题。记录用户的回答。

### 步骤 5：评分并呈现结果

所有轮次结束后，计算分数并呈现结果。

**计分规则：**
- 每答对一题 = 1 分
- 总分可能 = 10 分

**评级标准：**
- 9-10：已精通 — 理解优秀
- 7-8：熟练 — 掌握良好，有小差距
- 5-6：发展中 — 已理解基础，需要复习
- 3-4：入门 — 存在显著差距，建议复习
- 0-2：未入门 — 从本课程开头开始

**输出格式：**

```markdown
## 课时测验结果：[课程名称]

**得分：N/10** — [评级]
**测验时机**：[课前 / 课中 / 课后] 的课程
**题目分类**：N 道概念题正确，N 道实践题正确

### 逐题结果

| # | 类别 | 问题（简述）| 你的回答 | 结果 |
|---|------|-----------|---------|------|
| 1 | 概念 | [缩写的问题] | [你的回答] | [正确 / 错误] |
| 2 | 实践 | ... | ... | ... |
| ... | ... | ... | ... |

### 错误答案 —— 复习这些内容

[对于每道错误答案，显示：]

**Q[N]：[完整问题文本]**
- 你的回答：[你选择的选项]
- 正确答案：[正确选项]
- 解析：[为什么它是正确的]
- 复习建议：[课程 README 中需重读的具体章节]

### [针对时机的消息]

[如果是课前]：
**预测试得分：N/10。** 这为你建立了基线！将学习重点放在你错过的主题上。完成课程后重新测验以衡量进步。

[如果是课中]：
**进度检查：N/10。** [若 7+ 分：进展顺利——继续保持！若 4-6 分：在继续之前复习错误主题。若 <4 分：考虑从头重读。]

[如果是课后]：
**掌握验证：N/10。** [若 9-10 分：你已精通此课程！进入下一课。若 7-8 分：接近了——复习遗漏主题后重新测验。若 <7 分：花更多时间在此课程上，特别是上面标记的部分。]

### 推荐后续步骤

[基于分数和时机]：
- [若已精通]：进入路线图中的下一课：[下一课链接]
- [若熟练]：复习以下具体部分，然后重新测验：[列出章节]
- [若发展中或更低]：完整重读课程：[课程链接]。重点关注：[列出薄弱类别]
- [可选]："你想重新做这道测验、换一门课测验，还是就某个具体主题获取帮助？"
```

### 步骤 6：提供后续选项

呈现结果后，使用 AskUserQuestion：

"你想接下来做什么？"
选项：
1. "重新做这道测验" — 再做一次同一门课的测验
2. "换一门课测验" — 切换到不同课程
3. "解释我错过的某个主题" — 获取某道错误答案的详细解释
4. "结束" — 结束本次测验会话

如果选 **重新做**：返回步骤 4（跳过时机问题，使用相同时机）。
如果选 **换课测验**：返回步骤 1。
如果选 **解释主题**：询问哪道题号，然后从课程 README.md 中阅读相关章节并用示例解释。

## 错误处理

### 无效的课程参数
如果参数不匹配任何课程，展示有效课程列表并让用户选择。

### 用户中途想退出
如果用户在任何一轮表示想停止，则为已回答的问题呈现部分结果。

### 找不到课程 README
如果在预期路径找不到 README.md 文件，通知用户并建议检查仓库结构。

## 验证

### 触发测试套件

**应该触发：**
- "quiz me on hooks"
- "lesson quiz"
- "test my knowledge of lesson 3"
- "practice quiz for MCP"
- "do I understand skills"
- "quiz me on slash commands"
- "lesson-quiz 06"
- "test me on checkpoints"
- "how well do I know the CLI"
- "quiz me before I start the memory lesson"

**不应触发：**
- "assess my overall level"（使用 /self-assessment）
- "explain hooks to me"
- "create a hook"
- "what is MCP"
- "review my code"
