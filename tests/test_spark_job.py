from datetime import date

import pytest

from lakehouse.spark_job import build_gold_metrics


def test_spark_gold_metrics_matches_contract() -> None:
    pytest.importorskip("pyspark")
    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder.master("local[1]")
        .appName("retail-lakehouse-test")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    try:
        silver = spark.createDataFrame(
            [
                (date(2019, 1, 1), "BEER", "100", "Alpha", 2.0, 1.0, 4.0),
                (date(2019, 1, 1), "BEER", "101", "Alpha", 3.0, 0.0, 1.0),
                (date(2019, 1, 1), "WINE", "200", "Bravo", 1.0, 0.0, 2.0),
            ],
            [
                "year_month",
                "item_type",
                "item_code",
                "supplier",
                "retail_sales_cases",
                "retail_transfer_cases",
                "warehouse_sales_cases",
            ],
        )
        rows = {row["item_type"]: row.asDict() for row in build_gold_metrics(silver).collect()}
    finally:
        spark.stop()

    assert rows["BEER"]["retail_sales_cases"] == pytest.approx(5.0)
    assert rows["BEER"]["warehouse_sales_cases"] == pytest.approx(5.0)
    assert rows["BEER"]["net_cases"] == pytest.approx(10.0)
    assert rows["BEER"]["distinct_items"] == 2
    assert rows["BEER"]["distinct_suppliers"] == 1
