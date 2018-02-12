#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""#Import"""
import getopt
import os
import sys
import time

import tweepy
from binance.client import Client

"""# Authentifications"""


def authenticationTweeter():
    print("Connection to tweeter ...")

    auth = tweepy.OAuthHandler(os.environ['TWEETER_CONSUMER_KEY'], os.environ['TWEETER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWEETER_ACCESS_TOKEN'], os.environ['TWEETER_ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)


def authenticationBinance():
    print("Connection to binance ...")
    return Client(os.environ['BINANCE_API_KEY'], os.environ['BINANCE_API_SECRET'])


"""# Binance"""


def handle_orders(coin, coinFrom):
    # Récupération du temps de départ
    originalTime = time.time()

    # Récupération des fonds disponibles
    originalAssetETHJson = clientBinance.get_asset_balance(coinFrom)
    originalAssetETH = float(originalAssetETHJson['free'])
    print(str(originalAssetETH) + " " + coinFrom + " available")

    # Récupération du prix de départ
    symbol = coin + coinFrom
    originalPriceJson = clientBinance.get_symbol_ticker(symbol=symbol)
    originalPrice = float(originalPriceJson['price'])
    print(coin + " is at " + str(originalPrice) + " " + coinFrom)

    # Calcul de la quantité à acheter
    quantity = float(originalAssetETH / originalPrice)
    print("Can buy " + str(quantity) + " " + coin)
    quantity = int(quantity)
    print("Will buy " + str(quantity) + " " + coin + " (rounded)")

    # Placement ordre achat
    if testMode:
        print("-- In test mode")
        orderBuy = clientBinance.create_test_order(
            symbol=symbol,
            side=clientBinance.SIDE_BUY,
            type=clientBinance.ORDER_TYPE_MARKET,
            # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
            quantity=quantity,
            # price=repr(originalPrice)
        )
    else:
        orderBuy = clientBinance.create_order(
            symbol=symbol,
            side=clientBinance.SIDE_BUY,
            type=clientBinance.ORDER_TYPE_MARKET,
            # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
            quantity=quantity,
            # price=repr(originalPrice)
        )

    # Status order buy
    completed = 0
    while not completed:
        orderBuyId = orderBuy['clientOrderId']
        orderBuySt = clientBinance.get_order(
            symbol=symbol,
            orderId=orderBuyId)
        print("Order buy status : " + orderBuySt['status'] + " at : " + orderBuySt['price'])

        if not orderBuySt == clientBinance.ORDER_STATUS_NEW:
            completed = 1

    print("--> Bought " + str(quantity) + " " + coin)

    # Wait 15 secondes
    while ((time.time() - originalTime) < 15):
        newPriceJson = clientBinance.get_symbol_ticker(symbol=symbol)
        newPrice = float(newPriceJson['price'])
        print(coin + " is at " + str(newPrice) + coinFrom)
        time.sleep(0.5)

    # Placement ordre vente
    if testMode:
        print("-- In test mode")
        orderSell = clientBinance.create_test_order(
            symbol=symbol,
            side=clientBinance.SIDE_SELL,
            type=clientBinance.ORDER_TYPE_MARKET,
            # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
            quantity=quantity,
            # price=repr(newPrice)
        )
    else:
        orderSell = clientBinance.create_test_order(
            symbol=symbol,
            side=clientBinance.SIDE_SELL,
            type=clientBinance.ORDER_TYPE_MARKET,
            # timeInForce=clientBinance.TIME_IN_FORCE_GTC,
            quantity=quantity,
            # price=repr(newPrice)
        )

    # Status order sell
    completed = 0
    while not completed:
        orderSellId = orderBuy['clientOrderId']
        orderSellSt = clientBinance.get_order(
            symbol=symbol,
            orderId=orderSellId)
        print("Order buy status : " + orderSellSt['status'] + " at : " + orderSellSt['price'])

        if not orderSellSt == clientBinance.ORDER_STATUS_NEW:
            completed = 1

    finalAssetETHJson = clientBinance.get_asset_balance(coinFrom)
    finalAssetETH = float(finalAssetETHJson['free'])
    print(str(originalAssetETH) + " " + coinFrom + " available")
    print("--> Sold " + str(quantity) + " " + coin)
    print("Previously had " + str(originalAssetETH) + " " + coinFrom + ", now have " + str(finalAssetETH) + " " + coinFrom)
    print("Delta is " + str(finalAssetETH - originalAssetETH) + " " + coinFrom)


"""# Tweeter"""

def searchCoinOfTheWeek(tweet):
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
        print("Coin of the week not found :(")
        print("Get tweet from Macafee ...")

    return coinOfTheWeek.upper()


"""# Tweeter stream"""


class TwitterStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        handle_tweet(status)

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes
    def on_error(self, status_code):
        if status_code == 403:
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False


def handle_tweet(tweet):
    if (tweet.author.id_str != alexTweeterId):
        print("Tweet not from Macafee")
        print("Get tweet from Macafee ...")
        return False

    coin = searchCoinOfTheWeek(tweet.text)
    startTrading(coin)


def startTrading(coin):
    coinFrom = 'ETH'

    if (len(coin + coinFrom) < 4):
        return False

    print("Coin symbol : " + coin + coinFrom)

    handle_orders(coin, coinFrom)


def waitForUser():
    coin = raw_input("Enter the coin to trade ...\n")
    startTrading(coin)


def waitForTweet():
    alexTweeterId = os.environ['TWEETER_FOLLOW_ID']

    print("Get tweet from Macafee ...")

    streamListener = TwitterStreamListener()
    myStream = tweepy.Stream(auth=clientTweeter.auth, listener=streamListener)
    myStream.filter(follow=[alexTweeterId])


def help():
    print 'macafee_bot.py -m <user|tweet> [--test]'


"""# Main"""


def main(argv):
    mode = ''
    try:
        opts, args = getopt.getopt(argv, "hm:t", ["mode=", "test"])
    except getopt.GetoptError:
        print('error')
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
            if mode not in ('user', 'tweet'):
                help()
                sys.exit(2)
        elif opt in ("-t", "--test"):
            testMode = True

    print("Launching bot ...")

    if mode == 'user':
        waitForUser()
    elif mode == 'tweet':
        waitForTweet()
    else:
        help()
        sys.exit()


coinSymbol = ''
alexTweeterId = ''
clientTweeter = authenticationTweeter()
clientBinance = authenticationBinance()
testMode = False

if __name__ == "__main__":
    main(sys.argv[1:])
