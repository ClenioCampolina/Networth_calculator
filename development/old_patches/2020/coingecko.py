def coingecko():
    alldata = dict()
    
    bigstr=None
    for (k,v) in coinsdict.items():
        if bigstr == None:
            bigstr = v+'%2C'
        else:
            bigstr = bigstr+v+'%2C'
    bigstr = bigstr[:-3]
    #print(bigstr)
    
    bigcur=None
    for c in currencylist:
        if bigcur == None:
            bigcur = c+'%2C'
        else:
            bigcur = bigcur+c+'%2C'
    bigcur = bigcur[:-3]
    #print(bigstr)

    print('Retrieving coin prices from CoinGecko')
    url_cg = 'https://api.coingecko.com/api/v3/simple/price?ids='+bigstr+'&vs_currencies='+bigcur+'&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'
    uh = urllib.request.urlopen(url_cg, context=ctx)
    data = uh.read().decode()
    try:
        js = json.loads(data)
    except:
        js = None
    #print(json.dumps(js, indent=4),'\n\n')

    for currency in currencylist:
        for (k,v) in coinsdict.items():
            if k == currency:
                continue
            price = float(js[v][currency])
            market_cap = float(js[v][currency+'_market_cap'])
            vol24h = float(js[v][currency+'_24h_vol'])
            change24h = float(js[v][currency+'_24h_change'])
            coindata = (price,market_cap,vol24h,change24h)
            comb = k+'_'+currency
            alldata[comb]=alldata.get(comb,coindata)       
    return alldata


fulldata = coingecko()