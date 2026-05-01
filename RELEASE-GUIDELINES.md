# Release 版本管理规范 (Version Management Specification)

> **文档版本**: v1.0
> **创建日期**: 2026-05-01
> **适用范围**: claude-howto-zh 项目所有版本发布

---

## 一、版本号体系概述

本项目采用 **语义化版本号 (Semantic Versioning)** 规范，格式为：`v主版本.次版本.修订版`

### 1.1 版本号组成

```
vX.Y.Z
│ │ └── Z: 修订版 (Patch) - Bug修复、小改进
│ └──── Y: 次版本 (Minor) - 新功能、模块翻译完成
└─────── X: 主版本 (Major) - 架构变更、重大重构
```

### 1.2 版本号对应关系

| 版本组件 | 上游 Claude Code 版本 | 本项目含义 | 示例 |
|----------|---------------------|-----------|------|
| **X (主版本)** | 对应上游主版本 | 大版本同步 | `v2.x` |
| **Y (次版本)** | 翻译批次/里程碑 | 主要翻译更新 | `v2.3`, `v2.4` |
| **Z (修订版)** | 补丁/修复 | 小修复或补充 | `v2.3.0`, `v2.3.1` |

---

## 二、版本号命名规则

### 2.1 基本规则

✅ **正确示例**:
- `v2.3.0` - 标准格式（推荐）
- `v2.3.2` - 带补丁号
- `v3.0.0` - 主版本升级

❌ **错误示例**:
- `V2.3.0` ❌ （大写 V）
- `2.3.0` ❌ （缺少 v 前缀）
- `v2.3` ❌ （缺少修订号）

### 2.2 版本号递增规则

#### 主版本 (X) 递增条件：
- 上游仓库主版本升级（如 2.x → 3.x）
- 项目架构重大变更
- 完全重新翻译所有内容

#### 次版本 (Y) 递增条件：
- 完成 1 个或多个核心模块的完整翻译
- 新增重要功能或章节
- 大规模内容更新（>1000 行）

#### 修订版 (Z) 递增条件：
- 修正翻译错误或遗漏
- 小规模内容补充（<500 行）
- 更新配置文件或元数据
- 修复 README 或辅助文档

### 2.3 特殊版本标记

| 标记 | 格式 | 用途 |
|------|------|------|
| 正式版 | `vX.Y.Z` | 稳定发布版本 |
| 预发布 | `vX.Y.Z-alpha.N` | 内部测试版本 |
| 预发布 | `vX.Y.Z-beta.N` | 公开测试版本 |
| 里程碑 | `vX.Y.Z-rc.N` | 候选发布版本 |

---

## 三、三处版本号一致性要求

项目中存在 **3 个必须保持一致** 的版本号位置：

### 3.1 版本号位置清单

| # | 位置 | 文件路径 | 格式 | 用途 |
|---|------|---------|------|------|
| 1 | **版本标记文件** | `.version` | `vX.Y.Z` | AI 读取的当前版本 |
| 2 | **Git 标签** | Git Tag | `vX.Y.Z` | GitHub Release 关联 |
| 3 | **发布说明标题** | `RELEASE_NOTES.md` | `## vX.Y.Z` | 用户查看的版本 |

### 3.2 一致性检查命令

```bash
# 快速检查三者是否一致
VERSION=$(cat .version)
GIT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "无标签")
RELEASE_NOTE=$(head -1 RELEASE_NOTES.md | grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' || echo "未找到")

echo ".version:     $VERSION"
echo "Git Tag:      $GIT_TAG"
echo "RELEASE_NOTE: $RELEASE_NOTE"

# 检查是否一致
if [ "$VERSION" = "$GIT_TAG" ] && [ "$GIT_TAG" = "$RELEASE_NOTE" ]; then
    echo "✅ 三处版本号一致"
else
    echo "⚠️ 版本号不一致，需要修正！"
fi
```

---

## 四、Release 内容生成规范

### 4.1 RELEASE_NOTES.md 结构模板

每个版本的发布说明必须包含以下章节：

#### 必填章节：

1. **标题行**
   ```markdown
   ## vX.Y.Z - YYYY-MM-DD
   ```

2. **版本类型标识**
   选择合适的 emoji 和类型名称：
   - ✨ 功能更新 (Feature)
   - 🐛 问题修复 (Bugfix)
   - 🔧 维护更新 (Maintenance)
   - 📚 文档更新 (Documentation)

3. **核心成果摘要**（2-3 句话）

4. **详细变更列表**（按类别组织）

5. **质量指标表格**（必填）

6. **升级方式**（必填）

7. **已知问题**（如有则填写，无则省略）

#### 可选章节：

8. **破坏性变更**（如有）
9. **致谢**（可选）

### 4.2 质量指标模板

每次发布必须包含此表格：

```markdown
### 📊 质量指标

| 指标 | 数值 |
|------|------|
| 更新文件数 | **N 个** |
| 新增内容 | **+N 行** |
| 净增长 | **+N 行** |
| 平均中文占比 | **N%** |
| 代码块保留率 | **100%** |
```

### 4.3 升级方式模板

```markdown
### 🔄 升级方式

\`\`\`bash
git pull origin main
# 或
git fetch origin && git checkout vX.Y.Z
\`\`\`
```

---

## 五、GitHub Release 创建规范

### 5.1 Release 信息规范

| 字段 | 格式要求 | 示例 |
|------|----------|------|
| **Tag Name** | `vX.Y.Z` | `v2.3.2` |
| **Release Title** | `vX.Y.Z - 简短描述` | `v2.3.2 - 5大核心模块全文精细化翻译` |
| **Release Body** | 使用标准模板（见 5.2） | 见下方 |
| **Draft** | 正式版为 `false` | `false` |
| **Prerelease** | 正式版为 `false` | `false` |

