from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    def add(self, **kwargs):
        session = kwargs.get("session", None)
        if session is None:
            db.session.add(self)
            return db.session.commit()
        session.add(self)

    def update(self, **kwargs):
        session = kwargs.get("session", None)
        if session is None:
            return db.session.commit()

    def delete(self, **kwargs):
        session = kwargs.get("session", None)
        db.session.delete(self)
        if session is None:
            return db.session.commit()