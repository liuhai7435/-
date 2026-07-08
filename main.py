"""
APK 入口 - 在后台运行 Flask，通过 Android WebView 显示页面
"""

import threading
import os
import time

# ── Flask 后端 ────────────────────────────────
from flask import Flask, render_template

# 确保模板路径正确（Android APK 中工作目录可能不同）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
flask_app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)


@flask_app.route("/")
def index():
    return render_template("index.html", name="测试")


def run_flask():
    flask_app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


# ── Kivy + Android WebView ───────────────────
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform


class FlaskApp(App):

    def build(self):
        # 启动 Flask 后台线程
        threading.Thread(target=run_flask, daemon=True).start()

        if platform == "android":
            return self._build_android_webview()
        else:
            return self._build_desktop_fallback()

    def _build_android_webview(self):
        """Android：使用原生 WebView 嵌入 Kivy"""
        from jnius import autoclass, cast
        from android.runnable import run_on_ui_thread

        WebView = autoclass("android.webkit.WebView")
        WebViewClient = autoclass("android.webkit.WebViewClient")
        WebSettings = autoclass("android.webkit.WebSettings")
        LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
        RelativeLayout = autoclass("android.widget.RelativeLayout")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")

        activity = PythonActivity.mActivity

        # 创建 WebView
        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        # 允许混合内容（HTTP 本地）
        settings.setMixedContentMode(0)  # MIXED_CONTENT_ALWAYS_ALLOW

        webview.setWebViewClient(WebViewClient())

        # 等待 Flask 就绪后加载
        def load_when_ready():
            # 等待 Flask 启动
            for _ in range(30):
                try:
                    import urllib.request
                    urllib.request.urlopen("http://127.0.0.1:5000/", timeout=1)
                    break
                except Exception:
                    time.sleep(0.5)
            webview.loadUrl("http://127.0.0.1:5000/")

        threading.Thread(target=load_when_ready, daemon=True).start()

        # 将 WebView 放入 Activity
        activity.setContentView(webview)

        # 返回空布局（Kivy 不接管界面）
        return Label(text="", size_hint=(0, 0))

    def _build_desktop_fallback(self):
        """桌面端：显示提示信息"""
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(
            Label(
                text="服务器已启动\n请在浏览器打开 http://127.0.0.1:5000",
                halign="center",
                valign="center",
            )
        )
        return layout


if __name__ == "__main__":
    FlaskApp().run()
