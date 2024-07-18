from flask import Flask
import os
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# for password hashing
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)

# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# load the secret key defined in the .env file

bcrypt = Bcrypt(app)

# Path for our local sql lite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")

# To specify to track modifications of objects and emit signals
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

app.config["JWT_SECRET_KEY"]= os.environ.get("SECRET_KEY")

app.config["JWT_TOKEN_LOCATION"] = ["headers"]

app.config['GEMINI_API_KEY'] = os.environ.get("GEMINI_API_KEY")

app.config['ELASTICSEARCH_API_ID'] = os.environ.get("ELASTICSEARCH_API_ID")

app.config['ELASTICSEARCH_API_KEY'] = os.environ.get("ELASTICSEARCH_API_KEY")
# sql alchemy instance
db = SQLAlchemy(app)

# Flask Migrate instance to handle migrations
migrate = Migrate(app, db)

jwt = JWTManager(app)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(public_id=identity).one_or_none()

from src.routes import api
app.register_blueprint(api, url_prefix="/api")

CORS(app, resources={r"/api/*": {"origins": ["http://localhost:4200", "http://127.0.0.1:4200"]}})


# import models to let the migrate tool know

from src.models.Company import Company
from src.models.Document import Document
from src.models.User import User
from src.models.Property import Property
from src.models.Role import Role
