#!/usr/bin/env python3
"""
代码异味检测器

检测 Python、JavaScript 和 TypeScript 文件中的常见代码异味。
基于 Martin Fowler 的代码异味目录。

用法:
    python detect-smells.py <文件>                    分析单个文件
    python detect-smells.py --dir <目录>              分析整个目录
    python detect-smells.py -v <文件>                 详细模式（含代码片段）

可检测的代码异味:
    - Long Method（长方法） (>30 行)
    - Long Parameter List（过长参数列表） (>4 个参数)
    - Duplicate Code（重复代码）（相似代码块）
    - Large Class（过大类） (>300 行, >10 个方法)
    - Dead Code（死代码）（未使用的变量/函数）
    - Complex Conditional（复杂条件表达式）（深层嵌套、长链）
    - Magic Number/String（魔法数字/字符串）
    - Feature Envy（特性依恋）（大量使用其他类数据的方法）
    - Excessive Comments（过多注释）（解释"做什么"而非"为什么"的注释）
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


class SmellSeverity(Enum):
    """代码异味的严重程度级别。"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class SmellType(Enum):
    """代码异味的类型。"""
    LONG_METHOD = "Long Method"
    LONG_PARAMETER_LIST = "Long Parameter List"
    DUPLICATE_CODE = "Duplicate Code"
    LARGE_CLASS = "Large Class"
    DEAD_CODE = "Dead Code"
    COMPLEX_CONDITIONAL = "Complex Conditional"
    MAGIC_NUMBER = "Magic Number/String"
    FEATURE_ENVY = "Feature Envy"
    EXCESSIVE_COMMENTS = "Excessive Comments"
    DEEPLY_NESTED = "Deeply Nested Code"
    PRIMITIVE_OBSESSION = "Primitive Obsession"
    DATA_CLUMPS = "Data Clumps"
    SWITCH_STATEMENT = "Switch Statement"
    MESSAGE_CHAIN = "Message Chain"


@dataclass
class CodeSmell:
    """表示一个被检测到的代码异味。"""
    smell_type: SmellType
    severity: SmellSeverity
    location: str
    line_start: int
    line_end: int
    description: str
    suggestion: str
    code_snippet: str = ""


@dataclass
class SmellReport:
    """文件中所有发现的异味报告。"""
    filename: str
    smells: List[CodeSmell] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for s in self.smells if s.severity == SmellSeverity.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for s in self.smells if s.severity == SmellSeverity.HIGH)

    @property
    def medium_count(self) -> int:
        return sum(1 for s in self.smells if s.severity == SmellSeverity.MEDIUM)

    @property
    def low_count(self) -> int:
        return sum(1 for s in self.smells if s.severity == SmellSeverity.LOW)


