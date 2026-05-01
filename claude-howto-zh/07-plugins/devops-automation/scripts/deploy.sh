#!/bin/bash
set -e

echo "🚀 Starting deployment..."  # 开始部署...

# 加载环境变量
ENV=${1:-staging}
echo "📦 Target environment: $ENV"  # 目标环境

# 部署前检查
echo "✓ Running pre-deployment checks..."  # 正在运行部署前检查...
npm run lint
npm test

# 构建
echo "🔨 Building application..."  # 构建应用中...
npm run build

# 部署
echo "🚢 Deploying to $ENV..."  # 正在部署到 $ENV...
kubectl apply -f k8s/$ENV/

# 健康检查
echo "🏥 Running health checks..."  # 正在运行健康检查...
sleep 10
curl -f http://api.$ENV.example.com/health

echo "✅ Deployment complete!"  # 部署完成！
