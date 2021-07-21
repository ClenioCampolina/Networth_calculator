import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3
import time
import requests
from matplotlib import pyplot as plt
from matplotlib import style

import import_libraries as imp
imp.importing_all()
import sqlite_db_operations as sqlf
import url_connect as urlcon
ctx = urlcon.context_with_no_certificate_check()
import time_operations as timeop



def heading():
    print('\n\n______________Report______________','\n')
    print('''Date:  ''',timeop.day(),'/',timeop.month(),'/',timeop.year(),'\n')


def balances_in_currencies(coindict,usddict,auddict,brldict,btcdict,ethdict,total_debt,maker_debt):
    print('___________________________________________________')
    print('\n','Portifolio report','\n')    

    coindict2=dict()
    t_usd = 0
    t_aud = 0
    t_brl = 0
    t_btc = 0
    t_eth = 0
    for (s,b) in coindict.items():      #s - symble of token   b - balence of token
        if b <= 0:
            continue
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


    total_debt_usd = total_debt
    total_debt_aud = total_debt*(t_aud/t_usd)
    total_debt_brl = total_debt*(t_brl/t_usd)
    total_debt_btc = total_debt*(t_btc/t_usd)
    total_debt_eth = total_debt*(t_eth/t_usd)


    debt_list = (total_debt,total_debt_usd,total_debt_aud,total_debt_brl,total_debt_btc,total_debt_eth)
    coindict2['total_debt'] = coindict2.get('total_debt',debt_list)


    t_usd = t_usd + total_debt_usd
    t_aud = t_aud + total_debt_aud
    t_brl = t_brl + total_debt_brl
    t_btc = t_btc + total_debt_btc
    t_eth = t_eth + total_debt_eth

    print('___________________________________________________')
    print('\n','Totals report','\n')
    print('Net Worth in USD:     ', t_usd)
    print('Net Worth in AUD:     ', t_aud)
    print('Net Worth in BRL:     ', t_brl)
    print('Net Worth in BTC:     ', t_btc)
    print('Net Worth in ETH:     ', t_eth,'\n\n')
    
    print('___________________________________________________')
    print('\n','Debt report','\n')
    print('Debt on Maker Dao:     ', maker_debt)
    print('Debt on Alchemix:      ', 0,'\n')
    
    print('Total Debt in USD:     ', total_debt_usd)
    print('Total Debt in AUD:     ', total_debt_aud)
    print('Total Debt in BRL:     ', total_debt_brl)
    print('Total Debt in BTC:     ', total_debt_btc)
    print('Total Debt in ETH:     ', total_debt_eth,'\n\n')




    return coindict2, t_usd, t_aud, t_brl, t_btc, t_eth


def portifolio_percentages(coindict,coindict2,coindict3,t_usd,total_debt):
    print('___________________________________________________')
    print('\n','Percentage report','\n')

    t_usd = t_usd - total_debt

    for (s,b) in coindict.items():
        s=s.lower()
        try:
            t2_usd = coindict2[s][1]
        except:
            continue
        if t2_usd < 1:
            continue
        if s == 'total_debt':
            continue
        t_per = (t2_usd/t_usd)*100
        coindict3[s]=coindict3.get(s,t_per)
        s=s.upper()
        t_per = str(t_per)
        dotloc = 0
        dotloc = int(t_per.find("."))+4
        print(s,':',t_per[:dotloc],'%')

    print('\n')



def charts(savetime,coindict3):
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

            networthdata = sqlf.networthdata()

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

            perplotl, symbplotl = sqlf.get_lists_of_portifolio_percentages_and_symbols_for_plot(savetime)

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
            plt.xlabel('Time')
            plt.ylabel('BTC')
            plt.legend()
            plt.grid(True,color='w',axis='y')

            plt.subplot(212)
            plt.plot(datel,nethl,'green',label='Networth in ETH',linewidth=5)
            plt.title('Networth in ETH')
            plt.xlabel('Time')
            plt.ylabel('ETH')
            plt.legend()
            plt.grid(True,color='w',axis='y')

            plt.show()

            plt.subplot(311)
            plt.plot(datel,nusdl,'green',label='Networth in USD',linewidth=5)
            plt.title('Networth in USD')
            #plt.xlabel('Time')
            plt.ylabel('USD')
            plt.legend()
            plt.grid(True,color='w',axis='y')

            plt.subplot(312)
            plt.plot(datel,naudl,'green',label='Networth in AUD',linewidth=5)
            plt.title('Networth in AUD')
            #plt.xlabel('Time')
            plt.ylabel('AUD')
            plt.legend()
            plt.grid(True,color='w',axis='y')

            plt.subplot(313)
            plt.plot(datel,nbrll,'green',label='Networth in BRL',linewidth=5)
            plt.title('Networth in BRL')
            #plt.xlabel('Time')
            plt.ylabel('BRL')
            plt.legend()
            plt.grid(True,color='w',axis='y')

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