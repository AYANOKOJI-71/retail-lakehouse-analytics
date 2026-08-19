"""Generate reproducible Power BI import extracts and a data-derived local chart."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as pyplot
import pandas as pd


def export_reporting_assets(gold: pd.DataFrame, output_dir: Path) -> dict[str, str]:
    """Write the reporting extract and a chart from actual gold-layer measures."""

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "monthly_category_metrics.csv"
    png_path = output_dir / "monthly_category_mix.png"
    gold.to_csv(csv_path, index=False)
    figure, axis = pyplot.subplots(figsize=(10, 5))
    for item_type, frame in gold.groupby("item_type"):
        axis.plot(frame["year_month"], frame["net_cases"], marker="o", linewidth=2, label=item_type)
    axis.set_title("Monthly net cases by item category")
    axis.set_xlabel("Month")
    axis.set_ylabel("Net cases")
    axis.legend(title="Item type", ncols=2)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(png_path, dpi=150)
    pyplot.close(figure)
    return {"power_bi_csv": str(csv_path), "data_chart": str(png_path)}
