import json

coingeckolst = list()
fhand = open('all_coins_in_coingecko.json')
coingeckojs = fhand.read()
coingeckodata = json.loads(coingeckojs)
#print(json.dumps(coingeckodata,indent=4))
for x in range(len(coingeckodata)):
    id = coingeckodata[x]['id']
    #print(id)
    coingeckolst.append(id)

print(coingeckolst)