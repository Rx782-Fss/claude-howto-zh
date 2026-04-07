---
name: 文档结构重构
description: 分析现有文档结构并提出改进方案
tags: documentation, refactoring
allowed-tools: Read, Glob, Grep, Write
---

# 文档结构重构

分析和改进项目的文档架构:

## 工作流程

### 1. 审查现有文档

**扫描以下位置:**
- 根目录:`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`
- `docs/` 目录
- 各模块内的 `README.md`
- 代码中的注释文档(JSDoc/docstring)

### 2. 评估文档质量

**评估维度:**
| 维度 | 检查项 |
|------|--------|
| 完整性 | 是否覆盖所有公开 API 和主要功能? |
| 准确性 | 文档是否与实际代码保持同步? |
| 可读性 | 结构是否清晰?语言是否易懂? |
| 一致性 | 风格、术语是否统一? |
| 可维护性 | 是否容易随着代码变更而更新? |

### 3. 提出改进方案

**常见改进方向:**
- 统一文档目录结构
- 添加快速入门指南(Quick Start)
- 补充 API 参考文档
- 建立贡献指南中的文档规范
- 引入自动化文档生成工具

### 4. 输出重构计划

```markdown
## 📋 文档重构计划

### 当前问题
1. [问题描述]
2. [问题描述]

### 建议方案
1. [改进措施] → 预期效果
2. [改进措施] → 预期效果

### 推荐目录结构
docs/
├── README.md           # 文档导航页
├── getting-started/
│   ├── quick-start.md
│   └── installation.md
├── api-reference/
│   └── ...
├── guides/
│   └── ...
└── CONTRIBUTING.md
```

> 💡 **中文开发者提示**:好的文档是项目成功的关键。对于中文团队,建议将技术文档保持中英双语或统一使用中文,以降低团队成员的阅读门槛。
