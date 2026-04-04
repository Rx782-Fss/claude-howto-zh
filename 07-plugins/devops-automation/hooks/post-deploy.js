#!/usr/bin/env node

/**
 * 部署后钩子（Post-deployment Hook）
 * 在部署完成后运行
 */

async function postDeploy() {
  console.log('Running post-deployment tasks...');  // 正在运行部署后任务...

  const { execSync } = require('child_process');

  // 等待 Pod 就绪
  console.log('Waiting for pods to be ready...');  // 等待 Pod 就绪...
  try {
    execSync('kubectl wait --for=condition=ready pod -l app=myapp --timeout=300s', {
      stdio: 'inherit'
    });
  } catch (error) {
    console.error('❌ Pods failed to become ready');  // Pod 未能就绪
    process.exit(1);
  }

  // 运行冒烟测试
  console.log('Running smoke tests...');  // 正在运行冒烟测试...
  // 在此处添加你的冒烟测试命令

  console.log('✅ Post-deployment tasks complete');  // 部署后任务完成
}

postDeploy().catch(error => {
  console.error('Post-deploy hook failed:', error);  // 部署后钩子执行失败
  process.exit(1);
});
