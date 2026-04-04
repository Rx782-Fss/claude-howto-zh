---
name: 设置 CI/CD 流水线
description: 实现预提交钩子和 GitHub Actions 以保障代码质量
tags: ci-cd, devops, automation
---

# 设置 CI/CD 流水线

根据项目类型实现完整的 DevOps 质量门禁体系：

1. **分析项目**：检测语言、框架、构建系统和已有工具链
2. **配置预提交钩子**，使用各语言专属工具：
   - 代码格式化：Prettier/Black/gofmt/rustfmt 等
   - 代码检查：ESLint/Ruff/golangci-lint/Clippy 等
   - 安全扫描：Bandit/gosec/cargo-audit/npm audit 等
   - 类型检查：TypeScript/mypy/flow（如适用）
   - 运行测试套件
3. **创建 GitHub Actions 工作流**（`.github/workflows/`）：
   - 在推送/PR 时镜像预提交检查
   - 多版本/多平台构建矩阵（如适用）
   - 构建与测试验证
   - 部署步骤（如需要）
4. **验证流水线**：本地测试、创建测试 PR、确认所有检查通过

使用免费/开源工具。尊重已有配置。保持流水线执行高效。

> 💡 **中文开发者提示**：CI/CD 是团队协作的基础设施。建议在项目初期就建立好流水线，避免后期技术债务积累。国内可考虑使用 Gitee Actions 或 Coding CI 作为 GitHub Actions 的替代方案。
