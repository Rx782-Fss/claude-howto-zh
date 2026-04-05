#!/usr/bin/env python3
"""
Mermaid Diagram Completion Tool
从原版提取缺失的 Mermaid 图表，翻译成中文并插入到翻译版
"""

import re
import os
from pathlib import Path

ORIGINAL_BASE = "/home/hhbbfss/下载/claude-howto-src/claude-howto-main"
TRANSLATION_BASE = "/data/hhbbfss/project/tre/claude-howto/claude-howto-zh"

# GitHub Mermaid 兼容性规则映射表
TRANSLATIONS = {
    # Subagents 相关
    "Subagent": "子代理",
    "Session": "会话",
    "writes": "写入",
    "loads into": "加载到",
    "updates": "更新",
    "Main Working Tree": "主工作树",
    "spawns": "生成",
    "Subagent with Isolated Worktree": "带隔离工作树的子代理",
    "makes changes in": "在...中修改",
    "Separate Git Worktree + Branch": "独立Git工作树+分支",
    "no changes": "无变更",
    "Auto-cleaned": "自动清理",
    "has changes": "有变更",
    "Returns worktree path and branch": "返回工作树路径和分支",
    
    # MCP 相关
    "Claude": "Claude",
    "MCP Server": "MCP服务器",
    "External Service": "外部服务",
    "Request: list_issues": "请求: 列出问题",
    "Query": "查询",
    "Data": "数据",
    "Response": "响应",
    "Request: create_issue": "请求: 创建问题",
    "Action": "操作",
    "Result": "结果",
    "Filesystem MCP Server": "文件系统MCP服务器",
    "GitHub MCP Server": "GitHub MCP服务器",
    "Database MCP Server": "数据库MCP服务器",
    "Slack MCP Server": "Slack MCP服务器",
    "Google Docs MCP Server": "Google Docs MCP服务器",
    "File I/O": "文件I/O",
    "Local Files": "本地文件",
    "API": "API接口",
    "GitHub Repos": "GitHub仓库",
    "PostgreSQL/MySQL": "PostgreSQL/MySQL数据库",
    "Messages": "消息",
    "Slack Workspace": "Slack工作区",
    "Docs": "文档",
    "Google Drive": "Google云端硬盘",
    
    # Memory 相关
    "User": "用户",
    "Project": "项目",
    "CLAUDE.md": "CLAUDE.md",
    "memory file": "记忆文件",
    "persists across sessions": "跨会话持久化",
    "session scope": "会话范围",
    "project scope": "项目范围",
    "user scope": "用户范围",
    
    # Resources 相关
    "Official Documentation": "官方文档",
    "Anthropic Resources": "Anthropic资源",
    "Community Resources": "社区资源",
    "Learning Resources": "学习资源",
    "Tool References": "工具参考",
    "docs.anthropic.com": "docs.anthropic.com",
    "API Reference": "API参考文档",
    "Cookbook": "Cookbook示例库",
    "Quick Reference": "快速参考",
    "GitHub Repository": "GitHub仓库",
    "Discord Community": "Discord社区",
    "Examples Library": "示例库",
    "Tutorials": "教程集合",
    "MCP Servers": "MCP服务器列表",
    "Plugin Directory": "插件目录",
    "Skills Catalog": "技能目录",
    
    # Style Guide 相关
    "Good Prompt": "好的提示词",
    "Bad Prompt": "差的提示词",
    "Clear specific task": "清晰具体的任务",
    "Vague request": "模糊的请求",
    "Structured output format": "结构化的输出格式",
    "No format guidance": "无格式指导",
    "Includes context": "包含上下文",
    "Missing context": "缺少上下文",
    "Specifies constraints": "明确约束条件",
    "No constraints specified": "未指定约束条件",
}

