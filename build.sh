#!/bin/bash
# 一键构建 APK（需要 Docker）
# 用法: bash build.sh

set -e

echo "🔨 构建 Docker 镜像..."
docker build -t flask-apk-builder .

echo "📦 开始编译 APK（首次约 20-40 分钟）..."
docker run --rm -v "$(pwd)/bin:/app/bin" flask-apk-builder

echo "✅ 完成！APK 在 ./bin 目录下"
ls -lh bin/*.apk
