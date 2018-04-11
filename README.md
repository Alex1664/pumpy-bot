# pumpy-bot
Bot pour acheter et vendre des cryptomonnaies sur différentes plateformes (Binance, Cryptopia)

# Execution du script

## Packages nécessaires
* Installer les package `pip`
```
pip install tweepy
pip install python-binance
pip install cryptopia_api
```

## Arguments du programme :
```
-h : help
-c, --coin : coin de reference
-m, --mode : mode ('user' ou 'tweet')
-p, --platform : ('cryptopia' ou 'binance')
-t, --test : lancement du bot en mode test, aucun ordre n'est placé, tout est simulé
```

## Lancement
* Avant de lancer le script, sourcer les variables d'environnement contenant les clés d'API
```
source install.sh
```

* Exemple d'execution du script
```
python3 pumpNdump.py -c ETH -m user -p binance --test
```
## Vente
Après avoir acheté, le bot affiche les prix toutes les 0.5 secondes.

Pour faire la vente des monnaies, entrer le caractère 's' ou 'S'