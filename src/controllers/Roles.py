from flask import Blueprint, json, jsonify, request, make_response
from flask_jwt_extended import jwt_required, current_user

from src import db
from src.models.Role import Role

role = Blueprint("role", __name__)

@role.route("", methods=['POST'], endpoint="add_role")
@jwt_required()
def add_role():
    try:
        data = request.json
        name = data["name"]
        category = data["category"]
        subcategory = data["subcategory"]
        role = Role(
            name = name,
            category = category,
            subcategory = subcategory,
            company_id = current_user.company_id
        )
        db.session.add(role)
        db.session.commit()
        role = Role.query.filter_by(name=name).first_or_404()
        return make_response(jsonify({'msg': 'Role created successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)
    
@role.route("", methods=['GET'], endpoint="get_all_roles")
@jwt_required()
def get_all_roles():
    try:
        roles = Role.query.filter_by(company_id = current_user.company_id).all()
        roles = [role.to_dict() for role in roles]
        return make_response(json.dumps(roles))
    except Exception as e:
        return make_response(str(e), 400)

@role.route("/<int:role_id>", methods=['GET'], endpoint="get_role")
@jwt_required()
def get_role(role_id):
    try:
        role = Role.query.filter_by(id = role_id).first_or_404()
        return make_response(json.dumps(role.to_dict()), 200)
    except Exception as e:
        return make_response(str(e), 400)

@role.route("/<int:role_id>", methods=['PUT'], endpoint="update_role")
@jwt_required()
def update_roles(role_id):
    try:
        data = request.json
        name = data["name"]
        category = data["category"]
        subcategory = data["subcategory"]
        role = Role.query.filter_by(id = role_id).first_or_404()

        role.name = name
        role.category = category
        role.subcategory = subcategory
        db.session.commit()
        return make_response(jsonify({'msg': 'Role updated successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)

@role.route("/<int:role_id>", methods=['DELETE'], endpoint="delete_role")
@jwt_required()
def delete_roles(role_id):
    try:
        role = Role.query.filter_by(id = role_id).first_or_404()
        db.session.delete(role)
        db.session.commit()
        return make_response(jsonify({'msg': 'Role deleted successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)