# 翻译维护手册（面向 AI） (Translation Maintenance Guide)

> **项目**: claude-howto 中文翻译版
> **原始仓库**: https://github.com/luongnv89/claude-howto
> **GitHub 地址**: https://github.com/Rx782-Fss/claude-howto-zh
> **维护对象**: 根目录中文翻译文档（单目录模式）
> **维护边界**: 只操作本仓库根目录；不要同步任何仓库外文档目录
> **最后整理**: 2026-05-01
> **当前版本标记**: 以 `.version` 文件为准
> **当前文件数**: 以仓库内实时统计为准

---

## 一、适用范围

- 本文档写给未来的 AI 维护代理。
- 若本文档中的静态数字与仓库当前状态冲突，**以文件系统、`git status` 和脚本输出为准**。
- 所有路径默认相对于仓库根目录。
- 维护任务只包括：
  - 翻译和修正根目录下的文档
  - 修正文档中的链接和版本标记
  - 保持翻译内容与上游原版结构一致（仅限核心文件）
- 维护任务**不包括**：
  - 操作任何外部知识库或仓库外文档目录
  - 将本仓库内容导出到仓库外的文档系统
  - 重建已删除的 `claude-howto-zh/` 镜像目录
- 目录约定：
  - 根目录即为工作区，所有翻译内容在此维护
  - `scripts/` 视为**本地维护工具目录**，默认不上传 GitHub
  - `reference/` 为本地参考资料，不上传 GitHub
  - `translator.py` 为本地开发工具，已在 .gitignore 排除

---

## 二、目录位置

> **所有路径均为相对于项目根目录（仓库根目录）的相对路径。**

| 项目 | 相对路径 | 说明 |
|------|---------|------|
| **项目根目录** | `./` | 即仓库根目录 |
| **翻译输出** | `./` | 中文翻译直接在根目录 |
| **版本标记** | `./.version` | 当前对应的原版 tag |
| **本地脚本** | `./scripts/` | 本地维护脚本；默认不上传 GitHub |
| **参考资料** | `./reference/` | 本地参考文档；默认不上传 GitHub |

---

## 三、AI 执行原则

1. **先读取，再修改**：先运行 `git status`、`rg`、`find`，不要凭记忆操作。
2. **只在仓库内行动**：不要假设存在外部文档系统或镜像目录。
3. **以增量更新为主**：优先翻译变化部分，避免不必要的整篇重写。
4. **保留结构稳定性**：目录层级、文件名、代码块和链接结构应与上游保持一致。
5. **修改后自检**：至少检查 `git diff --stat` 和相关 `rg` 搜索结果。

---

## 四、翻译规范（必须严格遵守）

### 4.1 翻译范围

- **翻译内容**：教程/文档的正文、说明文字、注释、描述
- **不翻译内容**：
  - 代码逻辑（Python 函数体、Shell 命令本体、JavaScript 逻辑）
  - 文件名、目录名、变量名、函数名、API 名称
  - JSON 的 key 名（但 `description` / `comment` 等 value 要翻译）
  - Mermaid 图表的代码块语法关键字（`graph TD`、`flowchart` 等）
  - URL 链接、版本号、技术标识符

### 4.2 术语规则

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

### 4.3 各文件类型的具体处理方式

#### Markdown (.md) 文件
- 标题、正文、列表、表格内容 → **全部翻译**
- 代码块内的注释（`#` 或 `//` 开头）→ **翻译**
- Mermaid 图表中的文本标签 → **翻译**
- 代码块中的代码逻辑 → **不翻译**
- `> 💡` 提示框 → **翻译并保留格式**

#### Python (.py) 文件
- docstring（`"""..."""`）→ **翻译**
- 行内注释（`# ...`）→ **翻译**
- 代码逻辑 → **不翻译**
- 变量名/函数名 → **不翻译**

#### Shell (.sh) 脚本
- 注释行（`# ...`）→ **翻译**
- echo/print 的提示信息 → **翻译**
- 命令逻辑 → **不翻译**

#### JSON/YAML 配置文件
- `description`、`comment`、`name` 等 value → **翻译**
- key 名 → **不翻译**
- 配置值（URL、版本号等）→ **不翻译**

---

## 五、版本管理

### 5.1 版本号标记

- 当前版本号存储在 `.version` 文件中
- 格式：`vX.Y.Z`（例如 `v2.3.2`）
- 对应上游仓库的 tag 版本

### 5.2 版本同步检查清单

修改版本号时，必须同时更新以下文件：

```bash
# 1. 检查当前版本
cat .version

# 2. 更新 .version
echo "vX.Y.Z" > .version

# 3. 搜索需要更新的位置
rg -n "当前版本|最后更新|最新|v[0-9]+\.[0-9]+" README.md CHANGELOG.md RELEASE_NOTES.md QUICK_REFERENCE.md

# 4. 更新 README.md 中的 badge
# 5. 更新 CHANGELOG.md 添加新条目
# 6. 更新 RELEASE_NOTES.md
```

### 5.3 常见版本号位置

| 文件 | 位置 | 格式示例 |
|------|------|----------|
| `.version` | 文件内容 | `v2.3.2` |
| `README.md` | Badge URL | `badge/v2.3.2` |
| `README.md` | 页脚 | `Version 2.1.119` |
| `CHANGELOG.md` | 标题 | `## v2.3.2` |
| `RELEASE_NOTES.md` | 标题 | `## v2.3.2` |

