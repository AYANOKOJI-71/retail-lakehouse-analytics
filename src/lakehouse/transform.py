"""Silver and gold transformations for monthly retail-sales analytics."""
from __future__ import annotations

import pandas as pd

SOURCE_COLUMN_MAP = {
    "YEAR": "calendar_year",
    "MONTH": "calendar_month",
    "SUPPLIER": "supplier",
    "ITEM CODE": "item_code",
    "ITEM DESCRIPTION": "item_description",
    "ITEM TYPE": "item_type",
    "RETAIL SALES": "retail_sales_cases",
    "RETAIL TRANSFERS": "retail_transfer_cases",
    "WAREHOUSE SALES": "warehouse_sales_cases",
}
METRIC_COLUMNS = ("retail_sales_cases", "retail_transfer_cases", "warehouse_sales_cases")


def clean_to_silver(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Standardize public source fields and separate records with invalid calendar grain."""

    frame = raw.rename(columns=SOURCE_COLUMN_MAP).copy()
    frame = frame.loc[:, list(SOURCE_COLUMN_MAP.values())]
    frame["calendar_year"] = pd.to_numeric(frame["calendar_year"], errors="coerce")
    frame["calendar_month"] = pd.to_numeric(frame["calendar_month"], errors="coerce")
    for column in METRIC_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    for column in ("supplier", "item_code", "item_description", "item_type"):
        frame[column] = frame[column].astype("string").str.strip()

    valid_calendar = frame["calendar_year"].between(2010, 2100) & frame["calendar_month"].between(1, 12)
    valid_identity = frame["item_code"].notna() & frame["item_type"].notna()
    accepted = frame.loc[valid_calendar & valid_identity].copy()
    rejected = frame.loc[~(valid_calendar & valid_identity)].copy()
    accepted["calendar_year"] = accepted["calendar_year"].astype("int64")
    accepted["calendar_month"] = accepted["calendar_month"].astype("int64")
    accepted["year_month"] = pd.to_datetime(
        {"year": accepted["calendar_year"], "month": accepted["calendar_month"], "day": 1}
    )
    accepted["ingestion_source"] = "montgomery_county_open_data"
    return accepted, rejected


def build_monthly_category_metrics(silver: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the gold mart that feeds Power BI and warehouse adapters."""

    aggregations = {
        "retail_sales_cases": "sum",
        "retail_transfer_cases": "sum",
        "warehouse_sales_cases": "sum",
        "item_code": "nunique",
        "supplier": "nunique",
    }
    gold = (
        silver.groupby(["year_month", "item_type"], as_index=False)
        .agg(aggregations)
        .rename(columns={"item_code": "distinct_items", "supplier": "distinct_suppliers"})
        .sort_values(["year_month", "item_type"])
        .reset_index(drop=True)
    )
    gold["net_cases"] = gold["retail_sales_cases"] + gold["warehouse_sales_cases"]
    return gold
