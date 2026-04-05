#!/usr/bin/env bash
# =============================================================================
# claude-howto 中文翻译版 — 更新脚本
# =============================================================================
# 用法：
#   ./scripts/update_translation.sh check      # 检查是否有新版本
#   ./scripts/update_translation.sh fetch      # 下载最新源码到临时目录
#   ./scripts/update_translation.sh diff       # 对比差异，生成报告
#   ./scripts/update_translation.sh full       # 完整流程（check → fetch → diff）
#   ./scripts/update_translation.sh mermaid extract  # 提取原版Mermaid图表到reference/
#   ./scripts/update_translation.sh mermaid compare  # 对比原版与翻译版的图表结构
#   ./scripts/update_translation.sh mermaid fix      # 自动修复GitHub兼容性问题
#   ./scripts/update_translation.sh mermaid verify   # 最终扫描确认零问题
#   ./scripts/update_translation.sh mermaid full     # 完整Mermaid流程 (extract→compare→fix→verify)
#
# 环境变量（可选覆盖）：
#   OB_VAULT_PATH    — Obsidian 知识库根目录（默认自动检测）
#   SRC_DIR          — 指定源码目录（默认自动检测）
# =============================================================================

set -euo pipefail

# ======================== 自动推导路径 ========================
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TRANSLATION_DIR="$PROJECT_ROOT/claude-howto-zh"
SRC_BASE="/tmp/claude-howto-src"
REFERENCE_DIR="$PROJECT_ROOT/reference/mermaid-original"

OB_VAULT="${OB_VAULT_PATH:-}"
VERSION_FILE="$TRANSLATION_DIR/.version"
GITHUB_REPO="luongnv89/claude-howto"

# 排除的文件/目录（不需要翻译的）
EXCLUDE_PATTERNS=(
    ".git"
    ".obsidian"
    "slides/"
    "assets/logo/"
    ".gitignore"
    ".cspell"
    ".markdownlint"
    ".pre-commit"
    "LICENSE"
    "coverage.xml"
    "pyproject.toml"
    "requirements"
    "scripts/tests/"
    ".github/workflows/"
    ".github/FUNDING.yml"
    ".github/markdown-link-check"
)

# 只关注的文件扩展名
EXTENSIONS=("md" "py" "sh" "js" "json" "txt" "yml" "yaml")

# ======================== 工具函数 ========================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()   { echo -e "${RED}[ERROR]${NC} $*"; }
header() { echo -e "\n${BOLD}══════════════════════════════════════════════════════════${NC}"; echo -e "${BOLD}  $*${NC}"; echo -e "${BOLD}══════════════════════════════════════════════════════════${NC}\n"; }

check_cmd() {
    command -v "$1" >/dev/null 2>&1 || { err "需要安装 $1"; exit 1; }
}

should_track() {
    local f="$1"
    for pat in "${EXCLUDE_PATTERNS[@]}"; do
        [[ "$f" == *"$pat"* ]] && return 1
    done
    local ext="${f##*.}"
    for e in "${EXTENSIONS[@]}"; do
        [[ "$ext" == "$e" ]] && return 0
    done
    return 1
}

resolve_ob_path() {
    if [ -n "$OB_VAULT" ]; then
        echo "$OB_VAULT/40_学习资料/Claude Howto"
        return
    fi
    # 自动检测常见位置
    for candidate in \
        "$HOME/data/知识库/40_学习资料/Claude Howto" \
        "$HOME/知识库/40_学习资料/Claude Howto" \
        "$HOME/Documents/知识库/40_学习资料/Claude Howto"; do
        if [ -d "$candidate" ]; then
            echo "$candidate"
            return
        fi
    done
    echo ""
}

# ======================== 子命令 ========================

