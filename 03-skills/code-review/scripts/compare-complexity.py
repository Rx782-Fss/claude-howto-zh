#!/usr/bin/env python3
"""
圈复杂度比较工具

比较代码变更前后的圈复杂度（Cyclomatic Complexity）。
帮助判断重构是否真正简化了代码结构。

用法:
    python compare-complexity.py <变更前文件> <变更后文件>
"""

import re
import sys


class ComplexityAnalyzer:
    """分析代码复杂度指标。"""

    def __init__(self, code: str):
        self.code = code
        self.lines = code.split("\n")

    def calculate_cyclomatic_complexity(self) -> int:
        """
        使用 McCabe 方法计算圈复杂度。
        统计决策点：if, elif, else, for, while, except, and, or
        """
        complexity = 1  # 基础复杂度

        # 统计决策点模式
        decision_patterns = [
            r"\bif\b",
            r"\belif\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\bexcept\b",
            r"\band\b(?!$)",
            r"\bor\b(?!$)",
        ]

        for pattern in decision_patterns:
            matches = re.findall(pattern, self.code)
            complexity += len(matches)

        return complexity

    def calculate_cognitive_complexity(self) -> int:
        """
        认知复杂度 — 代码有多难理解？
        基于嵌套深度和控制流进行评估。
        """
        cognitive = 0
        nesting_depth = 0

        for line in self.lines:
            # 跟踪嵌套深度
            if re.search(r"^\s*(if|for|while|def|class|try)\b", line):
                nesting_depth += 1
                cognitive += nesting_depth
            elif re.search(r"^\s*(elif|else|except|finally)\b", line):
                cognitive += nesting_depth

            # 缩进减少时降低嵌套深度
            if line and not line[0].isspace():
                nesting_depth = 0

        return cognitive

    def calculate_maintainability_index(self) -> float:
        """
        可维护性指数（Maintainability Index），范围 0-100。
        > 85: 优秀
        > 65: 良好
        > 50: 一般
        < 50: 较差
        """
        lines = len(self.lines)
        cyclomatic = self.calculate_cyclomatic_complexity()
        cognitive = self.calculate_cognitive_complexity()

        # 简化的 MI 计算公式
        mi = (
            171
            - 5.2 * (cyclomatic / lines)
            - 0.23 * (cognitive)
            - 16.2 * (lines / 1000)
        )

        return max(0, min(100, mi))

    def get_complexity_report(self) -> dict:
        """生成完整的复杂度报告。"""
        return {
            "cyclomatic_complexity": self.calculate_cyclomatic_complexity(),
            "cognitive_complexity": self.calculate_cognitive_complexity(),
            "maintainability_index": round(self.calculate_maintainability_index(), 2),
            "lines_of_code": len(self.lines),
            "avg_line_length": round(
                sum(len(l) for l in self.lines) / len(self.lines), 2
            )
            if self.lines
            else 0,
        }


def compare_files(before_file: str, after_file: str) -> None:
    """比较两个代码版本之间的复杂度指标。"""

    with open(before_file) as f:
        before_code = f.read()

    with open(after_file) as f:
        after_code = f.read()

    before_analyzer = ComplexityAnalyzer(before_code)
    after_analyzer = ComplexityAnalyzer(after_code)

    before_metrics = before_analyzer.get_complexity_report()
    after_metrics = after_analyzer.get_complexity_report()

    print("=" * 60)
    print("CODE COMPLEXITY COMPARISON")  # 代码复杂度对比
    print("=" * 60)

    print("\nBEFORE:")  # 变更前
    print(f"  Cyclomatic Complexity:    {before_metrics['cyclomatic_complexity']}")
    print(f"  Cognitive Complexity:     {before_metrics['cognitive_complexity']}")
    print(f"  Maintainability Index:    {before_metrics['maintainability_index']}")
    print(f"  Lines of Code:            {before_metrics['lines_of_code']}")
    print(f"  Avg Line Length:          {before_metrics['avg_line_length']}")

    print("\nAFTER:")  # 变更后
    print(f"  Cyclomatic Complexity:    {after_metrics['cyclomatic_complexity']}")
    print(f"  Cognitive Complexity:     {after_metrics['cognitive_complexity']}")
    print(f"  Maintainability Index:    {after_metrics['maintainability_index']}")
    print(f"  Lines of Code:            {after_metrics['lines_of_code']}")
    print(f"  Avg Line Length:          {after_metrics['avg_line_length']}")

    print("\nCHANGES:")  # 变化量
    cyclomatic_change = (
        after_metrics["cyclomatic_complexity"] - before_metrics["cyclomatic_complexity"]
    )
    cognitive_change = (
        after_metrics["cognitive_complexity"] - before_metrics["cognitive_complexity"]
    )
    mi_change = (
        after_metrics["maintainability_index"] - before_metrics["maintainability_index"]
    )
    loc_change = after_metrics["lines_of_code"] - before_metrics["lines_of_code"]

    print(f"  Cyclomatic Complexity:    {cyclomatic_change:+d}")
    print(f"  Cognitive Complexity:     {cognitive_change:+d}")
    print(f"  Maintainability Index:    {mi_change:+.2f}")
    print(f"  Lines of Code:            {loc_change:+d}")

    print("\nASSESSMENT:")  # 评估结论
    if mi_change > 0:
        print("  ✅ Code is MORE maintainable")  # 代码可维护性提升
    elif mi_change < 0:
        print("  ⚠️  Code is LESS maintainable")  # 代码可维护性下降
    else:
        print("  ➡️  Maintainability unchanged")  # 可维护性不变

    if cyclomatic_change < 0:
        print("  ✅ Complexity DECREASED")  # 复杂度降低
    elif cyclomatic_change > 0:
        print("  ⚠️  Complexity INCREASED")  # 复杂度升高
    else:
        print("  ➡️  Complexity unchanged")  # 复杂度不变

    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare-complexity.py <before_file> <after_file>")
        sys.exit(1)

    compare_files(sys.argv[1], sys.argv[2])
