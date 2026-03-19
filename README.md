# smponline-utdb

# How To Create New Code

1. Symbol
INSERT INTO market_symbols (code, name, pricing_method, display_price_source, is_active, created_at, updated_at)
VALUES ('YOUR_CODE', 'Display Name', 'vwap', 'market_candles', true, NOW(), NOW());

2. Family
INSERT INTO market_asset_families (code, name, base_unit_name, is_active, created_at, updated_at)
VALUES ('YOUR_CODE', 'Family Name', 'Unit', true, NOW(), NOW());

3. Link
INSERT INTO market_symbol_families (symbol_code, family_code, include_all_forms, is_active, created_at)
VALUES ('YOUR_CODE', 'YOUR_CODE', true, true, NOW());

4. Item Mapping
INSERT INTO market_asset_family_items (family_code, item_type, item_name, quantity_multiplier, form_kind, sort_order, is_active, created_at)
VALUES ('YOUR_CODE', 'MC_ITEM_ID', 'Display Name', 1.0, 'item', 10, true, NOW());

5. Config
INSERT INTO market_symbol_config (symbol_code, is_enabled, quote_strategy, candle_strategy, outlier_filter_enabled, carry_forward_enabled, updated_at)
VALUES ('YOUR_CODE', true, 'vwap', 'standard', true, true, NOW());
