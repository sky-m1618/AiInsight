from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.ml_services import AutoML, build_charts, suggest_model
from app.services.auth_services import resolve_actor
from app.services.database_services import get_dataset_for_user, persist_eda_results


ml_bp = Blueprint("mlrun", __name__)


@ml_bp.post("/analyze")
@jwt_required(optional=True)
def automl():
    """Run EDA on a stored dataset, persist the report + related tables, and return it."""
    body = request.get_json(silent=True) or {}
    dataset_id = body.get("dataset_id")
    if not dataset_id:
        return jsonify({"error": "dataset_id is required"}), 400

    user_id, is_admin = resolve_actor()
    dataset = get_dataset_for_user(dataset_id, user_id, is_admin=is_admin)
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404

    try:
        engine = AutoML(file_path=dataset.file_path)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": f"Could not parse dataset: {str(e)}"}), 422

    try:
        eda_payload = engine.run_full_eda()
        charts = build_charts(engine)
        suggestion = suggest_model(engine, dataset.target_column)
        report = persist_eda_results(dataset, eda_payload, charts=charts, suggestion=suggestion)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    return jsonify({
        "dataset_id": dataset.id,
        "eda_report_id": report.id,
        "message": eda_payload,
        "charts": [{"chart_type": c["chart_type"], "target_column": c["target_column"]}
                   for c in charts],
        "suggestion": suggestion,
    }), 200