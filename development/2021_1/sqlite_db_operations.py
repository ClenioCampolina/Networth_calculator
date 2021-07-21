#functions to run the database operations


#Just adding this bit to avoid the editor marking this file as an error
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3
import time
import requests
from matplotlib import pyplot as plt
from matplotlib import style

conn = sqlite3.connect('networth.sqlite')
cur = conn.cursor()
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



#Functions

def database_file_name():
    db_file_name = input("Please enter the name of the account:\n")
    if len(db_file_name) < 1:
        db_file_name = "net.sqlite"
    return db_file_name


def addcursor(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    #print ("Cur cursor created")



def create_or_check_db_tables():

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
    
    #print("tables created or checked")



def insert_classic_coins():
    cur.execute('''SELECT symbol FROM Coins''')
    coindatabase = cur.fetchall()
    #print(coindatabase)
    coindatabase2=list()
    for o in coindatabase:
        coindatabase2.append(o[0])
    coindatabase = coindatabase2
    #print(coindatabase2)

    for i in ('btc','eth','dot','ewt','kda','total_debt'):
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
        if i not in coindatabase and i == 'total_debt':
            cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES ('Total-debt-across-all-defi-protocols','total_debt')''')
            conn.commit()



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



def userinterface():
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



def coingecko_db_update():
    while True:
        answer3 = input('\nDo you wish to update your Database? (y/n)\n')

        if len(answer3) < 1:
            addcgnames = True
            break 
        else:
            answer3 = answer3.lower()
            if answer3 not in ('yes','no','y','n'):
                print('Sorry, that is not a valid answer.')
                continue
            elif answer3 in ('yes','y'):
                addcgnames = True
                break
            else:
                addcgnames = False
                break


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
            #READ ME      READ ME     READ MEEEEEEE     Before adding new exceptions, remember to replace all spaces for "-" and put all letters in lower case
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
            elif id == 'dai':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'dai-stablecoin'))
            elif id == 'aave-link':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'aave-interest-bearing-link'))
            elif id == 'index-cooperative':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'index'))
            elif id == 'yearn-finance':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'yearn.finance'))
            elif id == 'the-graph':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'graph-token'))
            elif id == 'tornado-cash':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'tornadocash'))
            elif id == 'vesper-finance':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'vespertoken'))
            elif id == 'sushi':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'sushitoken'))
            elif id == 'alpha-finance':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'alphatoken'))    
            elif id == 'xsushi':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'sushibar'))
            elif id == 'aave':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'aave-token'))
            elif id == 'bankless-dao':
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko,blockchair) VALUES (?,?)''',(id,'bankless-token'))
            else:
                cur.execute('''INSERT OR IGNORE INTO Names_database (coingecko) VALUES (?)''',(id,))
        conn.commit()
        #print("Exceptions added")



def last_saved_date():
    cur.execute('''SELECT date FROM Networth''')
    alldates = cur.fetchall()
    datelst=list()
    for d in alldates:
        datelst.append(d[0])
    datelst = sorted(datelst,reverse=True)
    #print("Last saved date created")
    return datelst[0]



def get_coin_id(coin):
    cur.execute('''SELECT id FROM Coins WHERE symbol=?''',(coin,))
    coinid = cur.fetchall()
    coinid = coinid[0][0]
    #print("got coin id")
    return coinid



def get_addresses_list_of_a_coin(coin):
    coinid = get_coin_id(coin)
    cur.execute('''SELECT address FROM Addresses WHERE coins_id = ?''',(coinid,))
    coinaddlist = cur.fetchall()
    #print("got address list")
    return coinaddlist



def get_list_of_coingecko_tokens_from_table():
    cur.execute('''SELECT coingecko FROM Names_database''')
    coingeckolst = cur.fetchall()
    return coingeckolst



