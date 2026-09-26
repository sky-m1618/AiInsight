# app/models/visualization.py
from app.extensions import db

class Visualization(db.Model):
    __tablename__ = "visualizations"
    
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id"), nullable=False)
    
    chart_type = db.Column(db.String(50)) # e.g., 'correlation_heatmap', 'target_distribution'
    target_column = db.Column(db.String(100), nullable=True) # What column this graph represents
    
    # Store the base64 string directly so Vue.js can render it instantly
    base64_data = db.Column(db.Text, nullable=False) 
    
    dataset = db.relationship("Dataset", backref="graphs")