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

    def get_price(self, coin, coinfrom):
        print("[Cryptopia] Get price of " + coin + " in " + coinfrom)

    def buy_market(self, coin, coinfrom, quantity, testmode):
        print("[Cryptopia] Buy market " + str(quantity) + " " + coin + " from " + coinfrom + " with " + str(testmode) + " test mode")

    def sell_market(self, coin, coinTo, quantity, testmode):
        print("[Cryptopia] Sell market " + str(quantity) + " " + coin + " to " + coinTo + " with " + str(testmode) + " test mode")
