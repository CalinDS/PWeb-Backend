from distutils.log import error
import json
from flask import request, Blueprint, jsonify
from infrastrucure.db_config import db
from core.model.user_model import UserModel
from core.model.booking_model import BookingModel
from core.model.accommodation_model import AccommodationModel

users_api = Blueprint('users_api', __name__)

#create
@users_api.route('/users/create', methods = ['POST'])
def create_user():
    data = request.get_json()
    try:
        auth_id = data["auth_id"]
        email = data["email"]
        name = data["name"]
        type = data["type"]
        contact_info = data["contact_info"]
        family_members_no = data["family_members_no"]
        user = UserModel(
            auth_id=auth_id,
            email=email,
            name=name,
            type=type,
            contact_info=contact_info,
            family_members_no=family_members_no)
        db.session.add(user)
        db.session.commit()
        return "User added", 200
    except Exception as e:
        print(e)
        return "Error", 404


#retrieve
@users_api.route('/users', methods = ['GET'])
def retrieve_users():
    users = UserModel.query.all()
    return str(users), 200


@users_api.route('/users/<string:auth_id>', methods = ['GET'])
def retrieve_user_by_auth_id(auth_id):
    user = UserModel.query.filter_by(auth_id=auth_id).first()
    if user:
        resp = {
            "id": user.id,
            "auth_id": user.auth_id,
            "email": user.email,
            "name": user.name,
            "type": user.type,
            "contact_info": user.contact_info,
            "family_members_no": user.family_members_no
        }
        if user.type == 'refugee':
            booking = BookingModel.query.filter_by(refugee_id=user.id).first()
            if booking:
                accommodation = AccommodationModel.query.filter_by(id=booking.accommodation_id).first()
                owner = UserModel.query.filter_by(id=accommodation.owner_id).first()
                resp["accommodation"]= {
                    "address": accommodation.address,
                    "photo": accommodation.photo,
                    "owner_name": owner.name,
                    "contact_info": owner.contact_info,
                    "booking_id": booking.id
                }
        return jsonify(resp), 200
    return f"User with auth_id={auth_id} doesn't exist", 404


#update
@users_api.route('/users/<int:id>/update', methods = ['PUT'])
def update_user(id):
    user = UserModel.query.filter_by(id=id).first()
    data = request.get_json()
    if user:
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return json.loads(str(user)), 200
    return f"User with id={id} doesn't exist", 404


#delete
@users_api.route('/users/<int:id>/delete', methods=['GET','POST', 'PUT', 'DELETE'])
def delete_user(id):
    user = UserModel.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return "Deleted", 200
    return f"User with id={id} doesn't exist", 404