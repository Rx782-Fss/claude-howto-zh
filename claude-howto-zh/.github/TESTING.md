# 测试指南

本文档描述 Claude How To 项目的测试基础设施。

## 概述

项目使用 GitHub Actions 在每次推送和 Pull Request 时自动运行测试。测试覆盖:

- **单元测试**:使用 pytest 的 Python 测试
- **代码质量**:Ruff 的 Linting 和格式化检查
- **安全性**:Bandit 的漏洞扫描
- **类型检查**:mypy 的静态类型分析
- **构建验证**:EPUB 生成测试

## 本地运行测试

### 前提条件

```bash
# 安装 uv(快速 Python 包管理器)
pip install uv

# 或 macOS 使用 Homebrew
brew install uv
```

### 环境搭建

```bash
# 克隆仓库
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# 创建虚拟环境
uv venv

# 激活环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 安装开发依赖
uv pip install -r requirements-dev.txt
```

### 运行测试

```bash
# 运行全部单元测试
pytest scripts/tests/ -v

# 带覆盖率运行测试
pytest scripts/tests/ -v --cov=scripts --cov-report=html

# 运行特定测试文件
pytest scripts/tests/test_build_epub.py -v

# 运行特定测试函数
pytest scripts/tests/test_build_epub.py::test_function_name -v

# 以监视模式运行测试(需要 pytest-watch)
ptw scripts/tests/
```

### 运行 Linting

```bash
# 检查代码格式
ruff format --check scripts/

# 自动修复格式问题
ruff format scripts/

# 运行 linter
ruff check scripts/

# 自动修复 linter 问题
ruff check --fix scripts/
```

### 运行安全扫描

```bash
# 运行 Bandit 安全扫描
bandit -c pyproject.toml -r scripts/ --exclude scripts/tests/

# 生成 JSON 报告
bandit -c pyproject.toml -r scripts/ --exclude scripts/tests/ -f json -o bandit-report.json
```

### 运行类型检查

```bash
# 使用 mypy 检查类型
mypy scripts/ --ignore-missing-imports --no-implicit-optional
```

## GitHub Actions 工作流

### 触发条件

- **Push** 到 `main` 或 `develop` 分支(当脚本变更时)
- **Pull Request** 到 `main`(当脚本变更时)
- 手动触发工作流

### 任务(Jobs)

#### 1. 单元测试 (pytest)

- **运行环境**:Ubuntu latest
- **Python 版本**:3.10、3.11、3.12
- **执行内容**:
  - 从 `requirements-dev.txt` 安装依赖
  - 运行 pytest 并生成覆盖率报告
  - 上传覆盖率到 Codecov
  - 归档测试结果和覆盖率 HTML

**结果**:任何测试失败则工作流失败(关键任务)

#### 2. 代码质量 (Ruff)

- **运行环境**:Ubuntu latest
- **Python 版本**:3.11
- **执行内容**:
  - 使用 `ruff format` 检查代码格式
  - 使用 `ruff check` 运行 linter
  - 报告问题但不阻断工作流

**结果**:非阻塞(仅警告)

#### 3. 安全扫描 (Bandit)

- **运行环境**:Ubuntu latest
- **Python 版本**:3.11
- **执行内容**:
  - 扫描安全漏洞
  - 生成 JSON 报告
  - 上传报告为产物

**结果**:非阻塞(仅警告)

#### 4. 类型检查 (mypy)

- **运行环境**:Ubuntu latest
- **Python 版本**:3.11
- **执行内容**:
  - 执行静态类型分析
  - 报告类型不匹配
  - 提早发现 Bug

**结果**:非阻塞(仅警告)

#### 5. 构建 EPUB

- **运行环境**:Ubuntu latest
- **依赖**:pytest、lint、security(必须全部通过)
- **执行内容**:
  - 使用 `scripts/build_epub.py` 构建 EPUB 文件
  - 验证 EPUB 创建成功
  - 上传 EPUB 为产物

**结果**:构建失败则工作流失败(关键任务)

#### 6. 汇总

- **运行环境**:Ubuntu latest
- **依赖**:所有其他任务
- **执行内容**:
  - 生成工作流摘要
  - 列出所有产物
  - 报告整体状态

## 编写测试

### 测试结构

测试应放置在 `scripts/tests/` 目录下,命名为 `test_*.py`:

