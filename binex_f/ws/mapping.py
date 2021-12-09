# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying

aggregate_trade = {
  "e": "eventType",
  "E": "eventTime",
  "s": "symbol",
  "a": "aggTradeId",
  "p": "price",
  "q": "quantity",
  "f": "firstTradeId",
  "l": "lastTradeId",
  "T": "tradeTime",
  "m": "isMarketMaker",
}

mark_price = {
    "e": "eventType",
    "E": "eventTime",
    "s": "symbol",
    "p": "price",
    "i": "indexPrice",
    "P": "estimatedSettlePrice",
    "r": "fundingRate",
    "T": "nextFundingTime"
}

all_mark_price = mark_price
kline = {
    "e": "eventType",
    "E": "eventTime",
    "s": "symbol",
    "k": "kline",
    "kline": {
        "t": "startTime",
        "T": "closeTime",
        "s": "symbol",
        "i": "interval",
        "f": "firstTradeId",
        "L": "lastTradeId",
        "o": "openPrice",
        "c": "closePrice",
        "h": "highPrice",
        "l": "lowPrice",
        "v": "baseAssetVolume",
        "n": "numOfTrades",
        "x": "isClosed",
        "q": "quoteAssetVolume",
        "V": "takerByBaseAssetVolume",
        "Q": "takerByQuoteAssetVolumn"
    }
}

continuous_kline = {
    "e": "eventType",
    "E": "eventTime",
    "ps": "symbol",
    "ct": "contractType",
    "k": "kline",
    "kline": {
        "t": "startTime",
        "T": "closeTime",
        "i": "interval",
        "f": "firstTradeId",
        "L": "lastTradeId",
        "o": "openPrice",
        "c": "closePrice",
        "h": "highPrice",
        "l": "lowPrice",
        "v": "volume",
        "n": "numOfTrades",
        "x": "isClosed",
        "q": "quoteAssetVolume",
        "V": "takerByVolume",
        "Q": "takerByQuoteAssetVolumn"
    }
}

symbol_miniticker = {
    "e": "eventType",
    "E": "eventTime",
    "s": "symbol",
    "c": "closePrice",
    "o": "openPrice",
    "h": "highPrice",
    "l": "lowPrice",
    "v": "totalTradedBaseAssetVolume",
    "q": "totalTradedQuoteAssetVolume"
}

all_miniticker = symbol_miniticker

symbol_ticker = {
    "e": "eventType",
    "E": "eventTime",
    "s": "symbol",
    "p": "priceChange",
    "P": "priceChangePercent",
    "w": "weightedAvgPrice",
    "c": "lastPrice",
    "Q": "lastQuantity",
    "o": "openPrice",
    "h": "highPrice",
    "l": "lowPrice",
    "v": "totalTradedBaseAssetVolume",
    "q": "totoTradedQuoteAssetVolume",
    "O": "statisticsOpenTime",
    "C": "statisticsCloseTime",
    "F": "firstTradeId",
    "L": "lastTradeId",
    "n": "numOfTrades"
}

all_ticker = symbol_ticker

symbol_bookticker = {
    "e": "eventType",
    "u": "orderbookUpdateId",
    "E": "eventTime",
    "T": "transactionTime",
    "s": "symbol",
    "b": "bestBidPrice",
    "B": "bestBidQty",
    "a": "bestAskPrice",
    "A": "bestAskQty"
}

all_bookticker = symbol_bookticker

symbol_liquidation = {
    "e": "eventType",
    "E": "eventTime",
    "o": "order",
    "order":{
        "s":  "symbol",
        "S":  "side",
        "o":  "ordertype",
        "f":  "timeInForce",
        "q":  "origQty",
        "p":  "price",
        "ap": "avgPrice",
        "X":  "orderStatus",
        "l":  "lastFilledQty",
        "z":  "cumFilledQty",
        "T":  "tradeTime"
    }
}

all_liquidation = symbol_liquidation

book_depth = {
    "e": "eventType",
    "E": "eventTime",
    "s": "symbol",
    "T": "transactionTime",
    "U": "firstUpdateId",
    "u": "finalUpdateId",
    "pu": "finalUpdateIdInlastStream",
    "b": "bids",
    "a": "asks"
}

