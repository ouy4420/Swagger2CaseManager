from flask import request, jsonify
from . import auth
from SwaggerToCase.DB_operation.models import Auth
from backend.auth.auth_token import generate_token
from SwaggerToCase.DB_operation.curd import session


@auth.route('/auth/register/', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    obj = session.query(Auth).filter_by(username=username).first()
    if obj:
        return jsonify({'success': False, 'msg': '用户名已存在，请重新注册！'})
    else:
        save = Auth(username=username, email=email)
        save.hash_password(password)  # 调用密码加密方法
        session.add(save)
        session.commit()
        return jsonify({'success': True, 'msg': '用户注册成功！'})


@auth.route('/auth/login/', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    obj = session.query(Auth).filter_by(username=username).first()
    if not obj:
        return jsonify({'success': False, 'msg': '未找到该用户，请重新输入或注册账号！'})
    if obj.verify_password(password):
        token = generate_token(username)
        return jsonify({'success': True, 'token': token, 'msg': '用户登录成功！', 'user': username})
    else:
        return jsonify({'success': False, 'msg': '密码校验失败，请重新输入！'})

