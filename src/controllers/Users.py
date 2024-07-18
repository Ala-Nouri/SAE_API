import json
import uuid
from flask import jsonify, request, make_response, Blueprint
from flask_jwt_extended import jwt_required, current_user
from src import db, bcrypt
from src.models.Role import Role
from src.models.User import User

users = Blueprint("users", __name__)

@users.route('', methods=['POST'], endpoint='add_user')
@jwt_required()
def create_user():
    try:
        data = request.json
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        password = data['password']
        user = User(
            public_id = str(uuid.uuid4()),
            firstName = firstname,
            lastName =lastname,
            email = email,
            password = bcrypt.generate_password_hash(password).decode('utf-8'),
            company_id = current_user.company_id
        )
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'msg': 'User created successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)

@users.route('/<string:user_id>', methods=['GET'], endpoint='get_user')
@jwt_required()
def get_user(user_id):
    try:
        user = User.query.filter_by(public_id = user_id).first_or_404()
        return make_response(json.dumps(user.to_dict()),200)
    except Exception as e:
        return make_response(str(e), 400)

@users.route('', methods=['GET'], endpoint='get_all_user')
@jwt_required()
def get_user():
    try:
        users = User.query.filter_by(company_id = current_user.company_id).all()
        users = [user.to_dict() for user in users]
        return make_response(json.dumps(users),200)
    except Exception as e:
        return make_response(str(e), 400)

@users.route('/<string:user_id>', methods=['PUT'], endpoint='update_user')
@jwt_required()
def update_user(user_id):
    try:
        user = User.query.filter_by(public_id = user_id).first_or_404()
        data = request.json
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        password = data['password']
        user.firstName = firstname
        user.lastName = lastname
        user.email = email
        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8'),
        db.session.commit()
        return make_response(jsonify({'msg': 'User updated successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)

@users.route('/<string:user_id>', methods=['DELETE'], endpoint='delete_user')
@jwt_required()
def delete_user(user_id):
    try:
        user = User.query.filter_by(public_id = user_id).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'msg': 'User deleted successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)

@users.route("/assign/<string:user_id>", methods=['POST'], endpoint='assign_role')
@jwt_required()
def assign_role(user_id):
    try:
        data = request.json
        role_ids = data["roles"]
        roles = [Role.query.filter_by(id = role_id).first_or_404() for role_id in role_ids]
        user = User.query.filter_by(public_id = user_id).first_or_404()
        user.roles = roles
        db.session.commit()
        return make_response(jsonify({'msg': 'User updated successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)



