# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

import time
from binex_f.restapi import Dict2Class, RestApi

restapi = RestApi(api_key="****************", secret_key="****************")

def __print_obj(resp)
    print (Dict2Class.to_val(resp))
    time.sleep(0.5)

# Change Position Mode(TRADE)
# dualSidePosition: "true": Hedge Mode; "false": One-way Mode
# resp = restapi.change_position_side_dual(dualSidePosition, recvWindow=None)
resp = restapi.change_position_side_dual(dualSidePosition="true")
__print_obj(resp)

# Get Current Position Mode(USER_DATA)
# resp = restapi.check_position_side_dual()
resp = restapi.check_position_side_dual()
__print_obj(resp)

# Change Multi-Assets Mode (TRADE)
# multiAssetsMargin: "true": Multi-Assets Mode; "false": Single-Asset Mode
# resp = restapi.change_multi_assets_margin(multiAssetsMargin, recvWindow=None)
resp = restapi.change_multi_assets_margin(multiAssetsMargin="false")
__print_obj(resp)

# Get Current Multi-Assets Mode (USER_DATA)
# resp = restapi.check_multi_assets_margin()
resp = restapi.check_multi_assets_margin()
__print_obj(resp)

# Futures Account Balance V2 (USER_DATA)
# resp = restapi.get_balance()
resp = restapi.get_balance()
__print_obj(resp)

# Account Information V2 (USER_DATA)
# resp = restapi.get_account_information()
resp = restapi.get_account_information()
__print_obj(resp)

# Change Initial Leverage (TRADE)
# leverage: target initial leverage: int from 1 to 125
# resp = restapi.change_initial_leverage(symbol, leverage)
resp = restapi.change_initial_leverage(symbol="btcusdt", leverage=64)
__print_obj(resp)

# Change Margin Type (TRADE)
# marginType: ["ISOLATED", "CROSSED"]
# resp = restapi.change_margin_type(symbol, marginType)
resp = restapi.change_margin_type(symbol="btcusdt", marginType="CROSSED")
__print_obj(resp)

# Modify Isolated Position Margin (TRADE)
# _type: 1: Add position margin，2: Reduce position margin
# positionSide: Default BOTH for One-way Mode ; LONG or SHORT for Hedge Mode. It must be sent with Hedge Mode.
# resp = restapi.change_position_margin(symbol, amount, _type, positionSide=None)
resp = restapi.change_position_margin(symbol="btcusdt", amount=1.01, _type=1)
__print_obj(resp)

# Get Position Margin Change History (TRADE)
# _type: 1: Add position margin，2: Reduce position margin
# limit: Default: 500
# resp = restapi.get_position_margin_change_history(symbol, _type=None, startTime=None, endTime=None, limit=None)
resp = restapi.get_position_margin_change_history(symbol="btcusdt", _type=1)
__print_obj(resp)

# Position Information V2 (USER_DATA)
# resp = restapi.get_position_information(symbol=None)
resp = restapi.get_position_information()
__print_obj(resp)

# Account Trade List (USER_DATA)
# fromId: Trade id to fetch from. Default gets most recent trades.
# limit: Default 500; max 1000.
# resp = restapi.get_account_trades(symbol, startTime=None, endTime=None, fromId=None, limit=None)
resp = restapi.get_account_trades(symbol="btcusdt")
__print_obj(resp)

# Get Income History(USER_DATA)
# incomeType: ["TRANSFER", "WELCOME_BONUS", "REALIZED_PNL", "FUNDING_FEE",
#              "COMMISSION", "INSURANCE_CLEAR", "REFERRAL_KICKBACK", "COMMISSION_REBATE",
#              "DELIVERED_SETTELMENT", "COIN_SWAP_DEPOSIT", "COIN_SWAP_WITHDRAW"]
# startTime: Timestamp in ms to get funding from INCLUSIVE.
# endTime: Timestamp in ms to get funding until INCLUSIVE.
# limit: Default 100; max 1000
# resp = restapi.get_income_history(symbol=None, incomeType=None, startTime=None, endTime=None, limit=None)
resp = restapi.get_income_history()
__print_obj(resp)

# Notional and Leverage Brackets (USER_DATA)
# resp = restapi.get_leverage_bracket(symbol=None)
resp = restapi.get_leverage_bracket()
__print_obj(resp)

# Position ADL Quantile Estimation (USER_DATA)
# resp = restapi.get_adl_quantile(symbol=None)
resp = restapi.get_adl_quantile()
__print_obj(resp)

# User's Force Orders (USER_DATA)
# resp = restapi.get_force_orders(symbol=None, autoCloseType=None, startTime=None, endTime=None, limit=None)
# autoCloseType: "LIQUIDATION" for liquidation orders, "ADL" for ADL orders.
# limit: Default 50; max 100.
# resp = restapi.get_force_orders(symbol=None, autoCloseType=None, startTime=None, endTime=None, limit=None)
resp = restapi.get_force_orders()
__print_obj(resp)

# User API Trading Quantitative Rules Indicators (USER_DATA)
# resp = restapi.get_api_trading_stats(symbol=None)
resp = restapi.get_api_trading_stats()
__print_obj(resp)

# User Commission Rate (USER_DATA)
# resp = restapi.get_commission_rate(symbol)
resp = restapi.get_commission_rate(symbol="btcusdt")
__print_obj(resp)

# Start User Data Stream (USER_STREAM)
# resp = restapi.start_user_data_stream()
resp = restapi.start_user_data_stream()
__print_obj(resp)

# Keepalive User Data Stream (USER_STREAM)
# resp = restapi.keep_user_data_stream()
resp = restapi.keep_user_data_stream()
__print_obj(resp)

# Close User Data Stream (USER_STREAM)
# resp = restapi.close_user_data_stream()
resp = restapi.close_user_data_stream()
__print_obj(resp)
