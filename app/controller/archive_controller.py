# coding: utf-8

import datetime

from flask import Blueprint, render_template

from app.entity.PostEntity import PostEntity

archive_bp = Blueprint('archive', __name__)


@archive_bp.route('/archives')
def archives():
    post_records = PostEntity.query.order_by(PostEntity.time.desc()).all()

    year_list = []
    archive_group_list = []

    for post in post_records:
        post_time = datetime.datetime.strftime(post.time, '%Y-%m-%d')
        year_list.append(post_time[:4])
    year_list = sorted(set(year_list), reverse=True)

    for year in year_list:
        post_list = [post for post in post_records if year in datetime.datetime.strftime(post.time, '%Y-%m-%d')]
        archive_group_list.append({'year': year, 'post_list': post_list})

        # post_list = tuple(post_list)
        # print isinstance(post_list, collections.Hashable)

    return render_template('archives.html', archive_group_list=archive_group_list)
