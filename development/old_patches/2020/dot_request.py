import requests
import json

url_dot = "https://polkadot.subscan.io/api/open/account"
payload = "{\n\t\"address\": \"15yquC1wuBiJTLdA1q8dNAbniDSZEz8kx3g9MmftJZHWmy6Q\"\n}"
headers = {'Content-Type': 'application/json'}

response = requests.request("POST", url_dot, headers=headers, data = payload)
dotdata = response.text.encode('utf8')

js_dot = json.loads(dotdata)

print(payload)

#print(json.dumps(js_dot, indent=4),'\n\n')
#print(js_dot['data']['balance'])