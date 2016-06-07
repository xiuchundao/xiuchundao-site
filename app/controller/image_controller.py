# coding: utf-8
import datetime
import hashlib

from flask import Blueprint, render_template, request, redirect, Response, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from pinyin import pinyin

from app import db
from app.model.ResultModel import ResultModel
from app.entity.ImageEntity import ImageEntity

image_bp = Blueprint('image', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['png', 'jpg', 'jpeg', 'gif']


@image_bp.route('/attach/upload', methods=['GET', 'POST'])
@login_required
def image_upload():
    if request.method == 'POST':
        # 通过POST方式上传图片
        image_file = request.files['file']
        filename = secure_filename(pinyin.get(image_file.filename, format="numerical"))

        if allowed_file(filename):
            image_entity = ImageEntity()
            image_entity.name = image_file.filename
            image_entity.type = image_file.content_type
            image_entity.data = image_file.read()
            image_entity.time = datetime.datetime.now()

            md5 = hashlib.md5()
            md5.update(filename + datetime.datetime.strftime(image_entity.time, '%Y%m%d%H%M%S'))
            image_entity.md5_name = md5.hexdigest() + '.' + filename.rsplit('.', 1)[1]

            db.session.add(image_entity)
            db.session.commit()

            return redirect('/attach/' + image_entity.md5_name)
        else:
            result = ResultModel(ResultModel.FAILED_CODE, '图片格式不合法', None)
            return jsonify(vars(result))

    return render_template('upload.html')


@image_bp.route('/attach/<md5_name>')
def image(md5_name):
    image_entity = ImageEntity.query.filter_by(md5_name=md5_name).first_or_404()
    return Response(image_entity.data, mimetype=image_entity.type)


@image_bp.route('/attaches')
@login_required
def archives():
    image_list = ImageEntity.query.filter(ImageEntity.time >= datetime.date.today())\
        .order_by(ImageEntity.time.desc()).all()
    return render_template('attaches.html', image_list=image_list)


