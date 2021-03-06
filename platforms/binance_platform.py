#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from binance.client import Client


class Binance(object):

    def __init__(self):
        print("-- Connecting to binance ...")
        self.client = Client(os.environ['BINANCE_API_KEY'], os.environ['BINANCE_API_SECRET'])

    def get_balance(self, coin):
        print("-- Getting balance for " + coin)
        assetJSON = self.client.get_asset_balance(coin)
        if assetJSON == None:
            print(">>> PROBLEM get_balance returned null <<<")
            return 0
        return float(assetJSON['free'])

    def get_price(self, coin, coinfrom):
        priceJSON = self.client.get_symbol_ticker(symbol=coin + coinfrom)
        return float(priceJSON['price'])

    def buy_market(self, coin, coinfrom, ignored, quantity, testmode):
        print("-- Buying market " + str(quantity) + " " + coin + " from " + coinfrom)
        self.symbol = coin + coinfrom
        if testmode:
            print("[TEST] " + str(quantity) + " " + coin + " buy at : " + str(ignored) + " " + coinfrom + " (price is ignored on Binance)")
        else:
            orderBuy = self.client.create_order(
                symbol=coin + coinfrom,
                side=self.client.SIDE_BUY,
                type=self.client.ORDER_TYPE_MARKET,
                # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
                quantity=quantity,
                # price=repr(originalPrice)
            )
        """
            # Il a cette tete le clientOrderId 8Qun2GgcNnYrHKeK8Iv1gI
            # Alors que le get_order attend un nombre
            completed = False
            while not completed:
                time.sleep(0.2)
                
                print(self.orderID)
                orderBuySt = self.client.get_order(
                    symbol=coin + coinfrom,
                    orderId=self.orderID)
                print("+ Order buy status : " + orderBuySt['status'] + " at : " + orderBuySt['price'])

                if not orderBuySt == self.client.ORDER_STATUS_NEW:
                    completed = True
        """

    def sell_market(self, coin, coinTo, ignored, quantity, testmode):
        print("-- Selling market " + str(quantity) + " " + coin + " to " + coinTo)
        if testmode:
            print("[TEST] " + str(quantity) + " " + coin + " sell at : " + str(ignored) + " " + coinTo + " (price is ignored on Binance)")
        else:
            orderSell = self.client.create_order(
                symbol=coin + coinTo,
                side=self.client.SIDE_SELL,
                type=self.client.ORDER_TYPE_MARKET,
                # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
                quantity=quantity,
                # price=repr(newPrice)
            )
        """
        # Pareil que pour le buy
            completed = False
            while not completed:
                time.sleep(0.2)
                orderSellId = orderSell['clientOrderId']
                orderSellSt = self.client.get_order(
                    symbol=coin + coinTo,
                    orderId=orderSellId)
                print("+ Order sell status : " + orderSellSt['status'] + " at : " + orderSellSt['price'])

                if not orderSellSt == self.client.ORDER_STATUS_NEW:
                    completed = True
        """


    def cancel_order(self):
        print("-- Canceling order")
        self.client.cancel_order(symbol=self.symbol, orderId=self.orderID)
        self.symbol = None
        self.orderID = None

    def get_lot_size(self, coin, coinFrom):
        print("-- Getting lot size for " + coin + " in " + coinFrom)
        allInfos = self.client.get_exchange_info()
        for symbol in allInfos['symbols']:
            if symbol['baseAsset'] != coin or symbol['quoteAsset'] != coinFrom:
                continue
            for filter in symbol['filters']:
                if filter['filterType'] != 'LOT_SIZE':
                    continue
                return float(filter['minQty']), float(filter['stepSize'])
