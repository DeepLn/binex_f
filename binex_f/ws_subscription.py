# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

import logging
from binex_f.ws.channels import *
from binex_f.ws.ws_connection import WSConnection

class WsSubscription(object):
    def __init__(self):
        self.ws_conns = dict()
        self.logger = logging.getLogger("binex_f")

    def subscribe(self, channel, payload_handler, error_handler):
        ws_conn = WSConnection.create(channel, payload_handler, error_handler)
        channel_id = ws_conn.get_channel_id()
        self.ws_conns.update({channel_id: ws_conn})
        return channel_id

    def unsubscribe(self, channel_id):
        if channel_id:
            if channel_id in self.ws_conns:
                self.ws_conns.pop(self.ws_conns.get(channel_id).close())
            else:
                self.logger.error("unsubscribe: <unrecognized channel id: %s>" % channel_id)
        return self

    def subscribe_aggregate_trade(self, symbol, payload_handler, error_handler=None):
        return self.subscribe(aggregate_trade_channel(symbol), payload_handler, error_handler)

    def subscribe_mark_price(self, symbol, update_time, payload_handler, error_handler=None):
        return self.subscribe(mark_price_channel(symbol, update_time), payload_handler, error_handler)

    def subscribe_all_mark_price(self, update_time, payload_handler, error_handler=None):
        return self.subscribe(all_mark_price_channel(update_time), payload_handler, error_handler)

    def subscribe_continuous_kline(self, pair, contract_type, interval, payload_handler, error_handler=None):
        return self.subscribe(\
                       continuous_kline_channel(pair, contract_type, interval), payload_handler, error_handler)

    def subscribe_kline(self, symbol, interval, payload_handler, error_handler=None):
        return self.subscribe(kline_channel(symbol, interval), payload_handler, error_handler)

    def subscribe_symbol_miniticker(self, symbol, payload_handler, error_handler=None):
        return self.subscribe(symbol_miniticker_channel(symbol), payload_handler, error_handler)

    def subscribe_all_miniticker(self, payload_handler, error_handler=None):
        return self.subscribe(all_miniticker_channel(), payload_handler, error_handler)

    def subscribe_symbol_ticker(self, symbol, payload_handler, error_handler=None):
        return self.subscribe(symbol_ticker_channel(symbol), payload_handler, error_handler)

    def subscribe_all_ticker(self, payload_handler, error_handler=None):
        return self.subscribe(all_ticker_channel(), payload_handler, error_handler)

    def subscribe_symbol_bookticker(self, symbol, payload_handler, error_handler=None):
        return self.subscribe(symbol_bookticker_channel(symbol), payload_handler, error_handler)

    def subscribe_all_bookticker(self, payload_handler, error_handler=None):
        return self.subscribe(all_bookticker_channel(), payload_handler, error_handler)

    def subscribe_symbol_liquidation(self, symbol, payload_handler, error_handler=None):
        return self.subscribe(symbol_liquidation_channel(symbol), payload_handler, error_handler)

    def subscribe_all_liquidation(self, payload_handler, error_handler=None):
        return self.subscribe(all_liquidation_channel(), payload_handler, error_handler)

    def subscribe_book_depth(self, symbol_list, limit, update_time, payload_handler, error_handler=None):
        return self.subscribe(book_depth_channel(symbol_list, limit, update_time), payload_handler, error_handler)

    def subscribe_diff_book_depth(self, symbol_list, update_time, payload_handler, error_handler=None):
        return self.subscribe(diff_book_depth_channel(symbol_list, update_time), payload_handler, error_handler)

    def subscribe_nav(self, tokenName, payload_handler, error_handler=None):
        return self.subscribe(nav_channel(tokenName), payload_handler, error_handler)

    def subscribe_nav_kline(self, tokenName, interval, payload_handler, error_handler=None):
        return self.subscribe(nav_kline_channel(tokenName, interval), payload_handler, error_handler)

    def subscribe_composite_index(self, symbol, payload_handler, error_handler=None):
        return self.subscribe(composite_index_channel(symbol), payload_handler, error_handler)

    def subscribe_user_data(self, listenKey, payload_handler, error_handler=None):
        return self.subscribe(user_data_channel(listenKey), payload_handler, error_handler)
