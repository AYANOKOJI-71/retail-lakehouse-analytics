"""Ingest the approved public source into the bronze layer."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

from .contracts import SourceContract


class SourceContractError(ValueError):
    """Raised when an incoming source does not meet its approved schema contract."""


def download_public_source(contract: SourceContract, target: Path, timeout_seconds: int = 60) -> Path:
    """Download the approved public CSV without embedding source data in the repository."""

    response = requests.get(contract.url, timeout=timeout_seconds)
    response.raise_for_status()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response.content)
    return target


def read_and_validate_csv(path: Path, contract: SourceContract) -> pd.DataFrame:
    """Load a CSV and require every source field used by downstream transformations."""

    frame = pd.read_csv(path)
    missing_columns = sorted(set(contract.required_columns).difference(frame.columns))
    if missing_columns:
        joined = ", ".join(missing_columns)
        raise SourceContractError(f"Source is missing required columns: {joined}")
    return frame
