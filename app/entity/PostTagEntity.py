from app import db


class PostTagEntity(db.Model):
    __tablename__ = 'post_tag'

    pt_id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))

    def __repr__(self):
        return '<PostTagEntity %r>' % self.tag_id
