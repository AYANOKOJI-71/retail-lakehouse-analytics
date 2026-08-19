"""Spark implementation of the gold aggregation used in the distributed execution path."""
from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as functions


def build_gold_metrics(silver: DataFrame) -> DataFrame:
    """Aggregate a cleaned silver Spark DataFrame into the Power BI-ready gold mart."""

    return (
        silver.groupBy("year_month", "item_type")
        .agg(
            functions.sum("retail_sales_cases").alias("retail_sales_cases"),
            functions.sum("retail_transfer_cases").alias("retail_transfer_cases"),
            functions.sum("warehouse_sales_cases").alias("warehouse_sales_cases"),
            functions.countDistinct("item_code").alias("distinct_items"),
            functions.countDistinct("supplier").alias("distinct_suppliers"),
        )
        .withColumn("net_cases", functions.col("retail_sales_cases") + functions.col("warehouse_sales_cases"))
    )


def main() -> None:
    """Read silver Parquet from object storage and write the gold table with Spark."""

    spark = SparkSession.builder.appName("retail-lakehouse-gold").getOrCreate()
    silver = spark.read.parquet("s3a://lakehouse/silver/retail_sales/")
    build_gold_metrics(silver).write.mode("overwrite").parquet("s3a://lakehouse/gold/monthly_category_metrics/")
    spark.stop()


if __name__ == "__main__":
    main()
