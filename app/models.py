from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    """Base Model class"""
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_created = db.Column(db.DateTime(), default=db.func.now())

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


class Client(Base):
    """Model to hold Client Information"""
    phonenumber = db.Column(db.String(255))
    email = db.Column(db.String(255))
    fb_id = db.Column(db.Integer())
    client_type = db.Column(db.String(20), default='user')


class Transaction(Base):
    """Model to hold Transaction information"""
    paid_by = db.Column(db.Integer, default=0)
    amount = db.Column(db.Integer, default=0)
    paid_to = db.Column(db.Integer, default=0)
