# CLAUDE.md

## 目标

这是一个**文档优先**的仓库，不是应用程序仓库。AI 维护时的主要任务通常是：

- 更新教程和参考文档
- 保持根目录内容与 `claude-howto-zh/` 镜像一致
- 修复版本号、统计信息、链接和示例漂移
- 维护路线图、任务文档和翻译维护说明

默认不要把它当作需要“构建 / 运行 / 发布二进制”的项目。

翻译对象仓库是：

- `https://github.com/luongnv89/claude-howto`

维护这个 fork 时，GitHub 上应尽量保持与该上游仓库**结构一致、文件集合一致**；差异主要在于中文本地化内容，而不是任意删减文件类型。

## 真实信息优先级

当多个地方的信息冲突时，按这个优先级判断：

1. **文件系统当前状态**：`git status`、`find`、`rg`、实际文件内容
2. **根目录主文档和模块文档**
3. **`claude-howto-zh/` 镜像目录**
4. **计划型文档**：`docs/ROADMAP-20260401.md`、`docs/TASKS-20260401.md`
5. **静态统计说明**：`TRANSLATION-STATUS.md` 中的数字、人工汇总表

如果根目录和 `claude-howto-zh/` 冲突，默认先把**根目录**视为当前主工作区，再决定是否同步镜像。

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
- `TRANSLATION-STATUS.md`：面向 AI 的翻译维护手册

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

### 中文镜像层

- `claude-howto-zh/`：镜像目录，结构上大体对应主仓库内容
- 它不是本地工具目录；它是**需要维护的一部分内容**
- 当任务涉及“同步翻译版 / 镜像版”时，重点检查这里
- GitHub 发布时，默认目标是让它与上游仓库在结构上保持一致

### 本地维护工具层

这些目录默认视为**本地资产**，不作为 GitHub 发布内容：

- `scripts/`
- `reference/`

注意：

- 根目录 `scripts/` 是本地维护工具目录
- `claude-howto-zh/` 内凡是上游仓库对应目录中存在的文件，默认都属于镜像内容，应纳入发布范围
- 不要把上游仓库里的脚本、配置、资源、模板误判成“本地私有工具”

## 维护关系

### 1. 根目录是主工作区

大多数内容修订应先发生在根目录：

- 主文档修订
- 模块 README 修订
- 路线图和任务文档修订
- 版本号和统计口径修订

### 2. `claude-howto-zh/` 是镜像层

当根目录文档或模块发生会影响发布内容的变更时，检查是否需要同步到：

- `claude-howto-zh/README.md`
- `claude-howto-zh/QUICK_REFERENCE.md`
- `claude-howto-zh/CHANGELOG.md`
- `claude-howto-zh/RELEASE_NOTES.md`
- `claude-howto-zh/.version`
- 对应模块目录

### 3. 计划文档描述“想做什么”，不一定代表“已经做了”

以下文件常用于说明目标状态，但可能落后于实际仓库：

- `docs/ROADMAP-20260401.md`
- `docs/TASKS-20260401.md`

在执行计划前，必须先核对实际文件是否存在。

### 4. 翻译维护手册描述“如何维护镜像”

- `TRANSLATION-STATUS.md` 用于指导 AI 维护 `claude-howto-zh/`
- 它是维护说明，不是绝对真相来源
- 若文件数、版本号、路径与仓库不一致，以当前仓库为准并及时回写

## 常见维护任务

### 内容修订

适用于教程、示例、FAQ、安装说明更新。

建议顺序：

1. 修改根目录对应文件
2. 搜索是否存在镜像副本
3. 同步 `claude-howto-zh/` 中对应文件
4. 检查交叉引用和版本描述

### 版本同步

这是最容易漂移的任务。改版本时重点检查：

- `README.md`
- `CHANGELOG.md`
- `RELEASE_NOTES.md`
- `QUICK_REFERENCE.md`
- `TRANSLATION-STATUS.md`
- `claude-howto-zh/README.md`
- `claude-howto-zh/CHANGELOG.md`
- `claude-howto-zh/RELEASE_NOTES.md`
- `claude-howto-zh/.version`

版本同步时，不要只改 badge；还要检查 FAQ、统计区块、页脚和“当前版本”文案。

### 镜像同步

当根目录和 `claude-howto-zh/` 出现不一致时：

1. 先确认当前主工作区改动是否已完成
2. 再同步镜像目录
3. 最后更新 `TRANSLATION-STATUS.md` 中必要的说明

### 本地维护工具

默认规则：

- 可以使用 `scripts/update_translation.sh` 这类本地工具辅助分析
- 但不要把本地工具目录里的内容当作必须提交的项目产物
- 若用户没有明确要求，不要尝试把本地维护工具整理为 GitHub 发布内容
- 若某个文件在上游仓库存在对应路径，则默认应在 `claude-howto-zh/` 中保留对应镜像

## 操作前检查

开始任何较大修改前，先做这几步：

1. `git status --short`
2. `rg -n "当前版本|最后更新|最新：" README.md CHANGELOG.md RELEASE_NOTES.md QUICK_REFERENCE.md TRANSLATION-STATUS.md claude-howto-zh/README.md claude-howto-zh/CHANGELOG.md claude-howto-zh/RELEASE_NOTES.md`
3. 如果任务涉及镜像，同步检查 `claude-howto-zh/` 对应文件是否存在

## 操作后检查

完成后至少做：

1. `git diff --stat`
2. 针对改动文件做一次 `rg` 复查，确认没有遗留旧版本号、旧术语或失效路径
3. 如果动了本地维护脚本，执行相应的最小校验，例如：
   - `bash -n scripts/update_translation.sh`

## 不要做的事

- 不要把根目录 `scripts/` 默认当作要上传 GitHub 的正式内容
- 不要因为“看起来像代码”就删除 `claude-howto-zh/` 中上游对应的 `.py`、`.sh`、`.js`、`.json`、`.txt`、资源文件
- 不要仅凭 `docs/ROADMAP-20260401.md` 判断某个功能已经存在
- 不要在未核对镜像目录前，假设根目录和 `claude-howto-zh/` 已经同步
- 不要把模块内示例脚本误删为“私人工具”

## 维护目标

未来 AI 维护这个仓库时，应优先追求这四点：

1. **结构清晰**：入口文档、模块内容、镜像层、工具层边界明确
2. **版本一致**：同一版本号不要在不同文件里冲突
3. **镜像可维护**：根目录与 `claude-howto-zh/` 的同步路径清楚
4. **与上游同构**：GitHub 上的翻译仓库应尽量与上游仓库保持相同结构；只有本地维护工具不上云
