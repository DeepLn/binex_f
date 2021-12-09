# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

import _thread, time
from binex_f import Dict2Class, RestApi, WsSubscription
 
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
        """
        subscribe_user_data params:
            @listenKey:       Mandatory
            @payload_handler: Mandatory
            @error_handler:   default None
            @asdict:          True | False, default False, if True passed, payload as a dict to be handled
        """
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
        _thread.start_new_thread(__subscribe_user_data, ())
    elif "MARGIN_CALL" == payload.eventType:
        pass
    elif "ACCOUNT_UPDATE" == payload.eventType:
        pass
    elif "ORDER_TRADE_UPDATE" == payload.eventType:
        pass
    elif "ACCOUNT_CONFIG_UPDATE" == payload.eventType:
        pass
    print (Dict2Class.to_val(payload))

def error_handler(err_msg: 'dict'):
    print (err_msg)

def __listenKey_watch(restapi):
    while True:
        time.sleep(2_400)
        resp = restapi.keep_user_data_stream()

if __name__ == "__main__":
    if __subscribe_user_data():
        _thread.start_new_thread(__listenKey_watch, (__user_data.restapi,))
