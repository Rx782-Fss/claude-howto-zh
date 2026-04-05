---
name: 创建 Git 提交
description: 分析暂存区变更并生成规范的提交消息
tags: git, commit, conventional-commits
allowed-tools: Bash(git diff:*, git status:*, git log:*), Read, Write
---

# 创建 Git 提交

分析当前的暂存变更并创建一个规范的提交消息:

## 工作流程

### 1. 分析暂存内容

**收集信息:**
```bash
git status          # 查看暂存的文件
git diff --cached   # 查看具体变更内容
git log --oneline -5  # 参考最近的提交风格
```

### 2. 分类变更

**判断提交类型**:
| 类型 | 适用场景 |
|------|----------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 仅文档变更 |
| `style` | 代码格式调整(不影响功能) |
| `refactor` | 重构(非新功能也非 Bug 修复) |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖等杂项 |
| `perf` | 性能优化 |
| `build` | 构建系统或外部依赖变更 |
| `ci` | CI 配置变更 |

### 3. 生成提交消息

**格式**(Conventional Commits 中文版):
```
[type](scope): 简短描述(不超过 72 个字符)

详细说明(如有必要):

- 变更点 1
- 变更点 2
- 变更点 3

关联 Issue: #123
```

**示例**:
```
feat(auth): 添加 JWT 双 Token 刷新机制

- 实现 access token 和 refresh token 双 Token 方案
- 添加 Token 黑名单机制防止重放攻击
- 更新登录接口返回新的 Token 结构

Closes #142
```

### 4. 安全检查

**⚠️ 检测到以下内容时发出警告:**
- 密钥文件:`.env*`, `*.key`, `*.pem`, `credentials.json`
- 大文件:> 5MB 且未使用 Git LFS
- 构建产物:`node_modules/`, `dist/`, `__pycache__/`, `*.pyc`
- 临时文件:`.DS_Store`, `*.swp`, `*.tmp`

### 5. 执行提交

```bash
git commit -m "[生成的提交消息]"
```

> 💡 **中文开发者提示**:推荐使用 Conventional Commits 规范,这样可以让提交历史更加清晰,也方便后续自动化生成 CHANGELOG。团队应在项目初期统一约定使用中文还是英文作为提交消息的语言。
