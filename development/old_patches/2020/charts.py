from matplotlib import pyplot as plt
from matplotlib import style
import sqlite3

conn = sqlite3.connect('networth.sqlite')
#conn = sqlite3.connect('networth_test.sqlite')
cur = conn.cursor()

cur.execute('''SELECT date FROM Networth''')
alldates = cur.fetchall()
datelst=list()
for d in alldates:
    datelst.append(d[0])
datelst = sorted(datelst,reverse=True)

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
    ndate = ndate[-2:]+'.'+ndate[-5:-3]          #+'_'+ndate[:5]
    datel.append(ndate)
    nbtcl.append(float(d[1]))
    nethl.append(float(d[2]))
    nusdl.append(float(d[3]))
    naudl.append(float(d[4]))
    nbrll.append(float(d[5]))

cur.execute('''SELECT id FROM Networth WHERE date=?''',(datelst[0],))
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
plt.title('Portifolio Percentage')

plt.show()

#top=0.985,
#bottom=0.03,
#left=0.065,
#right=0.925,
#hspace=0.2,
#wspace=0.2