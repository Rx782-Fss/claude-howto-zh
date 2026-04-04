#!/usr/bin/env python3
"""
上下文用量追踪器（tiktoken 版本）— 追踪每次请求的 Token 消耗量。

使用 UserPromptSubmit 作为"消息前"钩子，Stop 作为"响应后"钩子，
来计算每次请求的 Token 用量差值。

此版本使用 tiktoken 的 p50k_base 编码，准确率约 90-95%。
依赖：pip install tiktoken

如需零依赖版本，请参见 context-tracker.py。

用法:
    配置两个钩子使用同一脚本：
    - UserPromptSubmit: 保存当前 token 计数
    - Stop: 计算差值并报告用量
"""
import json
import os
import sys
import tempfile

try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print(
        "Warning: tiktoken not installed. Install with: pip install tiktoken",
        file=sys.stderr,
    )

# 配置
CONTEXT_LIMIT = 128000  # Claude 的上下文窗口大小（根据模型调整）


def get_state_file(session_id: str) -> str:
    """获取用于存储消息前 token 计数的临时文件路径，按会话隔离。"""
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")


def count_tokens(text: str) -> int:
    """
    使用 tiktoken 的 p50k_base 编码统计 token 数。

    与 Claude 实际的分词器相比，准确率约 90-95%。
    如果 tiktoken 不可用，则回退到字符估算。

    注意：Anthropic 尚未发布官方的离线分词器。
    由于 Claude 和 GPT 模型都使用 BPE（字节对编码），
    tiktoken 的 p50k_base 是一个合理的近似方案。
    """
    if TIKTOKEN_AVAILABLE:
        enc = tiktoken.get_encoding("p50k_base")
        return len(enc.encode(text))
    else:
        # 回退到字符估算（约每 4 个字符 = 1 个 token）
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
                if "message" in entry:
                    msg = entry["message"]
                    if isinstance(msg.get("content"), str):
                        content.append(msg["content"])
                    elif isinstance(msg.get("content"), list):
                        for block in msg["content"]:
                            if isinstance(block, dict) and block.get("type") == "text":
                                content.append(block.get("text", ""))
            except json.JSONDecodeError:
                continue

    return "\n".join(content)


def handle_user_prompt_submit(data: dict) -> None:
    """消息前钩子：在请求前保存当前 token 计数。"""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 保存到临时文件供后续比较
    state_file = get_state_file(session_id)
    with open(state_file, "w") as f:
        json.dump({"pre_tokens": current_tokens}, f)


def handle_stop(data: dict) -> None:
    """响应后钩子：计算并报告 token 差值。"""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 加载消息前的计数
    state_file = get_state_file(session_id)
    pre_tokens = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
                pre_tokens = state.get("pre_tokens", 0)
        except (json.JSONDecodeError, IOError):
            pass

    # 计算差值
    delta_tokens = current_tokens - pre_tokens
    remaining = CONTEXT_LIMIT - current_tokens
    percentage = (current_tokens / CONTEXT_LIMIT) * 100

    # 报告用量（输出到 stderr 以免干扰钩子的正常输出）
    method = "tiktoken" if TIKTOKEN_AVAILABLE else "estimated"
    print(
        f"Context ({method}): ~{current_tokens:,} tokens "
        f"({percentage:.1f}% used, ~{remaining:,} remaining)",
        file=sys.stderr,
    )
    if delta_tokens > 0:
        print(f"This request: ~{delta_tokens:,} tokens", file=sys.stderr)


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        handle_user_prompt_submit(data)
    elif event == "Stop":
        handle_stop(data)

    sys.exit(0)


if __name__ == "__main__":
    main()