---

## 六、质量检查

### 6.1 翻译完成后自检

完成任何翻译任务后，执行以下检查：

```bash
# 1. 检查文件变更统计
git diff --stat

# 2. 搜索可能的遗留英文（排除代码块）
rg -n "[A-Z]{3,}" <translated-file>.md | head -20

# 3. 检查链接有效性
rg -n "\[.*\]\(.*\)" <translated-file>.md | head -20

# 4. 统计中文占比
python3 -c "
import re
with open('<translated-file>.md', 'r') as f:
    content = f.read()
cn = len(re.findall(r'[\u4e00-\u9fff]', content))
total = len(content)
print(f'中文占比: {cn/total*100:.1f}%')
"
```

### 6.2 翻译质量标准

| 文档类型 | 中文占比目标 | 说明 |
|----------|------------|------|
| 纯理论文档 | 30-50% | 如 08-checkpoints, LEARNING-ROADMAP |
| 平衡型文档 | 15-25% | 如 02-memory, 04-subagents |
| 代码密集型 | 10-18% | 如 06-hooks, 07-plugins |
| 配置参考 | 8-15% | 如 05-mcp, 10-cli |

> 注：代码块保留英文是正确做法，低占比不代表翻译不全。

### 6.3 常见问题排查

#### 问题 1：翻译后格式错乱

**原因**：Markdown 语法被误改  
**解决**：检查代码块围栏、表格对齐、列表缩进

#### 问题 2：链接失效

**原因**：路径未更新或使用了旧镜像路径  
**解决**：将 `claude-howto-zh/xxx` 改为 `xxx`（根目录相对路径）

#### 问题 3：版本号不一致

**原因**：漏更新某个文件  
**解决**：使用上述"版本同步检查清单"

---

## 七、上游同步流程

当上游仓库 (`luongnv89/claude-howto`) 有更新时：

### 7.1 同步步骤

```bash
# 1. 获取上游更新
git fetch upstream

# 2. 查看上游新增了什么
git log HEAD..upstream/main --oneline

# 3. 查看具体文件变更
git diff HEAD..upstream/main --stat

# 4. 选择性合并核心文件（忽略其他语言版本）
# 只关注根目录下的 10 个模块 + 辅助文档

# 5. 翻译新增或修改的内容

# 6. 更新版本号
echo "vX.Y.Z" > .version

# 7. 提交并推送
git add .
git commit -m "sync: 上游 vX.Y.Z 更新翻译"
git push origin main
```

### 7.2 应该同步的内容

✅ **需要同步：**
- 10 个模块的 README.md 更新
- 新增的核心功能文档
- 重要配置文件变更
- 安全修复相关文档

❌ **不需要同步：**
- `ja/`, `uk/`, `vi/`, `zh/` 其他语言版本
- `scripts/` 构建工具
- `slides/` 幻灯片 PDF
- `.github/workflows/` CI/CD 配置
- 测试文件和覆盖率报告

---

## 八、发布流程

### 8.1 创建新版本

```bash
# 1. 完成所有翻译和质量检查

# 2. 更新版本号
echo "vX.Y.Z" > .version

# 3. 更新 RELEASE_NOTES.md

# 4. 提交所有更改
git add .
git commit -m "feat: vX.Y.Z 翻译更新"

# 5. 创建 Git 标签
git tag -a vX.Y.Z -m "vX.Y.Z: 版本说明"

# 6. 推送代码和标签
git push origin main --tags

# 7. 创建 GitHub Release（通过 API 或网页界面）
```

### 8.2 Release 描述模板

参见 `RELEASE_NOTES.md` 或使用 `/tmp/release-body.md` 模板。

---

## 九、项目特色说明

本项目采用**单目录精简模式**，不同于传统的镜像模式：

### 9.1 与旧版镜像模式的区别

| 方面 | 旧模式（已废弃） | 当前模式 ✅ |
|------|----------------|-----------|
| 工作区 | 根目录 + `claude-howto-zh/` 镜像 | 仅根目录 |
| 维护复杂度 | 高（需同步两份） | 低（单一份） |
| 仓库大小 | ~23MB | ~21MB |
| 文件数量 | ~260+ | ~160 |
| 易用性 | 用户困惑用哪个目录 | 清晰明确 |

### 9.2 为什么删除镜像目录

- 冗余：与根目录 100% 重复
- 混淆：用户不知道应该用哪个
- 维护负担：每次要同步两份
- 不在上游：官方仓库无此结构

---

## 十、快速参考

### 常用命令速查

```bash
# 查看仓库状态
git status --short

# 统计文件数
find . -type f ! -path './.git/*' | wc -l

# 查找特定内容
rg -n "关键词" *.md

# 检查版本一致性
rg -n "v[0-9]+\.[0-9]+" .version README.md CHANGELOG.md RELEASE_NOTES.md

# 检查中文翻译质量
python3 << 'EOF'
import re, os
for f in ['README.md', 'CHANGELOG.md']:
    if os.path.exists(f):
        with open(f) as fh:
            c = fh.read()
        cn = len(re.findall(r'[\u4e00-\u9fff]', c))
        print(f"{f}: {cn/len(c)*100:.1f}% 中文")
EOF
```

---

**最后更新**: 2026-05-01
**适用版本**: v2.3.2+
**维护者**: AI Agent + 人工审核
