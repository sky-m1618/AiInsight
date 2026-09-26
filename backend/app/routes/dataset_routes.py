from flask import Blueprint , request,jsonify
from app.extensions import db
from app.models import database
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


    try:
        df = pd.read_csv(file.stream)
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            return jsonify({
                "message": "CSV processed successfully", 
                "summary": "No numerical columns found to calculate averages."
            }), 200
            
        averages = df[numeric_cols].mean().to_dict()
        row_count = len(df)
        # ----------------------------

        return jsonify({
            "message": "CSV processed successfully",
            "metadata": {
                "filename": file.filename,
                "total_rows": row_count,
                "columns_found": list(df.columns)
            },
            "analysis": {
                "column_averages": averages
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process CSV: {str(e)}"}), 500

