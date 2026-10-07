# app/services/database_services.py
"""
Persistence helpers for the EDA pipeline.

The small helpers only ``db.session.add`` (no commit); ``persist_eda_results`` owns the
single transaction and rolls back on failure, matching the repo's existing
``db.session.add`` / ``commit`` convention.
"""
from app.extensions import db
from app.models.database import Dataset, gen_uuid
from app.models.eda_report import EDAReport
from app.models.visualization import Visualization
from app.models.ai_suggestions import AISuggestion


def save_dataset(user_id, name, file_path, *, target_column=None, task_type=None,
                 rows=None, columns=None, status="uploaded"):
    """Create a Dataset row. The id is generated explicitly so the PK exists before any
    child (eda_reports/visualizations/ai_suggestions) is attached."""
    dataset = Dataset(
        id=gen_uuid(),
        user_id=user_id,
        name=(name or "dataset")[:255],
        file_path=file_path[:255],
        target_column=target_column[:100] if target_column else None,
        task_type=task_type,
        rows=rows,
        columns=columns,
        status=status,
    )
    db.session.add(dataset)
    db.session.flush()  # assign PK / surface constraint errors now
    return dataset


def get_dataset_for_user(dataset_id, user_id, *, is_admin=False):
    """Fetch a dataset enforcing ownership (admins bypass the user check)."""
    dataset = db.session.get(Dataset, dataset_id)
    if dataset is None:
        return None
    if not is_admin and dataset.user_id != user_id:
        return None
    return dataset


def save_eda_report(dataset, eda_payload):
    """Upsert the 1-1 EDA report for a dataset (safe to re-run analyze)."""
    report = EDAReport.query.filter_by(dataset_id=dataset.id).first()
    if report is None:
        report = EDAReport(dataset_id=dataset.id, full_report=eda_payload)
        db.session.add(report)
    else:
        report.full_report = eda_payload
    return report


def save_visualizations(dataset, charts):
    """Replace the dataset's chart rows with the freshly generated set (idempotent)."""
    Visualization.query.filter_by(dataset_id=dataset.id).delete()
    created = []
    for chart in charts or []:
        viz = Visualization(
            dataset_id=dataset.id,
            chart_type=chart.get("chart_type"),
            target_column=chart.get("target_column"),
            base64_data=chart.get("base64_data"),
        )
        db.session.add(viz)
        created.append(viz)
    return created


def save_ai_suggestion(dataset, suggestion):
    """Replace the dataset's AI suggestion row (idempotent). No-op if suggestion is None."""
    if not suggestion:
        return None
    AISuggestion.query.filter_by(dataset_id=dataset.id).delete()
    row = AISuggestion(
        dataset_id=dataset.id,
        target_variable=suggestion["target_variable"],
        task_type=suggestion.get("task_type"),
        suggested_model=suggestion["suggested_model"],
        hyperparameters=suggestion.get("hyperparameters") or {},
        ai_reasoning=suggestion.get("ai_reasoning"),
    )
    db.session.add(row)
    return row


def persist_eda_results(dataset, eda_payload, *, charts=None, suggestion=None):
    """
    Persist the EDA report and every related table in a single transaction:
    eda_reports -> visualizations -> ai_suggestions, then update the dataset's
    row/column counts and status.
    """
    try:
        report = save_eda_report(dataset, eda_payload)
        save_visualizations(dataset, charts)
        save_ai_suggestion(dataset, suggestion)

        metrics = (eda_payload or {}).get("overview", {}).get("file_metrics", {})
        dataset.rows = metrics.get("total_rows")
        dataset.columns = metrics.get("total_columns")
        dataset.status = "processed"

        db.session.commit()
        return report
    except Exception:
        db.session.rollback()
        raise
