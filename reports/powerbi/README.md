# Power BI reporting hand-off

The gold mart is published to `data/lakehouse/gold/monthly_category_metrics/monthly_category_metrics.parquet`. Use the local export command in the project README to generate a CSV, then import it into Power BI Desktop.

| Suggested visual | Fields | Decision supported |
|---|---|---|
| Monthly trend | `year_month`, `net_cases` | Demand and seasonal movement |
| Category mix | `item_type`, `net_cases` | Product-category contribution |
| Retail vs warehouse | `retail_sales_cases`, `warehouse_sales_cases` | Channel movement comparison |
| Supplier breadth | `item_type`, `distinct_suppliers` | Supply concentration review |

## DAX measures

```dax
Net Cases = SUM(monthly_category_metrics[net_cases])
Retail Cases = SUM(monthly_category_metrics[retail_sales_cases])
Warehouse Cases = SUM(monthly_category_metrics[warehouse_sales_cases])
Retail Share = DIVIDE([Retail Cases], [Retail Cases] + [Warehouse Cases])
```

The project does not ship a `.pbix` file because Power BI Desktop is an interactive client application. Instead, it provides the gold schema, column meanings, measures, and an import-ready extract that make the report reproducible.
