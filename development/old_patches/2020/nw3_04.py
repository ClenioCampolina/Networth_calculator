import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3
import time


print('Crypto Net Worth 3.04\n')
#Now supported: 
    #Multiple ETH addresses;                 DONE
    #API for AUD and BRL prices;             DONE
    #Data saved in database;                 DONE
    #Funtion to call prices from CoinGecko.  DONE


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Grab time of the call
ct = time.localtime()
savetime = str(ct.tm_year) + '_' + str(ct.tm_mon) + '_' + str(ct.tm_mday)

#_______________________________________SQLite

conn = sqlite3.connect('networth.sqlite')
cur = conn.cursor()

#cur.executescriptX('''DROP TABLE IF EXISTS Coins; DROP TABLE IF EXISTS Addresses; DROP TABLE IF EXISTS History; DROP TABLE IF EXISTS Currencies; DROP TABLE IF EXISTS Networth''')
#cur.execute('''DROP TABLE IF EXISTS Coins''')

cur.execute('''CREATE TABLE IF NOT EXISTS Coins (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            coin TEXT UNIQUE, 
            symbol TEXT UNIQUE
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Addresses (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            address TEXT UNIQUE,
            coins_id INTEGER
            )''')

#cur.execute('''CREATE TABLE IF NOT EXISTS History (
            #id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            #coins_id INTEGER,
            #date TEXT UNIQUE,
            #price REAL,
            #marketcap REAL,
            #vol24h REAL,
            #change24h REAL
            #)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Currencies (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            currency TEXT UNIQUE,
            symbol TEXT UNIQUE
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Networth (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            coins_id INTEGER,
            currencies_id INTEGER,
            date TEXT UNIQUE,
            netbtc REAL,
            neteth REAL,
            netusd REAL,
            netaud REAL,
            netbrl REAL
            )''')

#_______________________________________Add Address, Currency or Coin

def addcoin():
    coinname = input('Please enter the name of the coin: (ex: bitcoin)\n')
    coinname = coinname.lower()
    coinsymbol = input('Please enter the symbol of that coin: (ex: btc)\n')
    coinsymbol = coinsymbol.lower()
    cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES (?,?)''',(coinname, coinsymbol))

def addcurrency():
    currencyname = input('Please enter the name of the currency: (ex: american dollars)\n')
    currencyname = currencyname.lower()
    currencysymbol = input('Please enter the symbol of that currency: (ex: usd)\n')
    currencysymbol = currencysymbol.lower()
    cur.execute('''INSERT OR IGNORE INTO Currencies (currency, symbol) VALUES (?,?)''',(currencyname, currencysymbol))

def addaddress():
    fulladdress = input('Please enter the wallet address:\n')
    coinsymbol = input('Please enter the symbol of the coin this address belongs to: (ex: btc)\n')
    coinsymbol = coinsymbol.lower()
    cur.execute('''SELECT id FROM Coins WHERE symbol = ?''',(coinsymbol,))
    idcoin = cur.fetchall()
    idcoin = idcoin[0][0]
    cur.execute('''INSERT OR IGNORE INTO Addresses (address,coins_id) VALUES (?,?)''',(fulladdress,idcoin))

#add a debug to add call a add coin funtion if I decide to add a address of a coin that is not yet in the coins table

while True:
    enternew = input('If this is the first time you are using this program, select (y) to enter the coins, currencies and addresses.\nIf you used it before, do you want to insert a new coin, currency or address? (y/n)\n')
    enternew = enternew.lower()
    if len(enternew) < 1:
        break
    if enternew not in ('yes','no','y','n'):
        print('Sorry, that is not a valid answer.')
        continue
    elif enternew == 'no' or enternew == 'n':
        break
    else:
        answer = input('Please select what entity you want to insert: (coin/currency/address)\n')
        answer = answer.lower()
        number = int(input('How many entities of this type do you want to insert?\n'))
        if answer not in ('coin','currency','address'):
            print('Sorry, that is not a valid answer.')
            continue
        if answer == 'coin':
            for i in range(number):
                addcoin()
            conn.commit()
        if answer == 'currency':
            for i in range(number):
                addcurrency()
            conn.commit()
        if answer == 'address':
            for i in range(number):
                addaddress()
            conn.commit()
    answer2 = input('Do you want to continue inserting items? (y/n)\n')
    answer2 = answer2.lower()
    if answer2 not in ('yes','no','y','n'):
        print('Sorry, that is not a valid answer.')
        continue
    elif answer2 == 'yes' or answer2 == 'y':
        continue
    else:
        break





