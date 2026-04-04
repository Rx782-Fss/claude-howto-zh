#!/usr/bin/env python3
"""重建 Git 仓库：只包含纯净翻译内容"""
import subprocess, os, shutil

REPO = "/data/hhbbfss/project/tre/claude-howto"
os.chdir(REPO)

def run(cmd, **kw):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)
    return r.stdout.strip(), r.returncode, r.stderr.strip()

# 1. 删除旧的 .git
print("[1/5] 清理旧 Git 仓库...")
shutil.rmtree(os.path.join(REPO, ".git"), ignore_errors=True)

# 2. 重新 init
print("[2/5] 初始化新仓库...")
run("git init")
run("git branch -M main")

# 3. 配置用户
run('git config user.name "Rx782-Fss"')
run('git config user.email "Rx782-Fss@users.noreply.github.com"')

# 4. 只添加翻译文件（排除工具文件）
print("[3/5] 添加翻译文件...")

# 需要推送的文件规则：
# - claude-howto-zh/ 下的所有文件 → 添加到 git（展平后）
# - LICENSE → 添加
# - README.md → 添加（已重写为纯净版）
# 排除：
# - scripts/update_translation.sh
# - .gitignore
# - TRANSLATION-STATUS.md
# - .version
# - restructure.sh
# - clean_push.py

# 用 git add 直接指定路径，先复制文件到正确位置再 add
import fileinput

# 将 claude-howto-zh/* 复制到根目录（不删除原文件，本地保留嵌套结构）
src = os.path.join(REPO, "claude-howto-zh")
for root, dirs, files in os.walk(src):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, src)
        dest = os.path.join(REPO, rel)
        # 确保目录存在
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        # 如果目标不存在或不同，就处理
        if not os.path.exists(dest) or (os.path.exists(dest) and 
            os.path.getsize(full) != os.path.getsize(dest)):
            # 不覆盖已有的 README.md 和 LICENSE（我们自己的版本更好）
            if rel in ("README.md", "LICENSE"):
                continue
            if not os.path.exists(dest):
                # 创建符号链接或硬链接？不，直接 copy
                shutil.copy2(full, dest)

# 5. git add 所有需要的文件
print("[4/5] 暂存文件...")
EXCLUDE = {"scripts/update_translation.sh", ".gitignore", "TRANSLATION-STATUS.md",
           ".version", "restructure.sh", "clean_push.py"}

# 使用 git add . 然后移除不需要的
run("git add -A")
for f in EXCLUDE:
    run(f"git rm --cached '{f}' || true")

# 也移除 claude-howto-zh/ 下的内部文件
for f in [".version", "TRANSLATION-STATUS.md"]:
    run(f"git rm --cached 'claude-howto-zh/{f}' || true")

# 6. 提交
print("[5/5] 提交并推送...")
run('git commit -m "claude-howto 中文翻译版 v2.2.0\n\n基于 luongnv89/claude-howto (5900+ Stars)\n完整中文翻译 · 与官方结构 1:1 对齐 · 154 个文件"')

# 推送
token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
run(f"git remote add origin https://{token}@github.com/Rx782-Fss/claude-howto-zh.git")
os.environ["GIT_TERMINAL_PROMPT"] = "0"
out, rc, err = run("git push -u origin main --force")
print(f"Push: {'OK' if rc == 0 else f'FAIL({rc})'} {err[:200]}")

# 恢复干净 URL
run("git remote set-url origin https://github.com/Rx782-Fss/claude-howto-zh.git")

# 验证
out, _, _ = run("git ls-files")
files = out.split("\n") if out else []
nested = [f for f in files if f.startswith("claude-howto-zh/") and not f.startswith("claude-howto-zh/.")]
bad = [f for f in files if any(x in f for x in list(EXCLUDE) + ["restructure", "clean_push"])]

print(f"\n{'='*50}")
print(f"✅ 完成！")
print(f"Git 文件数: {len([f for f in files if f])}")
print(f"残留嵌套: {len(nested)}")
print(f"多余文件: {len(bad)}")
if nested:
    print(f"残留: {nested[:5]}")
if bad:
    print(f"多余: {bad}")
print(f"\nGitHub: https://github.com/Rx782-Fss/claude-howto-zh")
