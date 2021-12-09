# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying
# Subscribe the book depth infomation

from binex_f.ws.mapping import *
from binex_f.utils import random_id

def __subscribe(params: 'list'):
    return {
        "method": "SUBSCRIBE",
        "params": params,
        "id":     random_id()
        }

def __mapping_keys(pl, mapping: 'dict'):
    if isinstance(pl, dict):
        _r = dict()
        for (k, v) in pl.items():
            key = mapping.get(k, k)
            if isinstance(v, dict):
                _r[key] = __mapping_keys(v, mapping.get(key, dict()))
            elif isinstance(v, list):
                _r[key] = [(__mapping_keys(ele, mapping.get(key, dict())) if isinstance(ele, dict) else ele) for ele in v]
            else:
                _r[key] = v
        return _r
    elif isinstance(pl, list):
        return [__mapping_keys(ele, mapping) for ele in pl]
    return None

def aggregate_trade_channel(symbol):
    def match(payload: 'dict'):
        if "aggTrade" == payload.get("e", None):
            return __mapping_keys(payload, aggregate_trade)
        return None
    return __subscribe(["%s@aggTrade" % symbol]), match

def mark_price_channel(symbol, update_time=None): # update_time: 1 or 3
    def match(payload: 'dict'):
        if "markPriceUpdate" == payload.get("e", None):
            return __mapping_keys(payload, mark_price)
        return None
    return __subscribe([("%s@markPrice@%s" % (symbol, update_time)) if update_time else ("%s@markPrice" % symbol)]), match

def all_mark_price_channel(update_time=None):
    def match(payload: 'list'):
        if isinstance(payload, list) and (0 == len(payload) or "markPriceUpdate" == payload[0].get("e", None)):
            return __mapping_keys(payload, all_mark_price)
        return None
    return __subscribe([("!markPrice@arr@%s" % update_time) if update_time else "!markPrice@arr"]), match

def kline_channel(symbol, interval):
    """
    @interval:
        minute: 1m  3m  5m  15m  30m
        hour:   1h  2h  4h  6h   8h   12h
        day:    1d  3d
        week:   1w
        month:  1M
    """
    def match(payload: 'dict'):
        if "kline" == payload.get("e", None):
            return __mapping_keys(payload, kline)
        return None
    return __subscribe(["%s@kline_%s" % (symbol, interval)]), match

def continuous_kline_channel(pair, contract_type, interval):
    def match(payload: 'dict'):
        if "continuous_kline" == payload.get("e", None):
            return __mapping_keys(payload, continuous_kline)
        return None
    return __subscribe(["%s_%s@continuousKline_%s" % (pair, contract_type, interval)]), match

def symbol_miniticker_channel(symbol):
    def match(payload: 'dict'):
        if "MiniTicker" in payload.get("e", ""):
            return __mapping_keys(payload, symbol_miniticker)
        return None
    return __subscribe(["%s@miniTicker" % symbol]), match

def all_miniticker_channel():
    def match(payload: 'list'):
        if isinstance(payload, list) and (0 == len(payload) or "MiniTicker" in payload[0].get("e", "")):
            return __mapping_keys(payload, all_miniticker)
        return None
    return __subscribe(["!miniTicker@arr"]), match

def symbol_ticker_channel(symbol):
    def match(payload: 'dict'):
        if "Ticker" in payload.get("e", ""):
            return __mapping_keys(payload, symbol_ticker)
        return None
    return __subscribe(["%s@ticker" % symbol]), match

def all_ticker_channel():
    def match(payload: 'dict'):
        if isinstance(payload, list) and (0 == len(payload) or "Ticker" in payload[0].get("e", "")):
            return __mapping_keys(payload, all_ticker)
        return None
    return __subscribe(["!ticker@arr"]), match

def symbol_bookticker_channel(symbol):
    def match(payload: 'dict'):
        if "bookTicker" == payload.get("e", None):
            return __mapping_keys(payload, symbol_bookticker)
        return None
    return __subscribe(["%s@bookTicker" % symbol]), match

def all_bookticker_channel():
    def match(payload: 'dict'):
        if "bookTicker" == payload.get("e", None):
            return __mapping_keys(payload, all_bookticker)
        return None
    return __subscribe(["!bookTicker"]), match

def symbol_liquidation_channel(symbol):
    def match(payload: 'dict'):
        if "forceOrder" == payload.get("e", None):
            return __mapping_keys(payload, symbol_liquidation)
        return None
    return __subscribe(["%s@forceOrder" % symbol]), match

def all_liquidation_channel():
    def match(payload):
        if (isinstance(payload, dict) and "forceOrder" == payload.get("e", None)) or \
                 (isinstance(payload, list) and (0 == len(payload) or "forceOrder" == payload[0].get("e", None))):
            return __mapping_keys(payload, all_liquidation)
        return None
    return __subscribe(["!forceOrder@arr"]), match

def book_depth_channel(symbol_list, limit, update_time):
    def match(payload: 'dict'):
        if "depthUpdate" == payload.get("e", None):
            return __mapping_keys(payload, book_depth)
        return None
    params = list()
    for symbol in symbol_list:
        params.append("%s@depth%s%s" % (symbol, limit, (update_time if update_time else "")))
    return __subscribe(params), match

def diff_book_depth_channel(symbol_list, update_time):
    def match(payload: 'dict'):
        if "depthUpdate" == payload.get("e", None):
            return __mapping_keys(payload, diff_depth)
        return None
    params = list()
    for symbol in symbol_list:
        params.append("%s@depth%s" % (symbol, (update_time if update_time else "")))
    return __subscribe(params), match

def nav_channel(tokenName): # tokenName must be uppercase, e.g. "TRXDOWN"
    def match(payload: 'dict'):
        if "nav" == payload.get("e", None):
            return __mapping_keys(payload, nav)
        return None
    return __subscribe(["%s@tokenNav" % tokenName.upper()]), match

def nav_kline_channel(tokenName, interval): # tokenName must be uppercase, e.g. "TRXDOWN"
    """
    @interval:
        minute: 1m  3m  5m  15m  30m
        hour:   1h  2h  4h  6h   8h   12h
        day:    1d  3d
        week:   1w
        month:  1M
    """
    def match(payload: 'dict'):
        if "kline" == payload.get("e", None):
            return __mapping_keys(payload, nav_kline)
        return None
    return __subscribe(["%s@nav_Kline_%s" % (tokenName.upper(), interval)]), match

def composite_index_channel(symbol):
    def match(payload: 'dict'):
        if "compositeIndex" == payload.get("e", None):
            return __mapping_keys(payload, composite_index)
        return None
    return __subscribe(["%s@compositeIndex" % symbol]), match

def user_data_channel(listenKey):
    def match(payload: 'dict'):
        event = payload.get("e", None)
        if "ORDER_TRADE_UPDATE" == event:
            return __mapping_keys(payload, order_trade_update)
        elif "listenKeyExpired" == event:
            return __mapping_keys(payload, {})
        elif "MARGIN_CALL" == event:
            return __mapping_keys(payload, margin_call)
        elif "ACCOUNT_UPDATE" == event:
            return __mapping_keys(payload, account_update)
        elif "ACCOUNT_CONFIG_UPDATE" == event:
            return __mapping_keys(payload, account_config_update)
        return None
    return __subscribe([listenKey]), match
