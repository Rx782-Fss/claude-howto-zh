#!/usr/bin/env node

/**
 * 审查前钩子（Pre-review Hook）
 * 在开始 PR 审查之前运行，确保前置条件已满足
 */

async function preReview() {
  console.log('Running pre-review checks...');  // 正在运行审查前检查...

  // 检查是否为 git 仓库
  const { execSync } = require('child_process');
  try {
    execSync('git rev-parse --git-dir', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ Not a git repository');  // 不是 git 仓库
    process.exit(1);
  }

  // 检查是否有未提交的更改
  try {
    const status = execSync('git status --porcelain', { encoding: 'utf-8' });
    if (status.trim()) {
      console.warn('⚠️  Warning: Uncommitted changes detected');  // 警告：检测到未提交的更改
    }
  } catch (error) {
    console.error('❌ Failed to check git status');  // 无法检查 git 状态
    process.exit(1);
  }

  console.log('✅ Pre-review checks passed');  // 审查前检查通过
}

preReview().catch(error => {
  console.error('Pre-review hook failed:', error);  // 审查前钩子执行失败
  process.exit(1);
});
