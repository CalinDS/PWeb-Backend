from flask_sqlalchemy import SQLAlchemy
import json
from infrastrucure.db_config import db

class BookingModel(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    refugee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id'))
    

    def __init__(self, refugee_id, accommodation_id):
        self.refugee_id = refugee_id
        self.accommodation_id = accommodation_id

    def __repr__(self):
        data = {
            "id": self.id,
            "refugee_id": self.refugee_id,
            "accommodation_id": self.accommodation_id
        }
        return json.dumps(data)