### 5.2 GitHub Release Body 模板

```markdown
## ✨ vX.Y.Z - 简短描述

### 🎯 核心成果

简要描述本次更新的主要内容和价值（2-3 句话）。

### 📚 更新详情

#### 翻译完成的模块（如有）
- **模块名** (行数, 中文占比 ⭐⭐⭐ A+)
  - 核心特性列表

#### 新增/修改的文件（如有）
- **文件路径** (大小)
  - 功能描述

### 📊 质量指标

| 指标 | 数值 |
|------|------|
| 更新文件数 | **N 个** |
| 新增内容 | **+N 行** |
| ... | ... |

### 🔄 升级方式

\`\`\`bash
git pull origin main
\`\`\`

---
📖 [查看完整的 RELEASE_NOTES.md](RELEASE_NOTES.md) 了解详细变更日志。
```

---

## 六、发布流程检查清单

### 6.1 发布前检查（Pre-release Checklist）

```bash
#!/bin/bash
# release-check.sh - 发布前自动检查脚本

echo "=== Release 发布前检查 ==="
echo ""

# 1. 检查工作区是否干净
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ 错误：工作区有未提交的更改"
    git status --short
    exit 1
else
    echo "✅ 工作区干净"
fi

# 2. 检查版本号一致性
VERSION=$(cat .version)
GIT_TAG=$(git describe --tags --abbrev=0 2>/dev/null)

if [ -z "$GIT_TAG" ]; then
    echo "⚠️ 警告：当前 HEAD 无 Git 标签"
elif [ "$VERSION" != "$GIT_TAG" ]; then
    echo "❌ 错误：版本号不一致"
    echo "  .version: $VERSION"
    echo "  Git Tag:  $GIT_TAG"
    exit 1
else
    echo "✅ 版本号一致: $VERSION"
fi

# 3. 检查 RELEASE_NOTES.md 是否存在
if [ ! -f "RELEASE_NOTES.md" ]; then
    echo "❌ 错误：RELEASE_NOTES.md 不存在"
    exit 1
else
    echo "✅ RELEASE_NOTES.md 存在"
fi

# 4. 检查 .version 是否存在
if [ ! -f ".version" ]; then
    echo "❌ 错误：.version 不存在"
    exit 1
else
    echo "✅ .version 存在: $(cat .version)"
fi

echo ""
echo "=== 所有检查通过，可以发布 ==="
```

### 6.2 标准发布流程

```bash
#!/bin/bash
# release.sh - 标准化发布脚本

set -e

# 步骤 1: 运行发布前检查
./release-check.sh

# 步骤 2: 确认版本号
VERSION=$(cat .version)
echo "准备发布版本: $VERSION"
read -p "确认继续？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# 步骤 3: 创建 Git 标签
git tag -a $VERSION -m "$VERSION: $(head -3 RELEASE_NOTES.md | tail -1)"

# 步骤 4: 推送代码和标签
git push origin main --tags

# 步骤 5: 创建 GitHub Release（使用 API）
curl -X POST https://api.github.com/repos/Rx782-Fss/claude-howto-zh/releases \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d @release-body.json

echo ""
echo "✅ Release $VERSION 发布成功！"
echo "🔗 https://github.com/Rx782-Fss/claude-howto-zh/releases/tag/$VERSION"
```

---

## 七、版本历史记录规范

### 7.1 已发布版本归档

所有已发布的版本必须在 `RELEASE_NOTES.md` 中按时间倒序排列：

```markdown
## vX.Y.Z - YYYY-MM-DD (最新)
... (完整内容)

## vX.Y.(Z-1) - YYYY-MM-DD
... (完整内容)

...
```

### 7.2 版本存档策略

- **保留最近 10 个版本**的完整发布说明
- **更早的版本**可简化为单行摘要
- **永不删除**任何版本的 Git 标签

---

## 八、常见问题与解决方案

### Q1: 如果发现刚发布的版本有错误怎么办？

**A**: 
1. 修复问题
2. 递增修订版号（如 v2.3.0 → v2.3.1）
3. 更新 RELEASE_NOTES.md（在顶部添加新版本）
4. 创建新的 Git 标签和 Release
5. 在新版本中注明"修复了 v2.3.0 中的 XXX 问题"

### Q2: 是否需要为每次小修改都创建新版本？

**A**: 
- **不需要**。小的 typo 修正可以直接 commit 到 main 分支
- 只有当修正影响用户使用或有较大改进时才需要新版本
- 建议：累计多个小修改后统一发一个修订版

### Q3: 如何回滚到之前的版本？

**A**: 
```bash
# 查看可用版本
git tag -l

# 切换到指定版本
git checkout v2.3.1

# 返回最新版本
git checkout main
```

---

## 九、工具和自动化

### 9.1 推荐使用的命令别名

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc

alias version-check='bash /path/to/release-check.sh'
alias version-show='cat .version && git describe --tags --abbrev=0'
alias release-create='bash /path/to/release.sh'
```

### 9.2 VS Code / IDE 集成

建议安装以下插件以辅助版本管理：
- **GitLens** - 可视化 Git 历史
- **Release Notes Generator** - 自动生成发布说明
- **Semantic Versioning** - 版本号验证

---

## 十、文档维护

### 10.1 本文档更新记录

| 版本 | 日期 | 更新内容 | 作者 |
|------|------|----------|------|
| v1.0 | 2026-05-01 | 初始版本 | AI Agent |

### 10.2 审核周期

- **定期审核**: 每季度检查一次是否符合实际操作
- **触发审核**: 当发布流程发生重大变更时
- **负责人**: 项目维护者

---

**最后更新**: 2026-05-01
**下次审核**: 2026-08-01
