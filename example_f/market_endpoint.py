# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

import time
from binex_f import Dict2Class, RestApi

def __print_obj(resp):
    print (Dict2Class.to_val(resp))
    time.sleep(0.5)

restapi = RestApi()

# Test Connectivity
# resp = restapi.ping()
resp = restapi.ping()
__print_obj(resp)

# Check Server Time
# resp = restapi.get_servertime()
resp = restapi.get_servertime()
__print_obj(resp)

# Exchange Information
# resp = restapi.get_exchange_info()
resp = restapi.get_exchange_info()
__print_obj(resp)

# Order Book
# limit: Default 500; Valid limits:[5, 10, 20, 50, 100, 500, 1000]
# resp = restapi.get_book_depth(symbol, limit=None)
resp = restapi.get_book_depth(symbol="btcusdt", limit=10)
__print_obj(resp)

# Recent Trades List
# limit: Default 500; max 1000.
# resp = restapi.get_recent_trades(symbol, limit=None)
resp = restapi.get_recent_trades(symbol="btcusdt", limit=100)
__print_obj(resp)

# Old Trades Lookup (MARKET_DATA)
# limit: Default 500; max 1000.
# fromId: TradeId to fetch from. Default gets most recent trades.
# resp = restapi.get_historical_trades(symbol, limit=None, fromId=None)
resp = restapi.get_historical_trades(symbol="btcusdt")
__print_obj(resp)

# Compressed/Aggregate Trades List
# fromId: ID to get aggregate trades from INCLUSIVE.
# startTime: Timestamp in ms to get aggregate trades from INCLUSIVE.
# endTime: Timestamp in ms to get aggregate trades until INCLUSIVE.
# limit: Default 500; max 1000.
# resp = restapi.get_aggregate_trades(symbol, fromId=None, startTime=None, endTime=None, limit=None)
resp = restapi.get_aggregate_trades(symbol="btcusdt")
__print_obj(resp)

# Kline/Candlestick Data
# interval: ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1m"]
# limit: Default 500; max 1500.
# resp = restapi.get_klines(symbol, interval, startTime=None, endTime=None, limit=None)
resp = restapi.get_klines(symbol="btcusdt", interval="4h", limit=100)
__print_obj(resp)

# Continuous Contract Kline/Candlestick Data
# contractType: ["PERPETUAL", "CURRENT_MONTH", "NEXT_MONTH", "CURRENT_QUARTER", "NEXT_QUARTER"]
# interval: ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1m"]
# limit: Default 500; max 1500.
# resp = restapi.get_continuous_klines(pair, contractType, interval, startTime=None, endTime=None, limit=None)
resp = restapi.get_continuous_klines(pair="btcusdt", contractType="PERPETUAL", interval="4h", limit=100)
__print_obj(resp)

# Index Price Kline/Candlestick Data
# interval: ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1m"]
# limit: Default 500; max 1500.
# resp = restapi.get_index_price_klines(pair, interval, startTime=None, endTime=None, limit=None)
resp = restapi.get_index_price_klines(pair="btcusdt", interval="4h", limit=100)
__print_obj(resp)

# Mark Price Kline/Candlestick Data
# interval: ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1m"]
# limit: Default 500; max 1500.
# resp = restapi.get_mark_price_klines(symbol, interval, startTime=None, endTime=None, limit=None)
resp = restapi.get_mark_price_klines(symbol="btcusdt", interval="4h")
__print_obj(resp)

# Mark Price
# resp = restapi.get_mark_price(symbol=None)
resp = restapi.get_mark_price()
__print_obj(resp)

# Get Funding Rate History
# limit: Default 100; max 1000
# resp = restapi.get_funding_rate(symbol=None, startTime=None, endTime=None, limit=None)
resp = restapi.get_funding_rate()
__print_obj(resp)

# 24hr Ticker Price Change Statistics
# resp = restapi.get_ticker_24hr(symbol=None)
resp = restapi.get_ticker_24hr()
__print_obj(resp)

#Symbol Price Ticker
# resp = restapi.get_ticker_price(symbol=None)
resp = restapi.get_ticker_price()
__print_obj(resp)

# Symbol Order Book Ticker
# resp = restapi.get_book_ticker(symbol=None)
resp = restapi.get_book_ticker()
__print_obj(resp)

# Open Interest
# resp = restapi.get_open_interest(symbol)
resp = restapi.get_open_interest(symbol="btcusdt")
__print_obj(resp)

# Open Interest Statistics
# period: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]
# limit: default 30, max 500
# resp = restapi.get_open_interest_hist(symbol, period, startTime=None, endTime=None, limit=None)
resp = restapi.get_open_interest_hist(symbol="btcusdt", period="4h", limit=30)
__print_obj(resp)

# Top Trader Long/Short Ratio (Accounts)
# period: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]
# limit: default 30, max 500
# resp = restapi.get_top_long_short_account_ratio(symbol, period, startTime=None, endTime=None, limit=None)
resp = restapi.get_top_long_short_account_ratio(symbol="btcusdt", period="4h", limit=30)
__print_obj(resp)

# Top Trader Long/Short Ratio (Positions)
# period: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]
# limit: default 30, max 500
# resp = restapi.get_top_long_short_position_ratio(symbol, period, startTime=None, endTime=None, limit=None)
resp = restapi.get_top_long_short_position_ratio(symbol="btcusdt", period="4h", limit=30)
__print_obj(resp)

# Long/Short Ratio
# period: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]
# limit: default 30, max 500
# resp = restapi.get_global_long_short_account_ratio(symbol, period, startTime=None, endTime=None, limit=None)
resp = restapi.get_global_long_short_account_ratio(symbol="btcusdt", period="4h", limit=30)
__print_obj(resp)

# Taker Buy/Sell Volume
# period: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]
# limit: default 30, max 500
# resp = restapi.get_taker_long_short_ratio(symbol, period, startTime=None, endTime=None, limit=None)
resp = restapi.get_taker_long_short_ratio(symbol="btcusdt", period="4h", limit=30)
__print_obj(resp)

# Historical BLVT NAV Kline/Candlestick
# interval: ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1m"]
# limit: default 500, max 1000
# resp = restapi.get_lvt_klines(symbol, interval, startTime=None, endTime=None, limit=None)
resp = restapi.get_lvt_klines(symbol="BTCDOWN", interval="4h", limit=300)
__print_obj(resp)

# Composite Index Symbol Information
# resp = restapi.get_index_info(symbol=None)
resp = restapi.get_index_info()
__print_obj(resp)

# Multi-Assets Mode Asset Index
# resp = restapi.get_asset_index(symbol=None)
resp = restapi.get_asset_index()
__print_obj(resp)
