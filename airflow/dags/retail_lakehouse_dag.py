"""Airflow DAG for a bounded, operator-triggered retail lakehouse run."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from airflow.decorators import dag, task


@dag(
    dag_id="retail_lakehouse_monthly",
    description="Ingest public retail measures into bronze, silver, and gold layers.",
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["lakehouse", "retail", "portfolio"],
)
def retail_lakehouse_monthly():
    """Create an explicit-run DAG to keep the local demo deterministic and controlled."""

    @task
    def ingest_transform_publish() -> dict[str, object]:
        from lakehouse.pipeline import run_pipeline

        return run_pipeline(Path("/opt/airflow/data/lakehouse"))

    ingest_transform_publish()


retail_lakehouse_monthly()
