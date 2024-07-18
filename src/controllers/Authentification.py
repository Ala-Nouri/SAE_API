import datetime
import uuid
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token
from src import db, bcrypt
from src.models.Role import Role
from src.models.User import User
from src.models.Company import Company



auth = Blueprint('auth', __name__)

@auth.route('/signup', methods =['POST'],endpoint='signup')
def signup():
    data = request.json
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    password = data['password']
    company_name = data['company_name']

    # checking for existing user
    user = User.query.filter_by(email = email).first()
    company = Company.query.filter_by(admin_email = email).first()
    if company:
        return make_response('Company already existe', 202)
    if user:
        return make_response('User already exists', 202)

    company = Company(
        company_name = company_name,
        admin_email = email
    )

    db.session.add(company)
    db.session.commit()

    company = Company.query.filter_by(admin_email = email).first()
        
    user = User(
        public_id = str(uuid.uuid4()),
        firstName = firstname,
        lastName =lastname,
        email = email,
        password = bcrypt.generate_password_hash(password).decode('utf-8'),
        company_id = company.company_id
    )

    db.session.add(user)


    role = Role(
            name = "Admin",
            category = "All",
            subcategory = "All"
        )
    print(user.roles)
    db.session.add(role)
    
    user.roles.append([role])
        

    db.session.commit()

    return make_response('Successfully registered.', 201)
        
    

@auth.route('/signin', methods =['POST'], endpoint='signin')
def login():
    # creates dictionary of form data
    data = request.json
  
    if not data or not data['email'] or not data['password']:
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query.filter_by(email = data['email']).first()
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if bcrypt.check_password_hash(user.password, data['password']):
        # generates the JWT Token
        company = Company.query.filter_by(admin_email = user.email).first()
        if company:
            token = create_access_token(user.public_id,expires_delta=datetime.timedelta(days=1), additional_claims={"isAdmin":True})
        else:
            token = create_access_token(user.public_id,expires_delta=datetime.timedelta(days=1), additional_claims={"isAdmin":False})
  
        return make_response(jsonify({'token' : token}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

