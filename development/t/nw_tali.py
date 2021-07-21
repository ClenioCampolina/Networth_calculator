import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3
import time
import requests
from matplotlib import pyplot as plt
from matplotlib import style


print('Crypto Net Worth 2020.3.008\n')
#Now supported:
    #DONE   SQLite bug of increasing the coins table index fixed  
    #DONE   Multiple DOT addresses;                 
    #DONE   API for Dot balances;                   
    #DONE   Value of each coin in different currencies saved in the database;
    #DONE   Portifolio percentages of each coin in different currencies saved in the database;
    #DONE   Line chart representing total value in different currencies;
    #DONE   Pie chart representing the percentages of portifolio for each coin;
    #DONE   Database with the matching coin names between Coingecko and Blockchair
    #DONE   Add the functionality of adding a new coin that is not in the coingecko/blockchair database  (line 370)
    #       Update the CoinGecko list in the database automatically without losing the values entered in the Blochair column



# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


#_______________________________________SQLite

conn = sqlite3.connect('networth.sqlite')
cur = conn.cursor()

#cur.executescriptX('''DROP TABLE IF EXISTS Coins; DROP TABLE IF EXISTS Addresses; DROP TABLE IF EXISTS History; DROP TABLE IF EXISTS Currencies; DROP TABLE IF EXISTS Networth''')
#cur.execute('''DROP TABLE IF EXISTS Coins''')
#quit()

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

cur.execute('''CREATE TABLE IF NOT EXISTS History (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            coins_id INTEGER,
            date_id INTEGER,
            balance REAL,
            value_usd REAL,
            value_aud REAL,
            value_brl REAL,
            value_btc REAL,
            value_eth REAL
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Portifolio (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            coins_id INTEGER,
            date_id INTEGER,
            percentage REAL
            )''')            

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

cur.execute('''CREATE TABLE IF NOT EXISTS Names_database (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            coingecko TEXT UNIQUE,
            blockchair TEXT UNIQUE
            )''')

cur.execute('''SELECT symbol FROM Coins''')
coindatabase = cur.fetchall()
coindatabase2=list()
for o in coindatabase:
    coindatabase2.append(o[0])
coindatabase = coindatabase2

for i in ('btc','eth','dot','ewt','kda'):
    if i not in coindatabase and i == 'btc':
       cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES ('bitcoin','btc')''')
       conn.commit()
    if i not in coindatabase and i == 'eth':
       cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES ('ethereum','eth')''')
       conn.commit()
    if i not in coindatabase and i == 'dot':
       cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES ('polkadot','dot')''')
       conn.commit()
    if i not in coindatabase and i == 'ewt':
       cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES ('energy-web-token','ewt')''')
       conn.commit()
    if i not in coindatabase and i == 'kda':
       cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES ('kadena','kda')''')
       conn.commit()
        



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
        if answer not in ('coin','currency','address'):
            print('Sorry, that is not a valid answer.')
            continue
        number = int(input('How many entities of this type do you want to insert?\n'))
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

##_______________________________________Time Settings

ct = time.localtime()
if len(str(ct.tm_mday)) < 2:
    day = '0' + str(ct.tm_mday)
else:
    day = str(ct.tm_mday)
if len(str(ct.tm_mon)) < 2:
    mon = '0' + str(ct.tm_mon)
else:
    mon = str(ct.tm_mon)
savetime = str(ct.tm_year) + '_' + mon + '_' + day


cur.execute('''SELECT date FROM Networth''')
alldates = cur.fetchall()
datelst=list()
for d in alldates:
    datelst.append(d[0])
datelst = sorted(datelst,reverse=True)






coindict = dict()   #coindict_definition - This dictionary is NOT temporary and it saves the symbol of the coins/tokens and their balances


#_______________________________________BTC balance from blockchair

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

coindict['btc']=coindict.get('btc',btc_bal)

print('-##________- 20% complete')

#_______________________________________ETH balance from blockchair

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

coindict['eth']=coindict.get('eth',eth_bal)


print('-####______- 40% complete')

#_______________________________________ERC-20 Tokens from blockchair

addcgnames = False                  #Default value is False. We should only turn addcgnames True once, to add all names of coins from coinbase website and the exceptions for blockchair
if addcgnames:
    cur.execute('''DROP TABLE IF EXISTS Names_database''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Names_database (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            coingecko TEXT UNIQUE,
            blockchair TEXT UNIQUE
            )''')
    url_cg = 'https://api.coingecko.com/api/v3/coins/list'
    uhcg = urllib.request.urlopen(url_cg, context=ctx)
    cgdata = uhcg.read().decode()
    cg_js = json.loads(cgdata)
    #print(json.dumps(cg_js,indent=4))
    for x in range(len(cg_js)):
        id = cg_js[x]['id']
        #before adding new exceptions, remember to replace all spaces for "-" and put all letters in lower case
        if id == 'chainlink':
            cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'chainlink-token'))
        elif id == '0x':
            cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'0x-protocol-token'))
        elif id == 'usd-coin':
            cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'usd//c'))
        elif id == 'robonomics-network':
            cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'robonomics'))
        elif id == 'xdai-stake':
            cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'stake'))
        #elif id == 'dai-stake':
            #cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'stake'))
        else:
            cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko) VALUES (?)''',(id,))
    conn.commit()

