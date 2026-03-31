# smponline-utdb

# Check User Credit Table
```
SELECT 
    a.discord_uuid, 
    a.mc_name, 
    COALESCE(w.weekly_credits, 0) AS total_weekly_credits, 
    COALESCE(w.used_credits, 0) AS credits_used, 
    (COALESCE(w.weekly_credits, 0) - COALESCE(w.used_credits, 0)) AS credits_remaining,
    w.week_end_at AS reset_at
FROM accounts a
LEFT JOIN user_credit_wallets w ON a.discord_uuid = w.discord_uuid
ORDER BY credits_used DESC;
```
Filter by specific user.
```
SELECT 
    a.discord_uuid, 
    a.mc_name, 
    COALESCE(w.weekly_credits, 0) AS total_weekly_credits, 
    COALESCE(w.used_credits, 0) AS credits_used, 
    (COALESCE(w.weekly_credits, 0) - COALESCE(w.used_credits, 0)) AS credits_remaining,
    w.week_end_at AS reset_at
FROM accounts a
LEFT JOIN user_credit_wallets w ON a.discord_uuid = w.discord_uuid
WHERE a.discord_uuid = 'TARGET_DISCORD_UUID';
```

# Check Total Membership Sales
Simple Total Spent
```
SELECT COALESCE(SUM(amount), 0) AS total_membership_diamonds_spent
FROM balance_transactions
WHERE kind = 'membership_purchase';
```
Per User Total Spent
```
SELECT
    discord_uuid,
    COALESCE(SUM(amount), 0) AS total_membership_diamonds_spent
FROM balance_transactions
WHERE kind = 'membership_purchase'
GROUP BY discord_uuid
ORDER BY total_membership_diamonds_spent DESC;
```
Per Tier Totals
```
SELECT
    metadata->>'tier' AS tier,
    COALESCE(SUM(amount), 0) AS diamonds_spent
FROM balance_transactions
WHERE kind = 'membership_purchase'
GROUP BY metadata->>'tier'
ORDER BY diamonds_spent DESC;
```
Weekly Sales
```
SELECT
    DATE_TRUNC('week', created_at) AS week_start,
    COALESCE(SUM(amount), 0) AS diamonds_spent
FROM balance_transactions
WHERE kind = 'membership_purchase'
GROUP BY DATE_TRUNC('week', created_at)
ORDER BY week_start DESC;
```

# How To Add A Deposit Shop
```
INSERT INTO shops (
    shop_id,
    owner_name,
    owner_uuid,
    world,
    x,
    y,
    z,
    shop_type,
    price,
    remaining,
    item_type,
    item_name,
    item_quantity,
    snbt,
    last_seen
)
VALUES (
    36846,                                  -- unique shop_id
    'Suijin___',                             -- owner_name
    '998dffa4-b706-41ed-bd89-fdc80667d235',    -- owner_uuid (MUST match allowlist)
    'world',                                  -- world
    -480,                                     -- x
    109,                                       -- y
    -8614,                                     -- z
    'SELLING',                                -- shop_type
    1,                                       -- price (diamonds)
    162,                                     -- remaining stock
    'PAPER',                                   -- item_type
    'Wall Street Deposit Slip',                                   -- item_name
    1,                                        -- item_quantity
    '{}',                                     -- snbt
    (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT -- last_seen (ms)
);
```

