from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import Users
from app.models.settings import get_settings

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json(force=True) or {}
    username = data.get("identifier") or data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = Users.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        # Same message for both cases — don't let attackers enumerate accounts.
        return jsonify({"message": "Invalid username or password"}), 401

    role = user.role or "USER"
    token = create_access_token(
        identity=user.id,
        additional_claims={"role": role},
    )
    payload = {"token": token, "role": role}
    if role == "ADMIN":
        payload["admin"] = user.to_dict()
    else:
        payload["user"] = user.to_dict()
    return jsonify(payload), 200


@auth_bp.post("/user/register")
def register():
    """Public registration. Always creates a USER; admins are seeded, not registered."""
    data = request.get_json(force=True) or {}

    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not username or not email or not password:
        return jsonify({"message": "Username, email and password are required"}), 400
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400

    if Users.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if Users.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = Users(username=username, email=email, role="USER")
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    user = Users.query.filter_by(username=username).first()
    token = create_access_token(
        identity=user.id,
        additional_claims={"role": "USER"},
    )
    return jsonify({
        "message": "Registration successful",
        "token": token,
        "user": user.to_dict(),
    }), 201


@auth_bp.get("/me")
def me():
    """Return the current user's profile from the JWT (no DB round-trip needed)."""
    from flask_jwt_extended import get_jwt_identity, get_jwt
    from app.models.user import Users

    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Missing authentication token"}), 401
    user = db.session.get(Users, user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"user": user.to_dict(), "role": user.role}), 200


@auth_bp.get("/settings")
def public_settings():
    """Non-admins can read the auth toggle so the UI can adapt (e.g. hide login)."""
    try:
        settings = get_settings()
    except Exception:
        return jsonify({"auth_enabled": True, "allow_public_upload": True}), 200
    return jsonify({
        "auth_enabled": bool(settings.auth_enabled),
        "allow_public_upload": bool(settings.allow_public_upload),
        "maintenance_message": settings.maintenance_message,
    }), 200