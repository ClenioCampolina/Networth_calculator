import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#btcaddlist = cur.execute('''SELECT address FROM Adresses WHERE symbol = btc''')
btcaddlist = ('1L5Bpeue7mDE1d4kwGAEzVgkaC8ziaWu4W','18gFBqE9WcyPA21b82o3dswX5LAB89VqUh','1BpFE9QViJ4xfNJiKxFMQCHRh8n9TDbnhA')
bigbtc = None
for adds in btcaddlist:
    if bigbtc == None:
        bigbtc = adds + ','
    else:
        bigbtc = bigbtc + adds + ','
bigbtc = bigbtc[:-1]
urlbtc_part1 = 'https://api.blockchair.com/bitcoin/dashboards/addresses/'
urlbtc_part2 = '?limit=1'
urlbtc = urlbtc_part1 + bigbtc + urlbtc_part2

uhbtc = urllib.request.urlopen(urlbtc, context=ctx)
btcdata = uhbtc.read().decode()
try:
    js_btc = json.loads(btcdata)
except:
    print('It was not possible to get the balances of btc wallets.')
    quit()
#print(json.dumps(js_btc, indent=4),'\n\n')

#print((js_btc['data']['addresses']['1L5Bpeue7mDE1d4kwGAEzVgkaC8ziaWu4W']['balance'])/100000000)

btc_bal = float(0)
for adds in btcaddlist:
    btc_bal = btc_bal + ((float(js_btc['data']['addresses'][adds]['balance']))/100000000)
print(btc_bal)




bigeth = None
#ethaddlist = cur.execute('''SELECT address FROM Adresses WHERE symbol = eth''')
ethaddlist = ('0x4b4276D6AE2C79064989D14dc6f03f33fa3cf8F7','0xd551234ae421e3bcba99a0da6d736074f22192ff','0x88282dEeDF2884274DaE445eF1F22F87CF61bfED','0x335D2d7a806243901172aA676ad36E0bbDF0BD01')
for adds in ethaddlist:
    if bigeth == None:
        bigeth = adds + ','
    else:
        bigeth = bigeth + adds + ','
bigeth = bigeth[:-1]     
urleth_part1 = 'https://api.etherscan.io/api?module=account&action=balancemulti&address='
urleth_part2 = '&tag=latest&apikey='
api_key_etherscan = 'FFFIW9CIYG769PYH39XVG26Q8SWX1552UJ'
url_eth = urleth_part1 + bigeth + urleth_part2 + api_key_etherscan

uheth = urllib.request.urlopen(url_eth, context=ctx)
ethdata = uheth.read().decode()
try:
    js_eth = json.loads(ethdata)
except:
    print('It was not possible to get the balances from the eth wallets.')
    quit()
#print(json.dumps(js_eth, indent=4),'\n\n')

eth_bal = float(0)
for adds in range(len(ethaddlist)):
    eth_bal = eth_bal + ((float(js_eth['result'][adds]['balance']))/1000000000000000000)

print(eth_bal)


tokendict = dict()
urltoken_part1 = 'https://api.blockchair.com/ethereum/dashboards/address/'
urltoken_part2 = '?erc_20=true'
for adds in ethaddlist:
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
        tokenbalance = float(tdict['balance'])
        tokendict[tokensymbol] = tokendict.get(tokensymbol,0)+tokenbalance


#print(tokendict['link']/1000000000000000000)