# How To Create New Prediction Market
Category Market
```
BEGIN;

-- Step 1: Create the Market Metadata
INSERT INTO prediction_markets (
    code, 
    title, 
    description, 
    market_type, 
    resolution_mode, 
    status, 
    closes_at
)
VALUES (
    'TEST009', 
    'Choose a player', 
    'Market resolves based on community vote at the end of the month.', 
    'categorical', 
    'admin_set_option', 
    'open', 
    '2026-03-31 00:33:59'
) ON CONFLICT (code) DO NOTHING;

-- Step 2: Add the Options (linked to 'MVP_MARCH_2026')
WITH inserted_options AS (
    INSERT INTO prediction_market_options (market_code, option_code, label, sort_order)
    VALUES 
        ('TEST009', 'PLAYER_A', 'Suijin___', 10),
        ('TEST009', 'PLAYER_B', 'ChadsGaming', 20),
        ('TEST009', 'PLAYER_C', 'BreezyMedic', 30),
        ('TEST009', 'OTHER', 'Someone Else', 40)
    ON CONFLICT (market_code, option_code) DO NOTHING
    RETURNING id, market_code
)
-- Step 3: Initialize the State
INSERT INTO prediction_option_state (market_code, option_id, pool_amount, implied_price)
SELECT market_code, id, 0, 0.25 
FROM inserted_options;

COMMIT;
```
Numeric Range Market
```
BEGIN;

INSERT INTO prediction_markets (code, title, market_type, resolution_mode)
VALUES ('NSTR_PRICE_EOM', 'Nether Star Price at End of Month', 'numeric_range', 'admin_set_numeric');

WITH inserted_options AS (
    INSERT INTO prediction_market_options (market_code, option_code, label, range_min, range_max, sort_order)
    VALUES 
        ('NSTR_PRICE_EOM', 'LOW', 'Under 500', 0, 499.99, 10),
        ('NSTR_PRICE_EOM', 'MID', '500 to 1000', 500, 1000, 20),
        ('NSTR_PRICE_EOM', 'HIGH', 'Over 1000', 1000.01, 999999, 30)
    RETURNING id, market_code
)
INSERT INTO prediction_option_state (market_code, option_id)
SELECT market_code, id FROM inserted_options;

COMMIT;
```
Query Live Odds
```
SELECT 
    pm.title,
    pmo.label AS option_name,
    pos.implied_price,
    pos.pool_amount,
    pos.wager_count
FROM prediction_markets pm
JOIN prediction_market_options pmo ON pm.code = pmo.market_code
JOIN prediction_option_state pos ON pmo.id = pos.option_id
WHERE pm.code = 'MVP_2026' -- Replace with your market code
ORDER BY pmo.sort_order ASC;
```

# How To Remove Prediction Market

```
BEGIN;

-- 1. Remove all wagers associated with this market
DELETE FROM prediction_wagers 
WHERE market_code = 'IRON_MOVE_25';

-- 2. Remove all price snapshots associated with this market
DELETE FROM prediction_market_snapshots 
WHERE market_code = 'IRON_MOVE_25';

-- 3. Finally, remove the market itself
DELETE FROM prediction_markets 
WHERE code = 'IRON_MOVE_25';

COMMIT;
```

# How To Create New Symbol

1. Symbol
   
```
INSERT INTO market_symbols (code, name, pricing_method, display_price_source, is_active, created_at, updated_at)
VALUES ('YOUR_CODE', 'Display Name', 'vwap', 'market_candles', true, NOW(), NOW());
```

2. Family
   
```
INSERT INTO market_asset_families (code, name, base_unit_name, is_active, created_at, updated_at)
VALUES ('YOUR_CODE', 'Family Name', 'Unit', true, NOW(), NOW());
```

3. Link

```
INSERT INTO market_symbol_families (symbol_code, family_code, include_all_forms, is_active, created_at)
VALUES ('YOUR_CODE', 'YOUR_CODE', true, true, NOW());
```

4. Item Mapping

```
INSERT INTO market_asset_family_items (family_code, item_type, item_name, quantity_multiplier, form_kind, sort_order, is_active, created_at)
VALUES ('YOUR_CODE', 'MC_ITEM_ID', 'Display Name', 1.0, 'item', 10, true, NOW());
```

5. Config

```    
INSERT INTO market_symbol_config (symbol_code, is_enabled, quote_strategy, candle_strategy, outlier_filter_enabled, carry_forward_enabled, updated_at)
VALUES ('YOUR_CODE', true, 'vwap', 'standard', true, true, NOW());
```
