<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../resources/logos/claude-howto-logo.svg">
</picture>

# PR 审查插件（PR Review Plugin）

完整的 PR（Pull Request）审查工作流，包含安全、测试和文档检查。

## 功能特性

✅ 安全分析
✅ 测试覆盖率检查
✅ 文档验证
✅ 代码质量评估
✅ 性能影响分析

## 安装

```bash
/plugin install pr-review
```

## 包含内容

### 斜杠命令（Slash Commands）
- `/review-pr` — 全面 PR 审查
- `/check-security` — 安全专项审查
- `/check-tests` — 测试覆盖率分析

### 子代理（Subagents）
- `security-reviewer` — 安全漏洞检测
- `test-checker` — 测试覆盖率分析
- `performance-analyzer` — 性能影响评估

### MCP 服务器
- GitHub 集成，用于获取 PR 数据

### 钩子（Hooks）
- `pre-review.js` — 审查前验证

## 使用方法

### 基本_PR 审查
```
/review-pr
```

### 仅安全检查
```
/check-security
```

### 测试覆盖率检查
```
/check-tests
```

## 要求

- Claude Code 1.0+
- GitHub 访问权限
- Git 仓库

## 配置

设置你的 GitHub Token：
```bash
export GITHUB_TOKEN="your_github_token"
```

## 示例工作流

```
用户: /review-pr

Claude:
1. 运行审查前钩子（验证 git 仓库）
2. 通过 GitHub MCP 获取 PR 数据
3. 将安全审查委托给 security-reviewer 子代理
4. 将测试检查委托给 test-checker 子代理
5. 将性能评估委托给 performance-analyzer 子代理
6. 综合所有发现
7. 提供全面的审查报告

结果：
✅ 安全：未发现严重问题
⚠️  测试：覆盖率为 65%，建议达到 80%+
✅ 性能：无显著影响
📝 建议：为边缘情况添加测试用例
```
