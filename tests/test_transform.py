from pathlib import Path

from lakehouse.contracts import DEFAULT_SOURCE_CONTRACT
from lakehouse.ingest import read_and_validate_csv
from lakehouse.quality import validate_silver
from lakehouse.transform import build_monthly_category_metrics, clean_to_silver

FIXTURE = Path("data/fixtures/montgomery_retail_sales.csv")


def test_public_fixture_satisfies_contract_and_builds_gold_mart() -> None:
    raw = read_and_validate_csv(FIXTURE, DEFAULT_SOURCE_CONTRACT)
    silver, rejected = clean_to_silver(raw)
    gold = build_monthly_category_metrics(silver)

    assert not silver.empty
    assert len(rejected) >= 0
    assert not gold.empty
    assert {"year_month", "item_type", "net_cases", "distinct_items"}.issubset(gold.columns)
    assert all(result.passed for result in validate_silver(silver))


def test_invalid_calendar_records_are_quarantined() -> None:
    raw = read_and_validate_csv(FIXTURE, DEFAULT_SOURCE_CONTRACT).head(2).copy()
    raw.loc[raw.index[0], "MONTH"] = 18

    silver, rejected = clean_to_silver(raw)

    assert len(silver) == 1
    assert len(rejected) == 1
