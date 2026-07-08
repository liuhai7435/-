[app]

# 应用包名
package.name = 测试
package.domain = com.test

# 源码和资源
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,json
source.include_patterns = templates/**,static/**
version = 1.0

# 应用标题
title = 测试

# 入口
main.py = main.py

# 依赖
requirements = python3,kivy,flask

# Android 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android 版本
android.api = 34
android.minapi = 24
android.ndk = 25b
android.sdk = 34

# 架构（armeabi-v7a 兼容更多设备，arm64-v8a 性能更好）
android.arch = arm64-v8a

# 允许 HTTP 明文（Flask 本地用）
android.allow_clear_text = True

# 竖屏
orientation = portrait

# 构建输出
build_dir = .buildozer
log_level = 2

# ── buildozer 设置 ────────────────────
[buildozer]
log_level = 2
