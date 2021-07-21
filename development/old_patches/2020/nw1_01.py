import urllib.request, urllib.parse, urllib.error
import json
import ssl
#import blockcypher

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('Clenio Net Worth 1.01\n') #First version of Net Worth

#Now supported: 
    #Multiple ETH addresses; 
    #API for AUD and BRL prices; 
    #Data saved in database;
    #Funtion to call prices from CoinGecko.





eth_address=input('Please enter any additional ETH address')
if len(eth_address)<1:
    eth_address1='0x4b4276D6AE2C79064989D14dc6f03f33fa3cf8F7'
    eth_address2='0x335D2d7a806243901172aA676ad36E0bbDF0BD01'

    

#_______________________________________BTC price from CoinGecko
print('\nRetrieving BTC prices from CoinGecko')

url_btc1 = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
uh1 = urllib.request.urlopen(url_btc1, context=ctx)
data1 = uh1.read().decode()
try:
    js_btc_price = json.loads(data1)
except:
    js_btc_price = None
#print(json.dumps(js_btc_price, indent=4),'\n\n')
btc_price_usd = float(js_btc_price['bitcoin']['usd'])


url_btc1 = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eth'
uh1 = urllib.request.urlopen(url_btc1, context=ctx)
data1 = uh1.read().decode()
try:
    js_btc_price = json.loads(data1)
except:
    js_btc_price = None
#print(json.dumps(js_btc_price, indent=4),'\n\n')
btc_price_eth = float(js_btc_price['bitcoin']['eth'])








#_______________________________________BTC balance from blockcypher

#btc_balance = get_address_overview('1L5Bpeue7mDE1d4kwGAEzVgkaC8ziaWu4W')
#blockcypher_token = 'ff67c2cbc54b46dfaaa2d3a09d443e9f'

btc_bal_total = float(0.00015225)








#_______________________________________ETH data from CoinGecko

print('Retrieving ETH prices from CoinGecko')

url_eth1 = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'
uh3 = urllib.request.urlopen(url_eth1, context=ctx)
data2 = uh3.read().decode()
try:
    js_eth_price = json.loads(data2)
except:
    js_eth_price = None
#print(json.dumps(js_eth_price, indent=4),'\n\n')
eth_price_usd = float(js_eth_price['ethereum']['usd'])


url_eth1 = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=btc'
uh3 = urllib.request.urlopen(url_eth1, context=ctx)
data2 = uh3.read().decode()
try:
    js_eth_price = json.loads(data2)
except:
    js_eth_price = None
#print(json.dumps(js_eth_price, indent=4),'\n\n')
eth_price_btc = float(js_eth_price['ethereum']['btc'])







#_______________________________________ETH_Etherscan
     
url_part1 = 'https://api.etherscan.io/api?module=account&action=balance&address='
url_part2 = '&tag=latest&apikey='
api_key_etherscan = 'FFFIW9CIYG769PYH39XVG26Q8SWX1552UJ'
url_eth2 = url_part1 + eth_address1 + url_part2 + api_key_etherscan

uh4 = urllib.request.urlopen(url_eth2, context=ctx)
data = uh4.read().decode()
try:
    js_eth_bal = json.loads(data)
except:
    js_eth_bal = None
#print(json.dumps(js_eth_bal, indent=4),'\n\n')

eth_bal1 = float(js_eth_bal['result'])/1000000000000000000

eth_bal_total = eth_bal1









#_______________________________________LINK_

#part1 = ' https://api.blockcypher.com/v1/eth/main/contracts/0x514910771af9ca656af840dff83e8264ecf986ca/balanceOf?token=$TOKEN'
#rest = 'token=$TOKEN'
#parameters = { "private": "ff67c2cbc54b46dfaaa2d3a09d443e9f", "gas_limit": 20000, "params": ["0x4b4276D6AE2C79064989D14dc6f03f33fa3cf8F7"] }
#part2 = urllib.parse.urlencode(parameters)
#url_0 = part1 + part2
#print('Retrieving BTC prices from', url_0)
#uh = urllib.request.urlopen(url_0, context=ctx)
#data = uh.read().decode()
#print(data)

link_bal_total = float(257.8872676413)




#_______________________________________LINK data from CoinGecko

print('Retrieving LINK prices from CoinGecko')

url_link = 'https://api.coingecko.com/api/v3/simple/price?ids=chainlink&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'
uh3 = urllib.request.urlopen(url_link, context=ctx)
data2 = uh3.read().decode()
try:
    js_link_price = json.loads(data2)
except:
    js_link_price = None
#print(json.dumps(js_link_price, indent=4),'\n\n')
link_price_usd = float(js_link_price['chainlink']['usd'])


url_link = 'https://api.coingecko.com/api/v3/simple/price?ids=chainlink&vs_currencies=btc&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'
uh3 = urllib.request.urlopen(url_link, context=ctx)
data2 = uh3.read().decode()
try:
    js_link_price = json.loads(data2)
except:
    js_link_price = None
#print(json.dumps(js_link_price, indent=4),'\n\n')
link_price_btc = float(js_link_price['chainlink']['btc'])


url_link = 'https://api.coingecko.com/api/v3/simple/price?ids=chainlink&vs_currencies=eth&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'
uh3 = urllib.request.urlopen(url_link, context=ctx)
data2 = uh3.read().decode()
try:
    js_link_price = json.loads(data2)
except:
    js_link_price = None
#print(json.dumps(js_link_price, indent=4),'\n\n')
link_price_eth = float(js_link_price['chainlink']['eth'])







#______________________________________Total in usd
print('\n\n______________Report______________','\n\n')

btc_bal_total_usd = btc_bal_total * btc_price_usd
btc_bal_total_btc = btc_bal_total
btc_bal_total_eth = btc_bal_total * btc_price_eth
print('Amount of BTC:        ', btc_bal_total)
print('ETH balance in BTC:   ', btc_bal_total_eth)
print('USD balance in BTC:   ', btc_bal_total_usd,'\n\n')

eth_bal_total_usd = eth_bal_total * eth_price_usd
eth_bal_total_btc = eth_bal_total * eth_price_btc
eth_bal_total_eth = eth_bal_total
print('Amount of ETH:        ', eth_bal_total)
print('BTC balance in ETH:   ', eth_bal_total_btc)
print('USD balance in ETH:   ', eth_bal_total_usd,'\n\n')

link_bal_total_usd = link_bal_total * link_price_usd
link_bal_total_btc = link_bal_total * link_price_btc
link_bal_total_eth = link_bal_total * link_price_eth
print('Amount of LINK:       ', link_bal_total)
print('BTC balance in LINK:  ', link_bal_total_btc)
print('ETH balance in LINK:  ', link_bal_total_eth)
print('USD balance in LINK:  ', link_bal_total_usd,'\n\n')


total_usd = btc_bal_total_usd + eth_bal_total_usd + link_bal_total_usd
total_btc = btc_bal_total_btc + eth_bal_total_btc + link_bal_total_btc 
total_eth = btc_bal_total_eth + eth_bal_total_eth + link_bal_total_eth
usd_aud_rate = float(1.407)
total_aud = total_usd * usd_aud_rate
usd_brl_rate = float(5.238)
total_brl = total_usd * usd_brl_rate
print('Net Worth in BTC:     ', total_btc)
print('Net Worth in ETH:     ', total_eth)
print('Net Worth in USD:     ', total_usd)
print('Net Worth in AUD:     ', total_aud)
print('Net Worth in BRL:     ', total_brl,'\n\n')