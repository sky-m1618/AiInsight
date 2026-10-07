from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.extensions import db
from app.models.user import Users
from app.models.database import Dataset
from app.models.eda_report import EDAReport
from app.models.visualization import Visualization
from app.models.ai_suggestions import AISuggestion
from app.models.settings import get_settings, set_settings, SystemSettings
from app.services.auth_services import resolve_actor
from app.services.database_services import get_dataset_for_user

user_bp = Blueprint("user", __name__)


@user_bp.get("/overview")
def overview():
    """Live overview for the currently-authenticated user."""
    user_id, is_admin = resolve_actor()
    if not is_admin and not user_id:
        return jsonify({"error": "Authentication required"}), 401

    query = Dataset.query
    if not is_admin:
        query = query.filter_by(user_id=user_id)

    datasets = query.order_by(Dataset.created_at.desc()).limit(10).all()
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


@user_bp.get("/eda")
@jwt_required(optional=True)
def eda():
    """Read back the stored EDA report + charts + AI suggestion for a dataset."""
    user_id, is_admin = resolve_actor()
    dataset_id = request.args.get("dataset_id")

    query = Dataset.query
    if not is_admin:
        query = query.filter_by(user_id=user_id)
    if dataset_id:
        dataset = query.filter_by(id=dataset_id).first()
    else:
        dataset = query.order_by(Dataset.created_at.desc()).first()

    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404

    report = EDAReport.query.filter_by(dataset_id=dataset.id).first()
    charts = Visualization.query.filter_by(dataset_id=dataset.id).all()
    suggestion = AISuggestion.query.filter_by(dataset_id=dataset.id).first()

    return jsonify({
        "dataset": {
            "id": dataset.id,
            "name": dataset.name,
            "target_column": dataset.target_column,
            "rows": dataset.rows,
            "columns": dataset.columns,
            "status": dataset.status,
        },
        "eda_report_id": report.id if report else None,
        "message": report.full_report if report else None,
        "charts": [{
            "chart_type": c.chart_type,
            "target_column": c.target_column,
            "base64_data": c.base64_data,
        } for c in charts],
        "suggestion": {
            "target_variable": suggestion.target_variable,
            "task_type": suggestion.task_type,
            "suggested_model": suggestion.suggested_model,
            "hyperparameters": suggestion.hyperparameters,
            "ai_reasoning": suggestion.ai_reasoning,
        } if suggestion else None,
    }), 200


@user_bp.delete("/dataset/<dataset_id>")
@jwt_required(optional=True)
def delete_dataset(dataset_id):
    """Delete a dataset and every derived report/chart/suggestion row + the file."""
    user_id, is_admin = resolve_actor()
    dataset = get_dataset_for_user(dataset_id, user_id, is_admin=is_admin)
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404

    # Remove derived rows first (FKs).
    EDAReport.query.filter_by(dataset_id=dataset.id).delete()
    Visualization.query.filter_by(dataset_id=dataset.id).delete()
    AISuggestion.query.filter_by(dataset_id=dataset.id).delete()
    db.session.delete(dataset)

    # Best-effort file cleanup — never let a missing file break the delete.
    try:
        import os
        if dataset.file_path and os.path.exists(dataset.file_path):
            os.remove(dataset.file_path)
    except Exception:
        pass

    db.session.commit()
    return jsonify({"message": "Dataset deleted", "dataset_id": dataset_id}), 200