import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
    

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    """ Create application context """

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
                        
    return app


from app.auth import models