cmd_check() {
    header "检查原项目版本"

    info "查询 GitHub Releases API..."
    local release_json
    release_json=$(curl -sf "https://api.github.com/repos/$GITHUB_REPO/releases/latest") || {
        err "无法连接 GitHub API"
        exit 1
    }

    LATEST_TAG=$(echo "$release_json" | grep '"tag_name"' | sed 's/.*: "//;s/".*//')
    LATEST_NAME=$(echo "$release_json" | grep '"name"' | sed 's/.*: "//;s/".*//')
    PUBLISHED_AT=$(echo "$release_json" | grep '"published_at"' | sed 's/.*: "//;s/".*//')

    ok "最新版本: $LATEST_NAME ($LATEST_TAG)"
    ok "发布时间: $PUBLISHED_AT"

    local current=""
    if [ -f "$VERSION_FILE" ]; then
        current=$(cat "$VERSION_FILE")
        ok "当前翻译版本: $current"
    else
        warn "未找到版本记录 ($VERSION_FILE)"
        current="未知"
    fi

    if [ "$current" = "$LATEST_TAG" ]; then
        ok "已是最新版本，无需更新"
        return 0
    else
        warn "发现新版本！$current -> $LATEST_TAG"
        echo ""
        echo "$release_json" | grep '"body"' | sed 's/.*: "//;s/".*//' | head -30
        return 1
    fi
}

cmd_fetch() {
    header "下载最新源码"

    local latest_tag
    latest_tag=$(curl -sf "https://api.github.com/repos/$GITHUB_REPO/releases/latest" | grep '"tag_name"' | sed 's/.*: "//;s/".*//')

    if [ -z "$latest_tag" ]; then
        err "无法获取最新版本号"
        exit 1
    fi

    local target_dir="$SRC_BASE/${latest_tag}"

    if [ -d "$target_dir" ]; then
        ok "$latest_tag 已存在，跳过下载"
        SRC_DIR="$target_dir"
        return 0
    fi

    info "下载 $latest_tag ..."

    mkdir -p "$SRC_BASE"

    local tmp_zip="$SRC_BASE/latest.zip"
    curl -sL "https://api.github.com/repos/$GITHUB_REPO/zipball/$latest_tag" -o "$tmp_zip"

    local tmp_extract="$SRC_BASE/_extract_$(date +%s)"
    mkdir -p "$tmp_extract"
    unzip -q "$tmp_zip" -d "$tmp_extract"

    local extracted_dir
    extracted_dir=$(find "$tmp_extract" -mindepth 1 -maxdepth 1 -type d | head -1)
    mv "$extracted_dir" "$target_dir"

    rm -rf "$tmp_extract" "$tmp_zip"

    ok "已下载到 $target_dir"
    export SRC_DIR="$target_dir"
}

