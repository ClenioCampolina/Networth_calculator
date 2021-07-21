import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3
import time
import requests
from matplotlib import pyplot as plt
from matplotlib import style
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


import import_libraries as imp
imp.importing_all()
import sqlite_db_operations as sqlf
import url_connect as urlcon
urlcon.context_with_no_certificate_check()






def btc_balance():                  #BTC balance from blockchair
    btcaddlist = sqlf.get_addresses_list_of_a_coin("btc")
    bigbtc = None

    for adds in btcaddlist:
        adds = adds[0]
        if bigbtc == None:
            bigbtc = adds + ','
        else:
            bigbtc = bigbtc + adds + ','
    bigbtc = bigbtc[:-1]

    urlbtc_part1 = 'https://api.blockchair.com/bitcoin/dashboards/addresses/'
    urlbtc_part2 = '?limit=1'
    urlbtc = urlbtc_part1 + bigbtc + urlbtc_part2
    #print("connecting to ",urlbtc,"\n")
    uhbtc = urllib.request.urlopen(urlbtc, context=ctx)
    btcdata = uhbtc.read().decode()
    try:
        js_btc = json.loads(btcdata)
    except:
        print('It was not possible to get the balances from the btc wallets.')
        quit()
    #print(json.dumps(js_btc, indent=4),'\n\n')

    btc_bal = float(0)
    for adds in btcaddlist:
        adds = adds[0]
        btc_bal = btc_bal + ((float(js_btc['data']['addresses'][adds]['balance']))/100000000)
    
    return btc_bal








def eth_balance():                  #ETH balance from Etherscan
    ethaddlist = sqlf.get_addresses_list_of_a_coin("eth")
    bigeth = None
    
    urleth_part2 = ""
    for adds in ethaddlist:
        adds = adds[0]
        if urleth_part2 == "":
            urleth_part2 = adds
        else:
            urleth_part2 = urleth_part2 + "," + adds

    urleth_part1 = "https://api.etherscan.io/api?module=account&action=balancemulti&address="
    urleth_part3 = "&tag=latest&apikey=YourApiKeyToken"
    url_eth = urleth_part1 + urleth_part2 + urleth_part3
    uheth = urllib.request.urlopen(url_eth, context=ctx)
    ethdata = uheth.read().decode()
    try:
        js_eth = json.loads(ethdata)
    except:
        print('It was not possible to get the balances from the eth wallets.')
        quit()
    #print(json.dumps(js_eth, indent=4),'\n\n')

    eth_bal = float(0)
    list_of_add_and_bal = js_eth['result']
    for item in list_of_add_and_bal:
        #print(item['account'],(float(item['balance'])/1000000000000000000))
        eth_bal = eth_bal + (float(item['balance'])/1000000000000000000)

    return eth_bal







def erc20_balance(coindict,tnamedict):                    #ERC-20 Tokens from blockchair
    ethaddlist = sqlf.get_addresses_list_of_a_coin("eth")
    coingeckolst = sqlf.get_list_of_coingecko_tokens_from_table()

    tdict = dict()       #This dict is jus temporary and you hold the info of each token as the iterations move

    urltoken_part1 = 'https://api.blockchair.com/ethereum/dashboards/address/'
    urltoken_part2 = '?erc_20=true'
    eth_bal2 = float(0)
    for adds in ethaddlist:
        adds = adds[0]
        url_token = urltoken_part1 + adds + urltoken_part2
        uhtoken = urllib.request.urlopen(url_token, context=ctx)
        tokendata = uhtoken.read().decode()
        try:
            js_token = json.loads(tokendata)
        except:
            print('It was not possible to get the tokens balances.')
            quit()
        #print(json.dumps(js_token, indent=4),'\n\n') 
        adds1 = adds.lower()
        tokenlist = js_token['data'][adds1]['layer_2']['erc_20']
        #print(tokenlist)

        for items in range(len(tokenlist)):
            tdict = tokenlist[items]
            tokensymbol = tdict['token_symbol']
            tokensymbol = tokensymbol.lower()
            if tokensymbol == "slp" or tokensymbol == "vtorn" or tokensymbol == "veth" or tokensymbol == "pcdai":  # "vesper eth", "slp" (sushiswap lp token) and "voulcher torn" are not available in coingecko
                continue
            tokenbalance = float(tdict['balance'])
            tdecimals = int(tdict['token_decimals'])
            divisor = 10**tdecimals
            tokenbalance = tokenbalance/divisor
            coindict[tokensymbol] = coindict.get(tokensymbol,0)+tokenbalance
            tokenname = tdict['token_name']
            original = tokenname
            if ' ' in tokenname:
                tokenname = tokenname.replace(' ','-')   
            tokenname = tokenname.lower()
            if (tokenname,) not in coingeckolst:
                tokenname = sqlf.get_the_coingecko_token_name_using_the_blockchair_name(tokenname)
            tnamedict[tokensymbol] = tnamedict.get(tokensymbol,tokenname)


        adds = adds.lower()
        if js_token['data'][adds]['address']['balance'] == None:
            continue
        eth_bal2 = eth_bal2 + ((float(js_token['data'][adds]['address']['balance']))/1000000000000000000)

    coindatabase = sqlf.list_of_all_coins_symbols_from_coins_table()
    for (s,n) in tnamedict.items():
        if s not in coindatabase:
            sqlf.insert_coin_in_coins_table(n,s)
    #print(tnamedict)



