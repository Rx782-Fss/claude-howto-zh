<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# 为 Claude How To 做出贡献

感谢你对本项目的兴趣!本指南将帮助你了解如何有效地做出贡献。

## 关于本项目

Claude How To 是一份面向 Claude Code 的可视化、示例驱动指南。我们提供:
- **Mermaid 图表** 解释各功能的运作原理
- **开箱即用的模板** 可立即使用
- **真实案例** 包含上下文和最佳实践
- **渐进式学习路径** 从入门到精通

## 贡献类型

### 1. 新示例或模板
为现有功能(斜杠命令、技能、钩子等)添加示例:
- 即拷即用的代码
- 清晰解释其工作原理
- 用例和优势
- 故障排除技巧

### 2. 文档改进
- 澄清令人困惑的部分
- 修正拼写和语法错误
- 补充缺失信息
- 改进代码示例

### 3. 功能指南
为新 Claude Code 功能创建指南:
- 分步教程
- 架构图
- 常见模式和反模式
- 真实工作流

### 4. Bug 报告
报告你遇到的问题:
- 描述你期望的结果
- 描述实际发生的情况
- 包含复现步骤
- 提供相关的 Claude Code 版本和操作系统信息

### 5. 反馈与建议
帮助改进本指南:
- 建议更好的解释方式
- 指出覆盖范围上的空白
- 推荐新增章节或重组建议

## 入门指南

### 1. Fork 并克隆
```bash
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto
```

### 2. 创建分支
使用描述性的分支名:
```bash
git checkout -b add/feature-name
git checkout -b fix/issue-description
git checkout -b docs/improvement-area
```

### 3. 设置环境

Pre-commit hooks(预提交钩子)在每次提交前本地运行与 CI 相同的检查。所有四项检查必须通过后 PR 才会被接受。

**所需依赖:**

```bash
# Python 工具链(uv 是本项目的包管理器)
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r scripts/requirements-dev.txt

# Markdown 格式检查工具(Node.js)
npm install -g markdownlint-cli

# Mermaid 图表验证工具(Node.js)
npm install -g @mermaid-js/mermaid-cli

# 安装 pre-commit 并激活钩子
uv pip install pre-commit
pre-commit install
```

**验证你的环境配置:**

```bash
pre-commit run --all-files
```

每次提交时运行的钩子:

| 钩子 | 检查内容 |
|------|----------|
| `markdown-lint` | Markdown 格式和结构 |
| `cross-references` | 相对链接、锚点、代码围栏 |
| `mermaid-syntax` | 所有 ````mermaid` 代码块能正确解析 |
| `link-check` | 外部 URL 是否可访问 |
| `build-epub` | EPUB 能无错误生成(针对 `.md` 变更时)|

## 目录结构

```
├── 01-slash-commands/      # 用户调用的快捷命令
├── 02-memory/              # 持久化上下文示例
├── 03-skills/              # 可复用的能力
├── 04-subagents/           # 专业的 AI 助手
├── 05-mcp/                 # Model Context Protocol 示例
├── 06-hooks/               # 事件驱动的自动化
├── 07-plugins/             # 打包的功能集合
├── 08-checkpoints/         # 会话快照
├── 09-advanced-features/   # 规划、思考、后台任务
├── 10-cli/                 # CLI 参考
├── scripts/                # 构建和工具脚本
└── README.md               # 主指南
```

## 如何贡献示例

### 添加斜杠命令
1. 在 `01-slash-commands/` 中创建 `.md` 文件
2. 包含以下内容:
   - 清晰描述其功能
   - 使用场景
   - 安装说明
   - 使用示例
   - 自定义技巧
3. 更新 `01-slash-commands/README.md`

### 添加技能
1. 在 `03-skills/` 中创建目录
2. 包含以下内容:
   - `SKILL.md` -- 主文档
   - `scripts/` -- 辅助脚本(如需要)
   - `templates/` -- 提示词模板
   - README 中的使用示例
3. 更新 `03-skills/README.md`

### 添加子代理
1. 在 `04-subagents/` 中创建 `.md` 文件
2. 包含以下内容:
   - 代理目的和能力
   - 系统提示词结构
   - 示例用例
   - 集成示例
3. 更新 `04-subagents/README.md`

### 添加 MCP 配置
1. 在 `05-mcp/` 中创建 `.json` 文件
2. 包含以下内容:
   - 配置说明
   - 所需的环境变量
   - 安装说明
   - 使用示例
3. 更新 `05-mcp/README.md`

### 添加钩子
1. 在 `06-hooks/` 中创建 `.sh` 文件
2. 包含以下内容:
   - Shebang 和描述
   - 清晰注释解释逻辑
   - 错误处理
   - 安全注意事项
3. 更新 `06-hooks/README.md`

## 编写规范

### Markdown 风格
- 使用清晰的标题(H2 用于章节,H3 用于小节)
- 保持段落简短且聚焦
- 使用无序列表
- 包含带语言标注的代码块
- 各章节之间留空行

### 代码示例
- 使示例即拷即用
- 对非显而易见的逻辑进行注释
- 同时包含简单版本和高级版本
- 展示真实使用场景
- 强调潜在问题

### 文档撰写
- 解释"为什么"而不仅仅是"是什么"
- 包含前提条件
- 添加故障排除章节
- 链接到相关主题
- 保持对初学者友好

### JSON/YAML
- 使用一致的缩进(2 或 4 个空格)
- 添加解释配置的注释
- 包含验证示例

### 图表
- 尽可能使用 Mermaid
- 保持图表简洁易读
- 在图表下方添加说明文字
- 链接到相关章节

## 提交规范

遵循 conventional commit 格式:
```
type(scope): description

