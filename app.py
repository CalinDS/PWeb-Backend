from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import api.routes.user_route as users
from infrastrucure.db_config import config_db_for_app

app = Flask(__name__)
CORS(app)

app = config_db_for_app(app)


app.register_blueprint(users.users_api)

app.run()