create schema if not exists `analytics`;

create or replace table `analytics.monthly_category_metrics` (
    year_month date,
    item_type string,
    retail_sales_cases numeric,
    retail_transfer_cases numeric,
    warehouse_sales_cases numeric,
    distinct_items int64,
    distinct_suppliers int64,
    net_cases numeric
)
partition by year_month
cluster by item_type;
