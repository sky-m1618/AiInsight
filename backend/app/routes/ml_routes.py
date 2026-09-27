import os
import json
import numpy as np
import pandas as pd
from flask import Blueprint ,jsonify
from app.extensions import db
from app.models.eda_report import EDAReport


ml_bp = Blueprint('mlrun',__name__)


class AutoML:
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset target not found at: {file_path}")
            
        self.file_path = file_path
        # Use low_memory=False to handle mixed data types cleanly in production
        self.df = pd.read_csv(file_path, low_memory=False)
        
    def clean_json_data(self, obj):
        if isinstance(obj, dict):
            return {k: self.clean_json_data(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.clean_json_data(x) for x in obj]
        elif isinstance(obj, (np.int64, np.int32, np.int16)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            # Convert NaNs/Infinities to None (which translates to null in SQL/NoSQL)
            return None if np.isnan(obj) or np.isinf(obj) else float(obj)
        elif pd.isna(obj):
            return None
        return obj

    def run_full_eda(self) -> dict:
        """
        Runs a comprehensive, flexible Exploratory Data Analysis (EDA) on ANY CSV dataset.
        Handles numerical, categorical, textual, and missing values safely.
        """
        df = self.df
        total_rows, total_cols = df.shape

        # 1. Structural Overview
        overview = {
            "file_metrics": {
                "total_rows": total_rows,
                "total_columns": total_cols,
                "memory_usage_bytes": int(df.memory_usage(deep=True).sum())
            },
            "missing_values_summary": {
                col: int(count) for col, count in df.isnull().sum().items() if count > 0
            }
        }

        # 2. Extract Variable Types
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()

        overview["column_types"] = {
            "numerical_count": len(numeric_cols),
            "categorical_count": len(categorical_cols),
            "datetime_count": len(datetime_cols),
            "all_columns": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }

        # 3. Dynamic Analysis: Numerical Columns
        numerical_analysis = {}
        for col in numeric_cols:
            desc = df[col].describe()
            numerical_analysis[col] = {
                "mean": desc.get("mean"),
                "min": desc.get("min"),
                "max": desc.get("max"),
                "std": desc.get("std"),
                "median": df[col].median(),
                "zeros_count": int((df[col] == 0).sum())
            }

        # 4. Dynamic Analysis: Categorical Columns
        categorical_analysis = {}
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            unique_count = int(df[col].nunique())
            
            # To avoid saving massive JSON trees, cap value frequencies to the top 10 values
            top_frequencies = value_counts.head(10).to_dict()
            
            categorical_analysis[col] = {
                "unique_values_count": unique_count,
                "top_categories_distribution": top_frequencies
            }

        # Combine all calculations into a single payload
        raw_eda_payload = {
            "overview": overview,
            "numerical_features": numerical_analysis,
            "categorical_features": categorical_analysis
        }

        # Clean all NumPy objects into strict JSON primitives before sending to DB layers
        return self.clean_json_data(raw_eda_payload)


@ml_bp.get('/analyze')
def automl():
    automl_engine = AutoML(file_path=r"D:\AiInsight\backend\uploads\mixed-types.csv")
    eda_json_payload = automl_engine.run_full_eda()

    # new_record = EDAReport(
            
    #         full_report=eda_json_payload  # Stored as JSON/JSONB natively
    #     )
    # db.session.add(new_record)
    # db.session.commit()
    print(eda_json_payload)
    return jsonify({"message":eda_json_payload})
