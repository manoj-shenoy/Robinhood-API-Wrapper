import robin_stocks as rs
from bs4 import BeautifulSoup
import requests
import alpaca_trade_api as tradeapi
import threading
import time, datetime
import pandas as pd
global data
# --- Robinhood Credentials -----
username = ''
password = ''
rs.login(username,password)

# ----- Alpaca Credentials ------
api_key=""
api_secret=""
alpaca_api_base_url="https://paper-api.alpaca.markets"

url = 'https://finance.yahoo.com/gainers'
timeframe = '5min'
start='2020-01-01'
curr_time = datetime.datetime.now()
end=curr_time.strftime('YYYY-MM-DD')
keltner_period=20
kelt_mult=1.0
no_of_stocks_to_trade = 5

# Option specific information
# expirationDate=''
# strike=
# optionType=

# Building Robinhood Profile and User Data
my_stocks=rs.build_holdings()
print('\nMy Stocks',my_stocks)
for key,value in my_stocks.items():
    print(key,value)
    
def WebScraper(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content)

    stock_list=[]
    for i in range(21,31,1):
        ind_stock=str(soup.find_all('a')[i]['href'])
        idx=ind_stock.find('=')
        stk=ind_stock[idx+1:]
        stock_list.append(stk)

    return stock_list

# WebScraper(url=url)
# from WebScraper import WebScraper

daily_stock_list = WebScraper(url=url)
print('\n')
print(daily_stock_list)

tradeapi=tradeapi.REST(api_key,api_secret,alpaca_api_base_url,'v2')

# # ----- Historical Data for Analysis-----
# def historical_data(timeframe):
#     for stock in daily_stock_list:
#         hist_data=api.polygon.historic_agg_v2(stock,1,unadjusted=False,
#                                               timespan=timeframe,
#                                               _from=start, to=end).df
        
# #         hist_data=rs.get_option_historicals(stock,expirationDate=)
#     return hist_data

# # OHLC Data for all stocks in daily list
# stock_data=historical_data(timeframe=timeframe)
# print(stock_data)
# ------------------------------------------

# -------- Algorithm-Keltner Channel-------------
def KeltnerChannel(df, n):
    MA=pd.Series(pd.rolling(df['Close']).mean())
    RangeMA = pd.Series(pd.rolling(df['High'] - df['Low']).mean())
    Upper=MA + RangeMA * kelt_mult
    Lower=MA - RangeMA * kelt_mult
    df = df.join(Upper)
    df = df.join(Lower)
    return df
# ----------------------------------

# ---- Account info, check trading permissions, Cash Balance ------
def account_info():
    # Get account information.
    account = rs.load_account_profile()
    print('\n')
    print(account)
    # Check if account is restricted from trading.
    if account['deactivated']==True:
        print('Account is currently restricted from trading.')
    
    # Check Cash Balance.
    print('\n${} is available as Cash Balance.'.format(account['buying_power']))
    
    print('\n${} is Held as Options Collateral.'.format(account['margin_balances']['cash_held_for_options_collateral']))

account_info()
    
# Wait for mkt to open
def awaitMarketOpen():
    isOpen = tradeapi.get_clock().is_open
    while(not isOpen):
        clock = tradeapi.get_clock()
        openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        timeToOpen = int((openingTime - currTime) / 60)
        print(str(timeToOpen) + " minutes till market open.")
        time.sleep(60)
        isOpen = tradeapi.get_clock().is_open

awaitMarketOpen()

# Determine position size of each asset
def position_sizing():
    account = rs.load_account_profile()
    cash_balance=account['buying_power']
    position_size=round(float(cash_balance)/no_of_stocks_to_trade)
    return position_size

def determine_expirationDate():
    

def get_option_book(daily_stock_list):
    rs.options.get_list_market_data(inputSymbols=daily_stock_list, expirationDate=exp)
#     rs.options.get_option_market_data
    
    


# Submit an order if quantity is above 0.
def submitOrder(qty, stock, side, resp):
    if(qty != 0):
        try:
#             tradeapi.submit_order(stock, qty, side, "market", "day")
            rs.orders.order_buy_option_limit(positionEffect='open',price=)
            print("Market order of | " + str(qty) + " of " + stock + " " + side + " | completed.")
            resp.append(True)
        except:
            print("Order of | " + str(qty) + " of " + stock + " " + side + " | did not go through.")
            resp.append(False)
    else:
        print("Quantity is 0, order of | " + str(qty) + " of " + stock + " " + side + " | not completed.")
        resp.append(True)

# Get a list of all Open positions 5 Mins before Close
def check_Open_Positions_5m_before_close_and_exit():
    
    clock=tradeapi.get_clock()
    closingTime=clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
    currTime=clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    timeToClose=closingTime - currTime

    try:
        if timeToClose < (60*5):
            # List of all open positions
            porfolio=tradeapi.list_positions()

            print("Mkt closing soon, Closing positions")

            for position in portfolio:
                print('\n{} Shares of {}'.format(position.qty, position.symbol))
            
    except:
        if portfolio is Null:
            print ('No Open positions')

# PK5WP4G3RE0BXZCMB6HM            
# zCJ8/9DnsKoiyn4pQWqpIsr9MyLE9IMLlHLQ6yfb
# 
