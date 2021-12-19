=================================
Welcome to binex_f v0.1.1
=================================

many interfaces are heavily used by myself in product environment, the websocket is reliable (re)connected.

Latest version: v0.1.1
--------------------

Quick Start
-----------

Install from pip:

.. code:: bash

    pip install binex-f


Install from source code:

.. code:: bash

    python3 setup.py install


.. code:: python

    import time
    from binex_f import Dict2Class, RestApi as RA

    restapi = RA()

    # Dict2Class object as response of all the interfaces.
    # Dict2Class has to_val(static method) to convert obj to a python struct value.
    def __print_obj(resp):
        if resp.hasattr("code") and 200 != int(resp.code):
            print ("ERROR: %s" % Dict2Class.to_val(resp))
        else:
            print (Dict2Class.to_val(resp))
        time.sleep(0.5)

    # Test Connectivity
    resp = restapi.ping()
    __print_obj(resp)
    
    # Check Server Time
    resp = restapi.get_servertime()
    __print_obj(resp)
    
    # Exchange Information
    resp = restapi.get_exchange_info()
    
    # Order Book
    resp = restapi.get_book_depth(symbol="btcusdt", limit=10)
    __print_obj(resp)

    # Recent Trades List
    resp = restapi.get_recent_trades(symbol="btcusdt", limit=100)
    __print_obj(resp)
    
    # Old Trades Lookup (MARKET_DATA)
    resp = restapi.get_historical_trades(symbol="btcusdt")
    __print_obj(resp)
    
    # Compressed/Aggregate Trades List
    resp = restapi.get_aggregate_trades(symbol="btcusdt")
    __print_obj(resp)
    
    # Kline/Candlestick Data
    resp = restapi.get_klines(symbol="btcusdt", interval="4h", limit=100)
    __print_obj(resp)
    
    # Continuous Contract Kline/Candlestick Data
    resp = restapi.get_continuous_klines(pair="btcusdt", contractType="PERPETUAL", interval="4h", limit=100)
    __print_obj(resp)
    
    # Index Price Kline/Candlestick Data
    resp = restapi.get_index_price_klines(pair="btcusdt", interval="4h", limit=100)
    __print_obj(resp)
    
    # Mark Price Kline/Candlestick Data
    resp = restapi.get_mark_price_klines(symbol="btcusdt", interval="4h")
    __print_obj(resp)
    
    # Mark Price
    resp = restapi.get_mark_price()
    __print_obj(resp)
    
    # Get Funding Rate History
    resp = restapi.get_funding_rate()
    __print_obj(resp)
    
    # 24hr Ticker Price Change Statistics
    resp = restapi.get_ticker_24hr()
    __print_obj(resp)
    
    #Symbol Price Ticker
    resp = restapi.get_ticker_price()
    __print_obj(resp)
    
    # Symbol Order Book Ticker
    resp = restapi.get_book_ticker()
    __print_obj(resp)
    
    # Open Interest
    resp = restapi.get_open_interest(symbol="btcusdt")
    __print_obj(resp)
    
    # Open Interest Statistics
    resp = restapi.get_open_interest_hist(symbol="btcusdt", period="4h", limit=30)
    __print_obj(resp)
    
    # Top Trader Long/Short Ratio (Accounts)
    resp = restapi.get_top_long_short_account_ratio(symbol="btcusdt", period="4h", limit=30)
    __print_obj(resp)
    
    # Top Trader Long/Short Ratio (Positions)
    resp = restapi.get_top_long_short_position_ratio(symbol="btcusdt", period="4h", limit=30)
    __print_obj(resp)
    
    # Long/Short Ratio
    resp = restapi.get_global_long_short_account_ratio(symbol="btcusdt", period="4h", limit=30)
    __print_obj(resp)
    
    # Taker Buy/Sell Volume
    resp = restapi.get_taker_long_short_ratio(symbol="btcusdt", period="4h", limit=30)
    __print_obj(resp)
    
    # Historical BLVT NAV Kline/Candlestick
    resp = restapi.get_lvt_klines(symbol="BTCDOWN", interval="4h", limit=300)
    __print_obj(resp)
    
    # Composite Index Symbol Information
    resp = restapi.get_index_info()
    __print_obj(resp)
    
    # Multi-Assets Mode Asset Index
    resp = restapi.get_asset_index()
    __print_obj(resp)

