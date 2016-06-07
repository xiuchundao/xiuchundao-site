# coding: utf-8
from flask import Blueprint, render_template


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
    return render_template('about.html')
