#!/bin/bash
# GitHub Releases 重建脚本
# 用途：删除旧 Release 并使用简洁格式重新创建

set -e

REPO="Rx782-Fss/claude-howto-zh"
API_BASE="https://api.github.com/repos/$REPO"

echo "🔧 GitHub Releases 重建工具"
echo "=========================="
echo ""

# 检查 Token
if [ -z "$1" ]; then
    echo "❌ 错误: 请提供 GitHub Personal Access Token"
    echo ""
    echo "用法: $0 <GITHUB_TOKEN>"
    echo ""
    echo "获取 Token:"
    echo "1. 访问 https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token (classic)'"
    echo "3. 勾选 'repo' 权限"
    echo "4. 生成并复制 Token"
    exit 1
fi

TOKEN="$1"
AUTH_HEADER="Authorization: token $TOKEN"

echo "✅ Token 已接收"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# API 调用函数
api_get() {
    curl -s -H "$AUTH_HEADER" -H "Accept: application/vnd.github.v3+json" "$1"
}

api_delete() {
    curl -s -o /dev/null -w "%{http_code}" -X DELETE -H "$AUTH_HEADER" "$1"
}

api_post() {
    curl -s -H "$AUTH_HEADER" -H "Accept: application/vnd.github.v3+json" "$1" -d "$2"
}

# Step 1: 获取现有 Releases
echo -e "${BLUE}[步骤 1/4] 获取现有 Releases...${NC}"
RELEASES_JSON=$(api_get "$API_BASE/releases?per_page=100")
RELEASE_COUNT=$(echo "$RELEASES_JSON" | jq '. | length')

echo -e "找到 $RELEASE_COUNT 个现有 Release"

if [ "$RELEASE_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  没有 Release 需要删除${NC}"
else
    echo ""
    echo "现有 Release 列表:"
    echo "$RELEASES_JSON" | jq -r '.[] | "  - \(.tag_name) (ID: \(.id))"'
fi
echo ""

# Step 2: 删除现有 Releases
echo -e "${BLUE}[步骤 2/4] 删除现有 Releases...${NC}"

DELETED_COUNT=0
for RELEASE_ID in $(echo "$RELEASES_JSON" | jq -r '.[].id'); do
    TAG_NAME=$(echo "$RELEASES_JSON" | jq -r ".[] | select(.id==$RELEASE_ID) | .tag_name")
    HTTP_CODE=$(api_delete "$API_BASE/releases/$RELEASE_ID")

    if [ "$HTTP_CODE" = "204" ]; then
        echo -e "  ${GREEN}✅ 已删除${NC} $TAG_NAME (ID: $RELEASE_ID)"
        DELETED_COUNT=$((DELETED_COUNT + 1))
    else
        echo -e "  ${RED}❌ 删除失败${NC} $TAG_NAME (HTTP: $HTTP_CODE)"
    fi
    
    sleep 1  # 避免 API 限流
done

echo -e "\n共删除 $DELETED_COUNT 个 Release\n"

# Step 3: 从 RELEASE_NOTES.md 提取各版本内容
echo -e "${BLUE}[步骤 3/4] 准备 Release 内容...${NC}"

VERSIONS=("v2.3.2" "v2.3.1" "v2.3.0" "v2.2.0" "v2.1.1" "v2.1.0" "v2.0.0")

declare -A VERSION_CONTENTS

for VERSION in "${VERSIONS[@]}"; do
    # 提取该版本的完整内容（从 ## vX.Y.Z 到下一个 ## 或文件结尾）
    CONTENT=$(sed -n "/^## ${VERSION} -/,/^## v/p" RELEASE_NOTES.md | head -n -1)
    
    if [ -z "$CONTENT" ]; then
        echo -e "  ${RED}❌ 未找到${NC} $VERSION 的内容"
        VERSION_CONTENTS[$VERSION]="## $VERSION\n\n暂无详细说明。"
    else
        # 统计行数
        LINE_COUNT=$(echo -e "$CONTENT" | wc -l)
        echo -e "  ${GREEN}✅${NC} $VERSION ($LINE_COUNT 行)"
        VERSION_CONTENTS[$VERSION]=$CONTENT
    fi
done

echo ""

# Step 4: 创建新 Releases
echo -e "${BLUE}[步骤 4/4] 创建新 Releases...${NC}"
echo ""

CREATED_COUNT=0

for VERSION in "${VERSIONS[@]}"; do
    TAG_NAME="$VERSION"
    RELEASE_NAME="Release $VERSION"  # 简洁的标题！
    BODY="${VERSION_CONTENTS[$VERSION]}"
    
    # 构建 JSON payload
    JSON_PAYLOAD=$(jq -n \
        --arg tag_name "$TAG_NAME" \
        --arg name "$RELEASE_NAME" \
        --arg body "$BODY" \
        --argjson draft "false" \
        --argjson prerelease "false" \
        '{
            tag_name: $tag_name,
            name: $name,
            body: $body,
            draft: $draft,
            prerelease: $prerelease
        }')
    
    # 调用 API 创建 Release
    RESPONSE=$(api_post "$API_BASE/releases" "$JSON_PAYLOAD")
    
    # 检查是否成功
    RELEASE_ID=$(echo "$RESPONSE" | jq -r '.id // empty')
    HTML_URL=$(echo "$RESPONSE" | jq -r '.html_url // empty')
    
    if [ -n "$RELEASE_ID" ] && [ "$RELEASE_ID" != "null" ]; then
        echo -e "  ${GREEN}✅ 已创建${NC} $TAG_NAME"
        echo -e "     标题: $RELEASE_NAME"
        echo -e "     URL:  $HTML_URL"
        CREATED_COUNT=$((CREATED_COUNT + 1))
    else
        ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // "未知错误"')
        echo -e "  ${RED}❌ 创建失败${NC} $TAG_NAME: $ERROR_MSG"
    fi
    
    sleep 1  # 避免 API 限流
done

echo ""
echo "=========================================="
echo -e "${GREEN}✅ 完成！${NC}"
echo ""
echo "统计信息:"
echo "  - 删除旧 Release: $DELETED_COUNT 个"
echo "  - 创建新 Release: $CREATED_COUNT 个"
echo "  - 总计版本数:     ${#VERSIONS[@]} 个"
echo ""
echo "所有 Release 现在使用简洁格式:"
echo "  - 标题: 'Release vX.Y.Z'"
echo "  - 内容: 来自优化后的 RELEASE_NOTES.md"
echo ""
echo -e "${BLUE}访问查看:${NC}"
echo "  https://github.com/$REPO/releases"
echo "=========================================="