Websocket<user data> Example
-------------
An almost finished code example to subscribe user data, enjoy it.

.. code:: python

    import time
    from binex_f import Dict2Class, RestApi, WsSubscription, start_thread
    
    class _UserData:
        def __init__(self):
            self.restapi = RestApi(api_key="****************", secret_key="****************")
            self.__ws_subscription = WsSubscription()
            self.channel_id = None
    
        def get_listenKey(self):
            resp = self.restapi.start_user_data_stream()
            if resp.hasattr("listenKey"):
                return resp.listenKey
            return None
    
        def subscribe(self, listenKey):
            self.channel_id = self.__ws_subscription.unsubscribe(self.channel_id).\
                                        subscribe_user_data(listenKey, payload_handler, error_handler)

    __user_data = _UserData()

    def __subscribe_user_data():
        try:
            listenKey = __user_data.get_listenKey()
            if listenKey:
                __user_data.subscribe(listenKey)
                return True
        except Exception as e:
            print (str(e))
        return False
    
    def payload_handler(payload):
        if "ORDER_TRADE_UPDATE" == payload.eventType:
            pass
        elif "listenKeyExpired" == payload.eventType:
            start_thread(__subscribe_user_data, [])
        elif "MARGIN_CALL" == payload.eventType:
            pass
        elif "ACCOUNT_UPDATE" == payload.eventType:
            pass
        elif "ORDER_TRADE_UPDATE" == payload.eventType:
            pass
        elif "ACCOUNT_CONFIG_UPDATE" == payload.eventType:
            pass
        print (Dict2Class.to_val(payload))
    
    def error_handler(err_msg: 'Dict2Class'):
        print (err_msg.asstr())
    
    def __listenKey_watch(restapi):
        while True:
            time.sleep(2_400)
            resp = restapi.keep_user_data_stream()
    
    if __name__ == "__main__":
        if __subscribe_user_data():
            start_thread(__listenKey_watch, [__user_data.restapi])

Websocket<market> Example
-------------

.. code:: python

    from binex_f import Dict2Class, WsSubscription, start_thread

    ws = WsSubscription()
    def f01(pl, el):
        # Aggregate Trade Streams
        ws.subscribe_aggregate_trade(symbol="btcusdt", payload_handler=pl, error_handler=el)
    
    def f02(pl, el):
        # Mark Price Stream
        ws.subscribe_mark_price(symbol="btcusdt", update_time=None, payload_handler=pl, error_handler=el)
    
    def f03(pl, el):
        # Mark Price Stream for All market
        ws.subscribe_all_mark_price(update_time=None, payload_handler=pl, error_handler=el)
    
    def f04(pl, el):
        # Continuous Contract Kline/Candlestick Streams
        ws.subscribe_continuous_kline(pair="btcusdt", contract_type="perpetual", interval="4h", payload_handler=pl, error_handler=el)
    
    def f05(pl, el):
        # Kline/Candlestick Streams
        ws.subscribe_kline(symbol="btcusdt", interval="4h", payload_handler=pl, error_handler=el)
    
    def f06(pl, el):
        # Individual Symbol Mini Ticker Stream
        ws.subscribe_symbol_miniticker(symbol="btcusdt", payload_handler=pl, error_handler=el)
    
    def f07(pl, el):
        # All Market Mini Tickers Stream
        ws.subscribe_all_miniticker(payload_handler=pl, error_handler=el)
    
    def f08(pl, el):
        # Individual Symbol Ticker Streams
        ws.subscribe_symbol_ticker(symbol="btcusdt", payload_handler=pl, error_handler=el)
    
    def f09(pl, el):
        # All Market Tickers Streams
        ws.subscribe_all_ticker(payload_handler=pl, error_handler=el)
    
    def f10(pl, el):
        # Individual Symbol Book Ticker Streams
        ws.subscribe_symbol_bookticker(symbol="btcusdt", payload_handler=pl, error_handler=el)
    
    def f11(pl, el):
        # All Book Tickers Stream
        ws.subscribe_all_bookticker(payload_handler=pl, error_handler=el)
    
    def f12(pl, el):
        # Liquidation Order Streams
        ws.subscribe_symbol_liquidation(symbol="btcusdt", payload_handler=pl, error_handler=el)
    
    def f13(pl, el):
        # All Market Liquidation Order Streams
        ws.subscribe_all_liquidation(payload_handler=pl, error_handler=el)
    
    def f14(pl, el):
        # Partial Book Depth Streams
        ws.subscribe_book_depth(symbol_list=["btcusdt", "ethusdt"], limit=5, update_time="@100ms", payload_handler=pl, error_handler=el)
    
    def f15(pl, el):
        # Diff. Book Depth Streams
        ws.subscribe_diff_book_depth(symbol_list=["btcusdt", "ethusdt"], update_time="@100ms", payload_handler=pl, error_handler=el)
    
    def f16(pl, el):
        # BLVT Info Streams
        ws.subscribe_nav(tokenName="TRXDOWN", payload_handler=pl, error_handler=el)
    
    def f17(pl, el):
        # BLVT NAV Kline/Candlestick Streams
        ws.subscribe_nav_kline(tokenName="TRXDOWN", interval="4h", payload_handler=pl, error_handler=el)
    
    def f18(pl, el):
        # Composite Index Symbol Information Streams
        ws.subscribe_composite_index(symbol="btcusdt", payload_handler=pl, error_handler=el)
    
    def __payload_handler(payload: 'Dict2Class'):
        print (Dict2Class.to_val(payload))
    
    def __error_handler(err_msg: 'Dict2Class'):
        print (err_msg.asstr())

    start_thread(f01, [__payload_handler, __error_handler])


