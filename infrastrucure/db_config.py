from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def config_db_for_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PW_DB.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()

    return app

