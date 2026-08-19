# Retail Lakehouse Analytics

**Retail Lakehouse Analytics** is an end-to-end, local-first data engineering project that turns a public non-personal retail-sales export into governed bronze, silver, and gold layers. It combines Python ingestion, Apache Spark aggregation, Airflow orchestration, MinIO-compatible object storage, PostgreSQL serving tables, dbt models and tests, warehouse adapters, and Power BI-ready reporting.

> The checked-in fixture is derived from a public Montgomery County monthly sales dataset. It contains aggregate product and supplier business data, not customer data. The fixture is real source data sampled across January–November 2019; it is not fabricated. [1]

## Why this project is interview-ready

| Engineering concern | Implemented evidence |
|---|---|
| Reproducible ingestion | Versioned 825-row public fixture, source contract, bronze Parquet capture, and run manifest |
| Layered lakehouse | Immutable bronze, standardized silver with rejected-record quarantine, and a Power BI-ready gold mart |
| Distributed compute | Spark gold transformation with a real local Spark parity test |
| Orchestration | Airflow DAG with manual operator triggering for deterministic demonstrations |
| Data quality | Required column contract plus valid date grain, nonblank product identity, known category, and nonempty silver checks |
| Serving and reporting | PostgreSQL `analytics.monthly_category_metrics`, CSV extract, chart, Power BI theme, and DAX guidance |
| Warehouse portability | Parallel Snowflake and BigQuery model definitions for the gold mart |

## Architecture

```text
Montgomery County Open Data
          │
          ▼
Airflow-triggered Python ingestion ──► Bronze Parquet (MinIO/S3-compatible)
          │                               │
          ▼                               ▼
   Contract + quality gates ───────► Silver Parquet
                                          │
                                          ▼
                                 Spark / dbt gold transform
                                          │
                       ┌──────────────────┼──────────────────┐
                       ▼                  ▼                  ▼
              PostgreSQL serving      Power BI CSV    Snowflake / BigQuery
```

The static system topology is documented in [Architecture](docs/ARCHITECTURE.md), while [Data source and provenance](docs/DATA_SOURCE.md) records the retrieval contract and fixture choice. The [local operations guide](docs/OPERATIONS.md) and [demo verification record](docs/DEMO-VERIFICATION.md) provide a concise hand-off for reviewers.

## Quick start

The deterministic local pipeline requires Python 3.12 and Java 17 for its Spark test. Docker is required for the full multi-service topology.

```bash
cp .env.example .env
make install
make test
make demo
```

The demo writes Parquet layers and a `run_manifest.json` under `data/lakehouse/`. It also writes a Power BI import CSV and a data-derived chart to `reports/generated/`.

To run the complete operational stack, including PostgreSQL, MinIO, Spark, Airflow, and dbt:

```bash
docker compose up --build
```

Open Airflow at `http://localhost:8088`, then manually trigger `retail_lakehouse_monthly`. The DAG has no automatic schedule; this prevents unreviewed or unexpected live data refreshes. For a production schedule, set the cadence, budget, data-retention policy, and alerting policy before enabling it.

## Data model and business output

The gold mart groups each `year_month` and `item_type`, producing `retail_sales_cases`, `retail_transfer_cases`, `warehouse_sales_cases`, product and supplier breadth, and `net_cases` (retail plus warehouse cases). Negative values are retained because they may represent legitimate returns or adjustments.

For Power BI, import `reports/generated/monthly_category_metrics.csv`, apply the included theme, and follow the suggested visuals and DAX measures in [the reporting hand-off](reports/powerbi/README.md).

## Cloud warehouse adapters

The repository includes SQL adapters for [Snowflake](warehouse/snowflake/monthly_category_metrics.sql) and [BigQuery](warehouse/bigquery/monthly_category_metrics.sql). They are intentionally not executed by the deterministic demo, so reviewing the project does not require a cloud account or incur paid-service charges.

## Validation

The Quality Gate runs Ruff, Python pipeline tests, a real Spark aggregation test, and a bronze-to-gold demonstration run. Locally, run `make test`; on GitHub, the workflow additionally sets up Java 17 and executes the checked-in public-data fixture.

## References

[1] [Montgomery County Warehouse and Retail Sales — Data.gov catalog](https://catalog.data.gov/dataset/warehouse-and-retail-sales)
