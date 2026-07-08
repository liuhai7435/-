[app]

package.name = 测试
package.domain = com.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,json
source.include_patterns = templates/**,static/**
version = 1.0

title = 测试

main.py = main.py

requirements = python3,kivy,flask

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 24
android.ndk = 26b
android.accept_sdk_license = True
android.allow_clear_text = True
android.build_tools_version = 33.0.2

orientation = portrait

build_dir = .buildozer
log_level = 2

[buildozer]
log_level = 2
