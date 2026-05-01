---
描述: 暂存所有变更、创建提交并推送到远程仓库(请谨慎使用)
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git 提交:*), Bash(git push:*), Bash(git diff:*), Bash(git log:*), Bash(git pull:*)
---

# 暂存、提交并推送所有变更

⚠️ **注意**:将暂存所有变更、创建提交并推送。仅在确信所有变更是一体的情况下使用。

## 工作流程

### 1. 分析变更

**并行执行:**
- `git status` -- 显示修改/新增/删除/未跟踪的文件
- `git diff --stat` -- 显示变更统计
- `git log -1 --oneline` -- 查看最近一次提交以参考消息风格

### 2. 安全检查

**❌ 如果检测到以下内容则停止并警告:**
- 密钥文件:`.env*`, `*.key`, `*.pem`, `credentials.JSON`, `secrets.YAML`, `id_rsa`, `*.p12`, `*.pfx`, `*.cer`
- API 密钥:包含真实值的 `*_API_KEY`, `*_SECRET`, `*_TOKEN` 变量(不包括占位符如 `your-API-key`, `xxx`, `placeholder`)
- 大文件:未使用 Git LFS 的 >10MB 文件
- 构建产物:`node_modules/`, `dist/`, `构建/`, `__pycache__/`, `*.pyc`, `.venv/`
- 临时文件:`.DS_Store`, `thumbs.db`, `*.swp`, `*.tmp`

**API 密钥校验规则:**
```bash
OPENAI_API_KEY=sk-proj-xxxxx  #   ❌ 检测到真实密钥!
AWS_SECRET_KEY=AKIA...         #   ❌ 检测到真实密钥!
STRIPE_API_KEY=sk_live_...    #   ❌ 检测到真实密钥!

#   ✅ 可接受的占位符:
API_KEY=your-api-key-here
SECRET_KEY=placeholder
TOKEN=xxx
API_KEY=<your-key>
SECRET=${YOUR_SECRET}
```

**✅ 确认检查:**
- `.gitignore` 配置正确
- 无合并冲突
- 分支正确(如果在 main/master 分支则警告)
- API 密钥仅为占位符

### 3. 请求确认

展示摘要:
```
📊 变更摘要:
- X 个文件修改,Y 个新增,Z 个删除
- 总计:+AAA 行新增,-BBB 行删除

🔒 安全检查:✅ 无密钥 | ✅ 无大文件 | ⚠️ [警告信息]
🌿 分支:[名称] → origin/[名称]

即将执行:git add . → commit → push

输入 'yes' 继续,输入 'no' 取消。
```

**等待明确的 "yes" 后再继续。**

### 4. 执行(确认后)

按顺序执行:
```bash
git add .
git status  #   验证暂存区
```

### 5. 生成提交消息

分析变更并创建 Conventional 提交 格式的提交消息:

**格式:**
```
[type](scope): 简短描述(不超过 72 个字符)

- 关键变更 1
- 关键变更 2
- 关键变更 3
```

**类型**:`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`

### 6. 提交并推送

```bash
git commit -m "$(cat <<'EOF'
[生成的提交消息]
EOF
)"
git push  #   如果失败:git pull --rebase && git push
git log -1 --oneline --decorate  #   验证
```

### 7. 确认成功

```
✅ 成功推送到远程!

提交:[hash] [消息]
分支:[branch] → origin/[branch]
变更文件数:X(+新增行数, -删除行数)
```

## 错误处理

- **git add 失败**:检查权限、锁定文件、确认仓库已初始化
- **git 提交 失败**:修复 pre-提交 钩子、检查 git config(用户.name/email)
- **git push 失败**:
  - 非快进式推送:`git pull --rebase && git push`
  - 远程无此分支:`git push -u origin [分支]`
  - 受保护分支:改用 PR 工作流

## 使用时机

✅ **适合使用:**
- 多文件文档更新
- 包含测试和文档的功能开发
- 跨文件的 Bug 修复
- 项目范围的格式化/重构
- 配置变更

❌ **避免使用:**
- 不确定要提交什么内容
- 包含密钥/敏感数据
- 受保护分支且未经审查
- 存在合并冲突
- 需要精细控制提交历史
- Pre-提交 钩子 正在失败

## 替代方案

如果用户希望更多控制权,建议:
1. **选择性暂存**:审阅/暂存特定文件
2. **交互式暂存**:使用 `git add -p` 进行补丁选择
3. **PR 工作流**:创建分支 → 推送 → 创建 PR(使用 `/pr` 命令)

> ⚠️ **重要提醒**:推送前务必审阅变更。如有疑虑,请使用单独的 git 命令以获得更多控制。
