#!/usr/bin/env python3
"""
setup-auto-mode-permissions.py

为 Claude Code 的 ~/.claude/settings.json 文件初始化一套保守且安全的权限基线。
默认集合为只读和本地检查导向；可选标志允许你扩展白名单，
以涵盖编辑操作、测试执行、Git 写操作、包安装以及 GitHub CLI 写操作。

用法:
    python3 setup-auto-mode-permissions.py
    python3 setup-auto-mode-permissions.py --dry-run
    python3 setup-auto-mode-permissions.py --include-edits --include-tests
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Iterable

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

# 核心基线：只读检查和低风险的本地 Shell 命令。
CORE_PERMISSIONS = [
    "Read(*)",
    "Glob(*)",
    "Grep(*)",
    "Agent(*)",
    "Skill(*)",
    "WebSearch(*)",
    "WebFetch(*)",
    "Bash(ls:*)",
    "Bash(pwd:*)",
    "Bash(which:*)",
    "Bash(echo:*)",
    "Bash(cat:*)",
    "Bash(head:*)",
    "Bash(tail:*)",
    "Bash(wc:*)",
    "Bash(sort:*)",
    "Bash(uniq:*)",
    "Bash(find:*)",
    "Bash(dirname:*)",
    "Bash(basename:*)",
    "Bash(realpath:*)",
    "Bash(file:*)",
    "Bash(stat:*)",
    "Bash(diff:*)",
    "Bash(md5sum:*)",
    "Bash(sha256sum:*)",
    "Bash(date:*)",
    "Bash(env:*)",
    "Bash(printenv:*)",
    "Bash(git status:*)",
    "Bash(git log:*)",
    "Bash(git diff:*)",
    "Bash(git branch:*)",
    "Bash(git show:*)",
    "Bash(git rev-parse:*)",
    "Bash(git remote -v:*)",
    "Bash(git remote get-url:*)",
    "Bash(git stash list:*)",
]

# 可选但仍属于本地的：文件编辑和任务管理。
EDITING_PERMISSIONS = [
    "Edit(*)",
    "Write(*)",
    "NotebookEdit(*)",
    "TaskCreate(*)",
    "TaskUpdate(*)",
]

# 可选的开发/测试命令。这些命令仍可执行任意项目脚本，
# 因此采用 opt-in 方式而非默认包含在基线中。
TEST_AND_BUILD_PERMISSIONS = [
    "Bash(npm test:*)",
    "Bash(cargo test:*)",
    "Bash(go test:*)",
    "Bash(pytest:*)",
    "Bash(python3 -m pytest:*)",
    "Bash(make:*)",
    "Bash(cmake:*)",
]

# 可选的本地 Git 写操作。历史重写命令被排除在默认基线之外，
# 因为它们容易被误用。
GIT_WRITE_PERMISSIONS = [
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git checkout:*)",
    "Bash(git switch:*)",
    "Bash(git stash:*)",
    "Bash(git tag:*)",
]

# 可选的依赖/包管理命令。这些被有意排除在默认基线之外，
# 因为它们可以执行项目钩子或拉取代码。
PACKAGE_MANAGER_PERMISSIONS = [
    "Bash(npm ci:*)",
    "Bash(npm install:*)",
    "Bash(pip install:*)",
    "Bash(pip3 install:*)",
]

# 可选的 GitHub CLI 写权限。
GITHUB_WRITE_PERMISSIONS = [
    "Bash(gh pr create:*)",
]

# 可选的 GitHub CLI 读权限。
GITHUB_READ_PERMISSIONS = [
    "Bash(gh pr view:*)",
    "Bash(gh pr list:*)",
    "Bash(gh issue view:*)",
    "Bash(gh issue list:*)",
    "Bash(gh repo view:*)",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="为 Claude Code 设置文件初始化保守的权限基线。"  # Seed Claude Code settings with a conservative permission baseline.
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览将要添加的规则而不实际写入 settings.json"  # Preview rules without writing settings.json
    )
    parser.add_argument(
        "--include-edits",
        action="store_true",
        help="添加文件编辑权限（Edit/Write/NotebookEdit/TaskCreate/TaskUpdate）"
    )
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="添加本地构建/测试命令，如 pytest、cargo test 和 make"
    )
    parser.add_argument(
        "--include-git-write",
        action="store_true",
        help="添加本地 Git 变更命令，如 add、commit、checkout 和 stash"
    )
    parser.add_argument(
        "--include-packages",
        action="store_true",
        help="添加包安装命令，如 npm ci、npm install 和 pip install"
    )
    parser.add_argument(
        "--include-gh-write",
        action="store_true",
        help="添加 GitHub CLI 写权限，如 gh pr create"
    )
    parser.add_argument(
        "--include-gh-read",
        action="store_true",
        help="添加 GitHub CLI 读权限，如 gh pr view 和 gh repo view"
    )
    return parser.parse_args()


def load_settings(path: Path) -> dict:
    """加载现有设置文件。"""
    if not path.exists():
        return {}

    try:
        with path.open() as f:
            settings = json.load(f)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path} 中的 JSON 无效: {exc}") from exc

    if not isinstance(settings, dict):
        raise SystemExit(f"期望 {path} 包含 JSON 对象。")

    return settings


def build_permissions(args: argparse.Namespace) -> list[str]:
    """根据参数构建完整的权限列表。"""
    permissions = list(CORE_PERMISSIONS)

    if args.include_edits:
        permissions.extend(EDITING_PERMISSIONS)

    if args.include_tests:
        permissions.extend(TEST_AND_BUILD_PERMISSIONS)

    if args.include_git_write:
        permissions.extend(GIT_WRITE_PERMISSIONS)

    if args.include_packages:
        permissions.extend(PACKAGE_MANAGER_PERMISSIONS)

    if args.include_gh_write:
        permissions.extend(GITHUB_WRITE_PERMISSIONS)

    if args.include_gh_read:
        permissions.extend(GITHUB_READ_PERMISSIONS)

    return permissions


def append_unique(existing: list, new_items: Iterable[str]) -> list[str]:
    """向已有列表追加唯一的新项目，返回新增的项目列表。"""
    seen = set(existing)
    added: list[str] = []
    for item in new_items:
        if item not in seen:
            existing.append(item)
            seen.add(item)
            added.append(item)
    return added


def atomic_write_json(path: Path, payload: dict) -> None:
    """原子性地写入 JSON 文件，避免写入中途损坏。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(path.parent),
        delete=False,
    ) as tmp:
        json.dump(payload, tmp, indent=2)
        tmp.write("\n")
        tmp_path = Path(tmp.name)

    tmp_path.replace(path)


def main() -> None:
    """主入口函数。"""
    args = parse_args()
    permissions_to_add = build_permissions(args)

    settings = load_settings(SETTINGS_PATH)
    permissions = settings.setdefault("permissions", {})

    if not isinstance(permissions, dict):
        raise SystemExit("期望 permissions 是一个 JSON 对象。")

    allow = permissions.setdefault("allow", [])
    if not isinstance(allow, list):
        raise SystemExit("期望 permissions.allow 是一个 JSON 数组。")

    added = append_unique(allow, permissions_to_add)

    if not added:
        print("无需添加 — 所有选定的规则已存在。")  # Nothing to add
        return

    print(f"{'将会添加' if args.dry_run else '正在添加'} {len(added)} 条规则:")
    for rule in added:
        print(f"  + {rule}")

    if args.dry_run:
        print("\n试运行模式 — 未做任何更改。")  # Dry run — no changes written.
        return

    atomic_write_json(SETTINGS_PATH, settings)
    print(f"\n完成。{len(added)} 条规则已添加到 {SETTINGS_PATH}")  # Done.


if __name__ == "__main__":
    main()
