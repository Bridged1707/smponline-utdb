-- ======================================================
-- UTDB SCHEMA
-- ======================================================

-- RAW EVENTS
-- Stores the exact JSON events from the SMP economy API

CREATE TABLE IF NOT EXISTS raw_events (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    event_timestamp BIGINT NOT NULL,
    received_timestamp BIGINT NOT NULL,
    payload JSONB NOT NULL,
    dedup_hash TEXT UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_raw_events_type
ON raw_events(event_type);

CREATE INDEX IF NOT EXISTS idx_raw_events_timestamp
ON raw_events(event_timestamp);

CREATE INDEX IF NOT EXISTS idx_raw_events_payload
ON raw_events USING GIN(payload);


-- ======================================================
-- NORMALIZED TRANSACTIONS
-- ======================================================

CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,

    event_type TEXT NOT NULL,

    item_type TEXT NOT NULL,
    item_snbt TEXT,

    quantity NUMERIC NOT NULL,
    price_per_item NUMERIC NOT NULL,
    total_value NUMERIC NOT NULL,

    location_world TEXT,
    location_x INT,
    location_y INT,
    location_z INT,

    timestamp BIGINT NOT NULL,

    payload JSONB
);

CREATE INDEX IF NOT EXISTS idx_transactions_item
ON transactions(item_type);

CREATE INDEX IF NOT EXISTS idx_transactions_time
ON transactions(timestamp);


-- ======================================================
-- MARKET PRICE HISTORY
-- ======================================================

CREATE TABLE IF NOT EXISTS market_ticks (
    id BIGSERIAL PRIMARY KEY,
    item_type TEXT NOT NULL,
    timestamp BIGINT NOT NULL,
    median_price NUMERIC,
    vwap NUMERIC,
    trade_volume NUMERIC,
    trade_count INT
);

CREATE INDEX IF NOT EXISTS idx_ticks_item
ON market_ticks(item_type);

CREATE INDEX IF NOT EXISTS idx_ticks_time
ON market_ticks(timestamp);
