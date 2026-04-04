#!/usr/bin/env python3
"""
代码复杂度分析器

分析 Python、JavaScript 和 TypeScript 文件的代码复杂度指标。
通过比较重构前后的指标来衡量重构的影响效果。

用法:
    python analyze-complexity.py <文件>                    分析单个文件
    python analyze-complexity.py <变更前文件> <变更后文件>  比较模式
    python analyze-complexity.py --dir <目录>              分析整个目录

指标说明:
    - Cyclomatic Complexity（圈复杂度）: 代码中的决策点数量
    - Cognitive Complexity（认知复杂度）: 代码理解难度
    - Maintainability Index（可维护性指数）: 整体可维护性评分 (0-100)
    - Lines of Code（代码行数）: 总行数
    - Function Count（函数数量）: 函数/方法总数
    - Average Function Length（平均函数长度）: 每个函数的平均行数
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class FunctionMetrics:
    """单个函数的指标数据。"""
    name: str
    start_line: int
    end_line: int
    lines: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    parameter_count: int


@dataclass
class FileMetrics:
    """文件的指标数据。"""
    filename: str
    lines_of_code: int
    blank_lines: int
    comment_lines: int
    function_count: int
    class_count: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    maintainability_index: float
    avg_function_length: float
    max_function_length: int
    functions: List[FunctionMetrics]


class ComplexityAnalyzer:
    """分析多种语言的代码复杂度。"""

    # 不同语言的模式定义
    PATTERNS = {
        'python': {
            'function': r'^\s*def\s+(\w+)\s*\(',
            'class': r'^\s*class\s+(\w+)',
            'decision': [r'\bif\b', r'\belif\b', r'\bfor\b', r'\bwhile\b',
                        r'\bexcept\b', r'\band\b(?!$)', r'\bor\b(?!$)',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*#',
            'multiline_comment_start': r'^\s*["\'][\"\'][\"\']',
            'multiline_comment_end': r'["\'][\"\'][\"\']',
        },
        'javascript': {
            'function': r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
            'class': r'class\s+(\w+)',
            'decision': [r'\bif\b', r'\belse\s+if\b', r'\bfor\b', r'\bwhile\b',
                        r'\bcatch\b', r'\b\?\b', r'\b&&\b', r'\b\|\|\b',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*//',
            'multiline_comment_start': r'/\*',
            'multiline_comment_end': r'\*/',
        },
        'typescript': {
            'function': r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
            'class': r'class\s+(\w+)',
            'decision': [r'\bif\b', r'\belse\s+if\b', r'\bfor\b', r'\bwhile\b',
                        r'\bcatch\b', r'\b\?\b', r'\b&&\b', r'\b\|\|\b',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*//',
            'multiline_comment_start': r'/\*',
            'multiline_comment_end': r'\*/',
        }
    }

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.language = self._detect_language()
        self.patterns = self.PATTERNS.get(self.language, self.PATTERNS['python'])

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            self.code = f.read()
        self.lines = self.code.split('\n')

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

    def calculate_cyclomatic_complexity(self, code: Optional[str] = None) -> int:
        """
        使用 McCabe 方法计算圈复杂度。
        CC = E - N + 2P，其中 E=边数, N=节点数, P=连通分量数
        简化版：统计决策点数 + 1
        """
        if code is None:
            code = self.code

        complexity = 1  # 基础复杂度

        for pattern in self.patterns['decision']:
            matches = re.findall(pattern, code)
            complexity += len(matches)

        return complexity

    def calculate_cognitive_complexity(self, code: Optional[str] = None) -> int:
        """
        计算认知复杂度。
        衡量代码的理解难度。
        考虑嵌套深度和控制流中断情况。
        """
        if code is None:
            code = self.code

        lines = code.split('\n')
        cognitive = 0
        nesting_depth = 0
        in_function = False

        for line in lines:
            stripped = line.strip()

            # 跟踪函数边界
            if re.search(self.patterns['function'], line):
                in_function = True
                nesting_depth = 0

            # 控制流结构时增加计数
            if re.search(r'\b(if|for|while|switch)\b', stripped):
                nesting_depth += 1
                cognitive += nesting_depth  # 嵌套结构代价更高

            elif re.search(r'\b(elif|else if|else|catch|finally)\b', stripped):
                cognitive += nesting_depth  # 与父级同级

            # 通过花括号/缩进跟踪嵌套深度
            if self.language in ['javascript', 'typescript']:
                nesting_depth += stripped.count('{') - stripped.count('}')
                nesting_depth = max(0, nesting_depth)

            # 线性流中断的额外加分
            if re.search(r'\b(break|continue|return|throw)\b', stripped):
                if nesting_depth > 1:
                    cognitive += 1

            # 递归的额外加分
            # （简化版：仅查找函数调用自身的情况）

        return cognitive

    def calculate_maintainability_index(self) -> float:
        """
        计算可维护性指数 (0-100)。
        基于 Halstead Volume、圈复杂度和代码行数。

        MI = max(0, (171 - 5.2*ln(V) - 0.23*CC - 16.2*ln(LOC)) * 100/171)

        解读标准：
        - 85-100: 高度可维护
        - 65-84: 中等可维护
        - 50-64: 难以维护
        - 0-49: 非常难以维护
        """
        import math

        loc = len([l for l in self.lines if l.strip()])
        cc = self.calculate_cyclomatic_complexity()

        # 简化的 Halstead Volume 近似计算
        # 统计唯一运算符和操作数
        operators = len(re.findall(r'[+\-*/%=<>!&|^~]', self.code))
        operands = len(re.findall(r'\b\w+\b', self.code))
        volume = (operators + operands) * math.log2(max(1, operators + operands))

        # 计算 MI
        mi = 171 - 5.2 * math.log(max(1, volume)) - 0.23 * cc - 16.2 * math.log(max(1, loc))
        mi = max(0, min(100, mi * 100 / 171))

        return round(mi, 2)

    def count_lines(self) -> Dict[str, int]:
        """统计不同类型的行数。"""
        total = len(self.lines)
        blank = 0
        comment = 0
        in_multiline_comment = False

        for line in self.lines:
            stripped = line.strip()

            # 检查多行注释
            if re.search(self.patterns['multiline_comment_start'], stripped):
                in_multiline_comment = True
            if re.search(self.patterns['multiline_comment_end'], stripped):
                in_multiline_comment = False
                comment += 1
                continue

            if in_multiline_comment:
                comment += 1
            elif not stripped:
                blank += 1
            elif re.match(self.patterns['comment'], stripped):
                comment += 1

        return {
            'total': total,
            'blank': blank,
            'comment': comment,
            'code': total - blank - comment
        }

    def find_functions(self) -> List[FunctionMetrics]:
        """查找所有函数并计算各自的指标。"""
        functions = []
        current_function = None
        function_start = 0
        brace_depth = 0

        for i, line in enumerate(self.lines):
            # 检查函数定义
            match = re.search(self.patterns['function'], line)
            if match:
                # 如果存在前一个函数则保存
                if current_function:
                    func_code = '\n'.join(self.lines[function_start:i])
                    functions.append(self._create_function_metrics(
                        current_function, function_start, i - 1, func_code
                    ))

                current_function = match.group(1) or match.group(2) if match.lastindex and match.lastindex > 1 else match.group(1)
                function_start = i
                brace_depth = 0

            # 跟踪 JS/TS 的花括号
            if self.language in ['javascript', 'typescript']:
                brace_depth += line.count('{') - line.count('}')

        # 不要忘记最后一个函数
        if current_function:
            func_code = '\n'.join(self.lines[function_start:])
            functions.append(self._create_function_metrics(
                current_function, function_start, len(self.lines) - 1, func_code
            ))

        return functions

    def _create_function_metrics(self, name: str, start: int, end: int, code: str) -> FunctionMetrics:
        """为单个函数创建指标。"""
        lines = end - start + 1

        # 统计参数（简化版）
        param_match = re.search(r'\(([^)]*)\)', code.split('\n')[0])
        param_count = 0
        if param_match and param_match.group(1).strip():
            param_count = len([p for p in param_match.group(1).split(',') if p.strip()])

        return FunctionMetrics(
            name=name,
            start_line=start + 1,
            end_line=end + 1,
            lines=lines,
            cyclomatic_complexity=self.calculate_cyclomatic_complexity(code),
            cognitive_complexity=self.calculate_cognitive_complexity(code),
            parameter_count=param_count
        )

    def analyze(self) -> FileMetrics:
        """对文件执行完整分析。"""
        line_counts = self.count_lines()
        functions = self.find_functions()

        # 统计类数量
        class_count = len(re.findall(self.patterns['class'], self.code))

        # 计算平均值
        func_lengths = [f.lines for f in functions] if functions else [0]
        avg_func_length = sum(func_lengths) / len(func_lengths)
        max_func_length = max(func_lengths)

        return FileMetrics(
            filename=self.filename,
            lines_of_code=line_counts['code'],
            blank_lines=line_counts['blank'],
            comment_lines=line_counts['comment'],
            function_count=len(functions),
            class_count=class_count,
            cyclomatic_complexity=self.calculate_cyclomatic_complexity(),
            cognitive_complexity=self.calculate_cognitive_complexity(),
            maintainability_index=self.calculate_maintainability_index(),
            avg_function_length=round(avg_func_length, 1),
            max_function_length=max_func_length,
            functions=functions
        )


def print_metrics(metrics: FileMetrics, verbose: bool = False) -> None:
    """以可读格式打印指标。"""
    print("=" * 60)
    print(f"CODE COMPLEXITY ANALYSIS: {metrics.filename}")  # 代码复杂度分析
    print("=" * 60)

    print("\n📊 OVERVIEW")  # 概览
    print("-" * 40)
    print(f"  Lines of Code:          {metrics.lines_of_code}")
    print(f"  Blank Lines:            {metrics.blank_lines}")
    print(f"  Comment Lines:          {metrics.comment_lines}")
    print(f"  Functions/Methods:      {metrics.function_count}")
    print(f"  Classes:                {metrics.class_count}")

    print("\n📈 COMPLEXITY METRICS")  # 复杂度指标
    print("-" * 40)
    print(f"  Cyclomatic Complexity:  {metrics.cyclomatic_complexity}")
    print(f"  Cognitive Complexity:   {metrics.cognitive_complexity}")
    print(f"  Maintainability Index:  {metrics.maintainability_index}")

    # 解读可维护性指数
    mi = metrics.maintainability_index
    if mi >= 85:
        mi_label = "Highly maintainable ✅"
    elif mi >= 65:
        mi_label = "Moderately maintainable 🔶"
    elif mi >= 50:
        mi_label = "Difficult to maintain ⚠️"
    else:
        mi_label = "Very difficult to maintain ❌"
    print(f"    → {mi_label}")

    print("\n📐 FUNCTION METRICS")  # 函数指标
    print("-" * 40)
    print(f"  Avg Function Length:    {metrics.avg_function_length} lines")
    print(f"  Max Function Length:    {metrics.max_function_length} lines")

    if verbose and metrics.functions:
        print("\n📋 FUNCTION DETAILS")  # 函数详情
        print("-" * 40)
        for f in sorted(metrics.functions, key=lambda x: x.cyclomatic_complexity, reverse=True):
            flag = " ⚠️" if f.cyclomatic_complexity > 10 or f.lines > 50 else ""
            print(f"  {f.name}() [lines {f.start_line}-{f.end_line}]{flag}")
            print(f"    - Lines: {f.lines}, CC: {f.cyclomatic_complexity}, "
                  f"Cognitive: {f.cognitive_complexity}, Params: {f.parameter_count}")

    print("\n" + "=" * 60)


def print_comparison(before: FileMetrics, after: FileMetrics) -> None:
    """打印两次分析之间的对比结果。"""
    print("=" * 70)
    print("CODE COMPLEXITY COMPARISON")  # 代码复杂度对比
    print("=" * 70)

    print(f"\n{'Metric':<30} {'Before':<15} {'After':<15} {'Change':<10}")
    print("-" * 70)

    def fmt_change(before_val, after_val, lower_is_better=True):
        diff = after_val - before_val
        if lower_is_better:
            symbol = "✅" if diff < 0 else ("⚠️" if diff > 0 else "➖")
        else:
            symbol = "✅" if diff > 0 else ("⚠️" if diff < 0 else "➖")
        return f"{diff:+.1f} {symbol}" if isinstance(diff, float) else f"{diff:+d} {symbol}"

    metrics = [
        ("Lines of Code", before.lines_of_code, after.lines_of_code, True),
        ("Function Count", before.function_count, after.function_count, False),
        ("Class Count", before.class_count, after.class_count, False),
        ("Cyclomatic Complexity", before.cyclomatic_complexity, after.cyclomatic_complexity, True),
        ("Cognitive Complexity", before.cognitive_complexity, after.cognitive_complexity, True),
        ("Maintainability Index", before.maintainability_index, after.maintainability_index, False),
        ("Avg Function Length", before.avg_function_length, after.avg_function_length, True),
        ("Max Function Length", before.max_function_length, after.max_function_length, True),
    ]

    for name, b_val, a_val, lower_better in metrics:
        change = fmt_change(b_val, a_val, lower_better)
        print(f"{name:<30} {b_val:<15} {a_val:<15} {change:<10}")

    print("\n" + "=" * 70)

    # 总体评估
    print("\n🎯 ASSESSMENT")  # 评估结论
    print("-" * 40)

    improvements = 0
    regressions = 0

    if after.maintainability_index > before.maintainability_index:
        print("  ✅ Maintainability improved")  # 可维护性提升
        improvements += 1
    elif after.maintainability_index < before.maintainability_index:
        print("  ⚠️ Maintainability decreased")  # 可维护性下降
        regressions += 1

    if after.cyclomatic_complexity < before.cyclomatic_complexity:
        print("  ✅ Complexity reduced")  # 复杂度降低
        improvements += 1
    elif after.cyclomatic_complexity > before.cyclomatic_complexity:
        print("  ⚠️ Complexity increased")  # 复杂度升高
        regressions += 1

    if after.avg_function_length < before.avg_function_length:
        print("  ✅ Functions are smaller on average")  # 平均函数更小
        improvements += 1
    elif after.avg_function_length > before.avg_function_length:
        print("  ⚠️ Functions grew larger on average")  # 平均函数变大
        regressions += 1

    print(f"\n  Summary: {improvements} improvements, {regressions} regressions")
    print("=" * 70)


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

    print(f"Analyzing {len(files)} files in {directory}...\n")  # 正在分析...

    total_loc = 0
    total_cc = 0
    total_functions = 0
    all_metrics = []

    for filepath in sorted(files):
        try:
            analyzer = ComplexityAnalyzer(filepath)
            metrics = analyzer.analyze()
            all_metrics.append(metrics)

            total_loc += metrics.lines_of_code
            total_cc += metrics.cyclomatic_complexity
            total_functions += metrics.function_count

            if verbose:
                print_metrics(metrics, verbose=True)
            else:
                flag = " ⚠️" if metrics.maintainability_index < 65 else ""
                print(f"  {metrics.filename}: LOC={metrics.lines_of_code}, "
                      f"CC={metrics.cyclomatic_complexity}, MI={metrics.maintainability_index}{flag}")
        except Exception as e:
            print(f"  Error analyzing {filepath}: {e}")  # 分析出错

    print("\n" + "=" * 60)
    print("SUMMARY")  # 汇总
    print("=" * 60)
    print(f"  Files analyzed:         {len(all_metrics)}")
    print(f"  Total lines of code:    {total_loc}")
    print(f"  Total complexity:       {total_cc}")
    print(f"  Total functions:        {total_functions}")

    if all_metrics:
        avg_mi = sum(m.maintainability_index for m in all_metrics) / len(all_metrics)
        print(f"  Avg maintainability:    {avg_mi:.1f}")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze code complexity metrics',  # 分析代码复杂度指标
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s myfile.py                    Analyze single file           分析单个文件
  %(prog)s before.py after.py           Compare two versions         比较两个版本
  %(prog)s --dir src/                   Analyze directory             分析目录
  %(prog)s -v myfile.py                 Verbose output with details   详细输出含函数详情
        """
    )
    parser.add_argument('files', nargs='*', help='File(s) to analyze')  # 要分析的文件
    parser.add_argument('--dir', '-d', help='Directory to analyze')     # 要分析的目录
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed function metrics')  # 显示详细函数指标
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')  # 以 JSON 格式输出

    args = parser.parse_args()

    if args.dir:
        analyze_directory(args.dir, args.verbose)
    elif len(args.files) == 1:
        analyzer = ComplexityAnalyzer(args.files[0])
        metrics = analyzer.analyze()

        if args.json:
            import json
            print(json.dumps({
                'filename': metrics.filename,
                'lines_of_code': metrics.lines_of_code,
                'cyclomatic_complexity': metrics.cyclomatic_complexity,
                'cognitive_complexity': metrics.cognitive_complexity,
                'maintainability_index': metrics.maintainability_index,
                'function_count': metrics.function_count,
                'avg_function_length': metrics.avg_function_length,
            }, indent=2))
        else:
            print_metrics(metrics, args.verbose)
    elif len(args.files) == 2:
        before_analyzer = ComplexityAnalyzer(args.files[0])
        after_analyzer = ComplexityAnalyzer(args.files[1])
        before_metrics = before_analyzer.analyze()
        after_metrics = after_analyzer.analyze()
        print_comparison(before_metrics, after_metrics)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
