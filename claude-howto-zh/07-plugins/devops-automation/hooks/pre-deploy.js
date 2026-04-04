#!/usr/bin/env node

/**
 * 部署前钩子（Pre-deployment Hook）
 * 在部署前验证环境和前置条件
 */

async function preDeploy() {
  console.log('Running pre-deployment checks...');  // 正在运行部署前检查...

  const { execSync } = require('child_process');

  // 检查 kubectl 是否已安装
  try {
    execSync('which kubectl', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ kubectl not found. Please install Kubernetes CLI.');  // 未找到 kubectl，请安装 Kubernetes CLI
    process.exit(1);
  }

  // 检查是否已连接集群
  try {
    execSync('kubectl cluster-info', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ Not connected to Kubernetes cluster');  // 未连接到 Kubernetes 集群
    process.exit(1);
  }

  console.log('✅ Pre-deployment checks passed');  // 部署前检查通过
}

preDeploy().catch(error => {
  console.error('Pre-deploy hook failed:', error);  // 部署前钩子执行失败
  process.exit(1);
});
