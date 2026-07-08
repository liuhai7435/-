#!/usr/bin/env python3
'''
测试 - Flask 应用
'''

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name='测试')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
