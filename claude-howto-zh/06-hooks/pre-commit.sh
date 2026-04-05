#!/bin/bash
# 提交前运行测试
# 钩子类型：PreToolUse（匹配器: Bash）— 检测命令是否为 git commit
# 注意：没有"PreCommit"钩子事件。请使用 PreToolUse 配合 Bash 匹配器，
# 并检查命令内容来检测 git commit 操作。

echo "🧪 提交前正在运行测试..."

# 检查是否存在 package.json（Node.js 项目）
if [ -f "package.json" ]; then
  if grep -q '"test"' package.json; then
    npm test
    if [ $? -ne 0 ]; then
      echo "❌ 测试失败！提交已被阻止。"
      exit 1
    fi
  fi
fi

# 检查是否可用 pytest（Python 项目）
if [ -f "pytest.ini" ] || [ -f "setup.py" ]; then
  if command -v pytest &> /dev/null; then
    pytest
    if [ $? -ne 0 ]; then
      echo "❌ 测试失败！提交已被阻止。"
      exit 1
    fi
  fi
fi

# 检查是否存在 go.mod（Go 项目）
if [ -f "go.mod" ]; then
  go test ./...
  if [ $? -ne 0 ]; then
    echo "❌ 测试失败！提交已被阻止。"
    exit 1
  fi
fi

# 检查是否存在 Cargo.toml（Rust 项目）
if [ -f "Cargo.toml" ]; then
  cargo test
  if [ $? -ne 0 ]; then
    echo "❌ 测试失败！提交已被阻止。"
    exit 1
  fi
fi

echo "✅ 所有测试通过！提交可以继续。"
exit 0
