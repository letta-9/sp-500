# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 20:04:36 2021

@author: mattb
"""

from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame

##----------------------------------------------------------------------------

sp_response = requests.get('https://www.stockmonitor.com/sp500-stocks/')

sp_soup = Soup(sp_response.text,'lxml')

table_search = sp_soup.find_all('table')

sp_table = table_search[0]

rows = sp_table.find_all('tr')

## Un-Nest Header Row <th class>
header_row = rows[0]
header_row.find_all('th')
y = [str(y.string) for y in header_row.find_all('th')]
y.insert(1, 'Ticker')

## Un-Nest First Data Row <td class>
first_data_row = rows[1]
first_data_row.find_all('td')
x = [str(x.string) for x in first_data_row.find_all('td')]

def parse_none(row):
    return[str(x.string) for x in row.find_all('a')]

none_table = [parse_none(row) for row in rows[1:]]

## Un-Nest the rest of the data rows
def parse_table(row):
    return[str(x.string) for x in row.find_all('td')]

table = [parse_table(row) for row in rows[1:]]

df_none = DataFrame(none_table)

df = DataFrame(table)
df.columns = y
df['Ticker'] = df_none
del df['Change%']
del df['Company']
del df['High']
del df['Low']

df['Price'] = df['Price'].str.strip()
df['Volume'] = df['Volume'].str.strip()

df.set_index('Ticker', inplace=True)

ticker_search = 'DIS' #INPUT STOCK TICKER

print(ticker_search + ' Price Is: ' + df.loc[ticker_search,'Price'])