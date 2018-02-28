#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from cryptopia.cryptopia_api import Api


class Cryptopia(object):

    def __init__(self):
        print("-- Connecting to cryptopia ...")
        self.api = Api(os.environ['CRYPTOPIA_API_KEY'], os.environ['CRYPTOPIA_API_SECRET'])

    def get_balance(self, coin):
        print("-- Getting balance for " + coin)
        balanceETH, error = self.api.get_balance(coin)

        if balanceETH is None:
            print("[ERROR] Balance is None")
            sys.exit(3)

        if error is not None:
            print("[ERROR] Balance error - " + error)
            sys.exit(3)

        return balanceETH['Available']

    def get_price(self, coin, coinfrom):
        print("-- Getting price of " + coin + " in " + coinfrom)
        coinPrice, error = self.api.get_market(coin + "_" + coinfrom)

        if coinPrice is None:
            print("[ERROR] Get price returned None")
            sys.exit(3)

        if error is not None:
            print("[ERROR] Get price of " + coin + " error - " + error)
            sys.exit(3)

        return coinPrice['AskPrice']

    def buy_market(self, coin, coinfrom, price, quantity, testmode):
        print("-- Buying market " + str(quantity) + " " + coin + " from " + coinfrom)
        print("-- Remove 2.1565% of the quantity to match fees")
        if testmode:
            print("[TEST] " + str(quantity * 0.978435) + " " + coin + " buy at : " + str(price))
        else:
            trade, error = self.api.submit_trade(coin + '/' + coinfrom, 'Buy', price, quantity * 0.978435)

            if trade is None:
                print("[ERROR] Buy market returned None")
                sys.exit(3)

            if error is not None:
                print("[ERROR] Error - " + error)
                sys.exit(3)

            print(trade)

    def sell_market(self, coin, coinTo, price, quantity, testmode):
        print("-- Selling market " + str(quantity) + " " + coin + " to " + coinTo)
        if testmode:
            print("[TEST] " + str(quantity) + " " + coin + " sell at : " + str(price) + " " + coinTo)
        else:
            trade, error = self.api.submit_trade(coin + '/' + coinTo, 'Sell', price, quantity)

            if trade is None:
                print("[ERROR] Sell market returned None")
                sys.exit(3)

            if error is not None:
                print("[ERROR] Error - " + error)
                sys.exit(3)

            print(trade)

    def cancel_order(self):
        print("-- Canceling ALL orders")
        trade, error = self.api.cancel_trade("All", None, None)

        if trade is None:
            print("[ERROR] Cancel order returned None")
            sys.exit(3)

        if error is not None:
            print("[ERROR] Error cancel order : IT'S BAD !")
            sys.exit(3)

        print(trade)
