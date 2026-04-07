---
name: 准备 Pull Request
description: 分析变更、生成 PR 描述并验证就绪状态
tags: git, pull-request, code-review
allowed-tools: Bash(git diff:*, git log:*, git status:*), Read, Glob, Grep, Write
---

# 准备 Pull Request

分析当前分支的所有变更并准备完整的 PR:

## 工作流程

### 1. 分析变更范围

**并行执行:**
```bash
git diff --stat origin/main...HEAD    # 变更统计
git log --oneline origin/main...HEAD   # 提交历史
```

### 2. 生成 PR 内容

**PR 标题**(Conventional Commits 格式):
```
[type](scope): 简短描述(不超过 72 个字符)
```

**类型**:`feat` | `fix` | `docs` | `style` | `refactor` | `test` | `chore` | `perf` | `ci` | `build`

**PR 正文模板**:
```markdown
## 📝 变更概述
[用 2-3 句话描述这个 PR 做了什么]

## 🔧 变更类型
- [ ] 新功能 (feature)
- [ ] Bug 修复 (bugfix)
- [ ] 重构 (refactoring)
- [ ] 文档更新 (documentation)
- [ ] 其他:______

## 📋 变更清单
[列出关键文件的变更]

## 🧪 测试情况
- [ ] 新增/更新的测试
- [ ] 测试覆盖的关键场景
- [ ] 手动测试结果

## 📸 截图/演示(如适用)
[添加截图或 GIF]

## ⚠️ 注意事项
[任何审查者需要注意的事项]
```

### 3. 质量门禁检查

**自动验证:**
- [ ] 无合并冲突
- [ ] 所有测试通过
- [ ] 代码风格一致
- [ ] 无敏感信息泄露(密钥、密码等)
- [ ] 提交消息符合规范

### 4. 输出最终报告

```markdown
## ✅ PR 准备完成

**建议标题**:`[type](scope): description`

**变更摘要**:
- X 个文件修改,+AAA 行新增,-BBB 行删除
- 主要涉及:[模块/功能列表]

**下一步操作**:
1. 推送到远程分支:`git push -u origin feature/your-branch`
2. 创建 PR 并粘贴以上内容
3. @ 相关审查者
```

> 💡 **中文开发者提示**:使用 `/pr` 命令可以在提交 PR 前自动整理所有变更信息,确保 PR 描述完整清晰。配合 code-review 技能效果更佳。
