#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import sys
import time

from platforms.binance_platform import Binance
from platforms.cryptopia_platform import Cryptopia


def print_prices(coin, coinFrom):
    coin = coin.upper()
    coinFrom = coinFrom.upper()

    # Time before trade
    timeBeforeTrade = time.time()

    # Wait 15 secondes
    while ((time.time() - timeBeforeTrade) < 20):
        newPrice = client.get_price(coin, coinFrom)
        print(coin + " is at " + str(newPrice) + coinFrom)
        time.sleep(0.2)


# TODO When to stop ?

def help():
    print(
        'python3 printPrices.py -p <cryptopia|binance> -c <MOD|QSP|...> -f <ETH|BTC|...>')  # TODO add other args to do some stats like price start, etc


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hp:c:f:", ["coin=", "coin-from=", "platform="])
    except getopt.GetoptError:
        print('error')
        help()
        sys.exit(2)

    platform = ''
    global coin
    global coinFrom
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-c", "--coin"):
            coin = arg
        elif opt in ("-f", "--coin-from"):
            coinFrom = arg
        elif opt in ("-p", "--platform"):
            platform = arg
            if platform not in ('cryptopia', 'binance'):
                help()
                sys.exit(2)

    print("-- Launching bot ...")

    global client
    if platform == 'binance':
        client = Binance()
    elif platform == 'cryptopia':
        client = Cryptopia()
    else:
        help()
        sys.exit()

    print_prices(coin, coinFrom)


client = None

if __name__ == "__main__":
    main(sys.argv[1:])
