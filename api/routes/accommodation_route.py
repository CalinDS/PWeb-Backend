from distutils.log import error
import json
from flask import request, Blueprint, jsonify
from core.model.booking_model import BookingModel
from infrastrucure.db_config import db
from core.model.accommodation_model import AccommodationModel
from core.model.user_model import UserModel

accommodations_api = Blueprint('accommodations_api', __name__)


#create
@accommodations_api.route('/accommodations/create', methods = ['POST'])
def create_accommodation():
    data = request.get_json()
    try:
        accommodation = AccommodationModel(
            owner_id=data["owner_id"],
            photo=data["photo"],
            beds_no=data["beds_no"],
            address=data["address"]
            )
        db.session.add(accommodation)
        db.session.commit()
        return "Accommodation added", 200
    except Exception as e:
        print(e)
        return "Error", 404


#retrieve
@accommodations_api.route('/accommodations', methods = ['GET'])
def retrieve_accommodations():
    accommodations = AccommodationModel.query.all()
    accomms = []
    for acc in accommodations:
        accommodation_id = acc.id
        acc_owner = UserModel.query.filter_by(id=acc.owner_id).first()
        owner = {
            "id": acc_owner.id,
            "contact_info": acc_owner.contact_info,
            "email": acc_owner.email,
            "name": acc_owner.name
        }
        all_beds = acc.beds_no
        occupied_beds = 0
        bookings = BookingModel.query.filter_by(accommodation_id=accommodation_id).all()
        for booking in bookings:
            refugee_id = booking.refugee_id
            refugee = UserModel.query.filter_by(id=refugee_id).first()
            occupied_beds += refugee.family_members_no
        free_beds_no = all_beds - occupied_beds
        accomms.append({
            "id": acc.id,
            "owner": owner,
            "photo": acc.photo,
            "beds_no": acc.beds_no,
            "address": acc.address,
            "free_beds_no": free_beds_no
        })

    return jsonify(accomms), 200


#update
@accommodations_api.route('/accommodations/<int:id>/update', methods = ['PUT'])
def update_accommodation(id):
    accommodation = AccommodationModel.query.filter_by(id=id).first()
    data = request.get_json()
    if accommodation:
        for key, value in data.items():
            setattr(accommodation, key, value)
        db.session.commit()
        return json.loads(str(accommodation)), 200
    return f"Accomodation with id={id} doesn't exist", 404


#delete
@accommodations_api.route('/accommodations/<int:id>/delete', methods=['GET','POST', 'PUT', 'DELETE'])
def delete_accommodation(id):
    accommodation = AccommodationModel.query.filter_by(id=id).first()
    if accommodation:
        bookings = BookingModel.query.filter_by(accommodation_id=accommodation.id).all()
        for b in bookings:
            db.session.delete(b)
        db.session.delete(accommodation)
        db.session.commit()
        return "Deleted", 200
    return f"User with id={id} doesn't exist", 404