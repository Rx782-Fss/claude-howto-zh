# CLAUDE.md

## 目标

这是一个**文档优先**的仓库，不是应用程序仓库。AI 维护时的主要任务通常是：

- 更新教程和参考文档
- 修复版本号、统计信息、链接和示例漂移
- 维护路线图、任务文档和翻译说明
- 保持文档质量和技术准确性

默认不要把它当作需要"构建 / 运行 / 发布二进制"的项目。

翻译对象仓库是：

- `https://github.com/luongnv89/claude-howto`

维护这个 fork 时，GitHub 上应保持**精简高效的中文版仓库结构**；差异主要在于：
1. 只保留中文翻译内容（根目录）
2. 删除其他语言版本（ja/uk/vi/zh旧版）
3. 删除非核心文件（构建工具、幻灯片等）
4. 保留上游仓库的核心功能文件（.claude/skills/ 等）

## 真实信息优先级

当多个地方的信息冲突时，按这个优先级判断：

1. **文件系统当前状态**：`git status`、`find`、`rg`、实际文件内容
2. **根目录主文档和模块文档**
3. **计划型文档**：`docs/ROADMAP-20260401.md`、`docs/TASKS-20260401.md`
4. **静态统计说明**：版本号、人工汇总表

## 仓库地图

### 根目录入口文档

这些文件决定仓库对外如何被理解，改动影响最大：

- `README.md`：主入口和落地页
- `INDEX.md`：全量索引
- `CATALOG.md`：功能目录
- `QUICK_REFERENCE.md`：速查卡
- `LEARNING-ROADMAP.md`：学习路径
- `CHANGELOG.md`：变更历史
- `RELEASE_NOTES.md`：版本说明
- `.version`：当前版本号标记

### 10 个主模块

按编号组织 Claude Code 能力：

- `01-slash-commands/`
- `02-memory/`
- `03-skills/`
- `04-subagents/`
- `05-mcp/`
- `06-hooks/`
- `07-plugins/`
- `08-checkpoints/`
- `09-advanced-features/`
- `10-cli/`

每个模块默认由 `README.md` 作为主文档，目录内其他文件是示例、模板、脚本或子主题。

### 支撑内容

- `resources/`：图标、logo、设计系统和资源索引
- `prompts/`：额外提示词素材
- `docs/`：路线图、任务规划等维护文档
- `.github/`：模板和项目协作文档
- `.claude/skills/`：交互式学习技能（lesson-quiz, self-assessment）

### 本地维护工具层

这些目录默认视为**本地资产**，不作为 GitHub 发布内容：

- `scripts/`
- `reference/`
- `translator.py`

注意：

- 根目录 `scripts/` 是本地维护工具目录
- 不要把本地工具目录里的内容当作必须提交的项目产物
- 若用户没有明确要求，不要尝试把本地维护工具整理为 GitHub 发布内容

## 维护关系

### 1. 根目录是唯一工作区

所有内容修订都发生在根目录：

- 主文档修订
- 模块 README 修订
- 路线图和任务文档修订
- 版本号和统计口径修订

**不再存在镜像同步机制** - 所有内容都在根目录维护。

### 2. 计划文档描述"想做什么"，不一定代表"已经做了"

以下文件常用于说明目标状态，但可能落后于实际仓库：

- `docs/ROADMAP-20260401.md`
- `docs/TASKS-20260401.md`

在执行计划前，必须先核对实际文件是否存在。

### 3. 翻译状态追踪

- `TRANSLATION-STATUS.md` 用于记录翻译进度和维护说明
- 它是参考文档，不是绝对真相来源
- 若文件数、版本号、路径与仓库不一致，以当前仓库为准并及时回写

## 常见维护任务

### 版本发布（完整工作流）

当需要发布新版本时，按以下标准流程执行：

#### 1️⃣ 准备阶段

```bash
# 1. 更新 RELEASE_NOTES.md（添加新版本条目）
#    - 标题格式：## vX.Y.Z - YYYY-MM-DD
#    - 内容包含：核心成果、详细变更、质量指标、升级方式

# 2. 更新 .version 文件
echo "vX.Y.Z" > .version
```

**版本号规范参考：`RELEASE-GUIDELINES.md`**

#### 2️⃣ 使用发布脚本

```bash
# 标准发布（自动完成所有步骤）
./scripts/release.sh v2.4.0
```

脚本会自动执行：
- ✅ 运行 pre-flight checks (release-check.sh)
- ✅ 更新 .version 文件
- ✅ 提交更改到 Git
- ✅ 创建 Git Tag (message: "Release vX.Y.Z")
- ✅ 推送到 GitHub
- ✅ 创建 GitHub Release (title: "Release vX.Y.Z")

