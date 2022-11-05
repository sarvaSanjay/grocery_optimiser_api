from . import db

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item = db.Column(db.String(150))
    base_quantity = db.Column(db.Integer)
    number = db.Column(db.Integer)
    is_discrete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)