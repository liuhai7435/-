"""Flask 统一响应格式 - JSON API 标准返回"""

from flask import jsonify
from typing import Any, Optional


def api_success(data: Any = None, message: str = "ok") -> tuple:
    """成功响应"""
    return jsonify({
        "code": 0,
        "message": message,
        "data": data,
    }), 200


def api_error(message: str = "服务器错误", code: int = 400, http_status: Optional[int] = None) -> tuple:
    """错误响应"""
    return jsonify({
        "code": code,
        "message": message,
        "data": None,
    }), http_status or (400 if code >= 400 else 200)


def api_paginate(items: list, total: int, page: int, page_size: int, message: str = "ok") -> tuple:
    """分页响应"""
    return jsonify({
        "code": 0,
        "message": message,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        },
    }), 200
