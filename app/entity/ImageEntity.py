from app import db


class ImageEntity(db.Model):
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    md5_name = db.Column(db.String, unique=True)
    type = db.Column(db.String)
    data = db.Column(db.LargeBinary)
    time = db.Column(db.DateTime)
    modify_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % self.en_title
