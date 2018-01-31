#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""#Import"""
import os
from binance.client import Client
from binance.websockets import BinanceSocketManager
import tweepy
import time
import sys, getopt

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


def handle_orders(coin):
    # Récupération du prix et temps de départ
    originalTime = time.time()
    originalAssetETHJson = clientBinance.get_asset_balance('ETH')
    originalAssetETH = float(originalAssetETHJson['free'])
    originalPriceJson = clientBinance.get_symbol_ticker(symbol=coin)
    originalPrice = float(originalPriceJson['price'])
    quantity = originalAssetETH * originalPrice

    # Placement ordre achat
    orderBuy = clientBinance.create_test_order(
        symbol=coin,
        side=clientBinance.SIDE_BUY,
        type=clientBinance.ORDER_TYPE_LIMIT,
        timeInForce=clientBinance.TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=repr(originalPrice))

    # Status order buy
    orderBuyId = orderBuy['clientOrderId']
    orderBuySt = clientBinance.get_order(
        symbol=coin,
        orderId=orderBuyId)

    print("Order buy status : " + orderBuySt + " at : " + originalPrice)

    # Wait 15 secondes
    while ((time.time() - originalTime) < 15):
        orderBuySt = clientBinance.get_order(
            symbol=coin,
            orderId=orderBuyId)

        print("Order buy status : " + orderBuySt)
        time.sleep(0.1)

    # Récupération quantité acheté
    originalAsset = clientBinance.get_asset_balance('ETH')

    # Récupération du prix de vente
    sellPriceJson = clientBinance.get_symbol_ticker(symbol=coin)
    sellPrice = float(sellPriceJson['price'])

    # Placement ordre vente
    orderSell = clientBinance.create_test_order(
        symbol=coin,
        side=clientBinance.SIDE_SELL,
        type=clientBinance.ORDER_TYPE_LIMIT,
        timeInForce=clientBinance.TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=repr(sellPrice))

    # Status order sell
    orderSellId = orderSell['clientOrderId']
    orderSellSt = clientBinance.get_order(
        symbol=coin,
        orderId=orderSellId)

    print("Order sell status :")


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
    coinSymbol = coin + 'ETH'

    if (len(coinSymbol) < 4):
        return False

    print("Coin symbol : " + coinSymbol)

    handle_orders(coinSymbol)


def waitForUser():
    coin=input('Enter the coin to trade ...')
    startTrading(coin)


def waitForTweet():
    alexTweeterId = os.environ['TWEETER_FOLLOW_ID']

    print("Get tweet from Macafee ...")

    streamListener = TwitterStreamListener()
    myStream = tweepy.Stream(auth=clientTweeter.auth, listener=streamListener)
    myStream.filter(follow=[alexTweeterId])


def help():
    print 'macafee_bot.py -m <wait|tweet>'


"""# Main"""


def main(argv):
    mode = ''
    try:
        opts, args = getopt.getopt(argv, "hm:", ["mode="])
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

    print("Launching bot ...")

    if mode == 'user':
        waitForUser()
    elif mode == 'tweet':
        waitForTweet()
    else:
        sys.exit()


coinSymbol = ''
alexTweeterId = ''
clientTweeter = authenticationTweeter()
clientBinance = authenticationBinance()

if __name__ == "__main__":
    main(sys.argv[1:])
