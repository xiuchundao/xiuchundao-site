from app import db, login_manager
from flask_login import UserMixin


class UserEntity(UserMixin, db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(16))

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return unicode(self.username)


@login_manager.user_loader
def load_user(username):
    return UserEntity.query.filter(UserEntity.username == username).first()
