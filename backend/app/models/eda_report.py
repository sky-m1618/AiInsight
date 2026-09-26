# app/models/eda_report.py
from app.extensions import db

class EDAReport(db.Model):
    __tablename__ = "eda_reports"
    
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id"), nullable=False)
    
    # Store aggregate stats like row count, missing values, etc.
    total_rows = db.Column(db.Integer)
    total_columns = db.Column(db.Integer)
    
    # db.JSON is perfect for storing Pandas output like {"Age": {"mean": 29, "nulls": 0}}
    numerical_stats = db.Column(db.JSON, nullable=True) 
    categorical_stats = db.Column(db.JSON, nullable=True)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    dataset = db.relationship("Dataset", backref="eda_report", uselist=False)