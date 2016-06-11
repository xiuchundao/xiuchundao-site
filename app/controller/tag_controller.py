# coding: utf-8

from flask import Blueprint, render_template

from app import db
from app.entity.PostEntity import PostEntity
from app.entity.TagEntity import TagEntity
from app.entity.PostTagEntity import PostTagEntity

tag_bp = Blueprint('tag', __name__)


@tag_bp.route('/tags')
def tags():
    return render_template('tags.html', tags=TagEntity.query.all())


@tag_bp.route('/tag/<tag_name>')
def tag_index(tag_name):
    return tag_detail(tag_name, 1)


@tag_bp.route('/tag/<tag_name>/<int:page_index>')
def tag_detail(tag_name, page_index):
    db.session.autoflush = False
    # 先查询tag
    tag = TagEntity.query.filter_by(tag_name=tag_name).first()

    # 根据tag_id查询出符合条件的PostTagEntity记录PTR,再查询PostEntity记录PR并对其做出筛选,
    # 筛选过程如下:PTR的post_id组成一个集合,某条PR记录的post_id是集合的一个元素,这条记录保留,否则废弃
    query = PostEntity.query.filter(PostEntity.en_title != 'about')\
        .filter(PostEntity.tags.any(PostTagEntity.tag_id == tag.tag_id))\
        .order_by(PostEntity.is_top.desc(), PostEntity.time.desc())
    pagination = query.paginate(page_index, per_page=8, error_out=False)
    posts = pagination.items

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

    return render_template('tag_detail.html',
                           tag_name=tag_name,
                           title=title,
                           posts=posts,
                           pagination=pagination,
                           total_page=total_page)
