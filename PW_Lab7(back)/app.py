from flask import Flask, jsonify, request
from routes import routes
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from database.db import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receipt-finder.db'
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random string
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 600  # 1 minute expiration
    db.init_app(app)
    app.register_blueprint(routes)

    # JWT initialization
    jwt = JWTManager(app)

    return app

if __name__ == '__main__':
    app = create_app()
    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Food Receipe API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    app.run(debug=True)
