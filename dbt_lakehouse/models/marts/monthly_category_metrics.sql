select
    year_month,
    item_type,
    sum(retail_sales_cases) as retail_sales_cases,
    sum(retail_transfer_cases) as retail_transfer_cases,
    sum(warehouse_sales_cases) as warehouse_sales_cases,
    count(distinct item_code) as distinct_items,
    count(distinct supplier) as distinct_suppliers,
    sum(retail_sales_cases) + sum(warehouse_sales_cases) as net_cases
from {{ ref('stg_retail_sales') }}
group by 1, 2
