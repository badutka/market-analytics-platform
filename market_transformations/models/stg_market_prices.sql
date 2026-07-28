with source_data as (
    select * from {{ source('gcp_raw_data', 'historical_market_prices') }}
)

select
    -- Primary identifier
    cast(ticker as string) as asset_ticker,
    
    -- Timestamps
    cast(date as date) as trading_date,
    
    -- Market Metrics
    cast(open as float64) as price_open,
    cast(high as float64) as price_high,
    cast(low as float64) as price_low,
    cast(close as float64) as price_close,
    cast(volume as int64) as trading_volume

from source_data