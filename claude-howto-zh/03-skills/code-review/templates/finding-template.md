# 代码审查发现模板

在记录代码审查中发现的问题时使用此模板。

---

## 问题：[标题]

### 严重程度
- [ ] Critical（阻塞发布）
- [ ] High（合并前应修复）
- [ ] Medium（应尽快修复）
- [ ] Low（锦上添花）

### 类别
- [ ] 安全
- [ ] 性能
- [ ] 代码质量
- [ ] 可维护性
- [ ] 测试
- [ ] 设计模式
- [ ] 文档

### 位置
**文件**：`src/components/UserCard.tsx`

**行号**：45-52

**函数/方法**：`renderUserDetails()`

### 问题描述

**现象描述**：描述问题的具体内容。

**影响说明**：解释为什么需要修复以及其影响。

**当前行为**：展示存在问题的代码或行为。

**期望行为**：描述应该改为怎样的正确行为。

### 代码示例

#### 当前（有问题）

```typescript
// 展示了 N+1 查询问题
const users = fetchUsers();
users.forEach(user => {
  const posts = fetchUserPosts(user.id); // 每个用户一次查询！
  renderUserPosts(posts);
});
```

#### 建议修复方案

```typescript
// 使用 JOIN 查询优化
const usersWithPosts = fetchUsersWithPosts();
usersWithPosts.forEach(({ user, posts }) => {
  renderUserPosts(posts);
});
```

### 影响分析

| 方面 | 影响 | 严重程度 |
|------|------|----------|
| 性能 | 20 个用户需要 100+ 次查询 | 高 |
| 用户体验 | 页面加载缓慢 | 高 |
| 可扩展性 | 规模扩大时会崩溃 | Critical |
| 可维护性 | 难以调试 | 中 |

### 相关问题

- `AdminUserList.tsx` 第 120 行存在类似问题
- 相关 PR：#456
- 相关 Issue：#789

### 补充资源

- [N+1 查询问题](https://zh.wikipedia.org/wiki/N%2B1%E6%9F%A5%E8%A9%A2)
- [数据库 JOIN 文档](https://docs.example.com/joins)

### 审查者备注

- 这是本代码库中的常见模式
- 考虑将其添加到代码风格指南中
- 可能值得创建一个辅助函数

### 作者反馈（用于回复）

*由代码作者填写：*

- [ ] 修复已在提交 `abc123` 中实现
- [ ] 修复状态：已完成 / 进行中 / 需要讨论
- [ ] 疑问或顾虑：（请描述）

---

## 发现统计（供审查者使用）

审查多个问题时，请跟踪：

- **发现问题总数**：X
- **Critical**：X
- **High**：X
- **Medium**：X
- **Low**：X

**建议**：✅ 批准 / ⚠️ 请求修改 / 🔄 需要讨论

**整体代码质量**：1-5 星
