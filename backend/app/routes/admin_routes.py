"""Admin-only routes: auth toggle, user management, platform overview."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.extensions import db
from app.models.user import Users
from app.models.database import Dataset
from app.models.eda_report import EDAReport
from app.models.visualization import Visualization
from app.models.ai_suggestions import AISuggestion
from app.models.settings import get_settings, set_settings

admin_bp = Blueprint("admin", __name__)


def _require_admin():
    """Return 403 if the caller is not an ADMIN."""
    claims = get_jwt() or {}
    if claims.get("role") != "ADMIN":
        return jsonify({"error": "Admin access required"}), 403
    return None


# ── Settings / Auth Toggle ──────────────────────────────────────────────


@admin_bp.get("/settings")
@jwt_required()
def read_settings():
    err = _require_admin()
    if err:
        return err
    return jsonify(get_settings().to_dict()), 200


@admin_bp.post("/settings/auth-toggle")
@jwt_required()
def toggle_auth():
    """Toggle global authentication on or off."""
    err = _require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    require_auth = body.get("require_auth")
    if require_auth is None:
        return jsonify({"error": "require_auth (bool) is required"}), 400
    row = set_settings(auth_enabled=bool(require_auth))
    return jsonify({"message": "Auth toggled", "settings": row.to_dict()}), 200


@admin_bp.post("/settings/update")
@jwt_required()
def update_settings():
    """Update any combination of system settings."""
    err = _require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    allowed = {"auth_enabled", "allow_public_upload", "maintenance_message", "max_concurrent_jobs"}
    updates = {k: v for k, v in body.items() if k in allowed}
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    row = set_settings(**updates)
    return jsonify({"message": "Settings updated", "settings": row.to_dict()}), 200


# ── User Management ─────────────────────────────────────────────────────


@admin_bp.get("/users")
@jwt_required()
def list_users():
    err = _require_admin()
    if err:
        return err
    users = Users.query.order_by(Users.created_at.desc()).all()
    return jsonify({"users": [u.to_dict() for u in users]}), 200


@admin_bp.delete("/users/<user_id>")
@jwt_required()
def delete_user(user_id):
    err = _require_admin()
    if err:
        return err
    user = db.session.get(Users, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    if user.role == "ADMIN":
        return jsonify({"error": "Cannot delete an admin user"}), 403

    # Cascade: delete user's datasets and derived rows.
    datasets = Dataset.query.filter_by(user_id=user.id).all()
    for d in datasets:
        EDAReport.query.filter_by(dataset_id=d.id).delete()
        Visualization.query.filter_by(dataset_id=d.id).delete()
        AISuggestion.query.filter_by(dataset_id=d.id).delete()
        import os
        try:
            if d.file_path and os.path.exists(d.file_path):
                os.remove(d.file_path)
        except Exception:
            pass
        db.session.delete(d)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} deleted"}), 200


# ── Platform Overview / Performance ─────────────────────────────────────


@admin_bp.get("/overview")
@jwt_required()
def admin_overview():
    """Aggregate stats for the admin dashboard."""
    err = _require_admin()
    if err:
        return err

    total_users = Users.query.count()
    total_datasets = Dataset.query.count()
    total_reports = EDAReport.query.count()
    total_charts = Visualization.query.count()
    total_suggestions = AISuggestion.query.count()
    processed = Dataset.query.filter_by(status="processed").count()
    uploaded = Dataset.query.filter_by(status="uploaded").count()

    # Recent datasets (across all users)
    recent_datasets = Dataset.query.order_by(Dataset.created_at.desc()).limit(10).all()

    # Recent users
    recent_users = Users.query.order_by(Users.created_at.desc()).limit(5).all()

    settings = get_settings()

    return jsonify({
        "stats": {
            "totalUsers": total_users,
            "totalDatasets": total_datasets,
            "totalReports": total_reports,
            "totalCharts": total_charts,
            "totalSuggestions": total_suggestions,
            "datasetsProcessed": processed,
            "datasetsUploaded": uploaded,
        },
        "recentDatasets": [{
            "id": d.id,
            "name": d.name,
            "rows": d.rows,
            "columns": d.columns,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        } for d in recent_datasets],
        "recentUsers": [u.to_dict() for u in recent_users],
        "settings": settings.to_dict(),
    }), 200


# ── All Datasets (admin view) ───────────────────────────────────────────


@admin_bp.get("/datasets")
@jwt_required()
def admin_datasets():
    """List every dataset in the system (admin only)."""
    err = _require_admin()
    if err:
        return err
    datasets = Dataset.query.order_by(Dataset.created_at.desc()).all()
    result = []
    for d in datasets:
        owner = db.session.get(Users, d.user_id)
        result.append({
            "id": d.id,
            "name": d.name,
            "owner": owner.username if owner else "unknown",
            "rows": d.rows,
            "columns": d.columns,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        })
    return jsonify({"datasets": result}), 200