def get_the_coingecko_token_name_using_the_blockchair_name(tokenname):
    cur.execute('''SELECT Names_database.coingecko FROM Names_database WHERE Names_database.blockchair = ?''',(tokenname,))
    try:
        tokenname = cur.fetchone()[0]
        return tokenname
    except:
        #print('The token name {} was not added as an exception in the column blockchair of the Names_database table. Please find out what name coingecko uses for this coin and add {} to the blockchair column (remember to replace all spaces for "-" and put all letters in lower case).'.format(original,original))
        #Every time this code runs, add this new exception to the list in the begining of the section "ERC-20 Tokens from blockchair" (scroll up a bit)
        #quit()
        cgname = input('\nCoinGecko and Blockchair do not use the same name for a specific token, Blockchair uses the following name: {}.\nPlease locate this token in the CoinGecko column and enter {} in the Blockchair column in the database.\nRemember to replace all spaces for "-" and put all letters in lower case\n'.format(original,original))
        print('Please run the program again and select YES to update your Database. The program will finish now.')
        quit()
        cur.execute('''UPDATE Names_database SET blockchair = ? WHERE coingecko = ? ''',(tokenname,cgname))
        conn.commit()
        cur.execute('''SELECT Names_database.coingecko FROM Names_database WHERE Names_database.blockchair = ?''',(tokenname,))
        tokenname = cur.fetchone()[0]



def list_of_all_coins_symbols_from_coins_table():
    cur.execute('''SELECT symbol FROM Coins''')
    coindatabase = cur.fetchall()
    #print(coindatabase)
    coindatabase2=list()
    for o in coindatabase:
        coindatabase2.append(o[0])
    coindatabase = coindatabase2
    #print(coindatabase2)
    return coindatabase


def get_name_of_coin_from_symbol(tokensymbol):
    cur.execute('''SELECT coin FROM Coins WHERE symbol = ?''',(tokensymbol,))
    tokenname = cur.fetchall()[0]
    return tokenname


def insert_coin_in_coins_table(name,symbol):
    cur.execute('''INSERT OR IGNORE INTO Coins (coin, symbol) VALUES (?,?)''',(name,symbol))
    conn.commit()



def get_currency_list():
    cur.execute('''SELECT symbol FROM Currencies''')
    currencylist = cur.fetchall()
    return currencylist



def get_the_total_number_of_coins():
    cur.execute('''SELECT coin FROM Coins''')
    numcoins = cur.fetchall()
    return len(numcoins)

def get_dict_coinname_and_symbol():
    coinsdict = dict()
    numcoins = range(get_the_total_number_of_coins())
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
    return coinsdict


def remove_zero_balances(coindict):
    #add function to remove coins from database that have zero balances
    # for (s,b) in coindict.items():      #s - symble of token   b - balence of token
    #     if b <= 0:
    return



def updating_database(savetime,datelst,t_btc,t_eth,t_usd,t_aud,t_brl,coindict2,coindict3):
    if savetime != datelst:
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


def networthdata():
    cur.execute('''SELECT date, netbtc, neteth, netusd, netaud, netbrl FROM Networth''')
    networthdata = cur.fetchall()
    return networthdata


def get_id_of_last_saved_date(savetime):
    cur.execute('''SELECT id FROM Networth WHERE date=?''',(savetime,))
    dateid = cur.fetchall()
    dateid = dateid[0][0]
    return dateid


def get_dict_coinid_and_symbol():
    cur.execute('''SELECT id, symbol FROM Coins''')
    cisl = cur.fetchall()
    cisd = dict()                       #dictionary with coin ID and SYMBOL (data from database)
    for cis in cisl:
        cisd[cis[0]]=cisd.get(cis[0],cis[1])
    return cisd


def get_lists_of_portifolio_percentages_and_symbols_for_plot(savetime):
    dateid = get_id_of_last_saved_date(savetime)
    cisd = get_dict_coinid_and_symbol()
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
    return perplotl, symbplotl


