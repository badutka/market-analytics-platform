with staging_data as (
    select * from {{ ref('stg_market_prices') }}
),

calculated_metrics as (
    select
        asset_ticker,
        trading_date,
        price_close,
        trading_volume,
        
        -- 14-Day Simple Moving Average using window partitions
        avg(price_close) over (
            partition by asset_ticker 
            order by trading_date 
            rows between 13 preceding and current row
        ) as moving_avg_14d

    from staging_data
)

select
    asset_ticker,
    trading_date,
    price_close,
    moving_avg_14d,
    trading_volume
    
from calculated_metrics
order by asset_ticker, trading_date desc
