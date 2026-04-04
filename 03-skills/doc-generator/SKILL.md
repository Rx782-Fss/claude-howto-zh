---
name: api-documentation-generator
description: 从源代码生成全面、准确的 API 文档。用于创建或更新 API 文档、生成 OpenAPI 规范，或当用户提及 API 文档、接口端点、文档时使用。
---

# API 文档生成器技能

## 生成内容

- OpenAPI/Swagger 规范
- API 接口文档
- SDK 使用示例
- 集成指南
- 错误码参考
- 认证指南

## 文档结构

### 每个接口端点的文档格式

```markdown
## GET /api/v1/users/:id

### 接口说明
简要解释该接口的功能

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | string | 是 | 用户 ID |

### 响应

**200 成功**
```json
{
  "id": "usr_123",
  "name": "张三",
  "email": "zhangsan@example.com",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**404 未找到**
```json
{
  "error": "USER_NOT_FOUND",
  "message": "用户不存在"
}
```

### 使用示例

**cURL**
```bash
curl -X GET "https://api.example.com/api/v1/users/usr_123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**JavaScript**
```javascript
const user = await fetch('/api/v1/users/usr_123', {
  headers: { 'Authorization': 'Bearer token' }
}).then(r => r.json());
```

**Python**
```python
response = requests.get(
    'https://api.example.com/api/v1/users/usr_123',
    headers={'Authorization': 'Bearer token'}
)
user = response.json()
```
```
