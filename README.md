# pumpy-bot
bot to buy and sell cryptocurrencies in Binance or Cryptopia

# Pour lancer le script
* Installer les package `pip`
```
pip install tweepy
pip install python-binance
pip install cryptopia_api
```
* Arguments du programme :
```
-h : help
-c, --coin : coin de reference
-m, --mode : mode ('user' ou 'tweet')
-p, --platform : ('cryptopia' ou 'binance')
-t, --test : lancement du bot en mode test
```
* Executer le script en mode TEST :
```
python pumpNdump.py -c ETH -m user -p binance --test
```
* Executer le script en mode REEL :
```
python -c ETH -m user -p binance
```
