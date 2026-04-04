#!/usr/bin/env python3
"""
上下文用量追踪器 — 跟踪每次请求的 Token 消耗量。

使用 UserPromptSubmit 作为"消息前"钩子，Stop 作为"响应后"钩子，
来计算每次请求的 Token 用量差值。

本版本使用基于字符数的估算（无外部依赖）。
如需更高精度，请参阅 context-tracker-tiktoken.py。

使用方法：
    将两个钩子配置为使用同一个脚本：
    - UserPromptSubmit：保存当前 Token 计数
    - Stop：计算差值并报告使用情况
"""
import json
import os
import sys
import tempfile

# 配置项
CONTEXT_LIMIT = 128000  # Claude 的上下文窗口大小（根据你的模型调整）


def get_state_file(session_id: str) -> str:
    """获取用于存储消息前 Token 计数的临时文件路径，按会话隔离。"""
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")


def count_tokens_estimate(text: str) -> int:
    """
    使用基于字符数的近似方法估算 Token 数量。
    
    使用约每 4 个字符对应 1 个 Token 的比例，对英文文本可达到约 80-90% 的准确率。
    对代码和非英文文本的准确性较低。
    """
    return len(text) // 4


def read_transcript(transcript_path: str) -> str:
    """读取并拼接对话记录文件中的所有内容。"""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    content = []
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                # 从各种消息格式中提取文本内容
                if isinstance(entry, dict):
                    if "message" in entry:
                        msg = entry["message"]
                        if isinstance(msg, dict) and "content" in msg:
                            content.append(str(msg["content"]))
                    elif "content" in entry:
                        content.append(str(entry["content"]))
                    elif "text" in entry:
                        content.append(str(entry["text"]))
            except json.JSONDecodeError:
                continue
    return "\n".join(content)


def main():
    """主函数：根据传入的参数执行相应操作。"""
    if len(sys.argv) < 2:
        print("用法: python context-tracker.py <save|report> [session_id] [transcript_path]")
        sys.exit(1)

    action = sys.argv[1]
    session_id = sys.argv[2] if len(sys.argv) > 2 else "default"
    transcript_path = sys.argv[3] if len(sys.argv) > 3 else None

    if action == "save":
        # 在 UserPromptSubmit 时保存当前 Token 计数
        if transcript_path:
            text = read_transcript(transcript_path)
        else:
            text = ""
        
        token_count = count_tokens_estimate(text)
        
        state_file = get_state_file(session_id)
        with open(state_file, "w") as f:
            json.dump({"tokens": token_count, "timestamp": time.time()}, f)
    
    elif action == "report":
        # 在 Stop 时计算差值并报告使用情况
        if transcript_path:
            current_text = read_transcript(transcript_path)
        else:
            current_text = ""
        
        current_tokens = count_tokens_estimate(current_text)
        
        state_file = get_state_file(session_id)
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                saved_data = json.load(f)
            previous_tokens = saved_data.get("tokens", 0)
        else:
            previous_tokens = 0
        
        delta = current_tokens - previous_tokens
        usage_percent = (current_tokens / CONTEXT_LIMIT) * 100
        
        print(f"📊 本次请求使用了 ~{delta} 个 Token")
        print(f"📈 当前总用量: ~{current_tokens}/{CONTEXT_LIMIT} ({usage_percent:.1f}%)")

if __name__ == "__main__":
    import time
    main()
