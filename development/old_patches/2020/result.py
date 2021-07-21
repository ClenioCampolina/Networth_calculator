import json

data1 = '''
{
    "bitcoin": {"usd": 11296.4}
}'''


data2='''
{
    "ethereum": {"usd": 368.94}
}'''


data3='''
{
    "status": "1",
    "message": "OK",
    "result": "109371736221990928000"
}'''

js1 = json.loads(data1)

price = js1['bitcoin']['usd']

print(price)
