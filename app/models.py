''' Created by Migwi Ndung'u
    @ The Samurai Community 2017
'''
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.String(255), default=lambda: uuid.uuid4().hex,
                   primary_key=True)
    date_created = db.Column(db.DateTime(), default=db.func.now())
    date_modified = db.Column(db.DateTime(), default=db.func.now(),
                              onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()
        db.session.remove()

    def get_base(self):
        return {
            'id': self.id if self.id else '',
            'date_created': self.date_created if self.date_created else 0,
            'date_modified': self.date_modified if self.date_modified else 0
        }


class Users(Base):
    name = db.Column(db.String(255))
    fb_id = db.Column(db.Integer, unique=True)
    transactions = db.relationship('Transactions', backref='users',
                                   lazy='dynamic')
    __tableargs__ = db.UniqueConstraint('name', 'fb_id')

    def get_user(self):
        data = self.get_base(self)
        data.add({'name': self.name, 'fb_id': self.fb_id})
        return data


class Transactions(Base):
    user = db.Column(db.Integer, db.ForeignKey('users.fb_id'))
    session = db.Column(db.String())
    __tableargs__ = db.UniqueConstraint('user', 'session')

    def get_transaction(self):
        data = self.get_base(self)
        data.add({'user': self.user, 'session': self.session})
        return data
