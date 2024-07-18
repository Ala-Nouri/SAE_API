from flask import Blueprint
from src.controllers.Authentification import auth
from src.controllers.Users import users
from src.controllers.Files import files
from src.controllers.Documents import documents
from src.controllers.Roles import role
from src.controllers.Logs import logs
# main blueprint to be registered with application
api = Blueprint('api', __name__)

api.register_blueprint(auth, url_prefix="/auth")

api.register_blueprint(users, url_prefix="/users")

api.register_blueprint(files, url_prefix="/files")

api.register_blueprint(documents, url_prefix="/documents")

api.register_blueprint(role, url_prefix="/roles")

api.register_blueprint(logs, url_prefix="/logs")


