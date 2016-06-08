from app import db


class ImageEntity(db.Model):
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    md5_name = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(40))
    data = db.Column(db.LargeBinary)
    time = db.Column(db.DateTime)
    modify_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % self.en_title
