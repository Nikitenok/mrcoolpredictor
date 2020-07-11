import yfinance as yf # https://github.com/ranaroussi/yfinance
from pandas_datareader import data as pdr
import sqlite3


class Parser:
    
    symbols = ['NOC']
    period='10y'
    interval = "1mo"

    def create_tables(self,symbols,c):

        for i in symbols:

            execute = ('drop table if exists {}').format(i)
            c.executescript(execute)   

            execute = ('CREATE TABLE {} (date DATE PRIMARY KEY, Close FLOAT(15))').format(i)
            c.execute(execute)
            
    def update_data(self, upd_syms=symbols):

        with sqlite3.connect("db.sqlite3") as x:
            c = x.cursor()
            self.create_tables(upd_syms,c)
            x.commit()
            self.insert_rows(upd_syms, self.period, self.interval, c)
            x.commit()


    def insert_rows(self,symbols, period, interval, c):

        drop_cols = ['Adj Close', 'Open', 'Low', 'High', 'Volume']

        for i in symbols:

            data = pdr.get_data_yahoo(i, period=period,interval = interval)        
            data = data.drop(drop_cols, axis=1)
            data = data.dropna()
            print(i)
            data = data.Close.resample('MS').mean().to_frame()


            for j in range(data.shape[0]):

                formatted_date = data.index[j].strftime('%Y-%m-%d')
                c.execute("INSERT INTO "+ i +" (date, Close) VALUES (?, ?)", (formatted_date, str(data.Close[j])))

    def __init__(self):
        
        yf.pdr_override()
       
    
    def init_data(self):

        with sqlite3.connect("db.sqlite3") as x:
            c = x.cursor()

            self.create_tables(self.symbols,c)
            x.commit()
            self.insert_rows(self.symbols, self.period, self.interval, c)
            x.commit()

