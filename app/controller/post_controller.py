# coding: utf-8

import datetime
import json

from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required

from app import db
from app.entity.PostEntity import PostEntity
from app.entity.TagEntity import TagEntity
from app.entity.PostTagEntity import PostTagEntity
from app.model.ResultModel import ResultModel

post_bp = Blueprint('post', __name__)


@post_bp.route('/')
def index():
    page_index = 1
    return page(page_index)


@post_bp.route('/page/<int:page_index>')
def page(page_index):
    query = PostEntity.query.order_by(PostEntity.is_top.desc(), PostEntity.time.desc())
    pagination = query.paginate(page_index, per_page=8, error_out=False)
    posts = pagination.items

    if not posts:
        abort(404)

    for post in posts:
        html_content = post.html_content
        summary_index = html_content.find('&lt;!-- more --&gt;')
        post.html_content = html_content[:summary_index]

    if page_index == 1:
        title = u'首页'
    else:
        title = u'第%s页' % page_index

    if pagination.total % pagination.per_page:
        total_page = pagination.total / pagination.per_page + 1
    else:
        total_page = pagination.total / pagination.per_page

    return render_template('post_list.html',
                           title=title,
                           posts=posts,
                           pagination=pagination,
                           total_page=total_page)


@post_bp.route('/post/<post_title>')
def post_detail(post_title):
    post = PostEntity.query.filter_by(en_title=post_title).first_or_404()
    post.html_content = post.html_content.replace('&lt;!-- more --&gt;', '')
    # for post_tag in post.tags:
    #     print post_tag.tag
    return render_template('post_detail.html', post=post)


@post_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_new():
    if len(request.data):
        # 表示这是前端通过ajax发送的post请求
        json_data = json.loads(request.data)

        # 获取前端参数
        zh_title = json_data['zh_title']
        en_title = json_data['en_title']
        en_title = en_title.replace(' ', '-')
        post_tags = json_data['tags']
        md_content = json_data['md_content']
        html_content = json_data['html_content']
        is_top = json_data['is_top']
        time = datetime.datetime.now()

        # 校验英文标题是否重复
        post = PostEntity.query.filter_by(en_title=en_title).first()
        if post:
            result = ResultModel(ResultModel.FAILED_CODE, '英文标题不可以重复', None)
            return jsonify(vars(result))

        # 插入标签
        tag_list = []
        for tag_name in post_tags:
            tag = TagEntity.query.filter_by(tag_name=tag_name).first()
            if tag is None:
                tag = TagEntity()
                tag.tag_name = tag_name
                db.session.add(tag)
            tag_list.append(tag)

        # 插入帖子
        post = PostEntity()
        post.zh_title = zh_title
        post.en_title = en_title.lower()
        post.md_content = md_content
        post.html_content = html_content
        post.is_top = is_top
        post.time = time
        db.session.add(post)

        # 插入帖子标签记录
        for tag in tag_list:
            post_tag = PostTagEntity(post=post, tag=tag)
            db.session.add(post_tag)

        db.session.commit()

        print post.post_id

        result = ResultModel(ResultModel.SUCCESS_CODE, ResultModel.SUCCESS_MSG, dict(title=en_title))

        return jsonify(vars(result))
    else:
        # 表明这是通过get方式发送的请求,因此跳转输入页面让用户进行输入
        return render_template('post_new_or_edit.html')


@post_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def post_edit_input(post_id):
    post = PostEntity.query.filter_by(post_id=post_id).first_or_404()
    return render_template('post_new_or_edit.html', post=post)


@post_bp.route('/post/edit', methods=['GET', 'POST'])
def post_edit():
    json_data = json.loads(request.data)

    post_id = json_data['post_id']
    zh_title = json_data['zh_title']
    en_title = json_data['en_title']
    en_title = en_title.replace(' ', '-')
    md_content = json_data['md_content']
    html_content = json_data['html_content']
    is_top = json_data['is_top']
    time = datetime.datetime.now()

    # 修改帖子
    post = PostEntity.query.get(post_id)
    post.zh_title = zh_title
    post.en_title = en_title
    post.md_content = md_content
    post.html_content = html_content
    post.is_top = is_top
    post.time = time

    db.session.add(post)
    db.session.commit()

    result = ResultModel(ResultModel.SUCCESS_CODE, ResultModel.SUCCESS_MSG, dict(title=en_title))

    return jsonify(vars(result))