if addcgnames:
    quit()

cur.execute('''SELECT coingecko FROM Names_database''')
coingeckolst = cur.fetchall()

tdict = dict()       #This dict is jus temporary and you hold the info of each token as the iterations move
tnamedict = dict()   #

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
        if tokensymbol == "vtorn" or tokensymbol == "veth":
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
            cur.execute('''SELECT Names_database.coingecko FROM Names_database WHERE Names_database.blockchair = ?''',(tokenname,))
            try:
                tokenname = cur.fetchone()[0]
            except:
                #print('The token name {} was not added as an exception in the column blockchair of the Names_database table. Please find out what name coingecko uses for this coin and add {} to the blockchair column (remember to replace all spaces for "-" and put all letters in lower case).'.format(original,original))
                #Every time this code runs, add this new exception to the list in the begining of the section "ERC-20 Tokens from blockchair" (scroll up a bit)
                #quit()
                cgname = input('\nThe coin/token {} does not have the same name in the CoinGecko and Blockchair websites.\nPlease check the json file with all coins from CoinGecko and enter the name CoinGecko uses for this coin/token.\n'.format(original))
                cur.execute('''UPDATE Names_database SET blockchair = ? WHERE coingecko = ? ''',(tokenname,cgname))
                conn.commit()
                cur.execute('''SELECT Names_database.coingecko FROM Names_database WHERE Names_database.blockchair = ?''',(tokenname,))
                tokenname = cur.fetchone()[0]
        tnamedict[tokensymbol] = tnamedict.get(tokensymbol,tokenname)


  
    adds = adds.lower()
    if js_token['data'][adds]['address']['balance'] == None:
        continue
    eth_bal2 = eth_bal2 + ((float(js_token['data'][adds]['address']['balance']))/1000000000000000000)
   

#print(tnamedict)


