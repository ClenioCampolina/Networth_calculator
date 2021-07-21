# bigeth = None
# cur.execute('''SELECT id FROM Coins WHERE symbol=?''',('eth',))
# ethid = cur.fetchall()
# ethid = ethid[0][0]
# cur.execute('''SELECT address FROM Addresses WHERE coins_id = ?''',(ethid,))
# ethaddlist = cur.fetchall()
# eth_bal = float(0)
# for adds in ethaddlist:
#     adds = adds[0]
#     #https://api.blockchair.com/ethereum/dashboards/address/0x3282791d6fd713f1e94f4bfd565eaa78b3a0599d?erc_20=true
#     urleth_part1 = 'https://api.blockchair.com/ethereum/dashboards/address/'
#     urleth_part2 = '?limit=1'
#     url_eth = urleth_part1 + adds + urleth_part2
#     #print(url_eth)
#     uheth = urllib.request.urlopen(url_eth, context=ctx)
#     ethdata = uheth.read().decode()
#     try:
#         js_eth = json.loads(ethdata)
#     except:
#         print('It was not possible to get the balances from the eth wallets.')
#         quit()
#     print(json.dumps(js_eth, indent=4),'\n\n')
#     adds = adds.lower()
#     if js_eth['data'][adds]['address']['balance'] == None:
#         continue
#     eth_bal = eth_bal + ((float(js_eth['data'][adds]['address']['balance']))/1000000000000000000)
#     print(eth_bal)

# coindict['eth']=coindict.get('eth',eth_bal)