[可选正文]
```

类型:
- `feat`:新功能或新示例
- `fix`:Bug 修复或更正
- `docs`:文档变更
- `refactor`:代码重构
- `style`:格式调整
- `test`:测试添加或修改
- `chore`:构建、依赖等

示例:
```
feat(slash-commands): 添加 API 文档生成器
docs(memory): 改进个人偏好示例
fix(README): 修正目录链接
docs(skills): 添加全面的代码审查技能
```

## 提交前检查清单

### 检查项
- [ ] 代码符合项目风格和规范
- [ ] 新示例包含清晰的文档
- [ ] README 文件已更新(包括本地和根目录)
- [ ] 无敏感信息(API 密钥、凭证等)
- [ ] 示例经过测试且可正常工作
- [ ] 链接经过验证且正确无误
- [ ] 文件权限正确(脚本具有可执行权限)
- [ ] 提交信息清晰且具有描述性

### 本地测试
```bash
# 运行所有 pre-commit 检查(与 CI 相同)
pre-commit run --all-files

# 审查你的更改
git diff
```

## Pull Request 流程

1. **创建带有清晰描述的 PR**:
   - 添加/修复了什么?
   - 为什么需要它?
   - 相关 Issue(如有)

2. **包含相关细节**:
   - 新功能?包含使用场景
   - 文档?说明改进之处
   - 示例?展示前后对比

3. **关联 Issue**:
   - 使用 `Closes #123` 自动关闭相关 Issue

4. **耐心等待审查**:
   - 维护者可能会提出改进建议
   - 根据反馈进行迭代
   - 最终决定权归维护者

## 代码审查流程

审查者会检查:
- **准确性**:是否按描述正常工作?
- **质量**:是否达到生产就绪标准?
- **一致性**:是否符合项目模式?
- **文档**:是否清晰完整?
- **安全性**:是否存在漏洞?

## 报告问题

### Bug 报告请包含:
- Claude Code 版本
- 操作系统
- 复现步骤
- 期望行为
- 实际行为
- 截图(如适用)

### 功能请求请包含:
- 用例或待解决的问题
- 建议的解决方案
- 你考虑过的替代方案
- 补充上下文

### 文档问题请包含:
- 什么内容令人困惑或缺失
- 建议的改进方向
- 示例或参考资料

## 项目策略

### 敏感信息
- 永远不要提交 API 密钥、Token 或凭证
- 在示例中使用占位符值
- 为配置文件包含 `.env.example`
- 记录所需的环境变量

### 代码质量
- 保持示例聚焦且易读
- 避免过度工程化的解决方案
- 为非显而易见的逻辑添加注释
- 提交前充分测试

### 知识产权
- 原创内容由作者拥有
- 项目使用教育许可证
- 尊重现有版权
- 在需要处注明出处

## 获取帮助

- **提问**:在 GitHub Issues 中发起讨论
- **一般帮助**:查看已有文档
- **开发帮助**:参考类似示例
- **代码审查**:在 PR 中 @ 维护者

## 致谢

贡献者将在以下位置获得致谢:
- README.md 的贡献者部分
- GitHub 贡献者页面
- 提交历史记录

## 安全

在贡献示例和文档时,请遵循安全编码实践:

- **永远不要硬编码密钥或 API Key** ---- 使用环境变量
- **警示安全影响** ---- 突出潜在风险
- **使用安全的默认值** ---- 默认启用安全功能
- **验证输入** ---- 展示正确的输入校验和清洗
- **包含安全备注** ---- 记录安全考量事项

关于安全问题,请参见 [SECURITY.md](SECURITY.md) 了解我们的漏洞报告流程。

## 行为准则

我们致力于提供一个热情包容的社区。请阅读 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 了解完整的社区标准。

简要概括:
- 保持尊重和包容
- 优雅地接受反馈
- 帮助他人学习和成长
- 避免骚扰或歧视
- 向维护者报告问题

所有贡献者都应遵守此准则,并以善意和尊重彼此相待。

## 许可证

通过为本项目做贡献,你同意你的贡献将以 MIT 许可证授权。详情请参阅 [LICENSE](LICENSE) 文件。

## 还有疑问?

- 查看 [README](README.md)
- 审阅 [LEARNING-ROADMAP.md](LEARNING-ROADMAP.md)
- 查看已有示例
- 发起 Issue 进行讨论

感谢你的贡献!🙏
