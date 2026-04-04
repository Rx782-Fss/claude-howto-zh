#!/usr/bin/env python3
"""
API 文档提取器

从 Python 源代码中提取 API 文档信息，
自动生成 Markdown 格式的 API 文档。

用法:
    python generate-docs.py <Python源文件>
"""

import ast


class APIDocExtractor(ast.NodeVisitor):
    """从 Python 源代码中提取 API 文档。"""

    def __init__(self):
        self.endpoints = []

    def visit_FunctionDef(self, node):
        """提取函数文档信息。"""
        if node.name.startswith("get_") or node.name.startswith("post_"):
            doc = ast.get_docstring(node)
            endpoint = {
                "name": node.name,
                "docstring": doc,
                "params": [arg.arg for arg in node.args.args],
                "returns": self._extract_return_type(node),
            }
            self.endpoints.append(endpoint)
        self.generic_visit(node)

    def _extract_return_type(self, node):
        """从函数注解中提取返回类型。"""
        if node.returns:
            return ast.unparse(node.returns)
        return "Any"


def generate_markdown_docs(endpoints: list[dict]) -> str:
    """根据端点列表生成 Markdown 格式的文档。"""
    docs = "# API Documentation\n\n"  # API 文档

    for endpoint in endpoints:
        docs += f"## {endpoint['name']}\n\n"
        docs += f"{endpoint['docstring']}\n\n"
        docs += f"**Parameters**: {', '.join(endpoint['params'])}\n\n"  # 参数
        docs += f"**Returns**: {endpoint['returns']}\n\n"  # 返回值
        docs += "---\n\n"

    return docs


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as f:
        tree = ast.parse(f.read())

    extractor = APIDocExtractor()
    extractor.visit(tree)

    markdown = generate_markdown_docs(extractor.endpoints)
    print(markdown)
