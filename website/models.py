from . import db

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item = db.Column(db.String(150))
    base_quantity = db.Column(db.Integer, default=100)
    number = db.Column(db.Integer)
    unit = db.Column(db.String(40))
    estimated_price = db.Column(db.Float)