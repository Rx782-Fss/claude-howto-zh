#!/usr/bin/env python3
"""
精确对比 claude_concepts_guide.md 的 31 个 Mermaid 图表顺序
找出所有偏移位置
"""

import re
import os

ORIG_FILE = "/home/hhbbfss/下载/claude-howto-src/claude-howto-main/claude_concepts_guide.md"
TRANS_FILE = "/data/hhbbfss/project/tre/claude-howto/claude-howto-zh/claude_concepts_guide.md"

def extract_mermaid_signatures(filepath):
    """提取每个 Mermaid 图表的签名特征（用于对比）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = []
    pattern = r'```mermaid\s*\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)

    for i, match in enumerate(matches, 1):
        raw = match.strip()
        lines = raw.split('\n')

        # 提取签名：类型 + 前3个节点定义 + 连接数
        diag_type = lines[0].strip() if lines else 'unknown'

        # 提取节点（前5个）
        nodes = []
        for line in lines[1:15]:
            line = line.strip()
            if not line or line.startswith('%%'):
                continue
            # 提取节点ID
            m = re.match(r'^(\w+)\[', line)
            if m:
                nodes.append(m.group(1))
            if len(nodes) >= 5:
                break

        # 提取连接数
        conn_count = sum(1 for l in lines if '-->' in l or '->>' in l or '-.' in l or '==>' in l)

        # 提取前80字符作为指纹
        fingerprint = raw[:120].replace('\n', ' | ')

        blocks.append({
            'index': i,
            'type': diag_type,
            'nodes': nodes[:5],
            'conn_count': conn_count,
            'fingerprint': fingerprint,
            'line_count': len(lines),
        })

    return blocks

def main():
    print("=" * 90)
    print("🔍 精确对比: claude_concepts_guide.md 31 个 Mermaid 图表")
    print("=" * 90)

    orig_blocks = extract_mermaid_signatures(ORIG_FILE)
    trans_blocks = extract_mermaid_signatures(TRANS_FILE)

    print(f"\n原版图表数: {len(orig_blocks)}")
    print(f"翻译版图表数: {len(trans_blocks)}")

    print("\n" + "=" * 90)
    print("📊 逐个对比详情")
    print("=" * 90)
    print(f"\n{'#':>3} {'原版类型':<20} {'翻译版类型':<20} {'节点(前3)':<25} {'连接数 原→译':<15} {'状态'}")
    print("-" * 90)

    mismatches = []
    for i in range(max(len(orig_blocks), len(trans_blocks))):
        o = orig_blocks[i] if i < len(orig_blocks) else None
        t = trans_blocks[i] if i < len(trans_blocks) else None

        if o and t:
            type_match = "✅" if o['type'] == t['type'] else "❌"
            node_match = "✅" if o['nodes'] == t['nodes'] else "⚠️"

            o_nodes = str(o['nodes'][:3])
            t_nodes = str(t['nodes'][:3])

            if o['type'] != t['type'] or o['nodes'] != t['nodes'] or o['conn_count'] != t['conn_count']:
                status = "❌ 不匹配"
                mismatches.append(i+1)
            else:
                status = "✅ 匹配"

            print(f"{i+1:>3} {o['type']:<20} {t['type']:<20} {o_nodes:<25} {o['conn_count']}→{t['conn_count']:<10} {status}")
        elif o:
            print(f"{i+1:>3} {o['type']:<20} {'(缺失)':<20} {str(o['nodes'][:3]):<25} {o['conn_count']}→{'-':<10} ❌ 翻译版缺失")
            mismatches.append(i+1)
        elif t:
            print(f"{i+1:>3} {'(缺失)':<20} {t['type']:<20} {str(t['nodes'][:3]):<25} {'-':<10}→{t['conn_count']} ➕ 翻译版多余")
            mismatches.append(i+1)

    print("\n" + "=" * 90)
    print(f"📈 结果: {len(orig_blocks) - len(mismatches)}/{len(orig_blocks)} 匹配, {len(mismatches)} 个不匹配")
    print("=" * 90)

    if mismatches:
        print(f"\n⚠️  不匹配的图表编号: {mismatches}")

        # 详细显示不匹配的图表内容
        print("\n" + "=" * 90)
        print("🔬 不匹配图表的详细内容对比")
        print("=" * 90)

        for idx in mismatches:
            o = orig_blocks[idx-1]
            t = trans_blocks[idx-1] if idx <= len(trans_blocks) else None

            print(f"\n{'─'*90}")
            print(f"📍 图表 #{idx}")
            print(f"{'─'*90}")
            print(f"原版:   类型={o['type']}, 节点={o['nodes']}, 连接={o['conn_count']}, 行数={o['line_count']}")
            print(f"原版指纹: {o['fingerprint']}")
            if t:
                print(f"翻译版: 类型={t['type']}, 节点={t['nodes']}, 连接={t['conn_count']}, 行数={t['line_count']}")
                print(f"翻译版指纹: {t['fingerprint']}")
            else:
                print(f"翻译版: (不存在)")

if __name__ == '__main__':
    main()
