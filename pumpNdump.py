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


def authentication_tweeter():
    print("Connection to tweeter ...")

    auth = tweepy.OAuthHandler(os.environ['TWEETER_CONSUMER_KEY'], os.environ['TWEETER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWEETER_ACCESS_TOKEN'], os.environ['TWEETER_ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)


def handle_orders(coin, coinFrom):
    coin = coin.upper()
    coinFrom = coinFrom.upper()

    # Récupération des fonds disponibles
    originalAsset = client.get_balance(coinFrom)
    print(str(originalAsset) + " " + coinFrom + " available")

    # Récupération du prix de départ
    originalPrice = client.get_price(coin, coinFrom)
    print(coin + " is at " + str(originalPrice) + " " + coinFrom)
    print("Can buy " + str(float(originalAsset / originalPrice)) + " " + coin)

    # Calcul de la quantité à acheter
    priceBuy = float(originalPrice * 1.02)
    quantity = float(originalAsset / priceBuy)
    print("Will buy " + str(quantity) + " " + coin + " (price + 2%)")

    # Placement ordre achat
    client.buy_market(coin, coinFrom, priceBuy, quantity, testMode)
    print("--> Bought")

    # Time before trade
    timeBeforeTrade = time.time()

    print("Press 'S' to sell NOW !\n")
    """tty.setraw(sys.stdin.fileno())"""

    # Wait 15 secondes
    while ((time.time() - timeBeforeTrade) < 20):
        newPrice = client.get_price(coin, coinFrom)
        print(coin + " is at " + str(newPrice) + coinFrom)
        """ch = sys.stdin.read(1)
        if ch == 'S':
             print "Wohoo" """
        time.sleep(0.1)

    # Placement ordre vente
    quantityAfter = client.get_balance(coin)
    print(str(quantityAfter) + " " + coin + " available")
    priceSell = float(client.get_price(coin, coinFrom) * 0.98)
    print("Will sell " + str(quantityAfter) + " " + coin + " (price - 2%)")
    client.sell_market(coin, coinFrom, priceSell, quantityAfter, testMode)

    # Status order sell
    finalAsset = client.get_balance(coinFrom)
    print(str(originalAsset) + " " + coinFrom + " available")
    print("--> Sold")
    print("Previously had " + str(originalAsset) + " " + coinFrom + ", now have " + str(finalAsset) + " " + coinFrom)
    print("Still have " + str(client.get_balance(coin)) + " " + coin)
    print("Delta is " + str(finalAsset - originalAsset) + " " + coinFrom)


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
    if tweet.author.id_str != alexTweeterId:
        print("Tweet not from Macafee")
        print("Get tweet from Macafee ...")
        return False

    coin = search_coin_of_the_week(tweet.text)
    start_trading(coin)


"""*******"""
""" Utils """
"""*******"""


def start_trading(coin):
    coinFrom = 'ETH'
    handle_orders(coin, coinFrom)


def wait_user():
    coin = raw_input("Enter the coin to trade ...\n")
    start_trading(coin)


def wait_tweet():
    clientTweeter = authentication_tweeter()

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
        wait_user()
    elif mode == 'tweet':
        wait_tweet()
    else:
        help()
        sys.exit()


client = None
coinSymbol = ''
alexTweeterId = ''
testMode = False

if __name__ == "__main__":
    main(sys.argv[1:])
