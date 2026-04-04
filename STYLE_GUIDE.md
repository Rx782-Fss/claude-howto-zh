# 项目风格指南

本文档定义了整个项目的编码风格和格式规范。

## Markdown 格式规范

### 标题层级
- 使用 H2（`##`）作为章节标题
- 使用 H3（`###`）作为子节标题
- 不使用 H1（保留给文件标题）

### 代码块
- 始终指定语言标识符
- 保持代码简洁且可复制粘贴
- 对关键行添加注释说明

### 列表
- 无序列表用于一般项目
- 有序列表用于步骤
- 嵌套列表最多 2 层深度

### 表格
- 用于配置参考和对比
- 包含清晰的标题行
- 保持列宽合理

### Mermaid 图表
- 用于可视化工作流和架构
- 在图表下方添加简要说明文字
- 保持图表简单易读

## 文件命名规范

### 斜杠命令
- 使用 kebab-case（短横线命名法）：`generate-api-docs.md`
- 名称应反映功能
- 以 `.md` 结尾

### 子代理
- 使用 kebab-case：`code-reviewer.md`
- 名称应反映角色或专业领域
- 以 `.md` 结尾

### 技能目录
- 使用 kebab-case：`code-review/`
- `SKILL.md` 作为主文件名（大写）
- 相关文件放在子目录中

### 钩子脚本
- Shell 脚本：kebab-case + `.sh`
- Python 脚本：snake_case + `.py`
- JavaScript 脚本：camelCase + `.js`

### MCP 配置
- 使用 kebab-case：`github-mcp.json`
- 描述集成目标

## 内容结构规范

### README 文件
每个模块应包含：
1. 简介（1-2 段）
2. 功能特性列表
3. 安装说明
4. 使用示例
5. 配置选项
6. 故障排除

### SKILL.md 文件
应包含 YAML frontmatter：
```yaml
---
name: skill-name
description: 一句话描述技能功能
tools: read, write, bash, grep
---
```

### 子代理定义
应包含 YAML frontmatter：
```yaml
---
name: agent-name
description: 代理的专业领域
tools: read, grep, diff
---
```

### 钩子脚本
应包含：
1. Shebang 行
2. 功能描述注释
3. 清晰的错误处理
4. 日志输出

## 编写风格

### 语气
- 专业但友好
- 清晰简洁
- 对初学者友好
- 避免行话

### 语言
- 中文为主（翻译版）
- 术语首次出现时附英文原文
- 代码和技术术语保留英文

### 格式一致性
- 统一使用中文标点
- 列表项末尾不加标点
- 表头使用名词短语
- 代码示例保持原始语言

## 代码示例规范

### Shell 脚本
```bash
#!/bin/bash
set -e  # 遇错退出

# 功能描述
echo "Starting process..."  # 开始处理...

# 错误处理
if [ ! -f "$FILE" ]; then
    echo "Error: File not found" >&2  # 错误：文件未找到
    exit 1
fi
```

### Python 脚本
```python
#!/usr/bin/env python3
"""模块功能的简要描述。"""

def function_name(param: str) -> str:
    """函数功能的简要描述。
    
    Args:
        param: 参数描述
        
    Returns:
        返回值描述
    """
    # 实现代码
    pass
```

### JSON 配置
```json
{
  "description": "配置用途的中文描述",
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-example"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

## 文档字符串和注释

### Shell 注释
```bash
# 单行注释：简短描述
# 多行注释：更详细的解释
# 可以跨多行
```

### Python 文档字符串
```python
def example():
    """一行摘要。

    更详细的描述（如需要）。
    
    Returns:
        返回类型和含义。
    """
    return None
```

### JSON 描述字段
```json
{
  "description": "此配置的中文描述"
}
```

## 测试规范

### 测试文件位置
- 与被测文件同级放置
- 命名为 `*.test.*` 或 `test_*.py`

### 测试命名
- 描述性名称：`test_code_review_finds_security_issues`
- 一个测试一个概念

### 测试结构
```python
def test_feature():
    """测试功能的简要描述。"""
    # Arrange（准备）
    # Act（执行）
    # Assert（断言）
    assert result == expected
```

## Git 提交规范

### 提交信息格式
```
type(scope): description

[可选正文]
```

### 类型
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档变更
- `refactor`: 重构
- `style`: 格式调整
- `test`: 测试变更
- `chore`: 构建/工具链

### 示例
```
feat(skills): 添加代码异味检测器技能
fix(hooks): 修复上下文追踪器的 Token 计数问题
docs(plugins): 更新 DevOps 插件的 README 文档
```

## 许可证头部

对于新增文件，考虑添加许可证声明：

```markdown
<!-- 
  版权所有 (c) 2026 claude-howto 贡献者
  基于 MIT 许可证授权
-->
```

## 最终检查清单

在提交前确认：

- [ ] Markdown 格式正确
- [ ] 代码示例可运行
- [ ] 所有链接有效
- [ ] 文件命名符合规范
- [ ] 内容结构完整
- [ ] 中文翻译准确
- [ ] 无拼写错误
- [ ] 符合本指南规范