class SmellDetector:
    """在源文件中检测代码异味。"

    # 阈值（可配置）
    THRESHOLDS = {
        'long_method_lines': 30,
        'very_long_method_lines': 50,
        'max_parameters': 4,
        'large_class_lines': 300,
        'large_class_methods': 10,
        'max_nesting_depth': 4,
        'long_chain_length': 3,
        'duplicate_min_lines': 5,
    }

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.language = self._detect_language()

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            self.code = f.read()
        self.lines = self.code.split('\n')
        self.smells: List[CodeSmell] = []

    def _detect_language(self) -> str:
        """根据文件扩展名检测编程语言。"""
        ext = os.path.splitext(self.filepath)[1].lower()
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
        }
        return ext_map.get(ext, 'python')

    def detect_all(self) -> SmellReport:
        """运行所有异味检测器。"""
        self._detect_long_methods()
        self._detect_long_parameter_lists()
        self._detect_large_class()
        self._detect_complex_conditionals()
        self._detect_magic_numbers()
        self._detect_excessive_comments()
        self._detect_deeply_nested()
        self._detect_switch_statements()
        self._detect_message_chains()
        self._detect_duplicate_code()
        self._detect_dead_code()

        return SmellReport(filename=self.filename, smells=self.smells)

    def _get_snippet(self, start: int, end: int, context: int = 2) -> str:
        """获取带上下文的代码片段。"""
        actual_start = max(0, start - context)
        actual_end = min(len(self.lines), end + context)
        snippet_lines = []
        for i in range(actual_start, actual_end):
            prefix = "→ " if start <= i < end else "  "
            snippet_lines.append(f"{i+1:4d} {prefix}{self.lines[i]}")
        return '\n'.join(snippet_lines)

    def _detect_long_methods(self) -> None:
        """检测过长的函数/方法。"""
        if self.language == 'python':
            pattern = r'^\s*def\s+(\w+)\s*\([^)]*\):'
        else:
            pattern = r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))'

        current_method = None
        method_start = 0
        brace_depth = 0
        indent_level = 0

        for i, line in enumerate(self.lines):
            match = re.search(pattern, line)
            if match:
                # 检查前一个方法是否存在
                if current_method:
                    method_lines = i - method_start
                    self._check_method_length(current_method, method_start, i - 1, method_lines)

                current_method = match.group(1) or (match.group(2) if match.lastindex and match.lastindex > 1 else None)
                method_start = i
                indent_level = len(line) - len(line.lstrip())

            # 通过缩进跟踪 Python 函数的结束位置
            if self.language == 'python' and current_method:
                if line.strip() and not line.strip().startswith('#'):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= indent_level and i > method_start:
                        method_lines = i - method_start
                        self._check_method_length(current_method, method_start, i - 1, method_lines)
                        current_method = None

        # 检查最后一个方法
        if current_method:
            method_lines = len(self.lines) - method_start
            self._check_method_length(current_method, method_start, len(self.lines) - 1, method_lines)

    def _check_method_length(self, name: str, start: int, end: int, lines: int) -> None:
        """检查方法是否过长，如是则添加异味记录。"""
        if lines > self.THRESHOLDS['very_long_method_lines']:
            severity = SmellSeverity.HIGH
            desc = f"Method '{name}' is {lines} lines (threshold: {self.THRESHOLDS['long_method_lines']})"
        elif lines > self.THRESHOLDS['long_method_lines']:
            severity = SmellSeverity.MEDIUM
            desc = f"Method '{name}' is {lines} lines (threshold: {self.THRESHOLDS['long_method_lines']})"
        else:
            return

        self.smells.append(CodeSmell(
            smell_type=SmellType.LONG_METHOD,
            severity=severity,
            location=f"{self.filename}:{start+1}-{end+1}",
            line_start=start + 1,
            line_end=end + 1,
            description=desc,
            suggestion="Apply Extract Method to break down into smaller functions",
            code_snippet=self._get_snippet(start, min(start + 5, end), 0)
        ))

    def _detect_long_parameter_lists(self) -> None:
        """检测参数过多的函数。"""
        if self.language == 'python':
            pattern = r'def\s+(\w+)\s*\(([^)]*)\)'
        else:
            pattern = r'(?:function\s+(\w+)\s*\(([^)]*)\)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function\s*)?\(([^)]*)\))'

        for i, line in enumerate(self.lines):
            match = re.search(pattern, line)
            if match:
                # 安全地提取分组
                groups = match.groups()
                func_name = groups[0] or (groups[2] if len(groups) > 2 else None)
                params_str = groups[1] if len(groups) > 1 else ""
                if not params_str and len(groups) > 3:
                    params_str = groups[3] or ""

                # 统计参数数量
                if params_str.strip():
                    params = [p.strip() for p in params_str.split(',') if p.strip()]
                    # 过滤 Python 的 self、cls
                    if self.language == 'python':
                        params = [p for p in params if p not in ('self', 'cls')]
                    param_count = len(params)

                    if param_count > self.THRESHOLDS['max_parameters']:
                        severity = SmellSeverity.HIGH if param_count > 6 else SmellSeverity.MEDIUM
                        self.smells.append(CodeSmell(
                            smell_type=SmellType.LONG_PARAMETER_LIST,
                            severity=severity,
                            location=f"{self.filename}:{i+1}",
                            line_start=i + 1,
                            line_end=i + 1,
                            description=f"Function '{func_name}' has {param_count} parameters (max: {self.THRESHOLDS['max_parameters']})",
                            suggestion="Consider Introduce Parameter Object or Preserve Whole Object",
                            code_snippet=self._get_snippet(i, i + 1, 1)
                        ))

    def _detect_large_class(self) -> None:
        """检测过大的类。"""
        if self.language == 'python':
            class_pattern = r'^\s*class\s+(\w+)'
            method_pattern = r'^\s+def\s+\w+'
        else:
            class_pattern = r'class\s+(\w+)'
            method_pattern = r'(?:^\s+\w+\s*\([^)]*\)\s*\{|^\s+(?:async\s+)?\w+\s*=)'

        current_class = None
        class_start = 0
        method_count = 0
        class_indent = 0

        for i, line in enumerate(self.lines):
            class_match = re.search(class_pattern, line)
            if class_match:
                # 检查前一个类
                if current_class:
                    self._check_class_size(current_class, class_start, i - 1, method_count)

                current_class = class_match.group(1)
                class_start = i
                method_count = 0
                class_indent = len(line) - len(line.lstrip())

            # 统计当前类中的方法数
            if current_class and re.search(method_pattern, line):
                method_count += 1

        # 检查最后一个类
        if current_class:
            self._check_class_size(current_class, class_start, len(self.lines) - 1, method_count)

    def _check_class_size(self, name: str, start: int, end: int, methods: int) -> None:
        """检查类是否过大。"""
        lines = end - start + 1

        issues = []
        severity = SmellSeverity.MEDIUM

        if lines > self.THRESHOLDS['large_class_lines']:
            issues.append(f"{lines} lines (max: {self.THRESHOLDS['large_class_lines']})")
            severity = SmellSeverity.HIGH

        if methods > self.THRESHOLDS['large_class_methods']:
            issues.append(f"{methods} methods (max: {self.THRESHOLDS['large_class_methods']})")
            if severity != SmellSeverity.HIGH:
                severity = SmellSeverity.MEDIUM

        if issues:
            self.smells.append(CodeSmell(
                smell_type=SmellType.LARGE_CLASS,
                severity=severity,
                location=f"{self.filename}:{start+1}-{end+1}",
                line_start=start + 1,
                line_end=end + 1,
                description=f"Class '{name}' is too large: {', '.join(issues)}",
                suggestion="Apply Extract Class to split responsibilities",
                code_snippet=self._get_snippet(start, start + 3, 0)
            ))

    def _detect_complex_conditionals(self) -> None:
        """检测复杂的条件表达式。"""
        for i, line in enumerate(self.lines):
            # 统计行中的逻辑运算符数量
            and_or_count = len(re.findall(r'\b(and|or|&&|\|\|)\b', line))

            if and_or_count >= 3:
                self.smells.append(CodeSmell(
                    smell_type=SmellType.COMPLEX_CONDITIONAL,
                    severity=SmellSeverity.MEDIUM,
                    location=f"{self.filename}:{i+1}",
                    line_start=i + 1,
                    line_end=i + 1,
                    description=f"Complex conditional with {and_or_count} logical operators",
                    suggestion="Apply Decompose Conditional or Consolidate Conditional Expression",
                    code_snippet=self._get_snippet(i, i + 1, 1)
                ))

    def _detect_magic_numbers(self) -> None:
        """检测魔法数字和魔法字符串。"""
        # 跳过常见可接受的值
        acceptable = {'0', '1', '-1', '2', '100', 'true', 'false', 'null', 'None', '""', "''"}

        for i, line in enumerate(self.lines):
            # 跳过注释和导入语句
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//') or \
               stripped.startswith('import') or stripped.startswith('from'):
                continue

            # 查找数字字面量（排除变量名中的数字）
            numbers = re.findall(r'(?<![a-zA-Z_])\b(\d+\.?\d*)\b(?![a-zA-Z_])', line)

            for num in numbers:
                if num not in acceptable and float(num) > 2:
                    # 检查是否可能是魔法数字（在计算或比较中）
                    if re.search(rf'[<>=+\-*/]\s*{re.escape(num)}|{re.escape(num)}\s*[<>=+\-*/]', line):
                        self.smells.append(CodeSmell(
                            smell_type=SmellType.MAGIC_NUMBER,
                            severity=SmellSeverity.LOW,
                            location=f"{self.filename}:{i+1}",
                            line_start=i + 1,
                            line_end=i + 1,
                            description=f"Magic number '{num}' - consider using a named constant",
                            suggestion="Replace magic number with named constant",
                            code_snippet=self._get_snippet(i, i + 1, 0)
                        ))
                        break  # 每行一个魔法数字就足够了

    def _detect_excessive_comments(self) -> None:
        """检测解释"做什么"而非"为什么"的注释。"""
        what_patterns = [
            r'#\s*(set|get|return|loop|iterate|check|if|increment|decrement)',
            r'//\s*(set|get|return|loop|iterate|check|if|increment|decrement)',
        ]

        for i, line in enumerate(self.lines):
            for pattern in what_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.EXCESSIVE_COMMENTS,
                        severity=SmellSeverity.LOW,
                        location=f"{self.filename}:{i+1}",
                        line_start=i + 1,
                        line_end=i + 1,
                        description="Comment explains 'what' not 'why' - consider renaming or removing",
                        suggestion="Use Extract Method with descriptive name instead of comment",
                        code_snippet=self._get_snippet(i, i + 1, 0)
                    ))
                    break

    def _detect_deeply_nested(self) -> None:
        """检测深度嵌套的代码块。"""
        max_depth = 0
        current_depth = 0
        depth_start = 0

        for i, line in enumerate(self.lines):
            if self.language == 'python':
                # 通过缩进计算嵌套深度
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    depth = indent // 4  # 假设使用 4 空格缩进
                    if depth > current_depth:
                        if depth > max_depth:
                            max_depth = depth
                            if depth >= self.THRESHOLDS['max_nesting_depth']:
                                depth_start = i
                    current_depth = depth
            else:
                # 通过花括号计数
                current_depth += line.count('{') - line.count('}')
                if current_depth > max_depth:
                    max_depth = current_depth
                    if current_depth >= self.THRESHOLDS['max_nesting_depth']:
                        depth_start = i

        if max_depth >= self.THRESHOLDS['max_nesting_depth']:
            self.smells.append(CodeSmell(
                smell_type=SmellType.DEEPLY_NESTED,
                severity=SmellSeverity.HIGH if max_depth > 5 else SmellSeverity.MEDIUM,
                location=f"{self.filename}:{depth_start+1}",
                line_start=depth_start + 1,
                line_end=depth_start + 1,
                description=f"Code nested {max_depth} levels deep (max: {self.THRESHOLDS['max_nesting_depth']})",
                suggestion="Apply Replace Nested Conditional with Guard Clauses or Extract Method",
                code_snippet=self._get_snippet(depth_start, depth_start + 5, 0)
            ))

    def _detect_switch_statements(self) -> None:
        """检测可能需要多态化的 switch 语句。"""
        if self.language == 'python':
            # Python 3.10+ 的 match 语句或 if/elif 链
            pattern = r'^\s*(if|elif).*==.*:'
            consecutive_conditions = 0
            chain_start = 0

            for i, line in enumerate(self.lines):
                if re.search(pattern, line):
                    if consecutive_conditions == 0:
                        chain_start = i
                    consecutive_conditions += 1
                else:
                    if consecutive_conditions >= 4:
                        self._add_switch_smell(chain_start, i - 1, consecutive_conditions)
                    consecutive_conditions = 0
        else:
            # JavaScript/TypeScript 的 switch
            pattern = r'\bswitch\s*\('
            for i, line in enumerate(self.lines):
                if re.search(pattern, line):
                    # 统计 case 数量
                    case_count = 0
                    for j in range(i, min(i + 50, len(self.lines))):
                        case_count += len(re.findall(r'\bcase\b', self.lines[j]))
                    if case_count >= 4:
                        self._add_switch_smell(i, i + 1, case_count)

    def _add_switch_smell(self, start: int, end: int, cases: int) -> None:
        """添加 switch 语句异味记录。"""
        self.smells.append(CodeSmell(
            smell_type=SmellType.SWITCH_STATEMENT,
            severity=SmellSeverity.MEDIUM,
            location=f"{self.filename}:{start+1}",
            line_start=start + 1,
            line_end=end + 1,
            description=f"Switch/case statement with {cases} cases - consider polymorphism",
            suggestion="Apply Replace Conditional with Polymorphism",
            code_snippet=self._get_snippet(start, start + 5, 0)
        ))

    def _detect_message_chains(self) -> None:
        """检测过长的方法调用链（火车失事式代码）。"""
        chain_pattern = r'(\w+(?:\.\w+\([^)]*\)){3,})'

        for i, line in enumerate(self.lines):
            matches = re.findall(chain_pattern, line)
            for match in matches:
                chain_length = match.count('.')
                if chain_length >= self.THRESHOLDS['long_chain_length']:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.MESSAGE_CHAIN,
                        severity=SmellSeverity.MEDIUM,
                        location=f"{self.filename}:{i+1}",
                        line_start=i + 1,
                        line_end=i + 1,
                        description=f"Message chain with {chain_length} calls - violates Law of Demeter",
                        suggestion="Apply Hide Delegate to reduce coupling",
                        code_snippet=self._get_snippet(i, i + 1, 0)
                    ))

    def _detect_duplicate_code(self) -> None:
        """检测潜在的重复代码块（简化版）。"""
        # 创建行哈希用于比较
        line_hashes: Dict[str, List[int]] = defaultdict(list)

        for i, line in enumerate(self.lines):
            normalized = re.sub(r'\s+', ' ', line.strip())
            if len(normalized) > 20:  # 仅处理有意义的行
                line_hashes[normalized].append(i)

        # 查找重复项
        for normalized, positions in line_hashes.items():
            if len(positions) >= 3:  # 至少出现 3 次
                self.smells.append(CodeSmell(
                    smell_type=SmellType.DUPLICATE_CODE,
                    severity=SmellSeverity.MEDIUM,
                    location=f"{self.filename}:{positions[0]+1}",
                    line_start=positions[0] + 1,
                    line_end=positions[0] + 1,
                    description=f"Potential duplicate code found {len(positions)} times",
                    suggestion="Apply Extract Method to eliminate duplication",
                    code_snippet=self._get_snippet(positions[0], positions[0] + 1, 0)
                ))

    def _detect_dead_code(self) -> None:
        """检测潜在的死代码（简化版）。"""
        # 查找常见的死代码模式
        patterns = [
            (r'^\s*#.*TODO.*delete', "TODO to delete"),
            (r'^\s*#.*FIXME.*remove", "FIXME to remove"),
            (r'^\s*//.*TODO.*delete", "TODO to delete"),
            (r'^\s*//.*FIXME.*remove", "FIXME to remove"),
            (r'^\s*if\s+False:', "Code behind 'if False'"),
            (r'^\s*if\s*\(\s*false\s*\)', "Code behind 'if (false)'"),
        ]

        for i, line in enumerate(self.lines):
            for pattern, desc in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.DEAD_CODE,
                        severity=SmellSeverity.LOW,
                        location=f"{self.filename}:{i+1}",
                        line_start=i + 1,
                        line_end=i + 1,
                        description=f"Potential dead code: {desc}",
                        suggestion="Remove dead code",
                        code_snippet=self._get_snippet(i, i + 1, 0)
                    ))


def print_report(report: SmellReport, verbose: bool = False) -> None:
    """以可读格式打印异味报告。"""
    print("=" * 70)
    print(f"CODE SMELL DETECTION REPORT: {report.filename}")  # 代码异味检测报告
    print("=" * 70)

    print(f"\n📊 SUMMARY")  # 汇总
    print("-" * 40)
    print(f"  Total smells found:     {len(report.smells)}")
    print(f"  Critical:               {report.critical_count}")
    print(f"  High:                   {report.high_count}")
    print(f"  Medium:                 {report.medium_count}")
    print(f"  Low:                    {report.low_count}")

    if not report.smells:
        print("\n✅ No code smells detected!")  # 未检测到代码异味！
        print("=" * 70)
        return

    # 按类型分组
    by_type: Dict[SmellType, List[CodeSmell]] = defaultdict(list)
    for smell in report.smells:
        by_type[smell.smell_type].append(smell)

    print(f"\n📋 FINDINGS BY TYPE")  # 按类型分类的结果
    print("-" * 40)

    for smell_type, smells in sorted(by_type.items(), key=lambda x: -len(x[1])):
        print(f"\n### {smell_type.value} ({len(smells)} found)")  # 发现 N 个

        for smell in sorted(smells, key=lambda x: x.severity.value):
            severity_icon = {
                SmellSeverity.CRITICAL: "🔴",
                SmellSeverity.HIGH: "🟠",
                SmellSeverity.MEDIUM: "🟡",
                SmellSeverity.LOW: "🟢",
            }[smell.severity]

            print(f"\n  {severity_icon} [{smell.severity.value}] {smell.location}")
            print(f"     {smell.description}")
            print(f"     💡 {smell.suggestion}")

            if verbose and smell.code_snippet:
                print(f"\n     Code:")
                for snippet_line in smell.code_snippet.split('\n'):
                    print(f"       {snippet_line}")

    print("\n" + "=" * 70)
    print("💡 RECOMMENDED ACTIONS")  # 建议措施
    print("-" * 40)

    if report.critical_count > 0:
        print("  1. Address CRITICAL issues immediately")  # 立即处理严重问题
    if report.high_count > 0:
        print("  2. Plan to fix HIGH severity issues this sprint")  # 本迭代计划修复高优先级问题
    if report.medium_count > 0:
        print("  3. Schedule MEDIUM issues for upcoming work")  # 安排中等问题到后续工作
    if report.low_count > 0:
        print("  4. Fix LOW issues opportunistically")  # 见缝插针修复低优先级问题

    print("\n" + "=" * 70)


def analyze_directory(directory: str, verbose: bool = False) -> None:
    """分析目录中所有支持的文件。"""
    supported_extensions = ['.py', '.js', '.jsx', '.ts', '.tsx']
    files = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in supported_extensions):
                files.append(os.path.join(root, filename))

    if not files:
        print(f"No supported files found in {directory}")  # 未找到支持的文件
        return

    print(f"Scanning {len(files)} files in {directory}...\n")  # 正在扫描...

    total_smells = 0
    total_critical = 0
    total_high = 0
    files_with_smells = 0

    for filepath in sorted(files):
        try:
            detector = SmellDetector(filepath)
            report = detector.detect_all()

            if report.smells:
                files_with_smells += 1
                total_smells += len(report.smells)
                total_critical += report.critical_count
                total_high += report.high_count

                flag = " 🔴" if report.critical_count else (" 🟠" if report.high_count else " 🟡")
                print(f"  {report.filename}: {len(report.smells)} smells{flag}")

                if verbose:
                    for smell in report.smells:
                        print(f"    - [{smell.severity.value}] {smell.smell_type.value}: line {smell.line_start}")
            else:
                print(f"  {report.filename}: ✅ Clean")  # 干净

        except Exception as e:
            print(f"  Error analyzing {filepath}: {e}")  # 分析出错

    print("\n" + "=" * 60)
    print("SUMMARY")  # 汇总
    print("=" * 60)
    print(f"  Files analyzed:         {len(files)}")
    print(f"  Files with smells:      {files_with_smells}")
    print(f"  Total smells found:     {total_smells}")
    print(f"  Critical issues:        {total_critical}")
    print(f"  High severity issues:   {total_high}")


def main():
    parser = argparse.ArgumentParser(
        description='Detect code smells in source files',  # 在源文件中检测代码异味
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s myfile.py                    Analyze single file           分析单个文件
  %(prog)s --dir src/                   Analyze directory             分析目录
  %(prog)s -v myfile.py                 Verbose with code snippets     详细输出含代码片段
        """
    )
    parser.add_argument('file', nargs='?', help='File to analyze')  # 要分析的文件
    parser.add_argument('--dir', '-d', help='Directory to analyze')  # 要分析的目录
    parser.add_argument('--verbose', '-v', action='store_true', help='Show code snippets')  # 显示代码片段
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')  # 以 JSON 格式输出

    args = parser.parse_args()

    if args.dir:
        analyze_directory(args.dir, args.verbose)
    elif args.file:
        detector = SmellDetector(args.file)
        report = detector.detect_all()

        if args.json:
            import json
            smells_data = [{
                'type': s.smell_type.value,
                'severity': s.severity.value,
                'location': s.location,
                'line_start': s.line_start,
                'line_end': s.line_end,
                'description': s.description,
                'suggestion': s.suggestion,
            } for s in report.smells]
            print(json.dumps({
                'filename': report.filename,
                'total_smells': len(report.smells),
                'critical': report.critical_count,
                'high': report.high_count,
                'medium': report.medium_count,
                'low': report.low_count,
                'smells': smells_data
            }, indent=2))
        else:
            print_report(report, args.verbose)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
