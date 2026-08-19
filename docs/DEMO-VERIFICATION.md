# Deterministic Demo Verification

The local bronze-to-gold demonstration was executed on **2026-08-19** against the versioned public fixture. No cloud warehouse connection, user data, credentials, or paid service was required.

| Check | Verified outcome |
|---|---:|
| Public source fixture | 825 rows across January–November 2019 |
| Bronze layer | 825 Parquet records written |
| Silver layer | 825 accepted records; 0 rejected records |
| Gold mart | 56 month-and-item-type rows |
| Quality rules | 4 of 4 passed |
| Reporting assets | Power BI CSV and multi-month chart generated |
| Tests | 7 passed, including a real local Spark aggregation test |

The four quality rules enforce a nonempty silver layer, valid monthly grain, nonblank product codes, and known item types. The verified artifact manifest is generated at runtime under `data/lakehouse/metadata/run_manifest.json`; generated data and images remain untracked so every run is reproducible from the fixture.

![Data-derived monthly category mix](../reports/generated/monthly_category_mix.png)

The chart uses official source values sampled across eleven available 2019 months. It is a demonstrative business output, not a forecast or an estimate.
