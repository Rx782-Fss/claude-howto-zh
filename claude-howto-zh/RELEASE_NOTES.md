## v2.3.0 — 2026-04-07

### 🎉 重大更新：v2.3.0 全量重译

本次版本基于官方 [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto) v2.3.0 进行**全量中文重译**，覆盖所有严重滞后的文件。

### 新增内容

#### 全量重译（11 个文件）

| 文件 | 重译前 | 重译后 | 扩展倍率 |
|------|--------|--------|----------|
| **09-advanced-features/README.md** | ~200 行 | 848 行 | 4.2x |
| **06-hooks/README.md** | ~200 行 | 896 行 | 4.5x |
| **10-cli/README.md** | 155 行 | 839 行 | **5.4x** |
| **03-skills/README.md** | 157 行 | 815 行 | **5.2x** |
| **08-checkpoints/README.md** | 181 行 | 323 行 | 1.8x |
| **08-checkpoints/checkpoint-examples.md** | 72 行 | 343 行 | **4.8x** |
| **SECURITY.md** | 171 行 | 339 行 | **2.0x** |

#### 已更新（高覆盖率补齐）

| 文件 | 覆盖率 | 变更 |
|------|--------|------|
| **04-subagents/README.md** | 98% → 99% | 更新日期 |
| **05-mcp/README.md** | 97% → 98% | 补充日期页脚 |
| **07-plugins/README.md** | 99% → 100% | 补充日期页脚 |

#### 新增文件

| 文件 | 说明 |
|------|------|
| **04-subagents/performance-optimizer.md** | 性能分析与优化子代理（v2.3.0 新增） |

### v2.3.0 重译覆盖的新功能

以下为本次重译新增或大幅扩展的内容：

- **Planning Mode（规划模式）**—— 完整工作流、配置、示例
- **Extended Thinking（扩展思考）**—— ultrathink 关键字、努力级别
- **Background Tasks（后台任务）**—— 快捷键管理
- **6 种权限模式** —— default、acceptEdits、plan、dontAsk、bypassPermissions + auto
- **Session Management（会话管理）** —— resume/rename/fork/from-pr
- **Chrome Integration / Channels** —— 浏览器集成与频道插件
- **Voice Dictation（语音输入）**
- **Built-in Skills（内置技能）** —— simplify/batch/debug/loop/claude-api
- **Headless Mode（无头模式）**
- **Auto-Memory（自动记忆）**
- **Remote Control / Web Sessions** —— 远程控制与 Web 会话
- **Desktop App（桌面应用）**
- **Task List（任务列表）**
- **Prompt Suggestions（提示建议）**
- **Git Worktree 隔离**
- **Sandboxing（沙箱）**
- **Managed Settings（托管设置，企业版）**
- **Agent Teams（代理团队，实验性）**
- **26 个 Hook 事件 × 4 种 Hook 类型** —— command/http/prompt/agent
- **Agent 配置 JSON 格式** —— CLI/用户/项目三级优先级
- **Skills 渐进式加载架构** —— Level 1/2/3 三级机制
- **31 个环境变量**完整参考
- **7 大 CLI 高价值使用场景** —— CI/CD、管道处理、多会话、批量等
- **cc-context-stats 上下文区域监控**

### Mermaid 兼容性修复

- 修复 `as 中文别名` 问题（09-advanced-features 时序图）
- 全量扫描确认无 `style` 行、`N.` 编号标签等不兼容语法

### Bug 修复

- 修正 SECURITY.md 安全策略文档结构（完全重写，匹配官方格式）
- 补充 05-mcp、07-plugins 缺失的日期页脚
- 修复 04-subagents 日期格式

### 文档同步

- 所有变更已同步至 Obsidian 知识库（11/11 文件）

---

## v2.2.0 — 2026-03-26

### Bug 修复

- 移除失效的市场链接,修复 CI 链接检查失败问题 (3fdf0d6)
- 将 `sandboxed` 和 `pycache` 添加到 cSpell 字典 (dc64618)

**完整变更日志**: https://github.com/Rx782-Fss/claude-howto-zh/compare/v2.1.1...v2.2.0

---
**最后更新**: 2026 年 4 月 7 日
