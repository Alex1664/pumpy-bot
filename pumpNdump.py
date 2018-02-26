#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import time

import tweepy

from platforms.binance import Binance
from platforms.cryptopia import Cryptopia

"""*******************"""
""" Authentifications """
"""*******************"""


def authenticationTweeter():
    print("Connection to tweeter ...")

    auth = tweepy.OAuthHandler(os.environ['TWEETER_CONSUMER_KEY'], os.environ['TWEETER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWEETER_ACCESS_TOKEN'], os.environ['TWEETER_ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)


"""***********"""
""" Cryptopia """
"""***********"""


def handleOrders(coin, coinFrom):
    # Récupération du temps de départ
    originalTime = time.time()

    coin = coin.upper()
    coinFrom = coinFrom.upper()

    # Récupération des fonds disponibles
    originalAssetETH = client.get_balance(coinFrom)
    print(str(originalAssetETH) + " " + coinFrom + " available")

    # Récupération du prix de départ
    originalPrice = client.get_price(coin, coinFrom)
    print(coin + " is at " + str(originalPrice) + " " + coinFrom)

    # Calcul de la quantité à acheter
    quantity = float(originalAssetETH / originalPrice)
    print("Can buy " + str(quantity) + " " + coin)
    quantity = int(quantity)
    print("Will buy " + str(quantity) + " " + coin + " (rounded)")

    # Placement ordre achat
    client.buy_market(coin, coinFrom, quantity, testMode)
    print("--> Bought " + str(quantity) + " " + coin)

    # Wait 15 secondes
    while ((time.time() - originalTime) < 15):
        newPrice = client.get_price(coin, coinFrom)
        print(coin + " is at " + str(newPrice) + coinFrom)
        time.sleep(0.5)

    # Placement ordre vente
    client.sell_market(coin, coinFrom, quantity, testMode)

    # Status order sell
    finalAssetETH = client.get_balance(coinFrom)
    print(str(originalAssetETH) + " " + coinFrom + " available")
    print("--> Sold " + str(quantity) + " " + coin)
    print("Previously had " + str(originalAssetETH) + " " + coinFrom + ", now have " + str(finalAssetETH) + " " + coinFrom)
    print("Delta is " + str(finalAssetETH - originalAssetETH) + " " + coinFrom)


"""*********"""
""" Tweeter """
"""*********"""


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
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False


def handle_tweet(tweet):
    if (tweet.author.id_str != alexTweeterId):
        print("Tweet not from Macafee")
        print("Get tweet from Macafee ...")
        return False

    coin = searchCoinOfTheWeek(tweet.text)
    startTrading(coin)


"""*******"""
""" Utils """
"""*******"""


def startTrading(coin):
    coinFrom = 'ETH'
    handleOrders(coin, coinFrom)


def waitForUser():
    coin = raw_input("Enter the coin to trade ...\n")
    startTrading(coin)


def waitForTweet():
    clientTweeter = authenticationTweeter()

    print("Get tweet from Macafee ...")

    streamListener = TwitterStreamListener()
    myStream = tweepy.Stream(auth=clientTweeter.auth, listener=streamListener)
    myStream.filter(follow=[os.environ['TWEETER_FOLLOW_ID']])


def help():
    print('pumpNdump.py -m <user|tweet> -p <cryptopia|binance> [--test]')


"""******"""
""" Main """
"""******"""


def main(argv):
    mode = ''
    try:
        opts, args = getopt.getopt(argv, "hm:tp:", ["platform=", "mode=", "test"])
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
        elif opt in ("-p", "--platform"):
            platform = arg
            if platform not in ('cryptopia', 'binance'):
                help()
                sys.exit(2)
        elif opt in ("-t", "--test"):
            global testMode
            testMode = True

    print("Launching bot ...")

    global client
    if platform == 'binance':
        client = Binance()
    elif platform == 'cryptopia':
        client = Cryptopia()
    else:
        help()
        sys.exit()

    if mode == 'user':
        waitForUser()
    elif mode == 'tweet':
        waitForTweet()
    else:
        help()
        sys.exit()


client = None
coinSymbol = ''
alexTweeterId = ''
testMode = False

if __name__ == "__main__":
    main(sys.argv[1:])
