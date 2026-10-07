# app/services/auth_services.py
"""Actor resolution shared by the EDA/upload routes.

The behaviour is now driven by the singleton ``SystemSettings`` row so an admin
can flip auth on/off at runtime (see ``/api/admin/settings``).  When auth is
disabled the pipeline still records *who* ran it, but no valid JWT is required.
"""
from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

from app.models.user import Users
from app.models.settings import get_settings


def _settings():
    try:
        return get_settings()
    except Exception:
        # If the DB is unavailable we fall back to "auth required" — safer than
        # silently opening the door.
        class _S:
            auth_enabled = True
            allow_public_upload = True
        return _S()


def resolve_actor(optional=True):
    """
    Resolve the acting user as ``(user_id, is_admin)``.

    - ``auth_enabled == False``: the pipeline is open.  We still try to read the
      JWT if one was sent (so audit trails stay meaningful), but we never reject
      a request for lacking one.
    - ``auth_enabled == True``: a valid JWT is required unless ``optional`` is
      False (callers that opt out get a 401 from flask-jwt-extended).
    """
    settings = _settings()
    user_id = None
    is_admin = False

    try:
        # When auth is off, never raise on a missing/invalid token.
        verify_jwt_in_request(optional=(optional or not settings.auth_enabled))
        user_id = get_jwt_identity()
        is_admin = (get_jwt() or {}).get("role") == "ADMIN"
    except Exception:
        user_id = None
        is_admin = False

    if user_id is None:
        # Fall back to the seeded ADMIN only when auth is disabled (demo mode).
        if not settings.auth_enabled:
            admin = Users.query.filter_by(role="ADMIN").first()
            if admin is not None:
                return admin.id, True
        return None, False
    return user_id, is_admin


def require_auth():
    """Raise 401 unless auth is currently enabled AND a valid JWT is present."""
    settings = _settings()
    if not settings.auth_enabled:
        return True  # auth disabled globally — request is allowed
    verify_jwt_in_request()
    return True


def is_admin_request():
    """True when the acting JWT carries the ADMIN role (auth must be enabled)."""
    settings = _settings()
    if not settings.auth_enabled:
        return True
    verify_jwt_in_request()
    return (get_jwt() or {}).get("role") == "ADMIN"