#### 3️⃣ 如果需要重建所有 Releases

```bash
# 需要提供 GitHub Personal Access Token
./scripts/rebuild-releases.sh <GITHUB_TOKEN>
```

⚠️ **重要提示：**
- 脚本按 `v2.0.0 → v2.3.2` 顺序创建（先旧后新）
- 确保 v2.3.2 最后创建，才能被标记为 "Latest"
- Token 权限需要：`repo` (Full control)

#### 📌 发布检查清单

发布前必须确认：
- [ ] RELEASE_NOTES.md 已添加新版本条目
- [ ] .version 文件已更新
- [ ] 所有文档中的版本号一致
- [ ] 没有本地维护文件被误提交（scripts/, prompts/, .gitignore 等）

---

### 内容修订

适用于教程、示例、FAQ、安装说明更新。

建议顺序：

1. 修改根目录对应文件
2. 检查交叉引用和版本描述
3. 更新版本号标记（`.version` 文件）

### 版本同步

这是最容易漂移的任务。改版本时重点检查：

- `README.md`
- `CHANGELOG.md`
- `RELEASE_NOTES.md`
- `QUICK_REFERENCE.md`
- `.version`

版本同步时，不要只改 badge；还要检查 FAQ、统计区块、页脚和"当前版本"文案。

### 本地维护工具

默认规则：

- 可以使用 `translator.py` 或其他本地工具辅助分析
- 但不要把本地工具目录里的内容当作必须提交的项目产物
- 若用户没有明确要求，不要尝试把本地维护工具整理为 GitHub 发布内容

## 操作前检查

开始任何较大修改前，先做这几步：

1. `git status --short`
2. `rg -n "当前版本|最后更新|最新：" README.md CHANGELOG.md RELEASE_NOTES.md QUICK_REFERENCE.md`
3. 检查 `.version` 文件确认当前版本号

## 操作后检查

完成后至少做：

1. `git diff --stat`
2. 针对改动文件做一次 `rg` 复查，确认没有遗留旧版本号、旧术语或失效路径
3. 如果动了本地维护脚本，执行相应的最小校验

## 不要做的事

- ❌ **不要把本地维护文件推送到 GitHub**（见下方完整清单）
- ❌ 不要尝试重建已删除的 `claude-howto-zh/` 镜像目录
- ❌ 不要仅凭 `docs/ROADMAP-20260401.md` 判断某个功能已经存在
- ❌ 不要把模块内示例脚本误删为"私人工具"
- ❌ 不要添加不必要的文件或目录到仓库
- ❌ 不要修改 .gitignore 后忘记 `git rm --cached` 已跟踪文件

---

## 📋 文件推送规则（重要！）

### ✅ 应该推送到 GitHub 的内容

| 类别 | 文件/目录 | 说明 |
|------|----------|------|
| **核心文档** | README.md, CHANGELOG.md, CATALOG.md 等 | 项目主文档 |
| **模块文档** | 01-slash-commands/ ~ 10-cli/ | 10 个核心模块 |
| **版本管理** | RELEASE_NOTES.md, RELEASE-GUIDELINES.md | 发布说明和规范 |
| **资源文件** | resources/, claude-howto-logo.* | 图标、logo |
| **GitHub 配置** | .github/ | Issue 模板、Workflows |
| **交互式技能** | .claude/skills/ | lesson-quiz, self-assessment |
| **许可证** | LICENSE, CODE_OF_CONDUCT.md 等 | 法律文件 |

### ❌ 不应该推送的内容（仅本地使用）

| 类别 | 文件/目录 | 原因 |
|------|----------|------|
| **维护脚本** | scripts/ (整个目录) | 本地发布工具 |
| **配置文件** | .gitignore | 本地忽略规则 |
| **AI 指南** | CLAUDE.md | 仅本地 AI 使用 |
| **翻译工具** | translator.py | 翻译引擎脚本 |
| **版本标记** | .version | 本地版本号 |
| **状态追踪** | TRANSLATION-STATUS.md | 翻译进度记录 |
| **规划文档** | docs/ROADMAP-*.md, docs/TASKS-*.md | 本地任务规划 |
| **Prompt 模板** | prompts/ (整个目录) | 提示词素材 |
| **参考数据** | reference/ | 生成的参考数据 |

**验证命令：**
```bash
# 检查是否有不应存在的文件被跟踪
git ls-files | grep -E '^scripts/|^\.gitignore|^CLAUDE\.md|^translator|^\.version|^TRANSLATION|^prompts/|^reference/'
# 如果有输出，说明需要清理！
```