"""PostgreSQL serving-table writer for the Power BI-ready gold mart."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
import psycopg


def load_gold_to_postgres(gold: pd.DataFrame, database_url: str) -> int:
    """Replace the serving table atomically enough for a single local pipeline run."""

    columns = [
        "year_month",
        "item_type",
        "retail_sales_cases",
        "retail_transfer_cases",
        "warehouse_sales_cases",
        "distinct_items",
        "distinct_suppliers",
        "net_cases",
    ]
    rows: Iterable[tuple[object, ...]] = (
        tuple(record) for record in gold.loc[:, columns].itertuples(index=False, name=None)
    )
    with psycopg.connect(database_url) as connection, connection.cursor() as cursor:
        cursor.execute("create schema if not exists analytics")
        cursor.execute(
            """
            create table if not exists analytics.monthly_category_metrics (
                year_month date not null,
                item_type text not null,
                retail_sales_cases numeric not null,
                retail_transfer_cases numeric not null,
                warehouse_sales_cases numeric not null,
                distinct_items integer not null,
                distinct_suppliers integer not null,
                net_cases numeric not null
            )
            """
        )
        cursor.execute("truncate table analytics.monthly_category_metrics")
        with cursor.copy(
            "copy analytics.monthly_category_metrics (year_month, item_type, retail_sales_cases, "
            "retail_transfer_cases, warehouse_sales_cases, distinct_items, distinct_suppliers, net_cases) from stdin"
        ) as copy:
            for row in rows:
                copy.write_row(row)
        return len(gold)
