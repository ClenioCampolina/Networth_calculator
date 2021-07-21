import import_libraries as imp
imp.importing_all()
import url_connect as urlcon
import sqlite_db_operations as sqlf
import time_operations as timeop
import coin_balances as bal
import coingecko as cg
import report as rp
import defi as defi



print('Crypto Net Worth 2021.1.002\n')
#Now supported:
    #       Update the CoinGecko list in the database automatically without losing the values entered in the Blochair column (create a UI to let the user enter the name of the coin in the coingecko so that the software can automatically update the database).
    #       Add a counter for the Blockchair wallet balance requests (apparently they have a limit of requests per IP)
    #       Remove the coins that have balance equal zero from the database
    #       Mechanism to define what account is the default (in the database, create a table for all accounts in that machine and define which is the default).






# #_______________________________________Url connection operations

# urlcon.context_with_no_certificate_check()      # Ignore SSL certificate errors




#_______________________________________Database operations



db_file_name = sqlf.database_file_name()           #It asks what account name should be loaded. If nothing is enteed, the default is selected
 
sqlf.addcursor(db_file_name)        #It creates the "cur" cursor to make database operations

sqlf.create_or_check_db_tables()    #It checks if the nacessary tables of the user database already exist. If not it inserts them.

sqlf.insert_classic_coins()         #it checks if the main blockchain coins such as btc, eth, dot already is in the users database. If not, it inserts them.
        
sqlf.userinterface()                #It allows the users to add coins, currencies and addresses

sqlf.coingecko_db_update()          #Update the "Names_database" table to get all the coingecko listed coins. All exceptions are also added to the list.






print('\nLoading data')
print('\n-__________- 00% complete')



##_______________________________________Time Settings

savetime = timeop.savetime()
datelst = sqlf.last_saved_date()





##_______________________________________Checking All Balances

coindict = dict()   #coindict_definition - This dictionary is NOT temporary and it saves the symbol of the coins/tokens and their balances



#_______________________________________BTC balance from blockchair


# btc_bal = float(0.00015225)
btc_bal = bal.btc_balance()
coindict['btc']=coindict.get('btc',btc_bal)
#print (btc_bal)









#_______________________________________ETH balance from Etherscan


eth_bal = bal.eth_balance()
coindict['eth']=coindict.get('eth',eth_bal)
#print(eth_bal)

print('-####______- 20% complete')







#_______________________________________ERC-20 Tokens from blockchair

tnamedict = dict()      #tnamedict_definition - This dictionary is NOT temporary and it saves the coin/token symbol and the coin/token name from coingecko
bal.erc20_balance(coindict,tnamedict)
#print(coindict)
#print(tnamedict)

print('-####______- 40% complete')







#______________________________________DOT balance from 


dot_bal = bal.dot_balance()
coindict['dot']=coindict.get('dot',dot_bal)
#print(dot_bal)
#print(coindict)







#______________________________________Other coins


# kda_bal = float(0)  #HOTBIT
# coindict['kda']=coindict.get('kda',kda_bal)

# ewt_bal = float(0)  #Kucoin or Liquid
# coindict['ewt']=coindict.get('ewt',ewt_bal)


print('-######____- 60% complete')



#______________________________________Maker Dao Balances from Zapper

maker_debt = bal.maker(coindict,tnamedict)
total_debt = maker_debt

#REMEMBER TO REPORT AND SUBTRACT THE DEBT AT THE END. AS DEBT ONLY COMES IN USD, DIVIDE THE TOTALS (EX: TOTAL_AUD/TOTAL_USD TO GET THE RATES FOR ALL CURRENCIES)

#print(total_debt)



#_________________________________________________CoinGecko


usddict, auddict, brldict, btcdict, ethdict, allprices = cg.get_prices()

#print(usddict, auddict, brldict, btcdict, ethdict, allprices)

print('-########__- 80% complete')







#_________________________________________________Remove zero balances


sqlf.remove_zero_balances(coindict)








#_________________________________________________Original Investment


#original_investments.py 

print('-##########- 100% complete')








#______________________________________Printing Net Worth Report
#print('eth_bal2',eth_bal2)

rp.heading()

coindict2=dict()                          #coindict2_definition - dictionary with token symbol in lower case and list with (balance, value in usd, value in aud, value in brl, value in btc, value in eth) in this order
coindict2, t_usd, t_aud, t_brl, t_btc, t_eth = rp.balances_in_currencies(coindict,usddict,auddict,brldict,btcdict,ethdict,total_debt,maker_debt)










#____________________________________Calculating portifolio percentages


coindict3 = dict()                        #coindict3_definition - dictionary with token symbols in lower case and their percentages in the portifolio
rp.portifolio_percentages(coindict,coindict2,coindict3,t_usd,total_debt)










#____________________________________Updating database


sqlf.updating_database(savetime, datelst,t_btc,t_eth,t_usd,t_aud,t_brl,coindict2,coindict3)










#____________________________________Charts

rp.charts(savetime,coindict3)
