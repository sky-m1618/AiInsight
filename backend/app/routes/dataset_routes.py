from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
import uuid

from app.services.auth_services import resolve_actor
from app.services.ml_services import AutoML, build_charts, suggest_model
from app.services.database_services import save_dataset, persist_eda_results

dataset_bp = Blueprint("dataset", __name__)

ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@dataset_bp.get("/hello")
def hello():
    return jsonify({"message": "Hello"})


@dataset_bp.get("/list")
@jwt_required(optional=True)
def list_datasets():
    """List datasets visible to the current actor (own + all if admin)."""
    user_id, is_admin = resolve_actor()
    from app.models.database import Dataset
    query = Dataset.query
    if not is_admin:
        query = query.filter_by(user_id=user_id)
    datasets = query.order_by(Dataset.created_at.desc()).all()
    return jsonify({
        "datasets": [{
            "id": d.id,
            "name": d.name,
            "target_column": d.target_column,
            "rows": d.rows,
            "columns": d.columns,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        } for d in datasets],
    }), 200


@dataset_bp.post("/csv")
@jwt_required(optional=True)
def csv():
    file = request.files.get("file")
    if file is None or file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only CSV files are allowed"}), 400

    target_col = request.form.get("target_col", None)
    try:
        safe_name = secure_filename(file.filename)

        # Unique on-disk name so same-filename uploads don't overwrite each other.
        stored_name = f"{uuid.uuid4().hex[:8]}_{safe_name}"
        save_directory = current_app.config["UPLOAD_FOLDER"]
        full_storage_path = os.path.join(save_directory, stored_name)

        file.save(full_storage_path)
        file_size_bytes = os.path.getsize(full_storage_path)
        file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

        user_id, is_admin = resolve_actor()
        dataset = save_dataset(
            user_id=user_id,
            name=safe_name,
            file_path=full_storage_path,
            target_column=target_col,
            status="uploaded",
        )

        # Run EDA and persist the report + all related tables in one round trip.
        engine = AutoML(file_path=full_storage_path)
        eda_payload = engine.run_full_eda()
        charts = build_charts(engine)
        suggestion = suggest_model(engine, target_col)
        report = persist_eda_results(dataset, eda_payload, charts=charts, suggestion=suggestion)

        return jsonify({
            "message": "upload and EDA complete",
            "dataset_id": dataset.id,
            "eda_report_id": report.id,
            "file_size_mb": file_size_mb,
            "eda": eda_payload,
            "charts": [{"chart_type": c["chart_type"], "target_column": c["target_column"]}
                       for c in charts],
            "suggestion": suggestion,
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500