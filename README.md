# smponline-utdb

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

```
INSERT INTO prediction_markets (
    code, 
    title, 
    description, 
    closes_at, 
    resolves_at, 
    status, 
    created_by, 
    created_at, 
    updated_at, 
    yes_pool, 
    no_pool, 
    total_volume, 
    price_yes, 
    price_no
)
VALUES (
    'MARKET_CODE_HERE', 
    'Your Question Here?', 
    'A brief description of the market rules.', 
    NOW() + interval '7 days', 
    NOW() + interval '8 days', 
    'open', 
    'YOUR_NAME', 
    NOW(), 
    NOW(), 
    0, 
    0, 
    0, 
    0.50, 
    0.50 
);
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
