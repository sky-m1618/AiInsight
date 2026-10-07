# app/services/ml_services.py
"""
EDA engine, chart rendering and (placeholder) model suggestion.

Kept out of the route layer so both the upload and the analyze routes can reuse it
without circular imports.
"""
import os
import base64
import io

import numpy as np
import pandas as pd


class AutoML:
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset target not found at: {file_path}")

        self.file_path = file_path
        # Use low_memory=False to handle mixed data types cleanly in production.
        # comment="#" drops the sample-file credit line (and any '#'-prefixed line)
        # so the real header row is parsed as the header.
        self.df = pd.read_csv(file_path, low_memory=False, comment="#")

    def clean_json_data(self, obj):
        """Recursively convert NumPy/pandas scalars into strict JSON primitives."""
        if isinstance(obj, dict):
            return {k: self.clean_json_data(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self.clean_json_data(x) for x in obj]
        elif isinstance(obj, np.ndarray):
            return [self.clean_json_data(x) for x in obj.tolist()]
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            # Convert NaNs/Infinities to None (which translates to null in SQL/NoSQL)
            return None if np.isnan(obj) or np.isinf(obj) else float(obj)
        elif obj is None:
            return None
        elif isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
            return None
        elif isinstance(obj, (pd.Timestamp,)):
            return obj.isoformat()
        # Only call pd.isna on scalars; on a list/array it raises "truth value is ambiguous".
        elif isinstance(obj, (pd.NaT.__class__,)) or (
            not isinstance(obj, (dict, list, tuple, np.ndarray)) and pd.isna(obj)
        ):
            return None
        return obj

    def numeric_frame(self) -> pd.DataFrame:
        return self.df.select_dtypes(include=["number"])

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


def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def build_charts(automl: "AutoML", max_charts: int = 8) -> list:
    """
    Render a small, capped set of EDA charts as base64 PNG data-URIs.

    Returns [] if matplotlib is unavailable so that EDA persistence still succeeds
    on a bare environment. Each item is
    {"chart_type": str, "target_column": str | None, "base64_data": str}.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return []

    df = automl.df
    charts = []

    def add(fig, chart_type, target_column=None):
        if len(charts) >= max_charts:
            plt.close(fig)
            return
        try:
            charts.append({
                "chart_type": chart_type,
                "target_column": target_column,
                "base64_data": _fig_to_base64(fig),
            })
        finally:
            plt.close(fig)

    try:
        # 1. Correlation heatmap (numeric only)
        numeric = automl.numeric_frame()
        if len(numeric.columns) >= 2 and len(charts) < max_charts:
            corr = numeric.corr(numeric_only=True)
            fig, ax = plt.subplots(figsize=(6, 5))
            im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=90)
            ax.set_yticks(range(len(corr.columns)))
            ax.set_yticklabels(corr.columns)
            ax.set_title("Correlation Heatmap")
            fig.colorbar(im, ax=ax)
            add(fig, "correlation_heatmap")

        # 2. Numeric distributions (cap at 4)
        for col in list(numeric.columns)[:4]:
            if len(charts) >= max_charts:
                break
            fig, ax = plt.subplots(figsize=(5, 3))
            numeric[col].dropna().hist(ax=ax, bins=20)
            ax.set_title(f"Distribution: {col}")
            add(fig, "numeric_distribution", col)

        # 3. Categorical bars (top values, cap at 4)
        categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns
        for col in list(categorical_cols)[:4]:
            if len(charts) >= max_charts:
                break
            counts = df[col].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(5, 3))
            counts.plot(kind="bar", ax=ax)
            ax.set_title(f"Top values: {col}")
            add(fig, "categorical_bar", col)
    except Exception:
        # Never let a chart failure break EDA persistence.
        plt.close("all")
        return charts

    return charts


def suggest_model(automl: "AutoML", target_column: str | None) -> dict | None:
    """
    Rule-based placeholder for the future Gemini/Pydantic model suggestion.

    Infers task type from the target dtype and returns a sane default model. Returns
    None when no target column is supplied (the ai_suggestions columns are NOT NULL).
    """
    if not target_column or target_column not in automl.df.columns:
        return None

    series = automl.df[target_column]
    if pd.api.types.is_numeric_dtype(series) and series.nunique() > 15:
        task_type = "Regression"
        suggested_model = "RandomForestRegressor"
        hyperparameters = {"n_estimators": 100, "max_depth": None, "random_state": 42}
        reason = (
            f"Target '{target_column}' is numeric with {int(series.nunique())} distinct "
            "values, so this is treated as a regression task. A Random Forest is a robust "
            "baseline that handles non-linearity and mixed feature types."
        )
    else:
        task_type = "Classification"
        suggested_model = "RandomForestClassifier"
        hyperparameters = {"n_estimators": 100, "max_depth": None, "random_state": 42}
        reason = (
            f"Target '{target_column}' is categorical/boolean with "
            f"{int(series.nunique())} classes, so this is treated as a classification task. "
            "A Random Forest classifier is a strong, low-tuning baseline."
        )

    return {
        "target_variable": target_column,
        "task_type": task_type,
        "suggested_model": suggested_model,
        "hyperparameters": hyperparameters,
        "ai_reasoning": reason,
    }
