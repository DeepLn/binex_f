# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

import time
from binex_f import Dict2Class, RestApi, random_order_id

restapi = RestApi(api_key="****************", secret_key="****************")

def __print_obj(resp)
    print (Dict2Class.to_val(resp))
    time.sleep(0.5)

# New Order (TRADE)
# _type	                        Additional mandatory parameters
# -------------------------------------------------------------
# LIMIT	                             timeInForce, quantity, price
# MARKET	                     quantity
# STOP/TAKE_PROFIT	             quantity, price, stopPrice
# STOP_MARKET/TAKE_PROFIT_MARKET     stopPrice
# TRAILING_STOP_MARKET	             callbackRate
# resp = restapi.post_order(symbol, side, _type, quantity=None, \
#                  positionSide=None, reduceOnly=None, price=None, newClientOrderId=None, \
#                          stopPrice=None, closePosition=None, activationPrice=None, callbackRate=None, \
#                              timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None, test=False)
newClientOrderId = random_order_id()
resp = restapi.post_order(symbol="btcusdt", side="BUY", _type="LIMIT", quantity=0.001, price=50001.1, timeInForce="GTC", newClientOrderId=newClientOrderId)
__print_obj(resp)

# New Order for test
# _type	                        Additional mandatory parameters
# -------------------------------------------------------------
# LIMIT	                             timeInForce, quantity, price
# MARKET	                     quantity
# STOP/TAKE_PROFIT	             quantity, price, stopPrice
# STOP_MARKET/TAKE_PROFIT_MARKET     stopPrice
# TRAILING_STOP_MARKET	             callbackRate
# resp = restapi.post_order_test(symbol, side, _type, quantity=None, \
#                  positionSide=None, reduceOnly=None, price=None, newClientOrderId=None, \
#                          stopPrice=None, closePosition=None, activationPrice=None, callbackRate=None, \
#                              timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None)
resp = restapi.post_order_test(symbol="btcusdt", side="BUY", _type="LIMIT", quantity=0.001, price=50001.1, timeInForce="GTC")
__print_obj(resp)

# Place Multiple Orders (TRADE)
# resp = restapi.post_batch_orders(batchOrders: 'list')
resp = restapi.post_batch_orders(batchOrders=[{"symbol": "btcusdt",
                                               "side": "BUY",
                                               "_type": "LIMIT",
                                               "quantity": 0.001,
                                               "price": 50001.1,
                                               "timeInForce": "GTC"}, {"symbol": "btcusdt",
                                                                    "side": "BUY",
                                                                    "_type": "LIMIT",
                                                                    "quantity": 0.001,
                                                                    "price": 50001.1,
                                                                    "timeInForce": "GTC"
                                                                    }])
__print_obj(resp)

# Query Order (USER_DATA)
# Either orderId or origClientOrderId must be sent.
# resp = restapi.get_order(symbol, orderId=None, origClientOrderId=None)
resp = restapi.get_order(symbol="btcusdt", orderId=139879823454)
__print_obj(resp)

# Cancel Order (TRADE)
# Either orderId or origClientOrderId must be sent.
# resp = restapi.cancel_order(symbol, orderId=None, origClientOrderId=None)
resp = restapi.cancel_order(symbol="btcusdt", origClientOrderId=newClientOrderId)
__print_obj(resp)

# Cancel All Open Orders (TRADE)
# resp = restapi.cancel_all_open_orders(symbol)
resp = restapi.cancel_all_open_orders(symbol="btcusdt")
__print_obj(resp)

# Cancel Multiple Orders (TRADE)
# orderIdList: max length 10 e.g. [1234567,2345678]
# origClientOrderIdList: max length 10
# resp = restapi.cancel_batch_orders(orderIdList=None, origClientOrderIdList=None)
resp = restapi.cancel_batch_orders(origClientOrderIdList=["test1", "test2"])
__print_obj(resp)

# Auto-Cancel All Open Orders (TRADE)
# countdownTime: countdown time, 1000 for 1 second. 0 to cancel the timer
# resp = restapi.auto_cancel_all_open_orders(symbol, countdownTime)
resp = restapi.auto_cancel_all_open_orders(symbol="btcusdt", countdownTime=1000)
__print_obj(resp)

# Query Current Open Order (USER_DATA)
# resp = restapi.get_open_order(symbol, orderId=None, origClientOrderId=None)
# EitherorderId or origClientOrderId must be sent
# If the queried order has been filled or cancelled, the error message "Order does not exist" will be returned.
# resp = restapi.get_open_order(symbol, orderId=None, origClientOrderId=None)
resp = restapi.get_open_order(symbol="btcusdt", orderId=[123456789, 123456780])
__print_obj(resp)

# Current All Open Orders (USER_DATA)
# resp = restapi.get_all_open_orders(symbol=None)
resp = restapi.get_all_open_orders()
__print_obj(resp)

# All Orders (USER_DATA)
# If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.
# The query time period must be less then 7 days( default as the recent 7 days).
# limit: Default 500; max 1000.
# resp = restapi.get_all_orders(symbol, orderId=None, startTime=None, endTime=None, limit=None)
resp = restapi.get_all_orders(symbol="btcusdt")
__print_obj(resp)
