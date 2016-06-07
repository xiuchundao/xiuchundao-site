from app import db


class TagEntity(db.Model):
    __tablename__ = 'tag'

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, unique=True)
    create_time = db.Column(db.DateTime)

    posts = db.relationship("PostTagEntity", backref='tag')

    def __repr__(self):
        return '<Tag %r>' % self.tag_name
