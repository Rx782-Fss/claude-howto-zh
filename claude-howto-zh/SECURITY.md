<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# 安全策略

## 概述

Claude How To 项目的安全对我们至关重要。本文档概述了我们的安全实践，并说明了如何负责任地报告安全漏洞。

## 支持的版本

我们为以下版本提供安全更新：

| 版本 | 状态 | 支持至 |
|------|------|--------|
| Latest（main） | ✅ 活跃 | 当前 + 6 个月 |
| 1.x 版本 | ✅ 活跃 | 至下一个主版本 |

> **注意**：作为教育性指南项目，我们专注于维护当前的最佳实践和文档安全，而非传统的版本支持。更新直接应用到 main 分支。

## 安全实践

### 代码安全

**① 依赖管理**
- 所有 Python 依赖在 `requirements.txt` 中锁定版本
- 通过 Dependabot 和人工审查定期更新
- 每次提交使用 Bandit 进行安全扫描
- 预提交钩子执行安全检查

**② 代码质量**
- Ruff Linting 捕获常见问题
- mypy 类型检查防止类型相关漏洞
- 预提交钩子强制执行标准
- 所有变更在合并前经过审查

**③ 访问控制**
- `main` 分支受分支保护规则约束
- 合并前需要审查通过
- 合并前所有状态检查必须通过
- 仓库写入权限受限

### 文档安全

**① 示例中不含密钥**
- 示例中的 API 密钥均为占位符
- 凭证从不硬编码
- `.env.example` 文件展示所需变量
- 关于密钥管理的明确警告

**② 安全最佳实践**
- 示例演示安全的编码模式
- 文档中突出显示安全警告
- 链接到官方安全指南
- 在相关章节讨论凭证处理

**③ 内容审查**
- 所有文档均经安全审查
- 贡献指南中包含安全考量
- 外部链接和引用的验证

### 依赖安全

**① 扫描**
- Bandit 扫描所有 Python 代码中的漏洞
- 通过 GitHub 安全警报检查依赖漏洞
- 定期进行人工安全审计

**② 更新**
- 及时应用安全补丁
- 仔细评估主要版本升级
- Changelog 包含安全相关的更新记录

**③ 透明度**
- 在提交中记录安全更新
- 负责任地处理漏洞披露
- 适当时发布公开安全公告

## 报告漏洞

### 我们关注的安全问题

我们欢迎以下方面的报告：
- **代码漏洞**——脚本或示例中的
- **依赖漏洞**——Python 包中的
- **加密问题**——任何代码示例中的
- **认证/授权缺陷**——文档中的
- **数据泄露风险**——配置示例中的
- **注入漏洞**（SQL、命令注入等）
- **SSRF/XXE/路径遍历**问题

### 不在范围内的问题

以下内容不在本项目安全策略范围：
- Claude Code 本身的漏洞（请报告给 Anthropic）
- 外部服务或库的问题（请向上游报告）
- 社会工程学或用户教育（不适用于本指南）
- 无概念验证的理论漏洞
- 已通过官方渠道报告的依赖漏洞

## 如何报告

### 私密报告（推荐）

**对于敏感的安全问题，请使用 GitHub 的私密漏洞报告功能：**

1. 访问：https://github.com/Rx782-Fss/claude-howto-zh/security/advisories
2. 点击 "Report a vulnerability"
3. 填写漏洞详情
4. 包含：
   - 漏洞的清晰描述
   - 受影响的组件（文件、章节、示例）
   - 潜在影响
   - 复现步骤（如适用）
   - 建议的修复方案（如有）

**后续流程：**
- 我们将在 48 小时内确认收到
- 我们将调查并评估严重程度
- 我们将与您协作开发修复方案
- 我们将协调披露时间表
- 我们将在安全公告中致谢报告者（除非您希望匿名）

### 公开报告

对于非敏感问题或已公开的问题：

1. 创建一个带 `security` 标签的 GitHub Issue
2. 包含：
   - 标题：`[SECURITY]` 后跟简要描述
   - 详细描述
   - 受影响的文件或章节
   - 潜在影响
   - 建议修复方案

## 漏洞响应流程

### 评估阶段（24 小时）

