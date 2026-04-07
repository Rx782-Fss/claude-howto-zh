# 翻译项目交接文档 (Translation Handoff)

> **项目**: claude-howto 中文翻译版
> **原始仓库**: https://github.com/luongnv89/claude-howto (5900+ stars)
> **翻译完成时间**: 2026-04-05
> **当前版本**: v2.2.0
> **翻译文件数**: 152 个（全部完成） | **OB 手册**: 150 个文件
> **状态**: ✅ 全量翻译已完成 + OB 手册已生成，等待后续版本更新

---

## 一、目录位置

> **所有路径均为相对于项目根目录 (`tre/`) 的相对路径。项目可自由挪动，不影响使用。**

| 项目 | 相对路径 | 说明 |
|------|---------|------|
| **项目根目录** | `./` | 即 `tre/` 所在位置 |
| **翻译输出** | `./claude-howto-zh/` | 152 个中文翻译文件 |
| **更新脚本** | `./scripts/update_translation.sh` | 一键检测+对比脚本 |
| **版本标记** | `./claude-howto-zh/.version` | 当前对应的原版 tag |
| **OB 知识库手册** | `$HOME/data/知识库/40_学习资料/Claude Howto` | Obsidian 手册（外部路径，通过环境变量 `OB_VAULT_PATH` 可配置） |
| **源码临时目录** | `/tmp/claude-howto-src/` | 下载的原版源码（系统临时） |

> 源码位于 `/tmp/` 下，系统重启后可能丢失。运行 `./scripts/update_translation.sh fetch` 可重新下载。

---

## 二、翻译规范（必须严格遵守）

### 2.1 翻译范围

- **翻译内容**：教程/文档的正文、说明文字、注释、描述
- **不翻译内容**：
  - 代码逻辑（Python 函数体、Shell 命令本体、JavaScript 逻辑）
  - 文件名、目录名、变量名、函数名、API 名称
  - JSON 的 key 名（但 `description` / `comment` 等 value 要翻译）
  - Mermaid 图表的代码块语法关键字（`graph TD`、`flowchart` 等）
  - URL 链接、版本号、技术标识符

### 2.2 术语规则

- **专业术语首次出现时**：保留英文 + 中文注释，例如：`Slash Commands（斜杠命令）`
- **后续出现**：可直接使用中文或英文，保持上下文一致
- **常见术语对照表**：

| 英文 | 中文 |
|------|------|
| Slash Commands | 斜杠命令 |
| Memory / CLAUDE.md | 记忆 / CLAUDE.md 文件 |
| Skills | 技能 |
| Subagents | 子代理 |
| MCP (Model Context Protocol) | 模型上下文协议 |
| Hooks | 钩子 |
| Plugins | 插件 |
| Checkpoints | 检查点 |
| Permission Modes | 权限模式 |
| LSP | 语言服务器协议 |

### 2.3 各文件类型的具体处理方式

#### Markdown (.md) 文件
- 标题、正文、列表、表格内容 → **全部翻译**
- 代码块内的注释（`#` 或 `//` 开头）→ **翻译**
- Mermaid 图表中的文本标签 → **翻译**
- 代码块中的代码逻辑 → **不翻译**
- `> 💡` 提示框 → **翻译并保留格式**

#### Python (.py) 文件
- docstring（`"""..."""`）→ **翻译**
- 行内注释（`# ...`）→ **翻译**
- 函数/变量/类名 → **不翻译**
- 代码逻辑 → **不翻译**
- print/log 字符串中面向用户的提示信息 → **可翻译**

#### Shell (.sh) 文件
- `#` 注释行 → **翻译**
- echo/print 中面向用户的字符串 → **可翻译**
- 命令本身 → **不翻译**

#### JavaScript (.js) 文件
- `//` 注释 → **翻译**
- `/* */` 注释 → **翻译**
- console.log 中面向用户的信息 → **可翻译**
- 代码逻辑 → **不翻译**

#### JSON (.json) / YAML (.yml) 文件
- `description`、`comment`、`title` 等 value → **翻译**
- key 名、配置值、布尔值 → **不翻译**

#### 纯文本 (.txt) 文件
- 模板内容、说明文字 → **按上下文判断是否翻译**

---

## 三、已翻译文件完整清单

