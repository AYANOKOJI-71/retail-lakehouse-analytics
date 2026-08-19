with source_rows as (
    select * from {{ source('bronze', 'retail_sales') }}
),
standardized as (
    select
        cast(calendar_year as integer) as calendar_year,
        cast(calendar_month as integer) as calendar_month,
        cast(year_month as date) as year_month,
        trim(supplier) as supplier,
        trim(item_code) as item_code,
        trim(item_description) as item_description,
        trim(item_type) as item_type,
        cast(retail_sales_cases as numeric) as retail_sales_cases,
        cast(retail_transfer_cases as numeric) as retail_transfer_cases,
        cast(warehouse_sales_cases as numeric) as warehouse_sales_cases
    from source_rows
)
select * from standardized