print('-__________- 00% complete')

#_______________________________________BTC balance from blockchair

#btc_balance = get_address_overview('1L5Bpeue7mDE1d4kwGAEzVgkaC8ziaWu4W')
#blockcypher_token = 'ff67c2cbc54b46dfaaa2d3a09d443e9f'
#urlbtc = 'https://api.blockchair.com/bitcoin/dashboards/addresses/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa,12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX?limit=1'
#100000000
#btc_bal_total = float(0.00015225)

bigbtc = None
cur.execute('''SELECT id FROM Coins WHERE symbol=?''',('btc',))
btcid = cur.fetchall()
btcid = btcid[0][0]
cur.execute('''SELECT address FROM Addresses WHERE coins_id = ?''',(btcid,))
btcaddlist = cur.fetchall()
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
#print(urlbtc)
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

print('-##________- 20% complete')

#_______________________________________ETH balance from blockchair

#https://api.etherscan.io/api?module=account&action=balancemulti&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a,0x63a9975ba31b0b9626b34300f7f627147df1f526,0x198ef1ec325a96cc354c7266a038be8b5c558f67&tag=latest&apikey=YourApiKeyToken
#eth_address1='0x4b4276D6AE2C79064989D14dc6f03f33fa3cf8F7'
#eth_address2='0x335D2d7a806243901172aA676ad36E0bbDF0BD01'

#urleth_part1 = 'https://api.etherscan.io/api?module=account&action=balancemulti&address='
#urleth_part2 = '&tag=latest&apikey='
#api_key_etherscan = 'FFFIW9CIYG769PYH39XVG26Q8SWX1552UJ'
#url_eth = urleth_part1 + bigeth + urleth_part2 + api_key_etherscan

bigeth = None
cur.execute('''SELECT id FROM Coins WHERE symbol=?''',('eth',))
ethid = cur.fetchall()
ethid = ethid[0][0]
cur.execute('''SELECT address FROM Addresses WHERE coins_id = ?''',(ethid,))
ethaddlist = cur.fetchall()
eth_bal = float(0)
for adds in ethaddlist:
    adds = adds[0]
    #https://api.blockchair.com/ethereum/dashboards/address/0x3282791d6fd713f1e94f4bfd565eaa78b3a0599d?erc_20=true
    urleth_part1 = 'https://api.blockchair.com/ethereum/dashboards/address/'
    urleth_part2 = '?limit=1'
    url_eth = urleth_part1 + adds + urleth_part2
    #print(url_eth)
    uheth = urllib.request.urlopen(url_eth, context=ctx)
    ethdata = uheth.read().decode()
    try:
        js_eth = json.loads(ethdata)
    except:
        print('It was not possible to get the balances from the eth wallets.')
        quit()
    #print(json.dumps(js_eth, indent=4),'\n\n')
    adds = adds.lower()
    if js_eth['data'][adds]['address']['balance'] == None:
        continue
    eth_bal = eth_bal + ((float(js_eth['data'][adds]['address']['balance']))/1000000000000000000)

#print(eth_bal)

print('-####______- 40% complete')

#_______________________________________ERC-20 Tokens from blockchair

#part1 = ' https://api.blockcypher.com/v1/eth/main/contracts/0x514910771af9ca656af840dff83e8264ecf986ca/balanceOf?token=$TOKEN'
#rest = 'token=$TOKEN'
#parameters = { "private": "ff67c2cbc54b46dfaaa2d3a09d443e9f", "gas_limit": 20000, "params": ["0x4b4276D6AE2C79064989D14dc6f03f33fa3cf8F7"] }
#part2 = urllib.parse.urlencode(parameters)
#url_0 = part1 + part2
#print('Retrieving BTC prices from', url_0)
#uh = urllib.request.urlopen(url_0, context=ctx)
#data = uh.read().decode()
#print(data)
#link_bal_total = float(257.8872676413)
#https://api.blockchair.com/ethereum/dashboards/address/0x3282791d6fd713f1e94f4bfd565eaa78b3a0599d?erc_20=true