### 3.1 按模块统计

| # | 模块 | 目录 | 文件数 | 状态 |
|---|------|------|--------|------|
| 1 | Slash Commands | `01-slash-commands/` | 9 | ✅ 完成 |
| 2 | Memory | `02-memory/` | 6 | ✅ 完成 |
| 3 | Skills | `03-skills/` | 22 | ✅ 完成 |
| 4 | Subagents | `04-subagents/` | 9 | ✅ 完成 |
| 5 | MCP | `05-mcp/` | 5 | ✅ 完成 |
| 6 | Hooks | `06-hooks/` | 9 | ✅ 完成 |
| 7 | Plugins | `07-plugins/` | 40 | ✅ 完成 |
| 8 | Checkpoints | `08-checkpoints/` | 2 | ✅ 完成 |
| 9 | Advanced Features | `09-advanced-features/` | 4 | ✅ 完成 |
| 10 | CLI Reference | `10-cli/` | 1 | ✅ 完成 |
| 11 | .claude/skills/ | `.claude/skills/` | 5 | ✅ 完成 |
| 12 | .github/ | `.github/` | 8 | ✅ 完成 |
| 13 | docs/ | `docs/` | 2 | ✅ 完成 |
| 14 | resources/ | `resources/` | 14 | ✅ 完成 |
| 15 | prompts/ | `prompts/` | 1 | ✅ 完成 |
| 16 | scripts/ | `scripts/` | 1 | ✅ 完成 |
| 17 | 根目录文档 | `(root)` | 16 | ✅ 完成 |
| | **合计** | | **152** | **✅ 100%** |

### 3.2 已排除的内容（不需要翻译）

| 内容 | 原因 |
|------|------|
| `slides/*.pdf` | PDF 幻灯片，非文本内容 |
| `.gitignore`, `.cspell.json`, `.markdownlint.json` | 开发工具配置文件 |
| `.pre-commit-config.yaml` | Git 预提交钩子配置 |
| `LICENSE` | 许可证文件，通常不翻译 |
| `coverage.xml` | 测试覆盖率报告 |
| `pyproject.toml`, `requirements*.txt` | Python 项目依赖配置 |
| `scripts/build_epub.py`, `scripts/check_*.py` | 构建和检查脚本（仅保留了 README.md 翻译） |
| `scripts/tests/` | 测试代码 |
| `.github/workflows/*.yml` | CI/CD 工作流配置 |
| `.github/FUNDING.yml` | 资助配置 |
| `.github/markdown-link-check-config.json` | 链接检查配置 |
| `assets/logo/` | V2 版旧 Logo（已被 V3 替代） |
| 图片文件 (*.png, *.svg) | 二进制资源文件（原样保留） |
| `03-skills/.gitignore` | 技能模块内部 gitignore |

---

## 四、后续更新操作手册（给未来 AI 的完整工作流）

### 4.1 工具链

| 工具 | 路径 | 用途 |
|------|------|------|
| **更新脚本** | `./scripts/update_translation.sh` | 检测版本、下载源码、对比差异 |
| **翻译项目** | `./claude-howto-zh` | 中文翻译主目录 |
| **OB 手册** | `/home/hhbbfss/data/知识库/40_学习资料/Claude Howto` | Obsidian 知识库副本 |
| **版本标记** | `claude-howto-zh/.version` | 记录当前翻译对应的原版 tag |

### 4.2 一键更新流程

```bash
# 完整流程：检查 → 下载 → 对比
./scripts/update_translation.sh full

# 或分步执行：
./scripts/update_translation.sh check   # 仅检查新版本
./scripts/update_translation.sh fetch    # 下载最新源码
./scripts/update_translation.sh diff     # 生成差异报告
```

### 4.3 更新操作步骤（完整 SOP）

当 `update_translation.sh check` 报告有新版本时，按以下顺序执行：

#### Step 1 — 运行差异检测

```bash
./scripts/update_translation.sh full
```

输出会告诉你：
- 📁 **新增文件** → 需要全新翻译的文件列表
- ✏️ **修改文件** → 需要增量更新的文件列表 + diff 统计
- 🗑️ **删除文件** → 需要从翻译版中清理的文件

#### Step 2 — 处理新增文件

