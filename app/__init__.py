# coding: utf-8

import os
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

PROJDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name=''):
    # 初始化Flask应用实例
    app = Flask(
        __name__,
        template_folder="web/template",
        static_url_path='',
        static_folder='web')

    # 初始化应用相关参数
    app.config.from_object(config[config_name])

    # 初始化数据库实例
    init_database(app)

    # 初始化模板相关配置
    init_jinja(app)

    # # Bootstrap
    # Bootstrap(app)

    # 注册静态资源
    register_static(app)

    # 注册路由
    register_routes(app)

    # 初始化授权相关配置
    init_login_manager(app)

    return app


def init_database(app):
    db.init_app(app)


def register_static(app):
    from flask import send_file

    def _register(name):
        return app.add_url_rule('/%s' % name, name, view_func=lambda: send_file(os.path.join(PROJDIR, 'app/web', name)))

    _register('robots.txt')


def init_jinja(app):
    @app.template_filter('post_datetime')
    def post_datetime(value):
        if not isinstance(value, datetime.datetime):
            return value
        return value.strftime('%Y-%m-%d')

    @app.template_filter('image_datetime')
    def image_datetime(value):
        if not isinstance(value, datetime.datetime):
            return value
        return value.strftime('%H:%M')


def register_routes(app):
    from controller import archive_controller, \
        image_controller, main_controller, post_controller, tag_controller, user_controller

    app.register_blueprint(archive_controller.archive_bp)
    app.register_blueprint(image_controller.image_bp)
    app.register_blueprint(main_controller.main_bp)
    app.register_blueprint(post_controller.post_bp)
    app.register_blueprint(tag_controller.tag_bp)
    app.register_blueprint(user_controller.user_bp)


def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.session_protection = 'basic'
    login_manager.login_view = 'user.login'
