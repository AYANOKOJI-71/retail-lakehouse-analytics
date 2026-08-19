# Local Operations Guide

## Purpose and operating boundary

This repository is a **local-first reference lakehouse**. It is designed to demonstrate data-engineering practices without requiring a paid warehouse account or a background production deployment. The default demonstration uses a versioned, public non-personal retail-sales fixture and executes only when an operator starts it.

> The bundled Airflow DAG deliberately uses `schedule=None`. It is a manual-run control, not a production scheduler. Define cadence, owners, alerting, cost limits, retention, and incident procedures before enabling any recurring refresh.

## Runtime topology

| Component | Local responsibility | Endpoint or artifact |
|---|---|---|
| PostgreSQL 16 | Metadata and optional gold-mart serving table | `postgres:5432` inside Compose |
| MinIO | S3-compatible bronze, silver, and gold object-store target | API `http://localhost:9000`; console `http://localhost:9001` |
| Spark 3.5 | Distributed gold-mart aggregation reference path | UI `http://localhost:8080` |
| Airflow 2.10 | Manual orchestration entry point | `http://localhost:8088` |
| dbt-postgres 1.8 | SQL model and test execution image | `docker compose --profile transform run --rm dbt` |
| Python pipeline | Deterministic portable bronze-to-gold demo | `make demo` |

## Deterministic developer run

```bash
cp .env.example .env
make install
make test
make demo
```

This path uses the checked-in fixture. It produces local Parquet layers under `data/lakehouse/`, a `metadata/run_manifest.json` with source and quality information, and reporting assets under `reports/generated/`.

## Full local Compose run

```bash
cp .env.example .env
docker compose up --build
```

After the services are healthy, open Airflow and trigger `retail_lakehouse_monthly`. The demo has no automatic schedule and the local default credentials in `.env.example` are explicitly for local development only. Replace every default before placing the stack on a company-controlled host.

To test dbt against the PostgreSQL service, copy the example profile into a private local file, then run the transform profile:

```bash
cp dbt_lakehouse/profiles.yml.example dbt_lakehouse/profiles.yml
docker compose --profile transform run --rm dbt run --profiles-dir .
docker compose --profile transform run --rm dbt test --profiles-dir .
```

## Warehouse adapters and reporting hand-off

The Snowflake and BigQuery SQL files define the same monthly category grain as the local gold mart. They are **deployment adapters**, not connected cloud accounts. Configure credentials only through an untracked environment or a managed secret store; do not place them in this repository.

For reporting, import `reports/generated/monthly_category_metrics.csv` into Power BI and follow the recommended model, visuals, DAX measures, and theme in [`reports/powerbi`](../reports/powerbi/README.md).

## Shutdown and cleanup

```bash
make compose-down
```

This command removes Compose volumes. Export any artifacts or database records that you intend to keep before executing it.
