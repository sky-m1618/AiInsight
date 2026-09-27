from flask import Blueprint , request,jsonify , current_app
from app.extensions import db
from app.models import database
from werkzeug.utils import secure_filename
import os

import pandas as pd

dataset_bp = Blueprint('dataset',__name__)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@dataset_bp.get('/hello')
def hello():
    return jsonify({'message':'Hello'})

@dataset_bp.post('/csv')
def csv():
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only CSV files are allowed"}), 400

    target_col = request.form.get('target_col',None)
    try:
        safe_name = secure_filename(file.filename)
        
        # current_app dynamically references the configured folder path on local/production
        save_directory = current_app.config['UPLOAD_FOLDER']
        full_storage_path = os.path.join(save_directory, safe_name)
        
        # Stream the chunks straight to physical disk
        file.save(full_storage_path)

        # 3. Track Physical Disk Footprint 
        file_size_bytes = os.path.getsize(full_storage_path)
        file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

        
        return jsonify({'message':'file saved succefully'})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500