coingeckolst = list()
fhand = open('all_coins_in_coingecko.json')
coingeckojs = fhand.read()
coingeckodata = json.loads(coingeckojs)
#print(json.dumps(coingeckodata,indent=4))
for x in range(len(coingeckodata)):
    id = coingeckodata[x]['id']
    #print(id)
    coingeckolst.append(id)

tokendict = dict()
tdict = dict()
tnamedict = dict()
urltoken_part1 = 'https://api.blockchair.com/ethereum/dashboards/address/'
urltoken_part2 = '?erc_20=true'
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

    eth_bal2 = float(0)
    for items in range(len(tokenlist)):
        tdict = tokenlist[items]
        tokensymbol = tdict['token_symbol']
        tokensymbol = tokensymbol.lower()
        tokenbalance = float(tdict['balance'])
        tdecimals = int(tdict['token_decimals'])
        divisor = 10**tdecimals
        tokenbalance = tokenbalance/divisor
        tokendict[tokensymbol] = tokendict.get(tokensymbol,0)+tokenbalance
        tokenname = tdict['token_name']
        if tokenname == 'ChainLink Token':
            tokenname = 'chainlink'
        if tokenname == '0x Protocol Token':
            tokenname = '0x'
        if tokenname == 'USD//C':
            tokenname = 'usd-coin'
        if tokenname == 'robonomics':
            tokenname = 'robonomics-network'       
        if ' ' in tokenname:
            tokenname = tokenname.replace(' ','-')    
        tokenname = tokenname.lower()
        if tokenname not in coingeckolst:
            print('The token name',tokenname,'is not in the coingecko list. Please adjust the code before writing this token name in the database.')
            quit()
            #ADD A TABLE IN THE DATA BASE WITH ALL THE TOKENNAME ADJUSTMENTS AND IF THE TOKENNAME IS NOT IN THE COINGECKOLST, GO TO THAT TABLE AND GRAB THE CORRECT VALUE IF EXISTENT






        #print(tokenname)
        tnamedict[tokensymbol] = tnamedict.get(tokensymbol,tokenname)
    #adds = adds.lower()
    #if js_token['data'][adds]['address']['balance'] == None:
        #continue
    #eth_bal2 = eth_bal2 + ((float(js_token['data'][adds]['address']['balance']))/1000000000000000000)
   

#print(tnamedict)

#print(tokendict['link']/1000000000000000000)

