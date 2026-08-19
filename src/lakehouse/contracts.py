"""Source and data-quality contracts for the public retail-sales pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceContract:
    """Defines an approved public source and the schema required by the lakehouse."""

    name: str
    url: str
    required_columns: tuple[str, ...]
    attribution: str


DEFAULT_SOURCE_CONTRACT = SourceContract(
    name="Montgomery County Warehouse and Retail Sales",
    url="https://data.montgomerycountymd.gov/api/v3/views/v76h-r7br/export.csv?accessType=DOWNLOAD",
    required_columns=(
        "YEAR",
        "MONTH",
        "SUPPLIER",
        "ITEM CODE",
        "ITEM DESCRIPTION",
        "ITEM TYPE",
        "RETAIL SALES",
        "RETAIL TRANSFERS",
        "WAREHOUSE SALES",
    ),
    attribution=(
        "Montgomery County, Maryland open-data portal; monthly warehouse and retail sales by item and department."
    ),
)
