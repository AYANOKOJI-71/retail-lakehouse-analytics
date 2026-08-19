from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_compose_declares_lakehouse_control_plane() -> None:
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    for service in ("postgres:", "minio:", "spark-master:", "airflow-webserver:", "airflow-scheduler:"):
        assert service in compose


def test_reporting_and_warehouse_assets_exist() -> None:
    assert (ROOT / "reports" / "powerbi" / "README.md").exists()
    assert (ROOT / "warehouse" / "snowflake" / "monthly_category_metrics.sql").exists()
    assert (ROOT / "warehouse" / "bigquery" / "monthly_category_metrics.sql").exists()


def test_release_readme_and_quality_gate_exist() -> None:
    assert (ROOT / "README.md").exists()
    assert (ROOT / "docs" / "OPERATIONS.md").exists()
    assert (ROOT / "docs" / "DEMO-VERIFICATION.md").exists()
    workflow = ROOT / ".github" / "workflows" / "ci.yml"
    assert workflow.exists()
    workflow_text = workflow.read_text(encoding="utf-8")
    assert "setup-java" in workflow_text
    assert ".[dev,spark]" in workflow_text
