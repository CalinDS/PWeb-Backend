from distutils.log import error
import json
from flask import request, Blueprint
from infrastrucure.db_config import db
from core.model.booking_model import BookingModel

bookings_api = Blueprint('bookings_api', __name__)


#create
@bookings_api.route('/bookings/create', methods = ['POST'])
def create_booking():
    data = request.get_json()
    try:
        booking = BookingModel(
                refugee_id=data["refugee_id"],
                accommodation_id=data["accommodation_id"]
            )
        db.session.add(booking)
        db.session.commit()
        return "Booking added", 200
    except Exception as e:
        print(e)
        return "Error", 404


#retrieve
@bookings_api.route('/bookings', methods = ['GET'])
def retrieve_bookings():
    bookings = BookingModel.query.all()
    return str(bookings), 200


#update
@bookings_api.route('/bookings/<int:id>/update', methods = ['PUT'])
def update_booking(id):
    booking = BookingModel.query.filter_by(id=id).first()
    data = request.get_json()
    if booking:
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return json.loads(str(booking)), 200
    return f"Accomodation with id={id} doesn't exist", 404


#delete
@bookings_api.route('/bookings/<int:id>/delete', methods=['GET','POST', 'PUT', 'DELETE'])
def delete_booking(id):
    booking = BookingModel.query.filter_by(id=id).first()
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return "Deleted", 200
    return f"User with id={id} doesn't exist", 404