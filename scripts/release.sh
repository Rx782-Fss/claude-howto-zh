#!/bin/bash
# release.sh - 标准化 Release 发布脚本
# 用途：自动化完成版本发布的所有步骤
# 使用方法: bash release.sh [版本号]
# 示例: bash release.sh v2.4.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${blue}🚀 Release 版本发布工具${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 获取版本号
if [ -n "$1" ]; then
    NEW_VERSION="$1"
else
    # 从 .version 读取
    if [ -f ".version" ]; then
        NEW_VERSION=$(cat .version)
    else
        echo -e "${RED}❌ 错误：未提供版本号且 .version 文件不存在${NC}"
        echo "用法: bash release.sh <版本号>"
        echo "示例: bash release.sh v2.4.0"
        exit 1
    fi
fi

# 验证版本号格式
if [[ ! "$NEW_VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}❌ 错误：版本号格式不正确（应为 vX.Y.Z）${NC}"
    exit 1
fi

echo -e "准备发布版本: ${GREEN}${NEW_VERSION}${NC}"
echo ""

# 确认操作
read -p "确认继续发布？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消发布。${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}=== 开始发布流程 ===${NC}"
echo ""

# 步骤 1: 运行发布前检查
echo -e "${BLUE}[步骤 1/6] 运行发布前检查...${NC}"
if [ -f "scripts/release-check.sh" ]; then
    bash scripts/release-check.sh
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 发布前检查失败，中止发布${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️ 未找到 release-check.sh，跳过检查${NC}"
fi
echo ""

# 步骤 2: 更新 .version 文件（如果需要）
echo -e "${BLUE}[步骤 2/6] 更新版本标记文件...${NC}"
echo "$NEW_VERSION" > .version
echo -e "✅ .version 已更新为: ${NEW_VERSION}"
echo ""

# 步骤 3: 提交更改
echo -e "${BLUE}[步骤 3/6] 提交更改到 Git...${NC}"
git add .version RELEASE_NOTES.md
git commit -m "release: 准备发布 ${NEW_VERSION}" || true
echo -e "✅ 已提交"
echo ""

# 步骤 4: 创建 Git 标签
echo -e "${BLUE}[步骤 4/6] 创建 Git 标签...${NC}"

# 使用简洁格式的标签消息（符合规范）
TAG_MESSAGE="Release ${NEW_VERSION}"

git tag -a "${NEW_VERSION}" -m "${TAG_MESSAGE}"
echo -e "✅ Git 标签已创建: ${NEW_VERSION}"
echo "   消息: ${TAG_MESSAGE}"
echo ""

# 步骤 5: 推送到 GitHub
echo -e "${BLUE}[步骤 5/6] 推送到 GitHub...${NC}"
git push origin main --tags
echo -e "✅ 已推送到 GitHub"
echo ""

# 步骤 6: 创建 GitHub Release
echo -e "${BLUE}[步骤 6/6] 创建 GitHub Release...${NC}"

# 检查 GITHUB_TOKEN 是否设置
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠️ GITHUB_TOKEN 未设置，跳过自动创建 Release${NC}"
    echo ""
    echo "您可以手动在 GitHub 网页上创建 Release:"
    echo "👉 https://github.com/Rx782-Fss/claude-howto-zh/releases/new"
    echo ""
    echo "选择 tag: ${NEW_VERSION}"
else
    # 生成 Release body
    RELEASE_BODY=$(cat <<EOF
## ✨ ${NEW_VERSION} - $(date '+%Y-%m-%d')

### 🎯 核心成果

$(sed -n '/^## '${NEW_VERSION}'/,/^## /p' RELEASE_NOTES.md | head -20)

### 📊 详细信息

请查看完整的 [RELEASE_NOTES.md](RELEASE_NOTES.md) 了解详细变更日志。

---

**升级方式**:
\`\`\`bash
git pull origin main
\`\`\`
EOF
)

    # 调用 GitHub API 创建 Release
    RESPONSE=$(curl -s -X POST \
        https://api.github.com/repos/Rx782-Fss/claude-howto-zh/releases \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "{
            \"tag_name\": \"${NEW_VERSION}\",
            \"target_commitish\": \"main\",
            \"name\": \"Release ${NEW_VERSION}\",
            \"body\": $(echo "$RELEASE_BODY" | python3 -c 'import sys, json; print(json.dumps(sys.stdin.read()))'),
            \"draft\": false,
            \"prerelease\": false
        }")

    # 检查响应
    if echo "$RESPONSE" | grep -q '"html_url"'; then
        RELEASE_URL=$(echo "$RESPONSE" | grep -o '"html_url": "[^"]*"' | cut -d'"' -f4)
        echo -e "✅ GitHub Release 已创建"
        echo -e "🔗 ${GREEN}${RELEASE_URL}${NC}"
    else
        echo -e "${YELLOW}⚠️ Release 创建可能失败，请手动检查${NC}"
        echo "响应: $RESPONSE"
    fi
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Release ${NEW_VERSION} 发布成功！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "📦 版本信息:"
echo "   • 版本号: ${NEW_VERSION}"
echo "   • Git 标签: ${NEW_VERSION}"
echo "   • Release URL: https://github.com/Rx782-Fss/claude-howto-zh/releases/tag/${NEW_VERSION}"
echo ""
echo "🔗 快速访问:"
echo "   • GitHub Releases: https://github.com/Rx782-Fss/claude-howto-zh/releases"
echo "   • Git Tags: https://github.com/Rx782-Fss/claude-howto-zh/tags"
echo ""
echo "🎉 感谢使用！"