对每个新增文件：
1. 阅读英文原文，理解内容
2. 按照「二、翻译规范」进行翻译
3. 放入 `claude-howto-zh/` 对应目录
4. 勾选质量检查清单（4.5 节）

#### Step 3 — 处理修改文件

对每个修改文件：
1. 执行 `diff <源文件> <翻译文件>` 查看具体变更
2. 仅翻译**新增或变更的部分**
3. 保持已有翻译不变
4. 如果变更量大（>30%），考虑全文重新翻译

#### Step 4 — 清理删除文件

从 `claude-howto-zh/` 中删除已不存在的文件。

#### Step 5 — 同步到 OB 知识库

翻译完成后，将变更同步到 Obsidian 手册：

```bash
# 方式 A：仅处理变更的文件（推荐）
# 对每个新增/修改/删除的文件，手动在 OB 目录下执行相同操作
# OB 目录结构: /home/hhbbfss/data/知识库/40_学习资料/Claude Howto/

# 方式 B：如果变更量很大，可以重新运行转换脚本（需先更新 convert_to_ob.py 的 FILE_MAP）
# 运行 OB 转换脚本（如需重新生成）
```

> ⚠️ OB 文件需要添加 frontmatter 和索引章节，不能直接复制。参考已有的 OB 文件格式。

#### Step 6 — 更新版本标记

```bash
echo "vX.Y.Z" > ./claude-howto-zh/.version
```

### 4.4 差异处理策略速查

| 差异类型 | 判定标准 | 操作 |
|----------|---------|------|
| **新增** | 源有、译版无 | 全新翻译 |
| **小改** | diff 变更 < 10 行 | 增量翻译变更部分 |
| **中改** | diff 变更 10-50 行 | 增量翻译 + 审查上下文连贯性 |
| **大改** | diff 变更 > 50 行 或 >30% | 全文重译 |
| **删除** | 译版有、源无 | 从两个位置都删除 |
| **重命名** | 文件路径变化 | 同步重命名 |

### 4.5 翻译质量检查清单

每个文件翻译完成后，确认以下要点：

- [ ] 专业术语首次出现有中文注释
- [ ] Mermaid 图表中的文本已翻译
- [ ] 代码块内注释已翻译（代码本身未动）
- [ ] JSON 的 description 字段已翻译
- [ ] `> 💡` 提示框格式保留且已翻译
- [ ] 文档结构（标题层级、列表、表格）与原文一致
- [ ] 无遗漏的英文段落
- [ ] 中文表达自然流畅
- [ ] OB 版本包含正确的 frontmatter（type/status/tags）
- [ ] OB 版本包含 `## 索引（点击跳转）` 章节

---

## 五、关键文件索引

| 文件 | 说明 | 重要程度 |
|------|------|----------|
| `README.md` | 项目主入口文档 | ⭐⭐⭐ |
| `INDEX.md` | 完整文件索引（~500行） | ⭐⭐⭐ |
| `QUICK_REFERENCE.md` | 快速参考卡（~506行） | ⭐⭐⭐ |
| `CATALOG.md` | 学习目录 | ⭐⭐⭐ |
| `LEARNING-ROADMAP.md` | 学习路线图 | ⭐⭐⭐ |
| `CHANGELOG.md` | 版本更新日志 | ⭐⭐ |
| `07-plugins/README.md` | 插件架构总览（943行，最大单文件） | ⭐⭐⭐ |
| `.claude/skills/self-assessment/SKILL.md` | 自我评估技能定义 | ⭐⭐ |
| `.claude/skills/lesson-quiz/SKILL.md` | 课程测验技能定义 | ⭐⭐ |

---

## 六、注意事项

1. **不要重复翻译已有文件**：本项目的 152 个文件已全部翻译完成。更新时只处理**差异部分**。
2. **保留原文结构**：目录层次、文件命名、Markdown 格式必须与源项目一致。
3. **图片资源**：所有 `.png` 和 `.svg` 文件从原样复制，不做任何修改。
4. **二进制文件排除**：`slides/` 目录下的 PDF 不在翻译范围内。
5. **一致性**：同一术语在整个项目中应保持一致的翻译。

---

*本文档由 AI 翻译助手生成于 2026-04-05，用于跨会话交接。*
