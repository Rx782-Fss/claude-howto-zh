#!/usr/bin/env bash
# SessionEnd hook（会话结束钩子）: 提示用户输入学习的模块，然后将会话记录
# 追加到 ~/.claude-howto-progress.json 以实现持久化的学习进度跟踪。
#
# 在 Claude Code 会话终止时触发一次——不是每次响应后都触发。
# 使用 /dev/tty 进行交互式输入，因为 stdin 承载了 hook 的 JSON 载荷。
#
# 安装方法: 将其添加到 .claude/settings.json 的 "SessionEnd" 事件下（见下方说明）。

PROGRESS_FILE="$HOME/.claude-howto-progress.json"

# 守护条件：仅在此仓库内运行
if [[ "$CLAUDE_PROJECT_DIR" != *"claude-howto"* ]] && [[ "$PWD" != *"claude-howto"* ]]; then
  exit 0
fi

# 如果进度文件不存在则创建
if [ ! -f "$PROGRESS_FILE" ]; then
  echo '{"sessions":[]}' > "$PROGRESS_FILE"
fi

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Claude Code — 学习会话结束"
echo " $DATE $TIME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo " 你学习了哪些模块？（例如 06,07 或按 Enter 跳过）"
echo " 01=Slash  02=Memory  03=Skills  04=Subagents  05=MCP"
echo " 06=Hooks  07=Plugins 08=Checkpoints 09=Advanced 10=CLI"
echo ""
printf " > "
read -r INPUT </dev/tty

if [ -z "$INPUT" ] || [ "$INPUT" = "skip" ]; then
  echo " 已跳过——未记录会话。"
  echo ""
  exit 0
fi

# 将短数字映射为模块名称（使用 for 循环避免管道+while，因为 bash 3.2 无法解析后者）
IFS=',' read -ra PARTS <<< "$INPUT"
MODULES_JSON=""
for m in "${PARTS[@]}"; do
  m="${m// /}"  # 去除空格
  case "$m" in
    01) label='"01-slash-commands"' ;;
    02) label='"02-memory"' ;;
    03) label='"03-skills"' ;;
    04) label='"04-subagents"' ;;
    05) label='"05-mcp"' ;;
    06) label='"06-hooks"' ;;
    07) label='"07-plugins"' ;;
    08) label='"08-checkpoints"' ;;
    09) label='"09-advanced-features"' ;;
    10) label='"10-cli"' ;;
    *)  label="\"$m\"" ;;
  esac
  MODULES_JSON="${MODULES_JSON:+$MODULES_JSON,}$label"
done

printf " 备注？（可选，按 Enter 跳过）："
read -r NOTES </dev/tty

# 将 NOTES 作为单独的参数传递，以便 Python 处理 JSON 转义——
# 避免当备注包含引号或反斜杠时 JSON 损坏。
python3 - "$PROGRESS_FILE" "$DATE" "$TIME" "$MODULES_JSON" "$NOTES" <<'PYEOF'
import sys, json

path, date, time_str, modules_raw, notes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

new_session = {
    "date": date,
    "time": time_str,
    "modules": json.loads(f"[{modules_raw}]") if modules_raw else [],
    "notes": notes,
}

with open(path, 'r') as f:
    data = json.load(f)

data.setdefault('sessions', []).append(new_session)

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
PYEOF

echo ""
echo " 已保存到 $PROGRESS_FILE"
[ -n "$NOTES" ] && echo " 备注: $NOTES"
echo ""
