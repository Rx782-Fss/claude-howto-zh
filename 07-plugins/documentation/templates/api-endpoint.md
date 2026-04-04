# [HTTP 方法] /api/v1/[端点名称]

## 简介
简要描述此端点的功能。

## 认证方式
所需的认证方法（例如：Bearer Token）。

## 参数

### 路径参数
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | string | 是 | 资源 ID |

### 查询参数
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码（默认：1）|
| limit | integer | 否 | 每页条数（默认：20）|

### 请求体
```json
{
  "field": "value"
}
```

## 响应

### 200 OK
```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "示例"
  }
}
```

### 400 Bad Request（错误请求）
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "无效输入"
  }
}
```

### 404 Not Found（未找到）
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "资源未找到"
  }
}
```

## 示例

### cURL
```bash
curl -X GET "https://api.example.com/api/v1/endpoint" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### JavaScript
```javascript
const response = await fetch('/api/v1/endpoint', {
  headers: {
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

### Python
```python
import requests

response = requests.get(
    'https://api.example.com/api/v1/endpoint',
    headers={'Authorization': 'Bearer token'}
)
data = response.json()
```

## 速率限制
- 认证用户：每小时 1000 次请求
- 公开端点：每小时 100 次请求

## 相关端点
- [GET /api/v1/related](#)
- [POST /api/v1/related](#)
