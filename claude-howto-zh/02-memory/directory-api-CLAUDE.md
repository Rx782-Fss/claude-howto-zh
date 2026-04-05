# API 模块规范

本文件为 `/src/api/` 目录下的所有内容覆盖根目录的 CLAUDE.md 配置。

## API 专用规范

### 请求校验
- 使用 Zod 进行 Schema 校验
- 始终校验输入参数
- 校验失败时返回 400 状态码
- 包含字段级别的错误详情

### 身份认证
- 所有接口均要求 JWT Token 认证
- Token 通过 Authorization 请求头传递
- Token 有效期为 24 小时
- 实现刷新令牌(Refresh Token)机制

### 响应格式

所有响应必须遵循以下结构:

```json
{
  "success": true,
  "data": { /* 实际数据 */ },
  "timestamp": "2025-11-06T10:30:00Z",
  "version": "1.0"
}
```

错误响应格式:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "用户可读的错误消息",
    "details": { /* 字段级错误详情 */ }
  },
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### 分页规范
- 使用基于游标(cursor)的分页方式(而非偏移量 offset)
- 包含 `hasMore` 布尔字段表示是否有更多数据
- 单页最大条目数限制为 100
- 默认每页大小:20 条

### 速率限制
- 已认证用户:每小时 1000 次请求
- 公开接口:每小时 100 次请求
- 超出限制时返回 429 状态码
- 响应中包含 Retry-After 请求头

### 缓存策略
- 使用 Redis 进行会话缓存
- 默认缓存时长:5 分钟
- 写入操作时使缓存失效
- 缓存键按资源类型打标签
