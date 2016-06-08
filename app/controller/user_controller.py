# coding: utf-8

import json
import hashlib

from flask import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_user, logout_user, current_user

from app.entity.UserEntity import UserEntity
from app.model.ResultModel import ResultModel

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    print current_user
    if current_user.is_authenticated():
        return redirect('/')

    if len(request.data):
        # 表示这是前端通过ajax发送的post请求
        json_data = json.loads(request.data)

        user = UserEntity.query.filter_by(username=json_data['username']).first()

        if user is not None and user.password == hashlib.md5(json_data['password']).hexdigest():
            # 登录成功
            login_user(user)
            result = ResultModel(ResultModel.SUCCESS_CODE, ResultModel.SUCCESS_MSG, None)
        elif user is not None and user.password != json_data['password']:
            # 密码错误
            result = ResultModel(ResultModel.FAILED_CODE, '密码错误', None)
        else:
            # 用户不存在
            result = ResultModel(ResultModel.FAILED_CODE, '用户不存在', None)
        return jsonify(vars(result))
    else:
        # 表明这是通过get方式发送的请求,因此跳转到登录页面让用户进行登录
        return render_template('login.html')


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/login')