def extract_mermaid_with_context(filepath, context_lines=3):
    """提取 Mermaid 代码块及上下文"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    blocks = []
    in_mermaid = False
    block_start = 0
    block_content = []
    
    for i, line in enumerate(lines):
        if '```mermaid' in line:
            in_mermaid = True
            block_start = i
            block_content = []
        elif in_mermaid and line.strip() == '```':
            in_mermaid = False
            # 获取上下文
            start_ctx = max(0, block_start - context_lines)
            end_ctx = min(len(lines), i + 1 + context_lines)
            context_before = ''.join(lines[start_ctx:block_start])
            context_after = ''.join(lines[i+1:end_ctx])
            
            blocks.append({
                'index': len(blocks) + 1,
                'content': '\n'.join(block_content),
                'context_before': context_before,
                'context_after': context_after,
                'line_number': block_start + 1
            })
        elif in_mermaid:
            block_content.append(line)
    
    return blocks

def translate_mermaid(content):
    """翻译 Mermaid 内容，应用兼容性规则"""
    translated = content
    
    # 应用翻译映射
    for en, zh in TRANSLATIONS.items():
        translated = translated.replace(en, zh)
    
    # 应用 GitHub Mermaid 兼容性规则
    # 规则1: <br/> 替换为空格
    translated = translated.replace('<br/>', ' ')
    
    # 规则2: 移除可能的 emoji
    emoji_pattern = r'[✅❌👤🧭🟢🔵⚠️❓💡🎯📊]'
    translated = re.sub(emoji_pattern, '', translated)
    
    return translated

def find_insertion_point(trans_filepath, orig_context_before):
    """在翻译版中找到合适的插入点"""
    with open(trans_filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 尝试通过章节标题匹配
    lines = orig_context_before.strip().split('\n')
    for line in reversed(lines):
        line = line.strip()
        if line.startswith('## ') or line.startswith('### '):
            # 找到章节标题
            if line in content:
                pos = content.index(line)
                # 找到该章节下的合适位置（在第一个代码块或段落之后）
                section_content = content[pos:]
                
                # 寻找插入点：在章节标题后的空行处
                next_section = re.search(r'\n## ', section_content[10:])
                if next_section:
                    insert_pos = pos + 10 + next_section.start()
                    return insert_pos
                
                # 如果没有下一个章节，就在文件末尾
                return len(content)
    
    # 默认返回文件末尾
    return len(content)

def complete_missing_diagrams():
    """主函数：补全所有缺失的图表"""
    print("=" * 80)
    print("🔧 Mermaid 图表补全工具")
    print("=" * 80)
    
    # 需要处理的文件清单
    files_to_process = [
        ('04-subagents/README.md', 7),   # 原版7个，翻译版0个
        ('05-mcp/README.md', 7),        # 原版7个，翻译版1个
        ('02-memory/README.md', 5),     # 原版5个，翻译版4个
        ('resources.md', 2),            # 原版2个，翻译版0个
        ('STYLE_GUIDE.md', 1),          # 原版1个，翻译版0个
    ]
    
    total_completed = 0
    
    for rel_path, expected_count in files_to_process:
        orig_path = os.path.join(ORIGINAL_BASE, rel_path)
        trans_path = os.path.join(TRANSLATION_BASE, rel_path)
        
        print(f"\n{'='*60}")
        print(f"📄 处理: {rel_path}")
        print(f"{'='*60}")
        
        if not os.path.exists(orig_path):
            print(f"   ❌ 原版文件不存在: {orig_path}")
            continue
        
        if not os.path.exists(trans_path):
            print(f"   ❌ 翻译版文件不存在: {trans_path}")
            continue
        
        # 提取原版的所有 Mermaid 图表
        orig_blocks = extract_mermaid_with_context(orig_path)
        
        # 提取翻译版现有的 Mermaid 图表
        trans_blocks = extract_mermaid_with_context(trans_path)
        
        print(f"   原版图表数: {len(orig_blocks)}")
        print(f"   翻译版现有: {len(trans_blocks)}")
        
        # 找出缺失的图表
        missing_count = len(orig_blocks) - len(trans_blocks)
        
        if missing_count <= 0:
            print(f"   ✅ 无需补全")
            continue
        
        print(f"   ⚠️  需要补全: {missing_count} 个图表")
        
        # 读取翻译版文件
        with open(trans_path, 'r', encoding='utf-8') as f:
            trans_content = f.read()
        
        # 对每个缺失的图表进行补全
        for i, block in enumerate(orig_blocks[len(trans_blocks):], 1):
            print(f"\n   📊 补全图表 #{len(trans_blocks) + i}:")
            
            # 翻译图表内容
            translated_content = translate_mermaid(block['content'])
            
            # 构建完整的 Mermaid 代码块
            mermaid_block = f"\n\n```mermaid\n{translated_content}\n```\n\n"
            
            # 查找插入点（基于上下文的章节标题）
            insertion_point = find_insertion_point(trans_path, block['context_before'])
            
            # 插入到翻译版
            trans_content = trans_content[:insertion_point] + mermaid_block + trans_content[insertion_point:]
            
            print(f"      ✅ 已在第 {insertion_point} 字符处插入")
            total_completed += 1
        
        # 写回文件
        with open(trans_path, 'w', encoding='utf-8') as f:
            f.write(trans_content)
        
        print(f"\n   ✅ 文件已更新: {rel_path}")
    
    print("\n" + "=" * 80)
    print("📈 补全结果统计")
    print("=" * 80)
    print(f"\n✅ 总共补全了 {total_completed} 个 Mermaid 图表\n")

if __name__ == '__main__':
    complete_missing_diagrams()
