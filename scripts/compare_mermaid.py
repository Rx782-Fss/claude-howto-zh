#!/usr/bin/env python3
"""
Mermaid Diagram Structure Comparator
比较原版英文 Mermaid 和中文翻译版的**结构差异**（忽略文本内容差异）
"""

import re
import os
from pathlib import Path
from collections import defaultdict

ORIGINAL_BASE = "/home/hhbbfss/下载/claude-howto-src/claude-howto-main"
TRANSLATION_BASE = "/data/hhbbfss/project/tre/claude-howto/claude-howto-zh"
REFERENCE_DIR = "/data/hhbbfss/project/tre/claude-howto/reference/mermaid-original"

def extract_mermaid_blocks(filepath):
    """从文件中提取所有 Mermaid 代码块"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = []
    # 匹配 ```mermaid ... ``` 代码块
    pattern = r'```mermaid\s*\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches, 1):
        blocks.append({
            'index': i,
            'raw': match.strip(),
            'source_file': filepath
        })
    
    return blocks

def analyze_mermaid_structure(block):
    """分析 Mermaid 图表的结构特征（不含文本内容）"""
    raw = block['raw']
    lines = raw.split('\n')
    
    # 提取图表类型（第一行）
    diagram_type = lines[0].strip() if lines else 'unknown'
    
    # 提取所有节点定义
    nodes = []
    node_pattern = r'^(\w+)\[.*?\]|^(\w+)\(.*?\)|^(\w+)\{.*?\}|^(\w+)\[\(.*?\)\]'
    for line in lines[1:]:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('%%{'):
            continue
        
        # 提取节点 ID
        for pattern in [r'^(\w+)\[', r'^(\w+)\(', r'^(\w+)\{', r'^\s*(\w+)\[', r'^\s*(\w+)\(', r'^\s*(\w+)\{']:
            match = re.match(pattern, line)
            if match and not any(op in line for op in ['-->', '->', '-.', '=>']):
                node_id = match.group(1)
                if node_id not in ['end', 'subgraph', 'classDef', 'style', 'click', 'linkStyle']:
                    nodes.append(node_id)
                    break
    
    # 提取所有连接关系
    connections = []
    conn_patterns = [
        r'(\w+)\s*-->\|.*?\|\s*(\w+)',
        r'(\w+)\s*-->\s*(\w+)',
        r'(\w+)\s*--\|.*?\|\s*(\w+)',
        r'(\w+)\s*-\.\|.*?\|\s*(\w+)',
        r'(\w+)\s*->\s*(\w+)',
        r'(\w+)\s*->>\s*(\w+)',
        r'(\w+)\s*-->>\s*(\w+)',
        r'(\w+)\s*==>|.*?\|==>(\w+)',
        r'(\w+)\s*===\s*(\w+)',
    ]

    for line in lines[1:]:
        line = line.strip()
        if not line or line.startswith('%%'):
            continue
        if '-->' in line or '->' in line or '-.' in line or '==>' in line or '===' in line or '->>' in line or '-->>' in line:
            for pattern in conn_patterns:
                match = re.search(pattern, line)
                if match:
                    connections.append((match.group(1), match.group(2)))
                    break
    
    # 检查特殊语法元素
    has_subgraph = 'subgraph' in raw
    has_classdef = 'classDef' in raw
    has_style = re.search(r'^style\s+\w+', raw, re.MULTILINE)
    has_click = 'click ' in raw
    has_linkstyle = 'linkStyle' in raw
    
    return {
        'type': diagram_type,
        'node_count': len(set(nodes)),
        'nodes': sorted(set(nodes)),
        'connection_count': len(connections),
        'connections': connections,
        'has_subgraph': has_subgraph,
        'has_classdef': has_classdef,
        'has_style': bool(has_style),
        'has_click': has_click,
        'has_linkstyle': has_linkstyle,
        'line_count': len(lines),
    }

def find_files_with_mermaid(base_dir):
    """递归查找包含 Mermaid 的文件"""
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '```mermaid' in content:
                        rel_path = os.path.relpath(filepath, base_dir)
                        files.append((filepath, rel_path))
    return files

def compare_structures(orig_struct, trans_struct):
    """比较两个结构的差异"""
    issues = []
    
    # 1. 图表类型是否一致
    if orig_struct['type'] != trans_struct['type']:
        issues.append(f"❌ 图表类型不同: 原版={orig_struct['type']} vs 翻译={trans_struct['type']}")
    
    # 2. 节点数量是否一致
    if orig_struct['node_count'] != trans_struct['node_count']:
        issues.append(f"❌ 节点数量不同: 原版={orig_struct['node_count']} vs 翻译={trans_struct['node_count']}")
    
    # 3. 具体节点列表差异
    orig_nodes = set(orig_struct['nodes'])
    trans_nodes = set(trans_struct['nodes'])
    
    missing_in_trans = orig_nodes - trans_nodes
    extra_in_trans = trans_nodes - orig_nodes
    
    if missing_in_trans:
        issues.append(f"⚠️  翻译版缺少节点: {sorted(missing_in_trans)}")
    if extra_in_trans:
        issues.append(f"⚠️  翻译版多余节点: {sorted(extra_in_trans)}")
    
    # 4. 连接数量是否一致
    if orig_struct['connection_count'] != trans_struct['connection_count']:
        issues.append(f"⚠️  连接数不同: 原版={orig_struct['connection_count']} vs 翻译={trans_struct['connection_count']}")
    
    # 5. 结构特性一致性检查
    features = ['has_subgraph', 'has_classdef', 'has_style', 'has_click', 'has_linkstyle']
    for feat in features:
        if orig_struct[feat] != trans_struct[feat]:
            issues.append(f"⚠️  {feat} 不同: 原版={orig_struct[feat]} vs 翻译={trans_struct[feat]}")
    
    return issues

def main():
    print("=" * 80)
    print("🔍 Mermaid 图表结构对比工具")
    print("=" * 80)
    print(f"\n📁 原版目录: {ORIGINAL_BASE}")
    print(f"📁 翻译目录: {TRANSLATION_BASE}")
    print()
    
    # 查找所有包含 Mermaid 的文件
    print("📋 正在扫描文件...")
    orig_files = find_files_with_mermaid(ORIGINAL_BASE)
    trans_files = find_files_with_mermaid(TRANSLATION_BASE)
    
    print(f"   原版: {len(orig_files)} 个文件含 Mermaid")
    print(f"   翻译: {len(trans_files)} 个文件含 Mermaid")
    print()
    
    # 构建文件到图表的映射
    orig_diagrams = {}  # (rel_path, index) -> structure
    trans_diagrams = {}
    
    total_orig = 0
    total_trans = 0
    
    print("\n📊 分析原版图表...")
    for filepath, rel_path in orig_files:
        blocks = extract_mermaid_blocks(filepath)
        for block in blocks:
            struct = analyze_mermaid_structure(block)
            key = (rel_path, block['index'])
            orig_diagrams[key] = struct
            total_orig += 1
    
    print(f"   共 {total_orig} 个图表")
    
    print("\n📊 分析翻译版图表...")
    for filepath, rel_path in trans_files:
        blocks = extract_mermaid_blocks(filepath)
        for block in blocks:
            struct = analyze_mermaid_structure(block)
            key = (rel_path, block['index'])
            trans_diagrams[key] = struct
            total_trans += 1
    
    print(f"   共 {total_trans} 个图表")
    
    # 对比结果
    print("\n" + "=" * 80)
    print("🔍 开始详细对比...")
    print("=" * 80 + "\n")
    
    all_issues = []
    matched_pairs = 0
    only_orig = 0
    only_trans = 0
    
    # 检查所有原版图表在翻译版中是否存在且匹配
    for key in sorted(orig_diagrams.keys()):
        if key in trans_diagrams:
            issues = compare_structures(orig_diagrams[key], trans_diagrams[key])
            if issues:
                all_issues.append((key, issues))
                print(f"📄 {key[0]} (图表 #{key[1]})")
                for issue in issues:
                    print(f"   {issue}")
                print()
            else:
                matched_pairs += 1
        else:
            all_issues.append((key, [f"❌ 翻译版中完全缺失此图表"]))
            only_orig += 1
            print(f"📄 {key[0]} (图表 #{key[1]})")
            print(f"   ❌ 翻译版中完全缺失此图表\n")
    
    # 检查翻译版是否有额外的图表
    for key in sorted(trans_diagrams.keys()):
        if key not in orig_diagrams:
            all_issues.append((key, [f"ℹ️  翻译版有额外图表（原版不存在）"]))
            only_trans += 1
            print(f"📄 {key[0]} (图表 #{key[1]})")
            print(f"   ℹ️  翻译版有额外图表（原版不存在）\n")
    
    # 输出统计摘要
    print("=" * 80)
    print("📈 对比结果摘要")
    print("=" * 80)
    print(f"\n✅ 完全匹配的图表: {matched_pairs} / {total_orig}")
    print(f"❌ 翻译版缺失的图表: {only_orig}")
    print(f"➕ 翻译版多余的图表: {only_trans}")
    print(f"⚠️  存在结构问题的图表: {len([i for i in all_issues if i[1] and '缺失' not in i[1][0] and '额外' not in i[1][0]])}")
    print()
    
    if len(all_issues) == 0:
        print("🎉 所有图表结构完全一致！无需修改。\n")
    else:
        print(f"⚠️  发现 {len(all_issues)} 个需要关注的项，详见上方详情。\n")

if __name__ == '__main__':
    main()
