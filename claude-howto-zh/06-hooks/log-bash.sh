#!/bin/bash
# 记录所有 Bash 命令
# 钩子类型：PostToolUse:Bash

COMMAND="$1"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
LOGFILE="$HOME/.claude/bash-commands.log"

# 如果日志目录不存在则创建
mkdir -p "$(dirname "$LOGFILE")"

# 写入命令日志
echo "[$TIMESTAMP] $COMMAND" >> "$LOGFILE"

# 可选：同时写入系统日志
# logger -t "claude-bash" "$COMMAND"

exit 0
