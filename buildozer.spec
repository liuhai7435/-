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

# Android SDK 版本
android.api = 33
android.minapi = 24

# 使用更稳定的 NDK（与 buildozer 1.6.0 兼容）
android.ndk = 26b

# 允许 HTTP
android.allow_clear_text = True

# 竖屏
orientation = portrait

# 自动接受 SDK 许可
android.accept_sdk_license = True

# p4a 分支
p4a.branch = master

# 构建输出
build_dir = .buildozer
log_level = 2

[buildozer]
log_level = 2