for (s,n) in tnamedict.items():
    if s not in coindatabase:
        cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES (?,?)''',(n,s))


conn.commit()

#______________________________________DOT balance from 


cur.execute('''SELECT id FROM Coins WHERE symbol=?''',('dot',))
dotid = cur.fetchall()
dotid = dotid[0][0]
cur.execute('''SELECT address FROM Addresses WHERE coins_id = ?''',(dotid,))
dotaddlist = cur.fetchall()
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


coindict['dot']=coindict.get('dot',dot_bal)


#______________________________________Other coins


kda_bal = float(0)  #HOTBIT
coindict['kda']=coindict.get('kda',kda_bal)

ewt_bal = float(0)  #Kucoin or Liquid
coindict['ewt']=coindict.get('ewt',ewt_bal)



print('-######____- 60% complete')

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

print('-########__- 80% complete')

#_________________________________________________Original Investment

#Original investments in USD

ori_usd_btc = float(1.22)     #8000*0.00015225
ori_usd_eth = float(23622.88) #220*107.376733
ori_usd_rpl = float(1250)     #2.49*502
ori_usd_bat = float(0)
ori_usd_ubt = float(1250)     #0.41*3021
ori_usd_link = float(3268)    #8*200+14*112
ori_usd_xrt = float(430)      #12.153744 * 35.39
ori_usd_dot = float(254)      #3.00 * 84.77783 + 2.83 * 264.101049 + 281.26 * 2.96 + 3.01 * 1312.15
ori_usd_ewt = float(1669)     #13.23 * 126.078
ori_usd_kda = float(418)      #0.74 * 565.45

#Original investments in ETH

ori_eth_btc = float(0.0050)     
ori_eth_eth = float(107) 
ori_eth_rpl = float(5)     
ori_eth_bat = float(0)
ori_eth_ubt = float(5)     
ori_eth_link = float(9)    
ori_eth_xrt = float(1)      
ori_eth_dot = float(2.5)
ori_eth_ewt = float(3.89)     
ori_eth_kda = float(1)      

print('-##########- 100% complete')

#______________________________________Printing Net Worth Report
#print('eth_bal2',eth_bal2)


print('\n\n______________Report______________','\n\n')
print('''Date:  ''',ct.tm_mday,'/',ct.tm_mon,'/',ct.tm_year,'\n')

coindict2=dict()        #coindict2_definition - dictionary with token symbol in lower case and list with (balance, value in usd, value in aud, value in brl, value in btc, value in eth) in this order
t_usd = 0
t_aud = 0
t_brl = 0
t_btc = 0
t_eth = 0
for (s,b) in coindict.items():      #s - symble of token   b - balence of token
    tlist = list()                   #list with (balance, value in usd, value in aud, value in brl, value in btc, value in eth) in this order
    v_usd = b * usddict[s]
    t_usd = t_usd + v_usd
    v_aud = b * auddict[s]
    t_aud = t_aud + v_aud
    v_brl = b * brldict[s]
    t_brl = t_brl + v_brl
    v_btc = b * btcdict[s]
    t_btc = t_btc + v_btc
    v_eth = b * ethdict[s]
    t_eth = t_eth + v_eth
    print('Amount of',s.upper(),':','                 ',b)
    print('Those coins worth in usd:        ',v_usd)
    print('Those coins worth in aud:        ',v_aud)
    print('Those coins worth in brl:        ',v_brl)
    print('Those coins worth in btc:        ',v_btc)
    print('Those coins worth in eth:        ',v_eth)
    tlist.append(b)
    tlist.append(v_usd)
    tlist.append(v_aud)
    tlist.append(v_brl)
    tlist.append(v_btc)
    tlist.append(v_eth)
    s=s.lower()
    coindict2[s] = coindict2.get(s,tlist)
    print('\n')


print('Net Worth in USD:     ', t_usd)
print('Net Worth in AUD:     ', t_aud)
print('Net Worth in BRL:     ', t_brl)
print('Net Worth in BTC:     ', t_btc)
print('Net Worth in ETH:     ', t_eth,'\n\n')

#____________________________________Calculating portifolio percentages


coindict3 = dict()                        #coindict3_definition - dictionary with token symbols in lower case and their percentages in the portifolio
print('Portifolio percentage')
for (s,b) in coindict.items():
    s=s.lower()
    t2_usd = coindict2[s][1]
    t_per = (t2_usd/t_usd)*100
    coindict3[s]=coindict3.get(s,t_per)
    s=s.upper()
    t_per = str(t_per)
    dotloc = 0
    dotloc = int(t_per.find("."))+4
    print(s,':',t_per[:dotloc],'%')

print('\n')


#____________________________________Updating database



if savetime != datelst[0]:
    cur.execute('''INSERT OR IGNORE INTO Networth (date, netbtc, neteth, netusd, netaud, netbrl) VALUES (?,?,?,?,?,?)''', (savetime,t_btc,t_eth,t_usd,t_aud,t_brl))
    conn.commit()
    for s,l in coindict2.items():
        cur.execute('''SELECT id FROM Coins WHERE symbol = ?''',(s,))
        coinid = cur.fetchall()
        coinid = coinid[0][0]
        cur.execute('''SELECT id FROM Networth WHERE date = ?''',(savetime,))
        dateid = cur.fetchall()
        dateid = dateid[0][0]
        cur.execute('''INSERT OR IGNORE INTO History (coins_id,date_id,balance,value_usd,value_aud,value_brl,value_btc,value_eth) VALUES (?,?,?,?,?,?,?,?)''',(coinid,dateid,l[0],l[1],l[2],l[3],l[4],l[5]))  
    for s,p in coindict3.items():
        cur.execute('''SELECT id FROM Coins WHERE symbol = ?''',(s,))
        coinid = cur.fetchall()
        coinid = coinid[0][0]
        cur.execute('''SELECT id FROM Networth WHERE date = ?''',(savetime,))
        dateid = cur.fetchall()
        dateid = dateid[0][0]
        cur.execute('''INSERT OR IGNORE INTO Portifolio (coins_id,date_id,percentage) VALUES (?,?,?)''',(coinid,dateid,p))
    conn.commit()
    print('Networth values saved to database')


#____________________________________Charts

while True:    
    answer3 = input('Do you want to see the charts for this report? (y/n)\n')
    answer3 = answer3.lower()
    if len(answer3) < 1:
        break
    elif answer3 not in ('yes','no','y','n'):
        print('Sorry, that is not a valid answer.')
        continue
    elif answer3 == 'no' or answer3 == 'n':
        break
    else:
        style.use('dark_background')

        cur.execute('''SELECT date, netbtc, neteth, netusd, netaud, netbrl FROM Networth''')
        networthdata = cur.fetchall()

        datel = list()
        nbtcl = list()
        nethl = list()
        nusdl = list()
        naudl = list()
        nbrll = list()

        for d in networthdata:
            ndate = str(d[0])
            ndate = ndate[-2:]+'.'+ndate[-5:-3]          #+'.'+ndate[:5]
            datel.append(ndate)
            nbtcl.append(float(d[1]))
            nethl.append(float(d[2]))
            nusdl.append(float(d[3]))
            naudl.append(float(d[4]))
            nbrll.append(float(d[5]))

        cur.execute('''SELECT id FROM Networth WHERE date=?''',(savetime,))
        dateid = cur.fetchall()
        dateid = dateid[0][0]

        cur.execute('''SELECT id, symbol FROM Coins''')
        cisl = cur.fetchall()
        cisd = dict()                       #dictionary with coin ID and SYMBOL (data from database)
        for cis in cisl:
            cisd[cis[0]]=cisd.get(cis[0],cis[1])

        cur.execute('''SELECT percentage, coins_id FROM Portifolio WHERE date_id=?''',(dateid,))
        cipl = cur.fetchall()
        cipl = sorted(cipl,reverse=True)
        symbplotl = list()
        perplotl = list()
        for cip in cipl:
            if cip[0] == 0:
                continue
            symbplotl.append(cisd[cip[1]])
            perplotl.append(cip[0])

        symbplotl2 = list()
        perplotl2 = list()
        sypel = list()
        for sy,pe in coindict3.items():
            sypel.append((pe,sy))
        syple = sorted(sypel,reverse=True)
        for sp in sypel:
            symbplotl2.append(sp[1])
            perplotl2.append(sp[0])

        plt.subplot(211)
        plt.plot(datel,nbtcl,'green',label='Networth in BTC',linewidth=5)
        plt.title('Networth in BTC')
        plt.xlabel('Date (Year 2020)')
        plt.ylabel('BTC')
        plt.legend()
        plt.grid(True,color='w')

        plt.subplot(212)
        plt.plot(datel,nethl,'green',label='Networth in ETH',linewidth=5)
        plt.title('Networth in ETH')
        plt.xlabel('Date (Year 2020)')
        plt.ylabel('ETH')
        plt.legend()
        plt.grid(True,color='w')

        plt.show()

        plt.subplot(311)
        plt.plot(datel,nusdl,'green',label='Networth in USD',linewidth=5)
        plt.title('Networth in USD')
        plt.xlabel('Date (Year 2020)')
        plt.ylabel('USD')
        plt.legend()
        plt.grid(True,color='w')

        plt.subplot(312)
        plt.plot(datel,naudl,'green',label='Networth in AUD',linewidth=5)
        plt.title('Networth in AUD')
        plt.xlabel('Date (Year 2020)')
        plt.ylabel('AUD')
        plt.legend()
        plt.grid(True,color='w')

        plt.subplot(313)
        plt.plot(datel,nbrll,'green',label='Networth in BRL',linewidth=5)
        plt.title('Networth in BRL')
        plt.xlabel('Date (Year 2020)')
        plt.ylabel('BRL')
        plt.legend()
        plt.grid(True,color='w')

        plt.show()

        plt.pie(perplotl,labels=symbplotl,colors=['grey','deeppink','b','g','c','m','darkkhaki','teal','orange','mediumaquamarine','mediumslateblue'],startangle=90,shadow=True,autopct='%1.1f%%')
        #plt.pie(perplotl2,labels=symbplotl2,colors=['grey','deeppink','b','g','c','m','darkkhaki','teal','orange','mediumaquamarine','mediumslateblue'],startangle=90,shadow=True,autopct='%1.1f%%')
        plt.title('Portifolio Percentage')

        plt.show()
        break

        #top=0.985,
        #bottom=0.03,
        #left=0.065,
        #right=0.925,
        #hspace=0.2,
        #wspace=0.2
