#!/usr/bin/env python3
"""
精确对比并生成 claude_concepts_guide.md 的修复方案
"""

import re

ORIG_FILE = "/home/hhbbfss/下载/claude-howto-src/claude-howto-main/claude_concepts_guide.md"
TRANS_FILE = "/data/hhbbfss/project/tre/claude-howto/claude-howto-zh/claude_concepts_guide.md"

def extract_all_blocks(filepath):
    """提取所有 Mermaid 块及其位置和上下文"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    blocks = []
    in_mermaid = False
    block_start = 0
    block_lines = []

    for i, line in enumerate(lines):
        if '```mermaid' in line:
            in_mermaid = True
            block_start = i
            block_lines = []
        elif in_mermaid and line.strip() == '```':
            in_mermaid = False
            # 获取上下文（前后各2行）
            ctx_before = '\n'.join(lines[max(0,block_start-2):block_start])
            ctx_after = '\n'.join(lines[i+1:i+3])

            raw = '\n'.join(block_lines)

            # 提取关键特征
            first_line = raw.split('\n')[0].strip() if raw else ''
            nodes = re.findall(r'^(\w+)\[', raw, re.MULTILINE)
            conns = sum(1 for l in raw.split('\n') if '-->' in l or '->>' in l)

            blocks.append({
                'index': len(blocks) + 1,
                'start_line': block_start + 1,
                'end_line': i + 1,
                'type': first_line,
                'nodes': nodes[:6],
                'conn_count': conns,
                'raw_preview': raw[:100].replace('\n', ' | '),
                'ctx_before': ctx_before.strip(),
                'ctx_after': ctx_after.strip(),
            })
        elif in_mermaid:
            block_lines.append(line)

    return blocks

def main():
    orig = extract_all_blocks(ORIG_FILE)
    trans = extract_all_blocks(TRANS_FILE)

    print(f"原版: {len(orig)} 个图表")
    print(f"翻译版: {len(trans)} 个图表\n")

    print("=" * 100)
    print(f"{'#':>3} {'原版类型':<18} {'原版节点':<25} {'翻译版类型':<18} {'翻译版节点':<25} {'匹配'}")
    print("-" * 100)

    for i in range(max(len(orig), len(trans))):
        o = orig[i] if i < len(orig) else None
        t = trans[i] if i < len(trans) else None

        if o and t:
            o_key = (o['type'], tuple(o['nodes'][:4]), o['conn_count'])
            t_key = (t['type'], tuple(t['nodes'][:4]), t['conn_count'])
            match = "✅" if o_key == t_key else "❌"
            print(f"{i+1:>3} {o['type']:<18} {str(o['nodes'][:4]):<25} {t['type']:<18} {str(t['nodes'][:4]):<25} {match}")

            if o_key != t_key:
                print(f"    原版上下文: ...{o['ctx_before'][-50:]}")
                print(f"    翻译上下文: ...{t['ctx_before'][-50:]}")
                print()

if __name__ == '__main__':
    main()
