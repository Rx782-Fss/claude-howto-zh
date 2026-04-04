#!/usr/bin/env python3
"""代码指标分析器

分析代码的常见指标，包括函数数量、类数量、
平均行长度和复杂度评分等。

用法:
    python analyze-metrics.py <源代码文件>
"""

import re
import sys


def analyze_code_metrics(code):
    """分析代码的常见指标。"""

    # 统计函数数量
    functions = len(re.findall(r"^def\s+\w+", code, re.MULTILINE))

    # 统计类数量
    classes = len(re.findall(r"^class\s+\w+", code, re.MULTILINE))

    # 平均行长度
    lines = code.split("\n")
    avg_length = sum(len(l) for l in lines) / len(lines) if lines else 0

    # 估算复杂度（统计决策点）
    complexity = len(re.findall(r"\b(if|elif|else|for|while|and|or)\b", code))

    return {
        "functions": functions,
        "classes": classes,
        "avg_line_length": avg_length,
        "complexity_score": complexity,
    }


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        code = f.read()
    metrics = analyze_code_metrics(code)
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")
