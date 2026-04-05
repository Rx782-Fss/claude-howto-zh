#!/bin/bash
# 文件写入后执行安全扫描
# 钩子类型：PostToolUse:Write

FILE=$1

if [ -z "$FILE" ]; then
  echo "用法: $0 <文件路径>"
  exit 0
fi

echo "🔒 正在对文件进行安全扫描：$FILE"

ISSUES_FOUND=0

# 检测硬编码的密码
if grep -qE "(password|passwd|pwd)\s*=\s*['\"][^'\"]+['\"]" "$FILE"; then
  echo "⚠️  警告：在 $FILE 中检测到可能的硬编码密码"
  ISSUES_FOUND=1
fi

# 检测硬编码的 API Key
if grep -qE "(api[_-]?key|apikey|access[_-]?token)\s*=\s*['\"][^'\"]+['\"]" "$FILE"; then
  echo "⚠️  警告：在 $FILE 中检测到可能的硬编码 API Key"
  ISSUES_FOUND=1
fi

# 检测硬编码的密钥
if grep -qE "(secret|token)\s*=\s*['\"][^'\"]+['\"]" "$FILE"; then
  echo "⚠️  警告：在 $FILE 中检测到可能的硬编码密钥"
  ISSUES_FOUND=1
fi

# 检测私钥
if grep -q "BEGIN.*PRIVATE KEY" "$FILE"; then
  echo "⚠️  警告：在 $FILE 中检测到私钥"
  ISSUES_FOUND=1
fi

# 检测 AWS 密钥
if grep -qE "AKIA[0-9A-Z]{16}" "$FILE"; then
  echo "⚠️  警告：在 $FILE 中检测到 AWS 访问密钥"
  ISSUES_FOUND=1
fi

exit $ISSUES_FOUND
