"""Local file-system implementation of bronze, silver, and gold storage contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class LakehousePaths:
    """Maps storage layers to deterministic local paths used in tests and local demos."""

    root: Path

    @property
    def bronze(self) -> Path:
        return self.root / "bronze" / "source=montgomery_county"

    @property
    def silver(self) -> Path:
        return self.root / "silver" / "retail_sales"

    @property
    def gold(self) -> Path:
        return self.root / "gold" / "monthly_category_metrics"

    @property
    def metadata(self) -> Path:
        return self.root / "metadata"

    def bronze_file(self) -> Path:
        partition = datetime.now(UTC).date().isoformat()
        return self.bronze / f"ingest_date={partition}" / "retail_sales.parquet"
