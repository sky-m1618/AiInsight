"""System-wide settings persisted in the DB.

A single ``SystemSettings`` row holds every runtime-tunable flag so the admin
can flip auth / features on or off without editing config files or restarting
the server.  The row is created on first boot (idempotent) and mutated in place
by the admin routes.
"""
from app.extensions import db


class SystemSettings(db.Model):
    __tablename__ = "system_settings"

    id = db.Column(db.Integer, primary_key=True, default=1)
    # When False the app accepts requests with no/invalid JWT (demo mode).
    auth_enabled = db.Column(db.Boolean, default=True, nullable=False)
    # When False the upload/EDA pipeline is open to anyone (no auth at all).
    allow_public_upload = db.Column(db.Boolean, default=True, nullable=False)
    # Maintenance banner shown to every user on the dashboard.
    maintenance_message = db.Column(db.String(512), default=None, nullable=True)
    # Cap on concurrent EDA runs per user (0 = unlimited).
    max_concurrent_jobs = db.Column(db.Integer, default=2, nullable=False)
    updated_at = db.Column(db.DateTime, default=None, nullable=True)

    def to_dict(self):
        from datetime import datetime
        return {
            "id": self.id,
            "auth_enabled": bool(self.auth_enabled),
            "allow_public_upload": bool(self.allow_public_upload),
            "maintenance_message": self.maintenance_message,
            "max_concurrent_jobs": int(self.max_concurrent_jobs),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


def get_settings():
    """Return the singleton settings row, creating it on first access."""
    row = SystemSettings.query.get(1)
    if row is None:
        row = SystemSettings(id=1)
        db.session.add(row)
        db.session.commit()
    return row


def set_settings(**kwargs):
    """Update one or more settings fields and persist."""
    row = get_settings()
    for key, value in kwargs.items():
        if hasattr(row, key):
            setattr(row, key, value)
    from datetime import datetime, timezone
    row.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return row