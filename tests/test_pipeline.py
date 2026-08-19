from pathlib import Path

from lakehouse.pipeline import run_pipeline


def test_pipeline_writes_layered_parquet_and_manifest(tmp_path: Path) -> None:
    manifest = run_pipeline(tmp_path, Path("data/fixtures/montgomery_retail_sales.csv"))

    assert manifest["bronze_rows"] > 0
    assert manifest["silver_rows"] > 0
    assert manifest["gold_rows"] > 0
    assert (tmp_path / "metadata" / "run_manifest.json").exists()
    assert list((tmp_path / "bronze").rglob("*.parquet"))
    assert (tmp_path / "silver" / "retail_sales" / "retail_sales.parquet").exists()
    assert (tmp_path / "gold" / "monthly_category_metrics" / "monthly_category_metrics.parquet").exists()
