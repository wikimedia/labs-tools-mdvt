from sqlalchemy.sql import func

from mdvt import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.username)


class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    media_id = db.Column(db.Integer, nullable=False)
    data_type = db.Column(db.String(20), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    undo = db.Column(db.Boolean, nullable=False, default=False)
    time_created = db.Column(db.Date, nullable=False,
                             server_default=func.now())

    def __repr__(self):
        return '<Contribution {} {} {} {} {} {} {}>'.format(
            self.id, self.user_id, self.media_id, self.data_type, self.data,
            self.undo, self.time_created)
