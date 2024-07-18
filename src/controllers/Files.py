import os
from flask import Blueprint, request, make_response, send_file, url_for
from flask_jwt_extended import current_user, jwt_required
from werkzeug.utils import secure_filename

from src.middlewares.GeminiConnector import GeminiConnector
from src.middlewares.Crypter import Crypter
from src.middlewares.Logger import Logger
from src.models.Document import Document


files = Blueprint("files", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = "src/temp"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files.route('/upload', methods=['POST'], endpoint='uplaod_files')
@jwt_required()
def upload_file():
    try:
        files = request.files.getlist('files')
        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                f.save(path)     
            else:
                return make_response("uncorrect file type", 415)
        return make_response({"filename": filename}, 200)
    except Exception as e:
        return make_response(str(e), 500)

@files.route("/process", methods=['POST'], endpoint="extract")
@jwt_required()
def extract():
    try:
        files = [os.path.join(UPLOAD_FOLDER, file) for file in request.json['files']]
        ext = GeminiConnector()
        resp = ext.extractInfo(files)
        return make_response(resp, 200)
    except Exception as e:
        return make_response(str(e), 500)
    

@files.route("/download/<int:document_id>", methods=['GET'], endpoint='download_file')
def download_file(document_id):
    try:
        document = Document.query.filter_by(document_id = document_id).first_or_404()
        file_path = os.path.join('temp',document.file_name)
        return send_file(file_path, 
                     as_attachment=False, 
                     mimetype='application/pdf')
    except Exception as e:
        return make_response(str(e), 500)
    
@files.route("/decrypt/<int:document_id>", methods=['POST'], endpoint="decrypt")
@jwt_required()
def decrypt(document_id):
    try:
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)     
        crypter =  Crypter()
        document = Document.query.get(document_id)
        crypter.decrypt(path, document.encryption_Key)
        path = os.path.join("temp", filename)
        url = url_for('.download_file', document_id=document_id)
        logger = Logger().get_company_logger(current_user.company_id)
        logger.info(f"Document {document.file_name} viewd by {current_user.firstName} {current_user.lastName}")
        return make_response({"url" : url}, 200)

    except Exception as e:  
        print(e)
        return make_response(str(e), 500)