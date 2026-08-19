"""Declarative quality checks used before gold-layer publication."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class QualityResult:
    """Captures a named quality rule and its result for the run manifest."""

    rule: str
    passed: bool
    observed: int
    expected: str


def validate_silver(frame: pd.DataFrame) -> list[QualityResult]:
    """Validate the cleaned sales grain while preserving valid negative adjustments."""

    checks = [
        QualityResult("silver_has_rows", not frame.empty, len(frame), "> 0"),
        QualityResult(
            "year_month_not_null",
            int(frame["year_month"].isna().sum()) == 0,
            int(frame["year_month"].isna().sum()),
            "0",
        ),
        QualityResult(
            "item_code_not_blank",
            int(frame["item_code"].fillna("").str.strip().eq("").sum()) == 0,
            int(frame["item_code"].fillna("").str.strip().eq("").sum()),
            "0",
        ),
        QualityResult(
            "known_item_type",
            int(frame["item_type"].fillna("").str.strip().eq("").sum()) == 0,
            int(frame["item_type"].fillna("").str.strip().eq("").sum()),
            "0",
        ),
    ]
    return checks


def require_quality_pass(checks: list[QualityResult]) -> None:
    """Fail publication when a bronze-to-silver quality rule fails."""

    failures = [check.rule for check in checks if not check.passed]
    if failures:
        raise ValueError(f"Quality gate failed: {', '.join(failures)}")
