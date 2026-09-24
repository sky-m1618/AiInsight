from app.extensions import db
from datetime import datetime ,timezone
from werkzeug.security import generate_password_hash , check_password_hash
import uuid

def gen_uuid():
    return str(uuid.uuid4())

def now():
    return datetime.now(timezone.utc)

class Users(db.Model):
    id = db.Column(db.String(36) , primary_key = True , default = gen_uuid)
    username = db.Column(db.String(30) , nullable = False,unique = True)
    email = db.Column(db.String(30) , nullable = False , unique = True)
    password_hash = db.Column(db.String(256),nullable = False)
    role = db.Column(db.String(10) , nullable = False , default = 'USER')
    created_at = db.Column(db.datetime() , default = now)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
            "email": self.email,
            "role":self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

