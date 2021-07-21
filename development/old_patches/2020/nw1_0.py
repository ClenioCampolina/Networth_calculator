import urllib.request, urllib.parse, urllib.error
import json
import ssl
#import blockcypher

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('Clenio Net Worth 1.02\n')   

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

url_btc1 = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
print('\nRetrieving BTC prices from CoinGecko')
uh1 = urllib.request.urlopen(url_btc1, context=ctx)
data1 = uh1.read().decode()
try:
    js_btc_price = json.loads(data1)
except:
    js_btc_price = None
#print(json.dumps(js_btc_price, indent=4),'\n\n')
btc_price_usd = float(js_btc_price['bitcoin']['usd'])






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






#______________________________________Total in usd
print('\n\n______________Report______________','\n\n')

btc_bal_total_usd = btc_bal_total * btc_price_usd
print('Amount of BTC:       ', btc_bal_total)
print('USD balance in BTC   ', btc_bal_total_usd,'\n\n')

eth_bal_total_usd = eth_bal_total * eth_price_usd
eth_bal_total_btc = eth_bal_total * eth_price_btc
print('Amount of ETH:       ', eth_bal_total)
print('BTC balance in ETH:  ', eth_bal_total_btc)
print('USD balance in ETH:  ', eth_bal_total_usd,'\n\n')

total_btc = btc_bal_total + eth_bal_total_btc
total_usd = btc_bal_total_usd + eth_bal_total_usd
print('Net Worth in BTC:    ', total_btc)
print('Net Worth in USD:    ', total_usd,'\n\n')
