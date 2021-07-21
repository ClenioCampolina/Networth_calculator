import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3
import time
import requests
from matplotlib import pyplot as plt
from matplotlib import style

import import_libraries as imp
imp.importing_all()
import sqlite_db_operations as sqlf
import url_connect as urlcon
ctx = urlcon.context_with_no_certificate_check()


def get_prices():
    coinsdict = sqlf.get_dict_coinname_and_symbol()
    currencylist = sqlf.get_currency_list()

    allprices = dict()
    usddict = dict()
    auddict = dict()
    brldict = dict()
    btcdict = dict()
    ethdict = dict()

    bigstr=None
    for (k,v) in coinsdict.items():
        if bigstr == None:
            bigstr = k+'%2C'
        else:
            bigstr = bigstr+k+'%2C'
    bigstr = bigstr[:-3]
    #print(bigstr)
        
    bigcur=None
    for c in currencylist:
        c = c[0]
        if bigcur == None:
            bigcur = c+'%2C'
        else:
            bigcur = bigcur+c+'%2C'
    bigcur = bigcur[:-3]
    #print(bigstr)

    #print('Retrieving coin prices from CoinGecko')
    url_cg = 'https://api.coingecko.com/api/v3/simple/price?ids='+bigstr+'&vs_currencies='+bigcur+'&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'
    #print(url_cg)
    uh = urllib.request.urlopen(url_cg, context=ctx)
    data = uh.read().decode()
    try:
        js = json.loads(data)
    except:
        js = None
    #print(json.dumps(js, indent=4),'\n\n')

    for currency in currencylist:
        currency = currency[0]
        #print(currency)
        for (v,k) in coinsdict.items():
            if v == 'Total-debt-across-all-defi-protocols':    #Total-debt-across-all-defi-protocols is a fake coin created to represent the debt position of this wallet. As the coin is fake, it is impossible to get its "price" on coingecko.
                 continue
            price = float(js[v][currency])
            market_cap = float(js[v][currency+'_market_cap'])
            try:
                vol24h = float(js[v][currency+'_24h_vol'])
            except:
                vol24h = 0
            try:
                change24h = float(js[v][currency+'_24h_change'])
            except:
                change24h = 0
            coindata = (price,market_cap,vol24h,change24h)
            comb = k+'_'+currency
            allprices[comb]=allprices.get(comb,coindata)
            if currency == 'usd':
                usddict[k]=usddict.get(k,price)
            if currency == 'aud':
                auddict[k]=usddict.get(k,price)
            if currency == 'brl':
                brldict[k]=usddict.get(k,price)
            if currency == 'btc':
                btcdict[k]=usddict.get(k,price)
            if currency == 'eth':
                ethdict[k]=usddict.get(k,price)       
    
    return usddict, auddict, brldict, btcdict, ethdict, allprices