1. 确认收到报告
2. 使用 [CVSS v3.1](https://www.first.org/cvss/v3.1/specification-document) 评估严重程度
3. 确定是否在范围内
4. 与报告者联系初步评估结果

### 开发阶段（1-7 天）

1. 开发修复方案
2. 审查和测试修复
3. 创建安全公告
4. 准备发布说明

### 披露时间表（按严重程度）

**Critical（CVSS 9.0-10.0）**
- 立即发布修复
- 发布公开公告
- 提前 24 小时通知报告者

**High（CVSS 7.0-8.9）**
- 48-72 小时内发布修复
- 提前 5 天通知报告者
- 发布时发布公开公告

**Medium（CVSS 4.0-6.9）**
- 下次常规更新时发布修复
- 发布时发布公告

**Low（CVSS 0.1-3.9）**
- 包含在下一次常规更新中
- 发布时发布公告

### 公告发布

我们发布的安全公告包含：
- 漏洞描述
- 受影响的组件
- 严重程度评估（CVSS 评分）
- 修复版本
- 临时缓解措施（如适用）
- 对报告者的致谢（经许可）

## 报告者最佳实践

### 报告之前

- **验证问题**：能否稳定复现？
- **搜索已有 Issue**：是否已被报告？
- **查阅文档**：是否有关于安全使用的指导？
- **测试修复**：建议的修复方案是否有效？

### 报告时

- **具体明确**：提供精确的文件路径和行号
- **提供上下文**：为什么这是一个安全问题？
- **说明影响**：攻击者能做什么？
- **给出步骤**：如何复现？
- **建议修复**：如何修复？

### 报告后

- **耐心等待**：我们的资源有限
- **及时响应**：快速回答后续问题
- **保持保密**：在修复前不要公开披露
- **尊重协调**：遵循我们的披露时间表

## 安全配置与规范

### 仓库安全

- **分支保护**：Main 分支修改需 2 人审批
- **状态检查**：所有 CI/CD 检查必须通过
- **CODEOWNERS**：关键文件的指定审查者
- **签名提交**：推荐贡献者使用签名提交

### 开发安全

```bash
# 安装预提交钩子
pre-commit install

# 本地运行安全扫描
bandit -c pyproject.toml -r scripts/
mypy scripts/ --ignore-missing-imports
ruff check scripts/
```

### 依赖安全

```bash
# 检查已知漏洞
pip install safety
safety check

# 或使用 pip-audit
pip install pip-audit
pip-audit
```

## 贡献者安全指南

### 编写示例时

**① 绝不硬编码密钥**
```python
# ❌ 错误做法
api_key = "sk-1234567890"

# ✅ 正确做法
api_key = os.getenv("API_KEY")
```

**② 警告安全隐患**
```markdown
⚠️ **安全提示**: 切勿将 `.env` 文件提交到 git。
立即添加到 `.gitignore`。
```

**③ 使用安全默认值**
- 默认启用认证
- 适用时使用 HTTPS
- 验证并清洗输入
- 使用参数化查询

**④ 记录安全考量**
- 解释为什么安全很重要
- 展示安全与不安全的模式对比
- 链接到权威来源
- 显著位置放置警告

### 审查贡献时

**① 检查暴露的密钥**
- 扫描常见模式（api_key=、password=）
- 审查配置文件
- 检查环境变量

**② 验证安全编码实践**
- 无硬编码凭证
- 正确的输入验证
- 安全的认证/授权
- 安全的文件处理

**③ 测试安全性影响**
- 是否可能被滥用？
- 最坏情况是什么？
- 是否存在边界情况？

## 安全资源

### 官方标准
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [CVSS Calculator](https://www.first.org/cvss/calculator/3.1)

### Python 安全
- [Python Security Advisories](https://www.python.org/dev/security/)
- [PyPI Security](https://pypi.org/help/#security)
- [Bandit Documentation](https://bandit.readthedocs.io/)

### 依赖管理
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- [GitHub Security Alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts)

### 通用安全
- [Anthropic Security](https://www.anthropic.com/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

## 安全公告归档

历史安全公告可在 [GitHub Security Advisories](https://github.com/Rx782-Fss/claude-howto-zh/security/advisories) 标签页查看。

## 联系方式

有关安全问题或讨论安全实践：

1. **私密安全报告**：使用 GitHub 的私密漏洞报告功能
2. **一般安全问题**：创建带 `[SECURITY]` 标签的 Discussion
3. **安全策略反馈**：创建带 `security` 标签的 Issue

## 致谢

我们感谢帮助维护本项目安全性的安全研究人员和社区成员。负责任地报告漏洞的贡献者将在我们的安全公告中获得致谢（除非您希望匿名）。

## 策略更新

本安全策略在以下情况下审查和更新：
- 发现新漏洞时
- 安全最佳实践演进时
- 项目范围变化时
- 至少每年一次

---
**最后更新: 2026 年 4 月 9 日
**下次审查**: 2027 年 4 月

感谢您帮助维护 Claude How To 的安全！🔒
