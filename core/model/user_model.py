from flask_sqlalchemy import SQLAlchemy
import json
from infrastrucure.db_config import db

class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    contact_info = db.Column(db.String)
    family_members_no = db.Column(db.Integer)

    def __init__(self, auth_id, email, name, type, contact_info, family_members_no):
        self.auth_id = auth_id
        self.email = email
        self.name = name
        self.type = type
        self.contact_info = contact_info
        self.family_members_no = family_members_no

    def __repr__(self):
        data = {
            "id": self.id,
            "auth_id": self.auth_id,
            "email": self.email,
            "name": self.name,
            "type": self.type,
            "contact_info": self.contact_info,
            "family_members_no": self.family_members_no
        }
        return json.dumps(data)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)