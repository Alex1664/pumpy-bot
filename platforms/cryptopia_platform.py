#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from cryptopia.cryptopia_api import Api


class Cryptopia(object):

    def __init__(self):
        print("Connection to cryptopia ...")
        self.api = Api(os.environ['CRYPTOPIA_API_KEY'], os.environ['CRYPTOPIA_API_SECRET'])

    def get_balance(self, coin):
        print("[Cryptopia] Get balance " + coin)
        balanceETH, error = self.api.get_balance(coin)
        if error is not None:
            print("Get balance error - " + error)
            return -1
        return balanceETH['Available']

    def get_price(self, coin, coinfrom):
        print("[Cryptopia] Get price of " + coin + " in " + coinfrom)
        coinPrice, error = self.api.get_market(coin + "_" + coin)
        if error is not None:
            print("Get price of " + coin + " error - " + error)
            return -1
        return coinPrice['AskPrice']

    def buy_market(self, coin, coinfrom, price, quantity, testmode):
        print("[Cryptopia] Buy market " + str(quantity) + " " + coin + " from " + coinfrom + " with " + str(testmode) + " test mode")
        print("Remove 2.1565% of the quantity to match fees")
        if testmode:
            print("Test mode : " + str(quantity * 0.978435) + " " + coin + " buy at : " + str(price))
        else:
            trade, error = self.api.submit_trade(coin + '/' + coinfrom, 'Buy', price, quantity * 0.978435)
            if error is not None:
                print("Error - " + error)
            print(trade)

    def sell_market(self, coin, coinTo, price, quantity, testmode):
        print("[Cryptopia] Sell market " + str(quantity) + " " + coin + " to " + coinTo + " with " + str(testmode) + " test mode")
        if testmode:
            print("Test mode : " + quantity + " " + coin + " sell at : " + str(price) + " " + coinTo)
        else:
            trade, error = self.api.submit_trade(coin + '/' + coinTo, 'Sell', price, quantity)
            if error is not None:
                print("Error - " + error)
            print(trade)

    def cancel_order(self):
        print("[Cryptopia] Cancel ALL orders")
        trade, error = self.api.cancel_trade("All", None, None)
        if error is not None:
            print("Error cancel order : IT'S BAD !")
        print(trade)
