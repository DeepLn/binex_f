# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

import base64, hashlib, hmac, json, requests, urllib.parse
from binex_f import const
from binex_f.utils import Dict2Class, check_filled, current_timestamp

class _RespObj:
    @staticmethod
    def loads(resp, limits):
        obj = Dict2Class.from_str(resp)
        if isinstance(obj, Dict2Class):
            return obj.setattr("limits", limits)
        elif isinstance(obj, list):
            return obj
        raise Exception("invalid response: %s" % resp)

__limits_headers = ["X-MBX-USED-WEIGHT-", "X-MBX-ORDER-COUNT-"]
def __get_limits_usage(response):
    limits = dict()
    for key, value in response.headers.items():
        if any([key.startswith(h) for h in __limits_headers]):
            limits[key] = value
    return limits

def create_signature(secret_key, mapping):
    mapping["signature"] = hmac.new(secret_key.encode(), \
            msg=urllib.parse.urlencode(mapping).encode(), digestmod=hashlib.sha256).hexdigest()
    return mapping

def call_sync(request):
    if "GET" == request.method:
        response = requests.get(request.host + request.url, headers=request.header)
        return response.text, __get_limits_usage(response)
    elif "POST" == request.method:
        response = requests.post(request.host + request.url, headers=request.header)
        return response.text, __get_limits_usage(response)
    elif "DELETE" == request.method:
        response = requests.delete(request.host + request.url, headers=request.header)
        return response.text, __get_limits_usage(response)
    elif "PUT" == request.method:
        response = requests.put(request.host + request.url, headers=request.header)
        return response.text, __get_limits_usage(response)
    raise Exception("invalid request method: %s" % request.method)

