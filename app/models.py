from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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


class Users(Base):
    name = db.Column(db.String(255))
    fb_id = db.Column(db.Integer)