Bash Show
-------------

.. code:: bash

    Python 3.8.8 (default, Apr 13 2021, 19:58:26)
    [GCC 7.3.0] :: Anaconda, Inc. on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from binex_f import RestApi
    >>> restapi = RestApi()
    >>> restapi.ping().asdict()
    {'limits': {}}
    >>> restapi.get_servertime()
    <binex_f.utils.Dict2Class object at 0x7f43a355a070>
    >>> restapi.get_servertime().asdict()
    {'serverTime': 1639041680361, 'limits': {'X-MBX-USED-WEIGHT-1M': '2'}}
    >>> restapi.get_servertime().serverTime
    1639041691379
    >>> exc = restapi.get_exchange_info()
    >>> print (len(exc.symbols))
    145
    >>> print (exc.symbols[0])
    <binex_f.utils.Dict2Class object at 0x7f43a34fc8e0>
    >>> print (exc.symbols[0].asdict())
    {'symbol': 'BTCUSDT', 'pair': 'BTCUSDT', 'contractType': 'PERPETUAL', 'deliveryDate': 4133404800000, 'onboardDate': 1569398400000, 'status': 'TRADING', 'maintMarginPercent': '2.5000', 'requiredMarginPercent': '5.0000', 'baseAsset': 'BTC', 'quoteAsset': 'USDT', 'marginAsset': 'USDT', 'pricePrecision': 2, 'quantityPrecision': 3, 'baseAssetPrecision': 8, 'quotePrecision': 8, 'underlyingType': 'COIN', 'underlyingSubType': [], 'settlePlan': 0, 'triggerProtect': '0.0500', 'liquidationFee': '0.012000', 'marketTakeBound': '0.05', 'filters': [{'minPrice': '556.72', 'maxPrice': '4529764', 'filterType': 'PRICE_FILTER', 'tickSize': '0.01'}, {'stepSize': '0.001', 'filterType': 'LOT_SIZE', 'maxQty': '1000', 'minQty': '0.001'}, {'stepSize': '0.001', 'filterType': 'MARKET_LOT_SIZE', 'maxQty': '120', 'minQty': '0.001'}, {'limit': 200, 'filterType': 'MAX_NUM_ORDERS'}, {'limit': 10, 'filterType': 'MAX_NUM_ALGO_ORDERS'}, {'notional': '5', 'filterType': 'MIN_NOTIONAL'}, {'multiplierDown': '0.9500', 'multiplierUp': '1.0500', 'multiplierDecimal': '4', 'filterType': 'PERCENT_PRICE'}], 'orderTypes': ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET'], 'timeInForce': ['GTC', 'IOC', 'FOK', 'GTX']}

Other examples
---------------

See example/
