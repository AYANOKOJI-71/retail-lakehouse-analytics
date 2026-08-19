"""Executable local reference pipeline for the retail lakehouse."""

from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from .contracts import DEFAULT_SOURCE_CONTRACT
from .ingest import download_public_source, read_and_validate_csv
from .quality import require_quality_pass, validate_silver
from .reporting import export_reporting_assets
from .serving import load_gold_to_postgres
from .storage import LakehousePaths
from .transform import build_monthly_category_metrics, clean_to_silver


def run_pipeline(
    data_root: Path,
    source_file: Path | None = None,
    database_url: str | None = None,
    reporting_dir: Path = Path("reports/generated"),
) -> dict[str, object]:
    """Run bronze-to-gold processing against an approved download or a checked-in public fixture."""

    paths = LakehousePaths(data_root)
    if source_file is None:
        source_file = download_public_source(DEFAULT_SOURCE_CONTRACT, data_root / "downloads" / "source.csv")
    raw = read_and_validate_csv(source_file, DEFAULT_SOURCE_CONTRACT)
    bronze_file = paths.bronze_file()
    bronze_file.parent.mkdir(parents=True, exist_ok=True)
    raw.to_parquet(bronze_file, index=False)

    silver, rejected = clean_to_silver(raw)
    checks = validate_silver(silver)
    require_quality_pass(checks)
    paths.silver.mkdir(parents=True, exist_ok=True)
    silver.to_parquet(paths.silver / "retail_sales.parquet", index=False)
    rejected.to_parquet(paths.silver / "rejected_records.parquet", index=False)

    gold = build_monthly_category_metrics(silver)
    paths.gold.mkdir(parents=True, exist_ok=True)
    gold.to_parquet(paths.gold / "monthly_category_metrics.parquet", index=False)
    reporting_assets = export_reporting_assets(gold, reporting_dir)
    database_url = database_url or os.environ.get("LAKEHOUSE_POSTGRES_URL")
    serving_rows = load_gold_to_postgres(gold, database_url) if database_url else 0
    paths.metadata.mkdir(parents=True, exist_ok=True)
    manifest = {
        "run_at_utc": datetime.now(UTC).isoformat(),
        "source": DEFAULT_SOURCE_CONTRACT.name,
        "source_url": DEFAULT_SOURCE_CONTRACT.url,
        "bronze_rows": len(raw),
        "silver_rows": len(silver),
        "rejected_rows": len(rejected),
        "gold_rows": len(gold),
        "postgres_serving_rows": serving_rows,
        "reporting_assets": reporting_assets,
        "quality_checks": [check.__dict__ for check in checks],
    }
    (paths.metadata / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    """Run the pipeline from the command line."""

    parser = argparse.ArgumentParser(description="Run the local retail lakehouse pipeline.")
    parser.add_argument("--data-root", type=Path, default=Path("data/lakehouse"))
    parser.add_argument("--source-file", type=Path)
    parser.add_argument("--database-url")
    parser.add_argument("--reporting-dir", type=Path, default=Path("reports/generated"))
    arguments = parser.parse_args()
    manifest = run_pipeline(arguments.data_root, arguments.source_file, arguments.database_url, arguments.reporting_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
