# 项目配置

## 项目概览
- **项目名称**:电商平台
- **技术栈**:Node.js、PostgreSQL、React 18、Docker
- **团队规模**:5 名开发人员
- **截止日期**:2025 年第四季度

## 架构说明
@docs/architecture.md
@docs/api-standards.md
@docs/database-schema.md

## 开发规范

### 代码风格
- 使用 Prettier 进行代码格式化
- 使用 ESLint 配合 airbnb 规则集
- 最大行宽:100 字符
- 使用 2 空格缩进

### 命名规范
- **文件名**:kebab-case(短横线命名,如 user-controller.js)
- **类名**:PascalCase(大驼峰,如 UserService)
- **函数/变量**:camelCase(小驼峰,如 getUserById)
- **常量**:UPPER_SNAKE_CASE(大写下划线,如 API_BASE_URL)
- **数据库表名**:snake_case(下划线命名,如 user_accounts)

### Git 工作流
- 分支命名:`feature/描述` 或 `fix/描述`
- 提交消息:遵循 Conventional Commits 规范
- 合并前必须提交 PR
- 所有 CI/CD 检查必须通过
- 至少需要 1 人审批通过

### 测试要求
- 最低代码覆盖率:80%
- 所有关键路径必须有测试覆盖
- 使用 Jest 编写单元测试
- 使用 Cypress 编写端到端测试
- 测试文件命名:`*.test.ts` 或 `*.spec.ts`

### API 标准
- 仅使用 RESTful 风格接口
- JSON 格式的请求和响应
- 正确使用 HTTP 状态码
- API 版本化:`/api/v1/`
- 所有接口必须附带示例文档

### 数据库规范
- 使用迁移脚本管理 Schema 变更
- 绝不硬编码凭证信息
- 使用连接池
- 开发环境启用查询日志
- 定期备份

### 部署规范
- 基于 Docker 的容器化部署
- Kubernetes 编排管理
- 蓝绿部署策略
- 失败时自动回滚
- 部署前先执行数据库迁移

## 常用命令

| 命令 | 用途 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm test` | 运行测试套件 |
| `npm run lint` | 检查代码风格 |
| `npm run build` | 生产环境构建 |
| `npm run migrate` | 执行数据库迁移 |

## 团队联系人
- 技术负责人:Sarah Chen (@sarah.chen)
- 产品经理:Mike Johnson (@mike.j)
- DevOps 工程师:Alex Kim (@alex.k)

## 已知问题与临时解决方案
- PostgreSQL 连接池在高峰期限制为 20 个
- 临时方案:实现查询队列机制
- Safari 14 与异步生成器存在兼容性问题
- 临时方案:使用 Babel 转译

## 相关项目
- 数据分析面板:`/projects/analytics`
- 移动端应用:`/projects/mobile`
- 管理后台:`/projects/admin`
