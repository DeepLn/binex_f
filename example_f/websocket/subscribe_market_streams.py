# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

from binex_f import Dict2Class, WsSubscription

ws = WsSubscription()

def f10(pl, el):
    """
    Aggregate Trade Streams
    ws.subscribe_aggregate_trade(symbol, payload_handler, error_handler=None)
    """
    ws.subscribe_aggregate_trade(symbol="btcusdt", payload_handler=pl, error_handler=el)

def f11(pl, el):
    """
    Mark Price Stream
    ws.subscribe_mark_price(symbol, update_time, payload_handler, error_handler=None)
    update_time: [1, 3, None]
    """
    ws.subscribe_mark_price(symbol="btcusdt", update_time=None, payload_handler=pl, error_handler=el)

def f12(pl, el):
    """
    Mark Price Stream for All market
    ws.subscribe_all_mark_price(payload_handler, error_handler=None)
    update_time: [1, 3, None]
    """
    ws.subscribe_all_mark_price(update_time=None, payload_handler=pl, error_handler=el)

def f13(pl, el):
    """
    Continuous Contract Kline/Candlestick Streams
    @ contract_type: ["perpetual", "current_quarter", "next_quarter"]
    @interval: ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1m"]
    ws.subscribe_continuous_kline(pair, contract_type, interval, payload_handler, error_handler=None)
    """
    ws.subscribe_continuous_kline(pair="btcusdt", contract_type="perpetual", interval="4h", payload_handler=pl, error_handler=el)

def f14(pl, el):
    """
    Kline/Candlestick Streams
    @interval: ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1m"]
    ws.subscribe_kline(symbol, interval, payload_handler, error_handler=None)
    """
    ws.subscribe_kline(symbol="btcusdt", interval="4h", payload_handler=pl, error_handler=el)

def f15(pl, el):
    """
    Individual Symbol Mini Ticker Stream
    ws.subscribe_symbol_miniticker(symbol, payload_handler, error_handler=None)
    """
    ws.subscribe_symbol_miniticker(symbol="btcusdt", payload_handler=pl, error_handler=el)

def f16(pl, el):
    """
    All Market Mini Tickers Stream
    ws.subscribe_all_miniticker(payload_handler, error_handler=None)
    """
    ws.subscribe_all_miniticker(payload_handler=pl, error_handler=el)

def f17(pl, el):
    """
    Individual Symbol Ticker Streams
    ws.subscribe_symbol_ticker(symbol, payload_handler, error_handler=None)
    """
    ws.subscribe_symbol_ticker(symbol="btcusdt", payload_handler=pl, error_handler=el)

def f18(pl, el):
    """
    All Market Tickers Streams
    ws.subscribe_all_ticker(payload_handler, error_handler=None)
    """
    ws.subscribe_all_ticker(payload_handler=pl, error_handler=el)

def f19(pl, el):
    """
    Individual Symbol Book Ticker Streams
    ws.subscribe_symbol_bookticker(symbol, payload_handler, error_handler=None)
    """
    ws.subscribe_symbol_bookticker(symbol="btcusdt", payload_handler=pl, error_handler=el)

def f20(pl, el):
    """
    All Book Tickers Stream
    ws.subscribe_all_bookticker(payload_handler, error_handler=None)
    """
    ws.subscribe_all_bookticker(payload_handler=pl, error_handler=el)

def f21(pl, el):
    """
    Liquidation Order Streams
    ws.subscribe_symbol_liquidation(symbol, payload_handler, error_handler=None)
    """
    ws.subscribe_symbol_liquidation(symbol="btcusdt", payload_handler=pl, error_handler=el)

def f22(pl, el):
    """
    All Market Liquidation Order Streams
    ws.subscribe_all_liquidation(payload_handler, error_handler=None)
    """
    ws.subscribe_all_liquidation(payload_handler=pl, error_handler=el)

def f23(pl, el):
    """
    Partial Book Depth Streams
    @limit: 5, 10, 20
    @update_time: ["@250ms", "@500ms", "@100ms"]
    ws.subscribe_book_depth(symbol_list, limit, update_time, payload_handler=None, error_handler=None)
    """
    ws.subscribe_book_depth(symbol_list=["btcusdt", "ethusdt"], limit=5, update_time="@100ms", payload_handler=pl, error_handler=el)

def f24(pl, el):
    """
    Diff. Book Depth Streams
    ws.subscribe_diff_book_depth(symbol_list, update_time, payload_handler, error_handler=None)
    """
    ws.subscribe_diff_book_depth(symbol_list=["btcusdt", "ethusdt"], update_time="@100ms", payload_handler=pl, error_handler=el)

def f25(pl, el):
    """
    BLVT Info Streams
    ws.subscribe_nav(tokenName, payload_handler, error_handler=None)
    """
    ws.subscribe_nav(tokenName="TRXDOWN", payload_handler=pl, error_handler=el)

def f26(pl, el):
    """
    BLVT NAV Kline/Candlestick Streams
    @interval: ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1m"]
    ws.subscribe_nav_kline(tokenName, interval, payload_handler=None, error_handler=None)
    """
    ws.subscribe_nav_kline(tokenName="TRXDOWN", interval="4h", payload_handler=pl, error_handler=el)

def f27(pl, el):
    """
    Composite Index Symbol Information Streams
    ws.subscribe_composite_index(symbol, payload_handler=None, error_handler=None)
    """
    ws.subscribe_composite_index(symbol="btcusdt", payload_handler=pl, error_handler=el)

def __payload_handler(payload: 'Dict2Class'):
    print (Dict2Class.to_val(payload))

def __error_handler(err_msg: 'dict'):
    print (err_msg)

if __name__ == "__main__":
    import sys
    if 2 == len(sys.argv):
        fn = sys.argv[1]
        if "f10" == fn:
            f10(__payload_handler, __error_handler)
        elif "f11" == fn:
            f11(__payload_handler, __error_handler)
        elif "f12" == fn:
            f12(__payload_handler, __error_handler)
        elif "f13" == fn:
            f13(__payload_handler, __error_handler)
        elif "f14" == fn:
            f14(__payload_handler, __error_handler)
        elif "f15" == fn:
            f15(__payload_handler, __error_handler)
        elif "f16" == fn:
            f16(__payload_handler, __error_handler)
        elif "f17" == fn:
            f17(__payload_handler, __error_handler)
        elif "f18" == fn:
            f18(__payload_handler, __error_handler)
        elif "f19" == fn:
            f19(__payload_handler, __error_handler)
        elif "f20" == fn:
            f20(__payload_handler, __error_handler)
        elif "f21" == fn:
            f21(__payload_handler, __error_handler)
        elif "f22" == fn:
            f22(__payload_handler, __error_handler)
        elif "f23" == fn:
            f23(__payload_handler, __error_handler)
        elif "f24" == fn:
            f24(__payload_handler, __error_handler)
        elif "f25" == fn:
            f25(__payload_handler, __error_handler)
        elif "f26" == fn:
            f26(__payload_handler, __error_handler)
        elif "f27" == fn:
            f27(__payload_handler, __error_handler)