class RestApi:
    uri = "https://fapi.binance.com"

    def __init__(self, api_key=None, secret_key=None):
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__diff_time = 1_000 + current_timestamp() - self.get_servertime().serverTime

    def __create_request_by_get(self, url, mapping=None):
        return Dict2Class({
            "method": "GET",
            "host":   RestApi.uri,
            "header": {"Content-Type": "application/json"},
            "url": "%s?%s" % (url, urllib.parse.urlencode(mapping if mapping else dict()))
            }, recursion=False)

    def __create_request_by_get_with_apikey(self, url, mapping=None):
        return Dict2Class({
            "method": "GET",
            "host":   RestApi.uri,
            "header": {
                "Content-Type": "application/json",
                "X-MBX-APIKEY": self.__api_key},
            "url": "%s?%s" % (url, urllib.parse.urlencode(mapping if mapping else dict()))
            }, recursion=False)

    def __create_request_by_post_with_signature(self, url, mapping=None):
        if not mapping:
            mapping = dict()
        mapping.update({
                "recvWindow": 60_000,
                "timestamp": str(current_timestamp() - self.__diff_time)
            })
        mapping = create_signature(self.__secret_key, mapping)
        return Dict2Class({
            "method": "POST",
            "host":   RestApi.uri,
            "header": {
                "Content-Type": "application/json",
                "X-MBX-APIKEY": self.__api_key},
            "post_body": {},
            "url": "%s?%s" % (url, urllib.parse.urlencode(mapping))
            }, recursion=False)

    def __create_request_by_delete_with_signature(self, url, mapping=None):
        if not mapping:
            mapping = dict()
        mapping.update({
                "recvWindow": 60_000,
                "timestamp": str(current_timestamp() - self.__diff_time)
            })
        mapping = create_signature(self.__secret_key, mapping)
        return Dict2Class({
            "method": "DELETE",
            "host":   RestApi.uri,
            "header": {
                "Content-Type": "application/json",
                "X-MBX-APIKEY": self.__api_key},
            "url": "%s?%s" % (url, urllib.parse.urlencode(mapping))
            }, recursion=False)

    def __create_request_by_get_with_signature(self, url, mapping=None):
        if not mapping:
            mapping = dict()
        mapping.update({
                "recvWindow": 60_000,
                "timestamp": str(current_timestamp() - self.__diff_time)
            })
        mapping = create_signature(self.__secret_key, mapping)
        return Dict2Class({
            "method": "GET",
            "host":   RestApi.uri,
            "header": {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-MBX-APIKEY": self.__api_key},
            "url": "%s?%s" % (url, urllib.parse.urlencode(mapping))
            }, recursion=False)

    def __create_request_by_put_with_signature(self, url, mapping=None):
        if not mapping:
            mapping = dict()
        mapping.update({
                "recvWindow": 60_000,
                "timestamp": str(current_timestamp() - self.__diff_time)
            })
        mapping = create_signature(self.__secret_key, mapping)
        return Dict2Class({
            "method": "PUT",
            "host":   RestApi.uri,
            "header": {
                "Content-Type": "application/json",
                "X-MBX-APIKEY": self.__api_key},
            "url": "%s?%s" % (url, urllib.parse.urlencode(mapping))
            }, recursion=False)

    def __mandatory(self, params: 'dict', mapping=None):
        if not mapping:
            mapping = dict()
        for k, v in params.items():
            check_filled(k, v)
        mapping.update(params)
        return mapping

    def __check_order_params(self, params: 'Dict2Class'):
        mapping = self.__mandatory({"symbol": params.symbol, "side": params.side, "type": params._type})
        if "LIMIT" == params._type:
            mapping = self.__mandatory({"price": params.price, "quantity": params.quantity, "timeInForce": params.timeInForce}, mapping)
        elif "MARKET" == params._type:
            mapping = self.__mandatory({"quantity": params.quantity}, mapping)
        elif "STOP" == params._type or "TAKE_PROFIT" == params._type:
            mapping = self.__mandatory({"price": params.price, "quantity": params.quantity, "stopPrice": params.stopPrice}, mapping)
        elif "STOP_MARKET" == params._type or "TAKE_PROFIT_MARKET" == params._type:
            mapping = self.__mandatory({"quantity": params.quantity}, mapping)
        elif "TRAILING_STOP_MARKET" == params._type:
            mapping = self.__mandatory({"callbackRate": params.callbackRate}, mapping)
        for k, v in params.asdict().items():
            if v and k not in mapping:
                mapping.update({k: v})
        return mapping

    def ping(self):
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/ping"))
        return _RespObj.loads(response, limits)

    def get_servertime(self):
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/time"))
        return _RespObj.loads(response, limits)

    def get_exchange_info(self):
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/exchangeInfo"))
        return _RespObj.loads(response, limits)

    def get_book_depth(self, symbol, limit=None):
        def convert(response):
            _r = json.loads(response)
            return {
                    "lastUpdatedId":   _r.get("lastUpdatedId"),
                    "eventTime":       _r.get("E"),
                    "transactionTime": _r.get("T"),
                    "bids": [{"price": ele[0], "qty": ele[1]} for ele in _r.get("bids")],
                    "asks": [{"price": ele[0], "qty": ele[1]} for ele in _r.get("asks")]
                }
        mapping = self.__mandatory({"symbol": symbol})
        if limit:
            if limit not in const.DEPTH:
                raise Exception("limit<%s> not in %s" % (limit, const.DEPTH))
            mapping.update({"limit": limit})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/depth", mapping))
        return _RespObj.loads(convert(response), limits)

    def get_recent_trades(self, symbol, limit=None):
        mapping = self.__mandatory({"symbol": symbol})
        if limit:
            if 1 > limit or limit > 1000:
                raise Exception("invalid limit<%s>, should be a number in (0, 1000])" % limit)
            mapping.update({"limit": limit})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/trades", mapping))
        return _RespObj.loads(response, limits)

    def get_historical_trades(self, symbol, limit=None, fromId=None):
        mapping = self.__mandatory({"symbol": symbol})
        if limit:
            if 1 > limit or limit > 1000:
                raise Exception("invalid limit<%s>, should be a number in (0, 1000])" % limit)
            mapping.update({"limit": limit})
        if fromId:
            mapping.update({"fromId": fromId})
        response, limits = call_sync(self.__create_request_by_get_with_apikey("/fapi/v1/historicalTrades", mapping))
        return _RespObj.loads(response, limits)

    def get_aggregate_trades(self, symbol, fromId=None, startTime=None, endTime=None, limit=None):
        def convert(response: 'str'):
            _l = list()
            for ele in json.loads(response):
                _l.append({
                    "tradeId":      ele.get("a"),
                    "price":        ele.get("p"),
                    "qty":          ele.get("q"),
                    "firstTradeId": ele.get("f"),
                    "lastTradeId":  ele.get("l"),
                    "timestamp":    ele.get("T"),
                    "isMaker":      ele.get("m")
                    })
            return _l
        mapping = self.__mandatory({"symbol": symbol})
        if limit:
            if 1 > limit or limit > 1000:
                raise Exception("invalid limit<%s>, should be a number in (0, 1000])" % limit)
            mapping.update({"limit": limit})
        if fromId:
            mapping.update({"fromId": fromId})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        if startTime and endTime:
            if endTime - startTime < (60 * 60 * 1_000):
                raise Exception("time between startTime and endTime must be less than 1 hour")
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/aggTrades", mapping))
        return _RespObj.loads(convert(response), limits)

    def get_klines(self, symbol, interval, startTime=None, endTime=None, limit=None):
        def convert(response: 'str'):
            _l = list()
            for ele in json.loads(response):
                _l.append({
                    "openTime":                 ele[0],
                    "open":                     ele[1],
                    "high":                     ele[2],
                    "low":                      ele[3],
                    "close":                    ele[4],
                    "volume":                   ele[5],
                    "closeTime":                ele[6],
                    "quoteAssetVolume":         ele[7],
                    "numOfTrades":              ele[8],
                    "takerBuyBaseAssetVolume":  ele[9],
                    "takerBuyQuoteAssetVolume": ele[10]
                    })
            return _l
        mapping = self.__mandatory({"symbol": symbol, "interval": interval})
        if interval not in const.KLINE_INTERVAL:
            raise Exception("interval<%s> not in %s" % (interval, const.KLINE_INTERVAL))
        if limit:
            if 1 > limit or limit > 1500:
                raise Exception("invalid limit<%s>, should be a number in (0, 1500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/klines", mapping))
        return _RespObj.loads(convert(response), limits)

    def get_continuous_klines(self, pair, contractType, interval, startTime=None, endTime=None, limit=None):
        def convert(response: 'str'):
            _l = list()
            for ele in json.loads(response):
                _l.append({
                    "openTime":                 ele[0],
                    "open":                     ele[1],
                    "high":                     ele[2],
                    "low":                      ele[3],
                    "closeOrLatestPrice":       ele[4],
                    "volume":                   ele[5],
                    "closeTime":                ele[6],
                    "quoteAssetVolume":         ele[7],
                    "numOfTrades":              ele[8],
                    "takerBuyVolume":           ele[9],
                    "takerBuyQuoteAssetVolume": ele[10]
                    })
            return _l
        mapping = self.__mandatory({"pair": pair, "contractType": contractType, "interval": interval})
        if contractType not in const.CONTRACT_TYPE:
            raise Exception("contractType<%s> not in %s" % (contractType, const.CONTRACT_TYPE))
        if interval not in const.KLINE_INTERVAL:
            raise Exception("interval<%s> not in %s" % (interval, const.KLINE_INTERVAL))
        if limit:
            if 1 > limit or limit > 1500:
                raise Exception("invalid limit<%s>, should be a number in (0, 1500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/continuousKlines", mapping))
        return _RespObj.loads(convert(response), limits)

    def get_index_price_klines(self, pair, interval, startTime=None, endTime=None, limit=None):
        def convert(response: 'str'):
            _l = list()
            for ele in json.loads(response):
                _l.append({
                    "openTime":                 ele[0],
                    "open":                     ele[1],
                    "high":                     ele[2],
                    "low":                      ele[3],
                    "closeOrLatestPrice":       ele[4],
                    "closeTime":                ele[6],
                    "numOfBasicData":           ele[8]
                    })
            return _l
        mapping = self.__mandatory({"pair": pair, "interval": interval})
        if interval not in const.KLINE_INTERVAL:
            raise Exception("interval<%s> not in %s" % (interval, const.KLINE_INTERVAL))
        if limit:
            if 1 > limit or limit > 1500:
                raise Exception("invalid limit<%s>, should be a number in (0, 1500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/indexPriceKlines", mapping))
        return _RespObj.loads(convert(response), limits)

    def get_mark_price_klines(self, symbol, interval, startTime=None, endTime=None, limit=None):
        def convert(response: 'str'):
            _l = list()
            for ele in json.loads(response):
                _l.append({
                    "openTime":                 ele[0],
                    "open":                     ele[1],
                    "high":                     ele[2],
                    "low":                      ele[3],
                    "closeOrLatestPrice":       ele[4],
                    "closeTime":                ele[6],
                    "numOfBasicData":           ele[8]
                    })
            return _l
        mapping = self.__mandatory({"symbol": symbol, "interval": interval})
        if interval not in const.KLINE_INTERVAL:
            raise Exception("interval<%s> not in %s" % (interval, const.KLINE_INTERVAL))
        if limit:
            if 1 > limit or limit > 1500:
                raise Exception("invalid limit<%s>, should be a number in (0, 1500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/markPriceKlines", mapping))
        return _RespObj.loads(convert(response), limits)

    def get_mark_price(self, symbol=None):
        mapping = dict()
        if symbol:
            mapping.update({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/premiumIndex", mapping))
        return _RespObj.loads(response, limits)

    def get_funding_rate(self, symbol=None, startTime=None, endTime=None, limit=None):
        mapping = dict()
        if symbol:
            mapping.update({"symbol": symbol})
        if limit:
            if 1 > limit or limit > 1000:
                raise Exception("invalid limit<%s>, should be a number in (0, 1000])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/fundingRate", mapping))
        return _RespObj.loads(response, limits)

    def get_ticker_24hr(self, symbol=None):
        mapping = dict()
        if symbol:
            mapping.update({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/ticker/24hr", mapping))
        return _RespObj.loads(response, limits)

    def get_ticker_price(self, symbol=None):
        mapping = dict()
        if symbol:
            mapping.update({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/ticker/price", mapping))
        return _RespObj.loads(response, limits)

    def get_book_ticker(self, symbol=None):
        mapping = dict()
        if symbol:
            mapping.update({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/ticker/bookTicker", mapping))
        return _RespObj.loads(response, limits)

    def get_open_interest(self, symbol):
        mapping = self.__mandatory({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/openInterest", mapping))
        return _RespObj.loads(response, limits)

    def get_open_interest_hist(self, symbol, period, startTime=None, endTime=None, limit=None):
        mapping = self.__mandatory({"symbol": symbol, "period": period})
        if period not in const.PERIOD:
            raise Exception("period<%s> not in %s" % (period, const.PERIOD))
        if limit:
            if 1 > limit or limit > 500:
                raise Exception("invalid limit<%s>, should be a number in (0, 500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/futures/data/openInterestHist", mapping))
        return _RespObj.loads(response, limits)

    def get_top_long_short_account_ratio(self, symbol, period, startTime=None, endTime=None, limit=None):
        mapping = self.__mandatory({"symbol": symbol, "period": period})
        if period not in const.PERIOD:
            raise Exception("period<%s> not in %s" % (period, const.PERIOD))
        if limit:
            if 1 > limit or limit > 500:
                raise Exception("invalid limit<%s>, should be a number in (0, 500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/futures/data/topLongShortAccountRatio", mapping))
        return _RespObj.loads(response, limits)

    def get_top_long_short_position_ratio(self, symbol, period, startTime=None, endTime=None, limit=None):
        mapping = self.__mandatory({"symbol": symbol, "period": period})
        if period not in const.PERIOD:
            raise Exception("period<%s> not in %s" % (period, const.PERIOD))
        if limit:
            if 1 > limit or limit > 500:
                raise Exception("invalid limit<%s>, should be a number in (0, 500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/futures/data/topLongShortPositionRatio", mapping))
        return _RespObj.loads(response, limits)

    def get_global_long_short_account_ratio(self, symbol, period, startTime=None, endTime=None, limit=None):
        mapping = self.__mandatory({"symbol": symbol, "period": period})
        if period not in const.PERIOD:
            raise Exception("period<%s> not in %s" % (period, const.PERIOD))
        if limit:
            if 1 > limit or limit > 500:
                raise Exception("invalid limit<%s>, should be a number in (0, 500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/futures/data/globalLongShortAccountRatio", mapping))
        return _RespObj.loads(response, limits)

    def get_taker_long_short_ratio(self, symbol, period, startTime=None, endTime=None, limit=None):
        mapping = self.__mandatory({"symbol": symbol, "period": period})
        if period not in const.PERIOD:
            raise Exception("period<%s> not in %s" % (period, const.PERIOD))
        if limit:
            if 1 > limit or limit > 500:
                raise Exception("invalid limit<%s>, should be a number in (0, 500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/futures/data/takerlongshortRatio", mapping))
        return _RespObj.loads(response, limits)

    def get_lvt_klines(self, symbol, interval, startTime=None, endTime=None, limit=None):
        def convert(response: 'str'):
            _l = list()
            for ele in json.loads(response):
                _l.append({
                    "openTime":                 ele[0],
                    "open":                     ele[1],
                    "high":                     ele[2],
                    "low":                      ele[3],
                    "closeOrLatestPrice":       ele[4],
                    "realLeverage":             ele[5],
                    "closeTime":                ele[6],
                    "numOfNavUpdate":           ele[8]
                    })
            return _l
        mapping = self.__mandatory({"symbol": symbol, "interval": interval})
        if interval not in const.KLINE_INTERVAL:
            raise Exception("interval<%s> not in %s" % (interval, const.KLINE_INTERVAL))
        if limit:
            if 1 > limit or limit > 500:
                raise Exception("invalid limit<%s>, should be a number in (0, 500])" % limit)
            mapping.update({"limit": limit})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/lvtKlines", mapping))
        return _RespObj.loads(convert(response), limits)

    def get_index_info(self, symbol=None):
        mapping = dict()
        if symbol:
            mapping.update({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/indexInfo", mapping))
        return _RespObj.loads(response, limits)

    def get_asset_index(self, symbol=None):
        mapping = dict()
        if symbol:
            mapping.update({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_get("/fapi/v1/assetIndex", mapping))
        return _RespObj.loads(response, limits)

    def change_position_side_dual(self, dualSidePosition, recvWindow=None):
        mapping = self.__mandatory({"dualSidePosition": dualSidePosition})
        if dualSidePosition not in ["true", "false"]:
            raise Exception("dualSidePosition<%s> not in ['true', 'false']" % dualSidePosition)
        response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/positionSide/dual", mapping))
        return _RespObj.loads(response, limits)

    def check_position_side_dual(self):
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/positionSide/dual"))
        return _RespObj.loads(response, limits)

    def change_multi_assets_margin(self, multiAssetsMargin, recvWindow=None):
        mapping = self.__mandatory({"multiAssetsMargin": multiAssetsMargin})
        if dualSidePosition not in ["true", "false"]:
            raise Exception("multiAssetsMargin<%s> not in ['true', 'false']" % multiAssetsMargin)
        response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/multiAssetsMargin", mapping))
        return _RespObj.loads(response, limits)

    def check_multi_assets_margin(self):
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/multiAssetsMargin"))
        return _RespObj.loads(response, limits)

    def post_order(self, symbol, side, _type, quantity=None, \
                         positionSide=None, reduceOnly=None, price=None, newClientOrderId=None, \
                                 stopPrice=None, closePosition=None, activationPrice=None, callbackRate=None, \
                                     timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None, test=False):
        mapping = self.__check_order_params(Dict2Class({
                "symbol": symbol,
                "side": side,
                "_type": _type,
                "quantity": quantity,
                "positionSide": positionSide,
                "reduceOnly": reduceOnly,
                "price": price,
                "newClientOrderId": newClientOrderId,
                "stopPrice": stopPrice,
                "closePosition": closePosition,
                "activationPrice": activationPrice,
                "callbackRate": callbackRate,
                "timeInForce": timeInForce,
                "workingType": workingType,
                "priceProtect": priceProtect,
                "newOrderRespType": newOrderRespType
            }))
        response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/order/test" if test else "/fapi/v1/order", mapping))
        return _RespObj.loads(response, limits)

    def post_order_test(self, symbol, side, _type, quantity=None, \
                         positionSide=None, reduceOnly=None, price=None, newClientOrderId=None, \
                                 stopPrice=None, closePosition=None, activationPrice=None, callbackRate=None, \
                                     timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None):
        return self.post_order(symbol, side, _type, quantity, \
                          positionSide, reduceOnly, price, newClientOrderId, \
                                  stopPrice, closePosition, activationPrice, callbackRate, \
                                      timeInForce, workingType, priceProtect, newOrderRespType, True)

    def post_batch_orders(self, batchOrders: 'list'):
        orders = Dict2Class.from_val(batchOrders)
        if isinstance(orders, list):
            if 1 > len(orders) or 5 < len(orders):
                raise Exception("max 5 orders supported, %s gived" % len(orders))
            _ = [self.__check_order_filled(ele) for ele in orders]
            mapping = {"batchOrders": batchOrders}
            response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/batchOrders", mapping))
            return _RespObj.loads(response, limits)
        raise Exception("invalid param: batchOrders, should be a list of json format")

    def get_order(self, symbol, orderId=None, origClientOrderId=None):
        if not orderId and not origClientOrderId:
            raise Exception("Either orderId or origClientOrderId must be sent.")
        mapping = self.__mandatory({"symbol": symbol})
        if orderId:
            mapping.update({"orderId": orderId})
        if origClientOrderId:
            mapping.update({"origClientOrderId": origClientOrderId})
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/order", mapping))
        return _RespObj.loads(response, limits)

    def cancel_order(self, symbol, orderId=None, origClientOrderId=None):
        if not orderId and not origClientOrderId:
            raise Exception("Either orderId or origClientOrderId must be sent.")
        mapping = self.__mandatory({"symbol": symbol})
        if orderId:
            mapping.update({"orderId": orderId})
        if origClientOrderId:
            mapping.update({"origClientOrderId": origClientOrderId})
        response, limits = call_sync(self.__create_request_by_delete_with_signature("/fapi/v1/order", mapping))
        return _RespObj.loads(response, limits)

    def cancel_all_open_orders(self, symbol):
        mapping = self.__mandatory({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_delete_with_signature("/fapi/v1/allOpenOrders", mapping))
        return _RespObj.loads(response, limits)

    def cancel_batch_orders(self, orderIdList=None, origClientOrderIdList=None):
        def list_2_str(l):
            if isinstance(l, list):
                if 10 < len(l):
                    raise Exception("max length 10, %s gived" % len(l))
                return json.dumps(l).replace(" ", "")
            elif isinstance(l, str):
                import ast
                return list_2_str(ast.literal_eval(l))
            raise Exception("invalid param: %s" % str(l))
        if not orderIdList and not origClientOrderIdList:
            raise Exception("Either orderIdList or origClientOrderIdList must be sent.")
        mapping = dict()
        if orderIdList:
            mapping.update({"orderIdList": list_2_str(orderIdList)})
        if origClientOrderIdList:
            mapping.update({"origClientOrderIdList": list_2_str(origClientOrderId)})
        response, limits = call_sync(self.__create_request_by_delete_with_signature("/fapi/v1/batchOrders", mapping))
        return _RespObj.loads(response, limits)

    def auto_cancel_all_open_orders(self, symbol, countdownTime):
        mapping = self.__mandatory({"symbol": symbol, "countdownTime": countdownTime})
        response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/countdownCancelAll", mapping))
        return _RespObj.loads(response, limits)

    def get_open_order(self, symbol, orderId=None, origClientOrderId=None):
        if not orderId and not origClientOrderId:
            raise Exception("Either orderId or origClientOrderId must be sent.")
        mapping = self.__mandatory({"symbol": symbol})
        if orderId:
            mapping.update({"orderId": orderId})
        if origClientOrderId:
            mapping.update({"origClientOrderId": origClientOrderId})
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/openOrder", mapping))
        return _RespObj.loads(response, limits)

    def get_all_open_orders(self, symbol=None):
        mapping = {"symbol": symbol} if symbol else dict()
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/openOrders", mapping))
        return _RespObj.loads(response, limits)

    def get_all_orders(self, symbol, orderId=None, startTime=None, endTime=None, limit=None):
        mapping = self.__mandatory({"symbol": symbol})
        if orderId:
            mapping.update({"orderId": orderId})
        if limit:
            if 1 > limit or limit > 1000:
                raise Exception("invalid limit<%s>, should be a number in (0, 1000])" % limit)
            mapping.update({"limit": limit})
        if startTime and endTime:
            if endTime - startTime > (7 * 24 * 60 * 60 * 1_000):
                raise Exception("The query time period must be less then 7 days")
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/allOrders", mapping))
        return _RespObj.loads(response, limits)

    def get_balance(self):
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v2/balance"))
        return _RespObj.loads(response, limits)

    def get_account_information(self):
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v2/accouont"))
        return _RespObj.loads(response, limits)

    def change_initial_leverage(self, symbol, leverage):
        def check_leverage(l):
            if isinstance(l, int):
                if 1 <= l <= 125:
                    return
            raise Exception("target initial leverage: int from 1 to 125")
        mapping = self.__mandatory({"symbol": symbol, "leverage": leverage})
        check_leverage(leverage)
        response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/leverage", mapping))
        return _RespObj.loads(response, limits)

    def change_margin_type(self, symbol, marginType):
        mapping = self.__mandatory({"symbol": symbol, "marginType": marginType})
        if marginType not in ["ISOLATED", "CROSSED"]:
            raise Exception("invalid marginType<%s>, should be in ['ISOLATED', 'CROSSED']")
        response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/marginType", mapping))
        return _RespObj.loads(response, limits)

    def change_position_margin(self, symbol, amount, _type, positionSide=None):
        mapping = self.__mandatory({"symbol": symbol, "amount": amount, "type": _type})
        if not isinstance(_type, int) or _type not in [1, 2]:
            raise Exception("invalid _type<%s>, should be in [1,2]" % _type)
        if positionSide:
            if positionSide not in ["BOTH", "LONG", "SHORT"]:
                raise Exception("invalid positionSide<%s>, should be in ['BOTH', 'LONG', 'SHORT']" % positionSide)
            mapping.update({"positionSide": positionSide})
        response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/positionMargin", mapping))
        return _RespObj.loads(response, limits)

    def get_position_margin_change_history(self, symbol, _type=None, startTime=None, endTime=None, limit=None):
        mapping = self.__mandatory({"symbol": symbol})
        if _type:
            if not isinstance(_type, int) or _type not in [1, 2]:
                raise Exception("invalid _type<%s>, should be in [1,2]" % _type)
            mapping.update({"type": _type})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        if limit:
            mapping.update({"limit": limit})
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/positionMargin/history", mapping))
        return _RespObj.loads(response, limits)

    def get_position_information(self, symbol=None):
        mapping = {"symbol": symbol} if symbol else dict()
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/positionRisk", mapping))
        return _RespObj.loads(response, limits)

    def get_account_trades(self, symbol, startTime=None, endTime=None, fromId=None, limit=None):
        mapping = self.__mandatory({"symbol": symbol})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        if fromId:
            mapping.update({"fromId": fromId})
        if limit:
            if 1 > limit or limit > 1000:
                raise Exception("invalid limit<%s>, should be a number in (0, 1000])" % limit)
            mapping.update({"limit": limit})
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/userTrades", mapping))
        return _RespObj.loads(response, limits)

    def get_income_history(self, symbol=None, incomeType=None, startTime=None, endTime=None, limit=None):
        mapping = dict()
        if symbol:
            mapping.update({"symbol": symbol})
        if incomeType:
            if incomeType not in const.INCOME_TYPE:
                raise Exception("invalid incomeType: %s" % incomeType)
            mapping.update({"incomeType": incomeType})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        if limit:
            if 1 > limit or limit > 1000:
                raise Exception("invalid limit<%s>, should be a number in (0, 1000])" % limit)
            mapping.update({"limit": limit})
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/income", mapping))
        return _RespObj.loads(response, limits)

    def get_leverage_bracket(self, symbol=None):
        mapping = {"symbol": symbol} if symbol else dict()
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/leverageBracket", mapping))
        return _RespObj.loads(response, limits)

    def get_adl_quantile(self, symbol=None):
        mapping = {"symbol": symbol} if symbol else dict()
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/adlQuantile", mapping))
        return _RespObj.loads(response, limits)

    def get_force_orders(self, symbol=None, autoCloseType=None, startTime=None, endTime=None, limit=None):
        mapping = {"symbol": symbol} if symbol else dict()
        if autoCloseType:
            if autoCloseType not in ["LIQUIDATION", "ADL"]:
                raise Exception("invalid autoCloseType<%s>, should be in ['LIQUIDATION', 'ADL']" % autoCloseType)
            mapping.update({"autoCloseType": autoCloseType})
        if startTime:
            mapping.update({"startTime": startTime})
        if endTime:
            mapping.update({"endTime": endTime})
        if limit:
            if 1 > limit or limit > 100:
                raise Exception("invalid limit<%s>, should be a number in (0, 100])" % limit)
            mapping.update({"limit": limit})
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/forceOrders", mapping))
        return _RespObj.loads(response, limits)

    def get_api_trading_stats(self, symbol=None):
        mapping = {"symbol": symbol} if symbol else dict()
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/apiTradingStatus", mapping))
        return _RespObj.loads(response, limits)

    def get_commission_rate(self, symbol):
        mapping = self.__mandatory({"symbol": symbol})
        response, limits = call_sync(self.__create_request_by_get_with_signature("/fapi/v1/commissionRate", mapping))
        return _RespObj.loads(response, limits)

    def start_user_data_stream(self):
        response, limits = call_sync(self.__create_request_by_post_with_signature("/fapi/v1/listenKey"))
        return _RespObj.loads(response, limits)

    def keep_user_data_stream(self):
        response, limits = call_sync(self.__create_request_by_put_with_signature("/fapi/v1/listenKey"))
        return _RespObj.loads(response, limits)

    def close_user_data_stream(self):
        response, limits = call_sync(self.__create_request_by_delete_with_signature("/fapi/v1/listenKey"))
        return _RespObj.loads(response, limits)