cmd_diff() {
    header "对比差异"

    local src_dir=""
    if [ -n "${SRC_DIR:-}" ] && [ -d "$SRC_DIR" ]; then
        src_dir="$SRC_DIR"
    elif [ -d "$SRC_BASE/claude-howto-main" ]; then
        src_dir="$SRC_BASE/claude-howto-main"
    else
        src_dir=$(ls -dt "$SRC_BASE"/* 2>/dev/null | head -1)
    fi

    if [ ! -d "$src_dir" ]; then
        err "找不到源码目录。请先运行: $0 fetch"
        exit 1
    fi

    # 解析 OB 路径
    local ob_path
    ob_path=$(resolve_ob_path)

    ok "项目根目录: $PROJECT_ROOT"
    ok "翻译目录:   $TRANSLATION_DIR"
    ok "源码目录:   $src_dir"
    if [ -n "$ob_path" ]; then
        ok "OB 手册:    $ob_path"
    else
        warn "OB 手册:    未检测到（设置 OB_VAULT_PATH 环境变量可指定）"
    fi
    echo ""

    # ====== 1. 新增文件 ======
    header "新增文件（需要全新翻译）"
    local new_count=0
    while IFS= read -r -d '' f; do
        local rel="${f#$src_dir/}"
        if ! should_track "$rel"; then continue; fi
        [[ "$rel" == "TRANSLATION-STATUS.md" ]] && continue

        local target="$TRANSLATION_DIR/$rel"
        if [ ! -f "$target" ]; then
            echo "  + $rel"
            ((new_count++)) || true
        fi
    done < <(find "$src_dir" -type f -print0 2>/dev/null | sort -z)

    [ "$new_count" -eq 0 ] && ok "无新增文件" || warn "共 $new_count 个新文件需要翻译"
    echo ""

    # ====== 2. 修改的文件 ======
    header "修改的文件（需要增量翻译）"
    local mod_count=0
    while IFS= read -r -d '' f; do
        local rel="${f#$src_dir/}"
        if ! should_track "$rel"; then continue; fi
        [[ "$rel" == "TRANSLATION-STATUS.md" ]] && continue

        local target="$TRANSLATION_DIR/$rel"
        if [ -f "$target" ]; then
            if ! diff -q "$f" "$target" >/dev/null 2>&1; then
                local added=$(diff --stat "$f" "$target" 2>/dev/null | tail -1)
                echo "  ~ $rel  ($added)"
                ((mod_count++)) || true
            fi
        fi
    done < <(find "$src_dir" -type f -print0 2>/dev/null | sort -z)

    [ "$mod_count" -eq 0 ] && ok "无修改文件" || warn "共 $mod_count 个文件需要增量更新"
    echo ""

    # ====== 3. 删除的文件 ======
    header "删除的文件（需同步清理）"
    local del_count=0
    while IFS= read -r -d '' f; do
        local rel="${f#$TRANSLATION_DIR/}"
        if ! should_track "$rel"; then continue; fi

        local src_file="$src_dir/$rel"
        if [ ! -f "$src_file" ]; then
            echo "  - $rel"
            ((del_count++)) || true
        fi
    done < <(find "$TRANSLATION_DIR" -type f -print0 2>/dev/null | sort -z)

    [ "$del_count" -eq 0 ] && ok "无删除文件" || warn "共 $del_count 个文件需从翻译版中删除"
    echo ""

    # ====== 4. 汇总 ======
    header "更新汇总"
    echo "
  ┌─────────────────┬──────┐
  │ 新增文件        │  ${new_count}   │
  │ 修改文件        │  ${mod_count}   │
  │ 删除文件        │  ${del_count}   │
  ├─────────────────┼──────┤
  │ 总计待处理      │  $(( new_count + mod_count + del_count ))   │
  └─────────────────┴──────┘
    "

    local latest_tag_for_display
    latest_tag_for_display=$(curl -sf "https://api.github.com/repos/$GITHUB_REPO/releases/latest" | grep '"tag_name"' | sed 's/.*: "//;s/".*//')

    if [ "$(( new_count + mod_count + del_count ))" -gt 0 ]; then
        echo "下一步操作:"
        echo "  1. 对新增文件执行完整翻译（遵循 claude-howto-zh/TRANSLATION-STATUS.md 规范）"
        echo "  2. 对修改文件执行 diff，仅翻译变更部分"
        echo "  3. 从翻译版中删除已移除的文件"
        if [ -n "$ob_path" ]; then
            echo "  4. 同步变更到 OB 知识库: $ob_path"
        fi
        echo "  5. 更新版本标记:"
        echo "     echo '$latest_tag_for_display' > $VERSION_FILE"
    fi
}

# ======================== Mermaid 子命令 ========================

_detect_src_dir() {
    if [ -n "${SRC_DIR:-}" ] && [ -d "$SRC_DIR" ]; then
        echo "$SRC_DIR"
        return
    fi
    for d in \
        "$SRC_BASE/claude-howto-main" \
        "/home/hhbbfss/下载/claude-howto-src/claude-howto-main" \
        $(ls -dt "$SRC_BASE"/*/ 2>/dev/null | head -1); do
        if [ -d "$d" ]; then
            echo "$d"
            return
        fi
    done
    err "找不到源码目录，请先运行: $0 fetch"
    exit 1
}

cmd_mermaid_extract() {
    header "提取原版 Mermaid 图表"

    local src_dir
    src_dir=$(_detect_src_dir)
    ok "源码目录: $src_dir"

    rm -rf "$REFERENCE_DIR"
    mkdir -p "$REFERENCE_DIR"

    local total=0
    while IFS= read -r -d '' md_file; do
        local rel_path="${md_file#$src_dir/}"
        local safe_name="${rel_path//\//-}"
        safe_name="${safe_name%.md}"

        local in_mermaid=false
        local block_num=0
        local block_content=""

        while IFS= read -r line || [ -n "$line" ]; do
            if [[ "$line" == '```mermaid' ]]; then
                in_mermaid=true
                ((block_num++)) || true
                block_content=""
                continue
            fi
            if $in_mermaid && [[ "$line" == '```' ]]; then
                in_mermaid=false
                local outfile="$REFERENCE_DIR/${safe_name}_diag${block_num}.mmd"
                echo "$block_content" > "$outfile"
                ((total++)) || true
                continue
            fi
            if $in_mermaid; then
                block_content+="$line"$'\n'
            fi
        done < "$md_file"
    done < <(find "$src_dir" -name "*.md" -type f -print0 2>/dev/null | sort -z)

    ok "已提取 $total 个图表 -> $REFERENCE_DIR/"
    ls "$REFERENCE_DIR"/*.mmd 2>/dev/null | wc -l | xargs -I{} echo "  文件数: {}"
}

cmd_mermaid_compare() {
    header "对比 Mermaid 结构"

    check_cmd "python3"

    local src_dir
    src_dir=$(_detect_src_dir)

    python3 "$SCRIPT_DIR/compare_mermaid.py" 2>&1 || {
        err "对比失败"
        exit 1
    }
}

cmd_mermaid_fix() {
    header "修复 GitHub 兼容性问题"

    local total_fixed=0
    local files_modified=0

    while IFS= read -r -d '' md_file; do
        local orig_content
        orig_content=$(cat "$md_file")

        local fixed_content
        fixed_content=$(python3 -c "
import re, sys
content = sys.stdin.read()

def fix_block(m):
    b = m.group(1)
    # {} 菱形节点含中文 -> []
    b = re.sub(r'\{([^}]+)\}', r'[\1]', b)
    # 全角字符
    fw = {'\uff08':'(', '\uff09':')', '\uff1f':'?', '\uff1a':':', '\uff0c':',', '\uff01':'!'}
    for k,v in fw.items(): b = b.replace(k, v)
    # emoji
    b = re.sub(r'[✅❌👤🧭🟢🔵⚠️❓💡🎯📊]', '', b)
    # <br/> -> 空格
    b = b.replace('<br/>', ' ')
    return '\`\`\`mermaid\n' + b + '\`\`\`'

content = re.sub(r'\`\`\`mermaid\s*\n(.*?)\`\`\`', fix_block, content, flags=re.DOTALL)
sys.stdout.write(content)
" <<< "$orig_content")

        if [ "$fixed_content" != "$orig_content" ]; then
            echo "$fixed_content" > "$md_file"
            local rel="${md_file#$PROJECT_ROOT/}"
            ok "已修复: $rel"
            ((files_modified++)) || true
        fi
    done < <(find "$TRANSLATION_DIR" -name "*.md" -type f -print0 2>/dev/null | sort -z)

    ok "修复完成: $files_modified 个文件"
}

cmd_mermaid_verify() {
    header "验证 GitHub 兼容性"

    check_cmd "python3"

    python3 -c "
import re, os, sys

TRANS_DIR = '$TRANSLATION_DIR'
issues = []
total_diagrams = 0

for root, dirs, files in os.walk(TRANS_DIR):
    for f in files:
        if not f.endswith('.md'): continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
        for block in re.findall(r'\`\`\`mermaid\s*\n(.*?)\`\`\`', content, re.DOTALL):
            total_diagrams += 1
            rel = os.path.relpath(fp, TRANS_DIR)
            # 全角检查
            for ch in ['\uff08','\uff09','\uff1f','\uff1a','\uff0c','\uff01']:
                if ch in block: issues.append(f'{rel}: 全角字符')
            # emoji 检查
            if re.search(r'[✅❌👤🧭🟢🔵⚠️❓💡🎯📊]', block): issues.append(f'{rel}: emoji')
            # <br/> 检查
            if '<br/>' in block: issues.append(f'{rel}: <br/>')
            # {} 中文检查
            if re.search(r'\{[^}]*[\u4e00-\u9fff]', block): issues.append(f'{rel}: 菱形节点含中文')

print(f'扫描文件: {TRANS_DIR}/')
print(f'Mermaid 图表总数: {total_diagrams}')
print(f'发现问题: {len(issues)}')
if issues:
    for x in issues: print(f'  ❌ {x}')
    sys.exit(1)
else:
    print('✅ 零问题！全部通过 GitHub 兼容性检查')
" 2>&1
}

cmd_mermaid() {
    case "${1:-full}" in
        extract) cmd_mermaid_extract ;;
        compare) cmd_mermaid_compare ;;
        fix)     cmd_mermaid_fix ;;
        verify)  cmd_mermaid_verify ;;
        full)
            cmd_mermaid_extract
            cmd_mermaid_compare
            cmd_mermaid_fix
            cmd_mermaid_verify
            ;;
        --help|-h)
            echo "用法: $0 mermaid {extract|compare|fix|verify|full}"
            echo ""
            echo "  extract  从原版提取所有Mermaid图表到 reference/mermaid-original/"
            echo "  compare  对比原版与翻译版的图表结构 (67/67验证)"
            echo "  fix      自动清除全角/emoji/<br/>/{}中文"
            echo "  verify   最终扫描确认零问题"
            echo "  full     完整流程 (extract→compare→fix→verify)"
            ;;
        *)      echo "用法: $0 mermaid {extract|compare|fix|verify|full|--help}" ;;
    esac
}

# ======================== 主入口 ========================

main() {
    check_cmd "curl"
    check_cmd "unzip"

    case "${1:-full}" in
        check)  cmd_check ;;
        fetch)  cmd_fetch ;;
        diff)   cmd_diff ;;
        full)
            cmd_check || true
            cmd_fetch
            cmd_diff
            ;;
        mermaid) shift; cmd_mermaid "${1:-full}" ;;
        --help|-h)
            echo "用法: $0 {check|fetch|diff|full|mermaid|--help}"
            echo ""
            echo "  check          检查原项目是否有新版本"
            echo "  fetch          下载最新源码到临时目录"
            echo "  diff           对比源码与翻译版的差异"
            echo "  full           完整流程 (check -> fetch -> diff)"
            echo ""
            echo "  mermaid extract   提取原版Mermaid图表到 reference/"
            echo "  mermaid compare   对比图表结构 (67/67验证)"
            echo "  mermaid fix       自动修复GitHub兼容性问题"
            echo "  mermaid verify    最终扫描确认零问题"
            echo "  mermaid full      完整Mermaid流程"
            echo ""
            echo "环境变量:"
            echo "  OB_VAULT_PATH   指定 Obsidian 知识库根目录"
            echo "  SRC_DIR         指定源码目录（跳过自动检测）"
            echo ""
            echo "路径（自动推导，无需硬编码）:"
            echo "  项目根目录:     $PROJECT_ROOT"
            echo "  翻译目录:       $TRANSLATION_DIR"
            echo "  源码临时目录:   $SRC_BASE"
            echo "  Mermaid参考:    $REFERENCE_DIR"
            ;;
        *)      echo "用法: $0 {check|fetch|diff|full|mermaid|--help}" ;;
    esac
}

main "$@"
