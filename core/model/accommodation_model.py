from flask_sqlalchemy import SQLAlchemy
import json
from infrastrucure.db_config import db

class AccommodationModel(db.Model):
    __tablename__ = "accommodation"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo = db.Column(db.String)
    beds_no = db.Column(db.Integer)
    address = db.Column(db.String)

    def __init__(self, owner_id, photo, beds_no, address):
        self.owner_id = owner_id
        self.photo = photo
        self.beds_no = beds_no
        self.address = address

    def __repr__(self):
        data = {
            "id": self.id,
            "owner_id": self.owner_id,
            "photo": self.photo,
            "beds_no": self.beds_no,
            "address": self.address
        }
        return json.dumps(data)
