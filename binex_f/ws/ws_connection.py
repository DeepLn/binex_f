# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

import _thread, json, logging, threading, time, websocket
from binex_f.utils import Dict2Class, current_timestamp

class _ConnectionState:
    IDLE      = 0
    CONNECTED = 1

def on_open(ws):
    WSConnection.ws_conn_handler[ws].on_open()

def on_message(ws, message):
    WSConnection.ws_conn_handler[ws].on_message(message)

def on_error(ws, error):
    WSConnection.ws_conn_handler[ws].on_error(error)

def on_close(ws, close_status_code, close_msg):
    WSConnection.ws_conn_handler[ws].on_close(close_status_code, close_msg)

def ws_func(ws_conn):
    ws = websocket.WebSocketApp(WSConnection.uri,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    WSConnection.ws_conn_handler[ws] = ws_conn.set_ws(ws)
    ws.run_forever()

def watch_dog_job(ws_conn):
    while ws_conn.suspend:
        time.sleep(1)
        ws_conn.re_connect()
    ws_conn.re_connect()

class WSConnection:
    ws_conn_handler = dict()
    uri = "wss://fstream.binance.com/ws"

    def __init__(self, channel):
        self.suspend = True
        self.__reset().set_ws(None).set_handlers(None, None).__set_channel(channel)
        self.__watch_dog_thread = threading.Thread(target=watch_dog_job, args=[self])
        self.__watch_dog_thread.start()
        self.logger = logging.getLogger("bin_f")

    def __reset(self):
        self.__channel_subscribed = False
        self.__receive_at = self.__connect_at = current_timestamp()
        self.state = _ConnectionState.IDLE
        return self

    def set_ws(self, ws):
        self.ws = ws
        return self

    def set_handlers(self, payload_handler, error_handler):
        self.__payload_handler = payload_handler
        self.__error_handler = error_handler
        return self

    def __handle_error(self, msg_type: 'str', msg: 'str'):
        if self.__error_handler:
            self.__error_handler({"type": msg_type, "msg": msg})
        else:
            if "warning" == msg_type:
                self.logger.warning(msg)
            elif "error" == msg_type:
                self.logger.error(msg)
            elif "critical" == msg_type:
                self.logger.critical(msg)

    def __set_channel(self, channel):
        self.__channel, self.__payload_match = channel
        return self

    def get_channel_id(self):
        return self.__channel.get("id")

    def __subscribe(self):
        sub = json.dumps(self.__channel)
        self.logger.info("ws_conn<%s> subscribe: %s" % (self.get_channel_id(), sub))
        try:
            self.ws.send(sub)
        except Exception as e:
            self.__handle_error("error", str(e))

    def __close(self):
        if self.ws:
            try:
                self.ws.close()
            except Exception as e:
                self.__handle_error("error", str(e))
            WSConnection.ws_conn_handler.pop(self.ws)
            self.set_ws(None)
        return self

    def close(self):
        self.suspend = False
        return self.get_channel_id()

    def __no_response(self, ms_exp=1_800_000):
        return current_timestamp() - self.__receive_at > ms_exp

    @staticmethod
    def create(channel, payload_handler, error_handler=None):
        ws_conn = WSConnection(channel).set_handlers(payload_handler, error_handler)
        _thread.start_new_thread(ws_func, (ws_conn,))
        return ws_conn

    def re_connect(self):
        if self.suspend:
            if _ConnectionState.CONNECTED == self.state:
                if not self.__channel_subscribed and self.__no_response(6_000):
                    self.__subscribe()
                elif self.__no_response():
                    self.__rebuild_connection()
            else:
                if current_timestamp() - self.__connect_at > 8_000:
                    self.__rebuild_connection()
        else:
            self.__close()

    def on_open(self):
        self.logger.info("ws_conn<%s> connected" % self.get_channel_id())
        self.__receive_at = current_timestamp()
        self.state = _ConnectionState.CONNECTED
        self.__subscribe()

    def on_message(self, message):
        self.__receive_at = current_timestamp()
        _m = json.loads(message)
        if "result" in _m and "id" in _m:
            if not self.__channel_subscribed:
                if int(_m.get("id")) == int(self.__channel.get("id")) and not _m.get("result"):
                    self.logger.info("subscribe result: %s" % message)
                    self.__channel_subscribed = True
                else:
                    self.__handle_error("warning", "unrecognized message: %s" % message)
            else:
                self.__handle_error("warning", "unrecognized message: %s" % message)
        elif "code" in _m:
            self.__handle_error("error", message)
        else:
            _payload = self.__payload_match(_m)
            if _payload:
                if self.__payload_handler:
                    self.__payload_handler(Dict2Class.from_val(_payload))
            else:
                self.__handle_error("warning", "unrecognized message: %s" % message)

    def on_error(self, error):
        self.__handle_error("warning", "ws_conn<%s> closed(on_error) <%s>" % \
                                           (self.get_channel_id(), str(error)))
        self.state = _ConnectionState.IDLE

    def on_close(self, close_status_code, close_msg):
        self.__handle_error("warning", "ws_conn<%s> closed <code: %s msg: %s>" % \
                                           (self.get_channel_id(), close_status_code, close_msg))
        self.state = _ConnectionState.IDLE

    def __rebuild_connection(self):
        self.logger.info("ws_conn<%s> (re)connecting..." % self.__channel.get("id"))
        _thread.start_new_thread(ws_func, (self.__close().__reset(),))
