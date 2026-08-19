# Data Source and Provenance

## Approved source

The local demonstration uses a checked-in **825-row fixture** sampled from the official export of the Montgomery County, Maryland Warehouse and Retail Sales open dataset. The official catalog describes this as sales and movement data by item and department that is appended monthly. The project intentionally uses this public aggregate business dataset rather than customer-level transactions, so the repository does not include personal customer information. [1]

| Field | Meaning in the source contract |
|---|---|
| `YEAR`, `MONTH` | Calendar grain used to derive `year_month` |
| `SUPPLIER` | Supplier business name |
| `ITEM CODE`, `ITEM DESCRIPTION`, `ITEM TYPE` | Product identity and category |
| `RETAIL SALES`, `RETAIL TRANSFERS`, `WAREHOUSE SALES` | Cases moved through the corresponding channel |

## Retrieval

The full source can be retrieved with the following documented CSV export endpoint:

```text
https://data.montgomerycountymd.gov/api/v3/views/v76h-r7br/export.csv?accessType=DOWNLOAD
```

The project processes the fixture for deterministic tests and local demonstrations. The live operator-triggered pipeline uses the same source contract and URL, writes an immutable bronze capture, validates the required columns, standardizes valid records to silver, quarantines invalid calendar or product-identity records, and publishes the Power BI-ready gold mart only after its quality gate passes.

## Source note

The demonstration fixture was retrieved on **2026-08-19**. It contains 75 official records from each available 2019 source month from January through November, which creates a real multi-month reporting series without fabricating data. Refreshes should be attributed to Montgomery County and recorded in the generated pipeline manifest.

## References

[1] [Montgomery County Warehouse and Retail Sales — Data.gov catalog](https://catalog.data.gov/dataset/warehouse-and-retail-sales)
