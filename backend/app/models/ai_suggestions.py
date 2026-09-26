# app/models/ai_suggestion.py
from app.extensions import db

class AISuggestion(db.Model):
    __tablename__ = "ai_suggestions"
    
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id"), nullable=False)
    
    # The target variable the user wants to predict
    target_variable = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(50)) # 'Classification' or 'Regression'
    
    # The AI's recommended model (e.g., 'RandomForestClassifier')
    suggested_model = db.Column(db.String(100), nullable=False)
    
    # The JSON payload returned by Gemini via your Pydantic schema
    hyperparameters = db.Column(db.JSON, nullable=False)
    
    # Why Gemini chose this model (e.g., "Data is highly non-linear...")
    ai_reasoning = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    dataset = db.relationship("Dataset", backref="ai_suggestions")