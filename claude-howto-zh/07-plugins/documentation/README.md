<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../resources/logos/claude-howto-logo.svg">
</picture>

# 文档插件(Documentation Plugin)

为你的项目提供全面的文档生成和维护功能。

## 功能特性

✅ API 文档生成
✅ README 创建和更新
✅ 文档同步
✅ 代码注释改进
✅ 示例代码生成

## 安装

```bash
/plugin install documentation
```

## 包含内容

### 斜杠命令(Slash Commands)
- `/generate-api-docs` -- 生成 API 文档
- `/generate-readme` -- 创建或更新 README
- `/sync-docs` -- 同步文档与代码变更
- `/validate-docs` -- 验证文档

### 子代理(Subagents)
- `api-documenter` -- API 文档专家
- `code-commentator` -- 代码注释改进专家
- `example-generator` -- 示例代码创建专家

### 模板(Templates)
- `api-endpoint.md` -- API 端点文档模板
- `function-docs.md` -- 函数文档模板
- `adr-template.md` -- 架构决策记录(ADR)模板

### MCP 服务器
- GitHub 集成,用于文档同步

## 使用方法

### 生成 API 文档
```
/generate-api-docs
```

### 创建 README
```
/generate-readme
```

### 同步文档
```
/sync-docs
```

### 验证文档
```
/validate-docs
```

## 要求

- Claude Code 1.0+
- GitHub 访问权限(可选)

## 示例工作流

```
用户: /generate-api-docs

Claude:
1. 扫描 /src/api/ 中的所有 API 端点
2. 委托给 api-documenter 子代理
3. 提取函数签名和 JSDoc 注释
4. 按模块/端点组织
5. 使用 api-endpoint.md 模板
6. 生成完整的 Markdown 文档
7. 包含 curl、JavaScript 和 Python 示例

结果:
✅ API 文档已生成
📄 已创建文件:
   - docs/api/users.md
   - docs/api/auth.md
   - docs/api/products.md
📊 覆盖率:23/23 个端点已记录文档
```

## 模板使用说明

### API 端点模板
用于记录 REST API 端点的完整示例。

### 函数文档模板
用于记录单个函数/方法的文档。

### ADR 模板
用于记录架构决策。

## 配置

设置 GitHub Token 以启用文档同步功能:
```bash
export GITHUB_TOKEN="your_github_token"
```

## 最佳实践

- 保持文档与代码紧密关联
- 随代码变更同步更新文档
- 包含实用的示例
- 定期验证文档
- 使用模板保持一致性
