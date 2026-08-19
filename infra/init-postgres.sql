create schema if not exists bronze;
create schema if not exists analytics;

create table if not exists analytics.pipeline_runs (
    run_id bigserial primary key,
    run_at_utc timestamptz not null default now(),
    source_name text not null,
    bronze_rows integer not null,
    silver_rows integer not null,
    gold_rows integer not null,
    quality_status text not null
);
