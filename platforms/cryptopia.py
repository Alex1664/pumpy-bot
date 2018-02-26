#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from cryptopia.cryptopia_api import Api


class Cryptopia(object):

    def __init__(self, keyEnv, secretEnv):
        print("Connection to cryptopia ...")
        self.api = Api(os.environ[keyEnv], os.environ[secretEnv])

    def get_balance(self, coin):
        print("[Cryptopia] Get balance " + coin)
        balanceETH, error = self.api.get_balance(coin)
        if error is not None:
            print ("Get balance error - " + error)
            return -1
        return balanceETH['Available']

    def get_price(self, coin, coinfrom):
        print("[Cryptopia] Get price of " + coin + " in " + coinfrom)
        coinPrice, error = self.api.get_market(coin + "_" + coin)
        if error is not None:
            print ("Get price of " + coin + " error - " + error)
            return -1
        return coinPrice['AskPrice']

    def buy_market(self, coin, coinfrom, price, quantity, testmode):
        print("[Cryptopia] Buy market " + str(quantity) + " " + coin + " from " + coinfrom + " with " + str(testmode) + " test mode")
        trade, error = self.api.submit_trade(coin + '/' + coinfrom, 'Buy', price, quantity)
        print ("Buy market " + str(quantity) + " " + coin + " from " + coinfrom + " error - " + error)
        if error is not None:
            return -1
        print trade

    def sell_market(self, coin, coinTo, price, quantity, testmode):
        print("[Cryptopia] Sell market " + str(quantity) + " " + coin + " to " + coinTo + " with " + str(testmode) + " test mode")
        trade, error = self.api.submit_trade(coin + '/' + coinTo, 'Sell', price, quantity)
        print ("Sell market " + str(quantity) + " " + coin + " from " + coinTo + " error - " + error)
        if error is not None:
            return -1
        print trade
