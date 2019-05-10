from backend.interfaces.auth.auth_token import certify_token
from flask import request, jsonify
import functools


def login_require(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        token = request.args.get("token", None)
        username = request.args.get("user", None)
        if token is not None:
            res = certify_token(username, token)
            if token is None or res is False:
                return jsonify({'success': False, 'msg': 'token不存在或已失效！请先登录', "code": -1})
        print('call %s():' % func.__name__)
        return func(*args, **kw)

    return wrapper
