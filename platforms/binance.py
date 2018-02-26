#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from binance.client import Client


class Binance(object):

    def __init__(self):
        print("Connection to binance ...")
        self.client = Client(os.environ['BINANCE_API_KEY'], os.environ['BINANCE_API_SECRET'])

    def get_balance(self, coin):
        print("[Binance] Get balance " + coin)
        assetJSON = self.client.get_asset_balance(coin)
        return float(assetJSON['free'])

    def get_price(self, coin, coinfrom):
        print("[Binance] Get price of " + coin + " in " + coinfrom)
        priceJSON = self.client.get_symbol_ticker(symbol=coin + coinfrom)
        return float(priceJSON['price'])

    def buy_market(self, coin, coinfrom, ignored, quantity, testmode):
        print("[Binance] Buy market " + str(quantity) + " " + coin + " from " + coinfrom + " with " + str(testmode) + " test mode")
        if testmode:
            orderBuy = self.client.create_test_order(
                symbol=coin + coinfrom,
                side=self.client.SIDE_BUY,
                type=self.client.ORDER_TYPE_MARKET,
                # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
                quantity=quantity,
                # price=repr(originalPrice)
            )
        else:
            orderBuy = self.client.create_order(
                symbol=coin + coinfrom,
                side=self.client.SIDE_BUY,
                type=self.client.ORDER_TYPE_MARKET,
                # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
                quantity=quantity,
                # price=repr(originalPrice)
            )

        completed = False
        while not completed:
            time.sleep(0.2)
            orderBuyId = orderBuy['clientOrderId']
            orderBuySt = self.client.get_order(
                symbol=coin + coinfrom,
                orderId=orderBuyId)
            print("Order buy status : " + orderBuySt['status'] + " at : " + orderBuySt['price'])

            if not orderBuySt == self.client.ORDER_STATUS_NEW:
                completed = True

    def sell_market(self, coin, coinTo, ignored, quantity, testmode):
        print("[Binance] Sell market " + str(quantity) + " " + coin + " to " + coinTo + " with " + str(testmode) + " test mode")
        if testmode:
            orderSell = self.client.create_test_order(
                symbol=coin + coinTo,
                side=self.client.SIDE_SELL,
                type=self.client.ORDER_TYPE_MARKET,
                # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
                quantity=quantity,
                # price=repr(newPrice)
            )
        else:
            orderSell = self.client.create_test_order(
                symbol=coin + coinTo,
                side=self.client.SIDE_SELL,
                type=self.client.ORDER_TYPE_MARKET,
                # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
                quantity=quantity,
                # price=repr(newPrice)
            )

        # Status order sell
        completed = False
        while not completed:
            time.sleep(0.2)
            orderSellId = orderSell['clientOrderId']
            orderSellSt = self.client.get_order(
                symbol=coin + coinTo,
                orderId=orderSellId)
            print("Order buy status : " + orderSellSt['status'] + " at : " + orderSellSt['price'])

            if not orderSellSt == self.client.ORDER_STATUS_NEW:
                completed = True
