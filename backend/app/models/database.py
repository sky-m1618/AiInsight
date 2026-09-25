from app.extensions import db
import uuid
from datetime import datetime ,timezone
from models.user import Users 

def gen_uuid():
    return str(uuid.uuid4())

def now():
    return datetime.now(timezone.utc)

class Dataset(db.Model):
    __tablename__ = 'datasets'
    id = db.Column(db.String(30) , primary_key = True , default = gen_uuid)
    user_id = db.Column(db.String(30) , db.ForeignKey("Users.id"),nullable =False)
    name = db.Column(db.String(30) , nullable = False)
    file_path = db.Column(db.String(80) , nullable = False)
    target_column = db.Column(db.String(20))
    task_type = db.Column(db.String(20)) # CLASSIFICATION , REGRESSION
    rows = db.Column(db.Integer)
    columns = db.Column(db.Integer)
    status = db.Column(db.String(10))
    created_at = db.Column(db.datetime ,nullable = False, default = now)