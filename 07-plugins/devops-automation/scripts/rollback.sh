#!/bin/bash
set -e

echo "⏪ Starting rollback..."  # 开始回滚...

ENV=${1:-staging}
echo "📦 Target environment: $ENV"  # 目标环境

# 获取上一个部署版本
PREVIOUS=$(kubectl rollout history deployment/app -n $ENV | tail -2 | head -1 | awk '{print $1}')
echo "🔄 Rolling back to revision: $PREVIOUS"  # 正在回滚到版本

# 执行回滚
kubectl rollout undo deployment/app -n $ENV

# 等待回滚完成
echo "⏳ Waiting for rollback to complete..."  # 等待回滚完成...
kubectl rollout status deployment/app -n $ENV

# 健康检查
echo "🏥 Running health checks..."  # 正在运行健康检查...
sleep 5
curl -f http://api.$ENV.example.com/health

echo "✅ Rollback complete!"  # 回滚完成！