def dot_balance():
    dotaddlist = sqlf.get_addresses_list_of_a_coin("dot")
    dot_bal = float(0)

    url_dot = "https://polkadot.subscan.io/api/open/account"
    payload1 = '''{"address": "'''
    payload2 = '''"}'''
    headers = {'Content-Type': 'application/json'}

    for adds in dotaddlist:
        adds = adds[0]
        payload = payload1 + adds + payload2
        response = requests.request("POST", url_dot, headers=headers, data = payload)
        dotdata = response.text.encode('utf8')
        try:
            js_dot = json.loads(dotdata)
        except:
            print('It was not possible to get the balances from the dot wallets.')
            quit()
        #print(json.dumps(js_dot, indent=4),'\n\n')
        if js_dot['data']['balance'] == None:
            continue
        dot_bal = dot_bal + (float(js_dot['data']['balance']))
    
    return dot_bal


def maker(coindict,tnamedict):
    # networklist = ('&network=ethereum') #,"&network=optimism","&network=xdai","&network=binance-smart-chain","&network=fantom")  #to be implemented by Zapper   "&network=polygon"
    ethaddlist = sqlf.get_addresses_list_of_a_coin("eth")
    
    url_add = ""
    for add in ethaddlist:
        # print("\n",add,"\n")
        url_add = url_add + "addresses%5B%5D=" + add[0] + "&"
    url_add = url_add[:-1]

    url_maker_part1 = "https://api.zapper.fi/v1/protocols/maker/balances?"
    network = '&network=ethereum'
    api_zapper = "&api_key=96e0cc51-a62e-42ca-acee-910ea7d2a241"


    url_maker = url_maker_part1 + url_add + network + api_zapper
    #print("\n",url_maker,"\n")
    uhmaker = urllib.request.urlopen(url_maker, context=ctx)
    makerdata = uhmaker.read().decode()
    try:
        js_maker = json.loads(makerdata)
    except:
        print('It was not possible to get the MakerDao balances.')
        quit()
    #print(json.dumps(js_maker, indent=4),'\n\n')

    maker_debt = 0
    for add in ethaddlist:
        add = add[0].lower()
        maker_meta_list = js_maker[add]["meta"]
        for meta in maker_meta_list:
            if meta["label"] == "Debt":
                debt = float(meta["value"])
                maker_debt = maker_debt + debt
        #print(add)
        try:
            maker_list = js_maker[add]["products"][0]["assets"]
        except:
            continue
        for item in maker_list:
            if item["category"] == "deposit":
                tokensymbol = item["symbol"].lower()
                tokenbalance = item["balance"]
                tokenname = sqlf.get_name_of_coin_from_symbol(tokensymbol)
                coindict[tokensymbol] = coindict.get(tokensymbol,0)+tokenbalance
                tnamedict[tokensymbol] = tnamedict.get(tokensymbol,tokenname)
    
    return maker_debt