for (s,n) in tnamedict.items():
    cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES (?,?)''',(n,s))


conn.commit()

print('-######____- 60% complete')

#______________________________________Polkadot

dot_bal = float(0)






print('-########__- 80% complete')

#_________________________________________________CoinGecko

#'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum&vs_currencies=usd%2Caud&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true'

#currencylist = ('usd','btc','eth','aud','brl')
cur.execute('''SELECT symbol FROM Currencies''')
currencylist = cur.fetchall()
#print(currencylist)

#coinsdict = {'btc':'bitcoin','eth':'ethereum','link':'chainlink','ubt':'unibright','rpl':'rocket-pool','dot':'polkadot'}
coinsdict = dict()
cur.execute('''SELECT coin FROM Coins''')
numcoins = cur.fetchall()
numcoins = range(len(numcoins))
for i in numcoins:
    i=i+1
    cur.execute('''SELECT coin, symbol FROM Coins WHERE id = ?''',(i,))
    grablist = cur.fetchall()
    grablist = grablist[0]
    #grablistc = grablist[0]
    #grablists = grablist[1]
    #print(grablist)
    coinsdict[grablist[0]]=coinsdict.get(grablist[0],grablist[1])

#print(coinsdict)

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
        if k == currency:
            continue
        price = float(js[v][currency])
        market_cap = float(js[v][currency+'_market_cap'])
        vol24h = float(js[v][currency+'_24h_vol'])
        change24h = float(js[v][currency+'_24h_change'])
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


#print(fulldata)
#print(fulldata['link_brl'])
#print(fulldata['ubt_eth'])

print('-##########- 100% complete')

#______________________________________Net Worth
print('\n\n______________Report______________','\n\n')
print('''Date:  ''',ct.tm_mday,'/',ct.tm_mon,'/',ct.tm_year,'\n')

print('Amount of BTC :        ', btc_bal)
btc_usd = btc_bal * allprices['btc_usd'][0]
print('Those coins worth in usd:        ',btc_usd)
btc_aud = btc_bal * allprices['btc_aud'][0]
print('Those coins worth in aud:        ',btc_aud)
btc_brl = btc_bal * allprices['btc_brl'][0]
print('Those coins worth in brl:        ',btc_brl)
btc_eth = btc_bal * allprices['btc_eth'][0]
print('Those coins worth in eth:        ',btc_eth)
print('\n')

print('Amount of ETH :        ', eth_bal)
eth_usd = eth_bal * allprices['eth_usd'][0]
print('Those coins worth in usd:        ',eth_usd)
eth_aud = eth_bal * allprices['eth_aud'][0]
print('Those coins worth in aud:        ',eth_aud)
eth_brl = eth_bal * allprices['eth_brl'][0]
print('Those coins worth in brl:        ',eth_brl)
eth_btc = eth_bal * allprices['eth_btc'][0]
print('Those coins worth in btc:        ',eth_btc)
print('\n')

t_usd = 0
t_aud = 0
t_brl = 0
t_btc = 0
t_eth = 0
for (s,b) in tokendict.items():
    print('Amount of',s.upper(),':','        ',b)
    v_usd = b * usddict[s]
    t_usd = t_usd + v_usd
    print('Those coins worth in usd:        ',v_usd)
    v_aud = b * auddict[s]
    t_aud = t_aud + v_aud
    print('Those coins worth in aud:        ',v_aud)
    v_brl = b * brldict[s]
    t_brl = t_brl + v_brl
    print('Those coins worth in brl:        ',v_brl)
    v_btc = b * btcdict[s]
    t_btc = t_btc + v_btc
    print('Those coins worth in btc:        ',v_btc)
    v_eth = b * ethdict[s]
    t_eth = t_eth + v_eth
    print('Those coins worth in eth:        ',v_eth)
    print('\n')


print('Amount of DOT :        ', dot_bal)
dot_usd = dot_bal * allprices['dot_usd'][0]
print('Those coins worth in usd:        ',dot_usd)
dot_aud = dot_bal * allprices['dot_aud'][0]
print('Those coins worth in aud:        ',dot_aud)
dot_brl = dot_bal * allprices['dot_brl'][0]
print('Those coins worth in brl:        ',dot_brl)
dot_btc = dot_bal * allprices['dot_btc'][0]
print('Those coins worth in btc:        ',dot_btc)
dot_eth = dot_bal * allprices['dot_eth'][0]
print('Those coins worth in eth:        ',dot_eth)
print('\n')
print('\n')


total_usd = btc_usd + eth_usd + t_usd + dot_usd
total_aud = btc_aud + eth_aud + t_aud + dot_aud
total_brl = btc_brl + eth_brl + t_brl + dot_brl
total_btc = btc_bal + eth_btc + t_btc + dot_btc
total_eth = btc_eth + eth_bal + t_eth + dot_eth
print('Net Worth in USD:     ', total_usd)
print('Net Worth in AUD:     ', total_aud)
print('Net Worth in BRL:     ', total_brl)
print('Net Worth in BTC:     ', total_btc)
print('Net Worth in ETH:     ', total_eth,'\n\n')


#____________________________________Add Net Worth and prices/marketcap to database

cur.execute('''INSERT OR IGNORE INTO Networth (date, netbtc, neteth, netusd, netaud, netbrl) VALUES (?,?,?,?,?,?)''', (savetime,total_btc,total_eth,total_usd,total_aud,total_brl))
conn.commit()


