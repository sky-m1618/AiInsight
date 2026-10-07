from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.auth_services import resolve_actor
from app.services.database_services import get_dataset_for_user
from app.models.database import Dataset
from app.models.eda_report import EDAReport
from app.models.visualization import Visualization
from app.models.ai_suggestions import AISuggestion


report_bp = Blueprint("report", __name__)


@report_bp.get("/reports")
@jwt_required(optional=True)
def list_reports():
    """List reports the current actor can see (own, or all if admin)."""
    user_id, is_admin = resolve_actor()
    query = Dataset.query
    if not is_admin:
        query = query.filter_by(user_id=user_id)
    datasets = query.order_by(Dataset.created_at.desc()).all()

    reports = []
    for d in datasets:
        report = EDAReport.query.filter_by(dataset_id=d.id).first()
        charts = Visualization.query.filter_by(dataset_id=d.id).count()
        suggestion = AISuggestion.query.filter_by(dataset_id=d.id).first()
        reports.append({
            "dataset_id": d.id,
            "name": d.name,
            "target_column": d.target_column,
            "rows": d.rows,
            "columns": d.columns,
            "status": d.status,
            "eda_report_id": report.id if report else None,
            "charts_count": charts,
            "task_type": suggestion.task_type if suggestion else None,
            "suggested_model": suggestion.suggested_model if suggestion else None,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        })
    return jsonify({"reports": reports}), 200


@report_bp.get("/reports/<report_id>")
@jwt_required(optional=True)
def get_report(report_id):
    user_id, is_admin = resolve_actor()
    report = EDAReport.query.get(report_id)
    if report is None:
        return jsonify({"error": "Report not found"}), 404
    dataset = db.session.get(Dataset, report.dataset_id) if False else None
    dataset = Dataset.query.get(report.dataset_id)
    if dataset is None:
        return jsonify({"error": "Report not found"}), 404
    if not is_admin and dataset.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    charts = Visualization.query.filter_by(dataset_id=report.dataset_id).all()
    suggestion = AISuggestion.query.filter_by(dataset_id=report.dataset_id).first()
    return jsonify({
        "dataset": {
            "id": dataset.id, "name": dataset.name,
            "target_column": dataset.target_column,
            "rows": dataset.rows, "columns": dataset.columns, "status": dataset.status,
        },
        "eda_report_id": report.id,
        "message": report.full_report,
        "charts": [{
            "chart_type": c.chart_type, "target_column": c.target_column,
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