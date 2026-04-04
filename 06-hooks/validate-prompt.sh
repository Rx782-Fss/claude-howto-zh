#!/bin/bash
# 校验用户输入的 Prompt
# 钩子类型：UserPromptSubmit

# 从标准输入读取 Prompt 内容
PROMPT=$(cat)

echo "🔍 正在校验 Prompt..."

# 检查危险操作
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "delete database"
  "drop database"
  "format disk"
  "dd if="
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$PROMPT" | grep -qi "$pattern"; then
    echo "❌ 已阻止：检测到危险操作：$pattern"
    exit 1
  fi
done

# 检查生产环境部署
if echo "$PROMPT" | grep -qiE "(deploy|push).*production"; then
  if [ ! -f ".deployment-approved" ]; then
    echo "❌ 已阻止：生产环境部署需要审批通过"
    echo "请创建 .deployment-approved 文件以继续操作"
    exit 1
  fi
fi

echo "✅ Prompt 校验通过"
exit 0
