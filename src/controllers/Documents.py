import datetime
import json
import os
from elasticsearch import Elasticsearch
from flask import jsonify, request, make_response, Blueprint
from flask_jwt_extended import jwt_required, current_user
from src import db, app
from src.models.Document import Document
from src.utils.Uility import create_properties
from src.middlewares.Crypter import Crypter
from src.middlewares.Logger import Logger
from werkzeug.utils import secure_filename

documents = Blueprint("documents", __name__)

def allowed_documents(documents, roles):
    allowed = set()
    for role in roles:
        if role.category == "All":
            return documents
        for document in documents:
            if document.category == role.category:
                if role.subcategory == "All":
                    allowed.add(document)
                elif document.subcategory == role.subcategory:
                    allowed.add(document)
        return list(allowed)
        

        
        

@documents.route('', methods=['POST'], endpoint='add_document')
@jwt_required()
def create_document():
    try:
        crypter = Crypter()
        key = crypter.generateKey()
        data = request.json
        file = secure_filename(data['file_name']+".pdf")
        image_list = [os.path.join("src/temp/", img) for img in data['files']]
        crypter.create_pdf(image_list,os.path.join("src/temp/",file))
        crypter.encrypt(os.path.join("src/temp/",file),key)
        document = Document(
            file_name = file,
            category = data['category'],
            subcategory = data['subcategory'],
            upload_date = datetime.datetime.now(),
            created_by = current_user.id,
            file_path = data["path"],
            company_id = current_user.company_id,
            encryption_Key = key
        )
        db.session.add(document)
        db.session.commit()
        document = Document.query.filter_by(file_name=file).first()
        properties = create_properties(properties = data['properties'], id = document.document_id)
        db.session.add_all(properties)
        db.session.commit()
        for img in image_list:
            os.remove(img)
        logger = Logger().get_company_logger(current_user.company_id)
        logger.info(f"Document {document.file_name} uploaded by {current_user.firstName} {current_user.lastName}")
        return make_response(json.dumps(document.to_dict()), 200)
    except Exception as e:
        return make_response(str(e), 400)

@documents.route('/<int:document_id>', methods=['GET'], endpoint='get_document')
@jwt_required()
def get_document(document_id):
    try:
        document = Document.query.filter_by(company_id = current_user.company_id, document_id = document_id).first_or_404()
        return make_response(json.dumps(document.to_dict()), 200)
    except Exception as e:
        return make_response(str(e), 400)

@documents.route('', methods=['GET'], endpoint='get_all_documents')
@jwt_required()
def get_all_documents():
    try:
        documents = Document.query.filter_by(company_id = current_user.company_id).all()
        roles = current_user.roles
        documents = allowed_documents(documents, roles)
        return make_response(json.dumps([document.to_dict() for document in documents]), 200)
    except Exception as e:
        return make_response(str(e), 400)


@documents.route('/<int:document_id>', methods=['DELETE'], endpoint='delete_document')
@jwt_required()
def delete_documents(document_id):
    try:
        document = Document.query.filter_by(company_id = current_user.company_id, document_id = document_id).first_or_404()
        db.session.delete(document)
        db.session.commit()
        return make_response(jsonify({'msg' : 'Document deleted successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)


@documents.route('/search', methods=['POST'], endpoint='search_document')
@jwt_required()
def search_document():
    try:
        client = Elasticsearch(
            "https://localhost:9200",
            api_key= (app.config['ELASTICSEARCH_API_ID'],app.config['ELASTICSEARCH_API_KEY']),
            verify_certs= False
            )
        data = request.json
        results = client.search(index="data", q=data['key'])
        results = [result['_source'] for result in results['hits']['hits']]
        return make_response(results, 200)
    except Exception as e:
        return make_response(str(e), 400)
    
@documents.route('/archive/<int:document_id>', methods=['PUT'], endpoint='archive_document')
@jwt_required()
def archive_document(document_id):
    try:
        document = Document.query.filter_by(document_id = document_id).first_or_404()
        document.archived = not document.archived
        db.session.commit()
        return make_response(jsonify({'msg' : 'Document archived successfully'}), 200)
    except Exception as e:
        return make_response(str(e), 400)