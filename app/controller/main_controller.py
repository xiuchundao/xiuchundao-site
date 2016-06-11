# coding: utf-8
from flask import Blueprint, render_template

from app import db
from app.entity.PostEntity import PostEntity


main_bp = Blueprint('main', __name__)


@main_bp.app_errorhandler(404)
def page_not_found(error):
    print error
    return render_template('404.html'), 404


@main_bp.route('/search')
def search():
    return render_template('search_input.html')


@main_bp.route('/about')
def about():
    db.session.autoflush = False
    post = PostEntity.query.filter_by(en_title='about').first_or_404()
    post.html_content = post.html_content.replace('&lt;!-- more --&gt;', '')
    # for post_tag in post.tags:
    #     print post_tag.tag
    return render_template('about.html', post=post)
