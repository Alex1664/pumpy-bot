#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import time

import tweepy

from platforms.binance_platform import Binance
from platforms.cryptopia_platform import Cryptopia

"""*******************"""
""" Authentifications """
"""*******************"""


def authentication_tweeter():
    print("-- Connecting to tweeter ...")

    auth = tweepy.OAuthHandler(os.environ['TWEETER_CONSUMER_KEY'], os.environ['TWEETER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWEETER_ACCESS_TOKEN'], os.environ['TWEETER_ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)


def number_of_decimals(stepSize):
    splitted = str(stepSize).split('1')[0].split('.')
    if len(splitted) == 1:
        return 0
    return len(splitted[1]) + 1


def roundAt(toRound, at):
    return ("{:10." + str(at) + "f}").format(toRound)


def handle_orders(coin, coinFrom):
    global buyFor
    coin = coin.upper()
    coinFrom = coinFrom.upper()

    # Initial time
    initTime = time.time()
    if testMode:
        print("[Time start]")

    # Récupération des fonds disponibles
    originalAsset = client.get_balance(coinFrom)
    print(str(originalAsset) + " " + coinFrom + " available")

    # Récupération du prix de départ
    originalPrice = client.get_price(coin, coinFrom)
    minQty, stepSize = client.get_lot_size(coin, coinFrom)

    print(coin + " is at " + roundAt(originalPrice, 8) + " " + coinFrom)

    nbDecimal = number_of_decimals(stepSize)

    # Calcul de la quantité à acheter
    priceBuy = float(originalPrice * 1.02)
    quantity = float(originalAsset / priceBuy)
    quantity = round(quantity * buyFor, nbDecimal)
    if quantity < minQty:
        print("Cant't buy " + roundAt(quantity, 8) + " " + coin + " cause it's below the minimum quantity : " + roundAt(minQty, 8) + " " + coin + " in " + coinFrom)

    print("Will buy " + roundAt(quantity, 8) + " " + coin + " (" + str(buyFor) + " x quantity at price + 2%)")

    # Time before buy
    timeBeforeBuy = time.time()
    if testMode:
        print("[Took " + roundAt(timeBeforeBuy - initTime, 2) + " seconds]")

    # Placement ordre achat (priceBuy ignored si market order sur binance)
    client.buy_market(coin, coinFrom, priceBuy, quantity, testMode)
    print("--> Bought")

    # Time before trade
    timeBeforeWait = time.time()
    if testMode:
        print("[Took " + roundAt(timeBeforeWait - timeBeforeBuy, 2) + " seconds]")

    # Wait 15 secondes
    """while ((time.time() - timeBeforeTrade) < 20):
        newPrice = client.get_price(coin, coinFrom)
        print(coin + " is at " + str(newPrice) + coinFrom)
        time.sleep(0.1)"""

    sellOrNot = ""
    while (sellOrNot != "S"):
        sellOrNot = input("Press 's' or 'S' to sell NOW : \n")
        sellOrNot = sellOrNot.upper()

    # Time before sell
    timeBeforeSell = time.time()
    if testMode:
        print("[Took " + roundAt(timeBeforeSell - timeBeforeWait, 2) + " seconds]")

    print("Selling ...")

    # Placement ordre vente
    quantityAfter = client.get_balance(coin)
    print(roundAt(quantityAfter, 8) + " " + coin + " available")
    priceSell = float(client.get_price(coin, coinFrom) * 0.98)
    quantityAfter = round(quantityAfter, nbDecimal)
    print("Will sell " + roundAt(quantityAfter, 8) + " " + coin + " (price - 2%)")
    client.sell_market(coin, coinFrom, priceSell, quantityAfter, testMode)

    # Time before status
    timeBeforeStatus = time.time()
    if testMode:
        print("[Took " + roundAt(timeBeforeStatus - timeBeforeSell, 2) + " seconds]")

    # Status order sell
    finalAsset = client.get_balance(coinFrom)
    print(roundAt(originalAsset, 8) + " " + coinFrom + " available")
    print("--> Sold")
    print("Previously had " + roundAt(originalAsset, 8) + " " + coinFrom + ", now have " + roundAt(finalAsset, 8) + " " + coinFrom)
    print("Now have " + roundAt(client.get_balance(coin), 8) + " " + coin)
    print("Delta is " + roundAt(finalAsset - originalAsset, 8) + " " + coinFrom)

    if testMode:
        print("[Took in total " + roundAt(time.time() - initTime, 2) + " seconds]")


"""*********"""
""" Tweeter """
"""*********"""


def search_coin_of_the_week(tweet):
    print("Searching coin ...")
    coinOfTheWeek = ""

    if ("coin of the week" in tweet.lower()):
        coin = tweet.split("(")

        # Si il a quelque chose après la 1ere parenthèse
        if (len(coin) > 1):
            coin = coin[1].split(")")

            # Si le texte est pas trop grand mais vérification pas forcément nécessaire
            if (len(coin[0]) < 10):
                coinOfTheWeek = coin[0]
                print("Coin of the week found : " + coinOfTheWeek)

    if (len(coinOfTheWeek) == 0):
        print("[ERROR] Coin of the week not found :(")
        print("Getting tweet from Macafee ...")

    return coinOfTheWeek


"""****************"""
""" Tweeter stream """
"""****************"""


class TwitterStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        handle_tweet(status)

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes
    def on_error(self, status_code):
        if status_code == 403:
            print("[ERROR] The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False


def handle_tweet(tweet):
    if tweet.author.id_str != os.environ['TWEETER_FOLLOW_ID']:
        print("[WARNING] Tweet not from Macafee")
        print("Getting tweet from Macafee ...")
        return False

    coin = search_coin_of_the_week(tweet.text)
    start_trading(coin)


"""*******"""
""" Utils """
"""*******"""


def start_trading(coin):
    global coinFrom
    global platform
    # subprocess.call(['python3 printPrices.py', '--coin', coin, '--coin-from', coinFrom, '--platform', platform])
    handle_orders(coin, coinFrom)


def wait_user():
    coin = input("Enter the coin to trade : \n")
    start_trading(coin)


def wait_tweet():
    clientTweeter = authentication_tweeter()

    print("-- Getting tweet from Macafee ...")

    streamListener = TwitterStreamListener()
    myStream = tweepy.Stream(auth=clientTweeter.auth, listener=streamListener)
    myStream.filter(follow=[os.environ['TWEETER_FOLLOW_ID']])


def help():
    print('pumpNdump.py -m <user|tweet> -p <cryptopia|binance> -c <ETH|BTC|...> [--buy-for 0.9] [--test]')


"""******"""
""" Main """
"""******"""


def main(argv):
    mode = ''
    try:
        opts, args = getopt.getopt(argv, "hm:tp:c:b:", ["coin=", "platform=", "mode=", "test", "buy-for="])
    except getopt.GetoptError:
        print('error')
        help()
        sys.exit(2)

    global platform
    global coinFrom
    global buyFor
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-c", "--coin"):
            coinFrom = arg
        elif opt in ("-b", "--buy-for"):
            buyFor = arg
        elif opt in ("-m", "--mode"):
            mode = arg
            if mode not in ('user', 'tweet'):
                help()
                sys.exit(2)
        elif opt in ("-p", "--platform"):
            platform = arg
            if platform not in ('cryptopia', 'binance'):
                help()
                sys.exit(2)
        elif opt in ("-t", "--test"):
            global testMode
            testMode = True

    print("-- Launching bot ...")

    global client
    if platform == 'binance':
        client = Binance()
    elif platform == 'cryptopia':
        client = Cryptopia()
    else:
        help()
        sys.exit()

    if mode == 'user':
        wait_user()
    elif mode == 'tweet':
        wait_tweet()
    else:
        help()
        sys.exit()

    if buyFor <= 0 or buyFor > 1:
        print("Can't buy for more thant what you have (or less than 0)")
        help()
        sys.exit()


client = None
coinSymbol = ''
alexTweeterId = ''
testMode = False
coinFrom = 'ETH'
platform = ''
buyFor = 0.9

if __name__ == "__main__":
    main(sys.argv[1:])
