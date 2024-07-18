import json
from flask import Blueprint, make_response
from flask_jwt_extended import current_user, jwt_required
from src.middlewares.Logger import Logger


logs = Blueprint("logs", __name__)


@logs.route("", methods=["GET"], endpoint='get_logs')
@jwt_required()
def get_logs():
    try:
        company_id = current_user.company_id
        logs = Logger().get_logs(company_id)
        return make_response(logs, 200)
    except Exception as e:
        return make_response(str(e),  500)