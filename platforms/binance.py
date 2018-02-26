#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from binance.client import Client


class Binance(object):

    def __init__(self, keyEnv, secretEnv):
        print("Connection to binance ...")
        self.client = Client(os.environ[keyEnv], os.environ[secretEnv])

    def get_balance(self, coin):
        print("[Binance] Get balance " + coin)

    def get_price(self, coin, coinfrom):
        print("[Binance] Get price of " + coin + " in " + coinfrom)

    def buy_market(self, coin, coinfrom, quantity, testmode):
        print("[Binance] Buy market " + str(quantity) + " " + coin + " from " + coinfrom + " with " + str(testmode) + " test mode")

    def sell_market(self, coin, coinTo, quantity, testmode):
        print("[Binance] Sell market " + str(quantity) + " " + coin + " to " + coinTo + " with " + str(testmode) + " test mode")
