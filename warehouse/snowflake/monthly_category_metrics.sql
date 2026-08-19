create schema if not exists analytics;

create or replace table analytics.monthly_category_metrics (
    year_month date,
    item_type string,
    retail_sales_cases number(18, 2),
    retail_transfer_cases number(18, 2),
    warehouse_sales_cases number(18, 2),
    distinct_items number(18, 0),
    distinct_suppliers number(18, 0),
    net_cases number(18, 2)
);