```python
# scripts/tests/test_example.py
import pytest
from scripts.example_module import some_function

def test_basic_functionality():
    """测试 some_function 是否正常工作。"""
    result = some_function("input")
    assert result == "expected_output"

def test_error_handling():
    """测试 some_function 是否能优雅处理错误。"""
    with pytest.raises(ValueError):
        some_function("invalid_input")

@pytest.mark.asyncio
async def test_async_function():
    """测试异步函数。"""
    result = await async_function()
    assert result is not None
```

### 测试最佳实践

- **使用描述性名称**:`test_function_returns_correct_value()`
- **每个测试一个断言**(尽可能):更易调试失败
- **使用 Fixtures 复用设置**:参见 `scripts/tests/conftest.py`
- **模拟外部服务**:使用 `unittest.mock` 或 `pytest-mock`
- **测试边缘情况**:空输入、None 值、错误
- **保持测试快速**:避免 sleep() 和外部 I/O
- **使用 pytest 标记**:`@pytest.mark.slow` 标记慢速测试

### Fixtures

通用 Fixtures 定义在 `scripts/tests/conftest.py` 中:

```python
# 在测试中使用 fixtures
def test_something(tmp_path):
    """tmp_path fixture 提供临时目录。"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    assert test_file.read_text() == "content"
```

## 覆盖率报告

### 本地覆盖率

```bash
# 生成覆盖率报告
pytest scripts/tests/ --cov=scripts --cov-report=html

# 在浏览器中打开覆盖率报告
open htmlcov/index.html
```

### 覆盖率目标

- **最低覆盖率**:80%
- **分支覆盖率**:启用
- **重点领域**:核心功能和错误路径

## Pre-commit Hooks

项目使用 pre-commit hooks 在提交前自动运行检查:

```bash
# 安装 pre-commit hooks
pre-commit install

# 手动运行 hooks
pre-commit run --all-files

# 跳过某次提交的 hooks(不推荐)
git commit --no-verify
```

`.pre-commit-config.yaml` 中配置的 hooks:
- Ruff 格式化工具
- Ruff linter
- Bandit 安全扫描器
- YAML 校验
- 文件大小检查
- 合并冲突检测

## 故障排除

### 本地测试通过但 CI 失败

常见原因:
1. **Python 版本差异**:CI 使用 3.10、3.11、3.12
2. **缺失依赖**:更新 `requirements-dev.txt`
3. **平台差异**:路径分隔符、环境变量
4. **不稳定测试**:依赖时间或顺序的测试

解决方案:
```bash
# 使用相同 Python 版本测试
uv python install 3.10 3.11 3.12

# 使用干净环境测试
rm -rf .venv
uv venv
uv pip install -r requirements-dev.txt
pytest scripts/tests/
```

### Bandit 误报

某些安全警告可能是误报。在 `pyproject.toml` 中配置:

```toml
[tool.bandit]
exclude_dirs = ["scripts/tests"]
skips = ["B101"]  # 跳过 assert_used 警告
```

### 类型检查过严

对特定文件放宽类型检查:

```python
# 在文件顶部添加
# type: ignore

# 或针对特定行
some_dynamic_code()  # type: ignore
```

## CI 最佳实践

1. **保持测试快速**:每个测试应在 <1 秒内完成
2. **不测试外部 API**:模拟外部服务
3. **独立测试**:每个测试应相互独立
4. **使用清晰的断言**:`assert x == 5` 而非 `assert x`
5. **处理异步测试**:使用 `@pytest.mark.asyncio`
6. **生成报告**:覆盖率、安全扫描、类型检查

## 资源

- [pytest 文档](https://docs.pytest.org/)
- [Ruff 文档](https://docs.astral.sh/ruff/)
- [Bandit 文档](https://bandit.readthedocs.io/)
- [mypy 文档](https://mypy.readthedocs.io/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

## 贡献测试

提交 PR 时:

1. **编写测试**用于新功能
2. **本地运行测试**:`pytest scripts/tests/ -v`
3. **检查覆盖率**:`pytest scripts/tests/ --cov=scripts`
4. **运行 linting**:`ruff check scripts/`
5. **安全扫描**:`bandit -r scripts/ --exclude scripts/tests/`
6. **更新文档**如测试有变更

所有 PR 必须包含测试!🧪

---

如有测试相关问题,请发起 GitHub Issue 或讨论。
