from sqlalchemy_sandbox.app.core import db

class Parent(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