diff_depth = {
    "e": "eventType",
    "E": "eventTime",
    "s": "symbol",
    "T": "transactionTime",
    "U": "firstUpdateId",
    "u": "finalUpdateId",
    "pu": "finalUpdateIdInLastStream",
    "b": "bids",
    "a": "asks"
}

nav = {
    "e": "eventType",
    "E": "eventTime",
    "s": "symbol",
    "m": "tokenIssued",
    "b": "baskets",
    "baskets": {
        "s": "futuresSymbol",
        "n": "position"
    },
    "n": "blvtNav",
    "l": "realLeverage",
    "t": "targetLeverage",
    "f": "fundingRatio"
}

nav_kline = {
    "e": "eventType",
    "E": "eventTime",
    "s": "blvtName",
    "k": "kline",
    "kline":{
        "t":"startTime",
        "T":"closeTime",
        "s":"blvtName",
        "i":"interval",
        "f":"firstNavUpdateTime",
        "L":"lastNavUpdateTime",
        "o":"openNavPrice",
        "c":"closeNavPrice",
        "h":"highestNavPrice",
        "l":"lowestNavPrice",
        "v":"realLeverage",
        "n":"numOfNavUpdate"
   }
}

composite_index = {
    "e": "eventType",
    "E": "eventTime",
    "s": "symbol",
    "p": "price",
    "C": "assettype",
    "c": "composition",
    "composition": {
          "b": "baseAsset",
          "q": "quoteAsset",
          "w": "weightInQuantity",
          "W": "weightInPercentage",
          "i": "indexPrice"
      }
}

margin_call = {
    "e": "eventType",
    "E": "eventTime",
    "cw": "crossWalletBalance",
    "p": "position",
    "position": {
        "s":  "symbol",
        "ps": "positionSide",
        "pa": "positionAmount",
        "mt": "marginType",
        "iw": "isolatedWallet",
        "mp": "markPrice",
        "up": "unrealizedPnL",
        "mm": "maintenanceMarginRequired"
    }
}

account_update = {
    "e": "eventType",
    "E": "eventTime",
    "T": "transaction",
    "a": "updateData",
    "updateData": {
        "m": "eventReasonType",
        "B": "Balance",
        "Balance": {
          "a":  "asset",
          "wb": "walletBalance",
          "cw": "crossWalletBalance",
          "bc": "balanceChangeExceptPnLAndCommission"
        },
        "P": "position",
        "position": {
            "s":  "symbol",
            "pa": "positionAmount",
            "ep": "entryPrice",
            "cr": "preFeeAccumulatedRealized",
            "up": "unrealizedPnL",
            "mt": "marginType",
            "iw": "isolatedWallet",
            "ps": "positionSide"
      }
    }
}

order_trade_update = {
    "e": "eventType",
    "E": "eventTime",
    "T": "transactionTime",
    "o": "order",
    "order":{
        "s": "symbol",
        "c": "clientOrderId",
        "S": "side",
        "o": "ordertype",
        "f": "timeInForce",
        "q": "origQty",
        "p": "origPrice",
        "ap" :"avgPrice",
        "sp" :"stopPrice",
        "x": "executionType",
        "X": "orderStatus",
        "i": "orderId",
        "l": "lastFilledQty",
        "z": "cumFilledQty",
        "L": "lastFilledPrice",
        "N": "commissionAsset",
        "n": "commission",
        "T": "tradeTime",
        "t": "tradeId",
        "b": "bidNotional",
        "a": "askNotional",
        "m": "isMakerSide",
        "R": "isReduceOnly",
        "wt": "stopPriceWorkingType",
        "ot": "origOrdertype",
        "ps": "positionSide",
        "cp": "isClosePosition",
        "AP": "activationPrice",
        "cr": "callbackRate",
        "rp": "realizedProfit"
    }
}

account_config_update = {
    "e": "eventType",
    "E": "eventTime",
    "T": "transactionTime",
    "ac": {
        "s":"symbol",
        "l":"leverage"
    },
    "ai":{
        "j": "isMultiAssetsMode"
    }
}
