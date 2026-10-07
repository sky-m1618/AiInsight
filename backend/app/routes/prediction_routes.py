from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.auth_services import resolve_actor
from app.services.database_services import get_dataset_for_user
from app.models.database import Dataset
from app.models.ai_suggestions import AISuggestion


prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.get("/predictions")
@jwt_required(optional=True)
def list_predictions():
    """Return the AI suggestion (task/model) for datasets the actor can see."""
    user_id, is_admin = resolve_actor()
    query = Dataset.query
    if not is_admin:
        query = query.filter_by(user_id=user_id)
    datasets = query.order_by(Dataset.created_at.desc()).all()

    preds = []
    for d in datasets:
        suggestion = AISuggestion.query.filter_by(dataset_id=d.id).first()
        if suggestion:
            preds.append({
                "dataset_id": d.id,
                "dataset_name": d.name,
                "target_variable": suggestion.target_variable,
                "task_type": suggestion.task_type,
                "suggested_model": suggestion.suggested_model,
                "hyperparameters": suggestion.hyperparameters,
                "ai_reasoning": suggestion.ai_reasoning,
            })
    return jsonify({"predictions": preds}), 200