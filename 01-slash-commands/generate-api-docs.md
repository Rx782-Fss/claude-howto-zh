---
name: 生成 API 文档
description: 为选定的 API 端点或模块生成全面的 API 文档
tags: documentation, api, openapi
allowed-tools: Read, Glob, Grep, Write
---

# 生成 API 文档

为指定的 API 或模块生成完整的 API 文档:

## 工作流程

### 1. 分析目标

**确定范围:**
- 用户指定了特定文件/目录?→ 聚焦该区域
- 未指定?→ 扫描项目中的 API 定义(路由、控制器、handler)

**检测框架/协议:**
- REST API(Express/FastAPI/Flask/Gin 等)
- GraphQL
- gRPC
- WebSocket

### 2. 收集信息

**从代码中提取:**
- 端点定义(路径、方法)
- 请求/响应模型(类型定义、schema)
- 认证方式
- 错误码和错误处理
- 速率限制配置

### 3. 生成文档

**输出格式**(根据用户偏好):
- OpenAPI/Swagger 规范(YAML/JSON)
- Markdown API 参考
- JSDoc/TSDoc 注释注入

**文档结构**:
```markdown
# [API 名称] API 文档

## 概述
[简要描述 API 的用途和范围]

## 认证
[说明认证方式和获取凭证的方法]

## 基础 URL
```
[环境对应的 base URL]
```

## 接口列表

### [端点名称]
**`[METHOD] /path`**

**描述**:[接口功能说明]

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| param1 | string | 是 | 参数说明 |

**响应示例**:
```json
{
  "code": 200,
  "data": {...},
  "message": "success"
}
```

**错误码**:

| 错误码 | 说明 |
|--------|------|
| 400 | 参数错误 |
| 401 | 未授权 |
...
```

### 4. 验证和输出

- [ ] 所有端点均已记录
- [ ] 请求/响应字段完整
- [ ] 示例数据有效
- [ ] 错误码覆盖全面

> 💡 **中文开发者提示**:生成的文档默认使用中文编写。如果团队使用英文文档,请在命令后注明"使用英文输出"。此命令可与 doc-generator 技能结合使用。
