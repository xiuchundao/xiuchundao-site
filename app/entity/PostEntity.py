from app import db


class PostEntity(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True)
    zh_title = db.Column(db.String(200))
    en_title = db.Column(db.String(200), unique=True)
    md_content = db.Column(db.String(9000))
    html_content = db.Column(db.String(9000))
    is_top = db.Column(db.Boolean)
    time = db.Column(db.DateTime)
    modify_time = db.Column(db.DateTime)

    tags = db.relationship("PostTagEntity", backref='post')

    def __repr__(self):
        return '<Post %r>' % self.en_title
