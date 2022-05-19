from distutils.log import error
from flask import request, Blueprint
from infrastrucure.db_config import db
from core.model.user_model import UserModel

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
        user = UserModel(auth_id=auth_id,
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