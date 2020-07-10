import statsmodels.api as sm
import numpy as np
import pandas as pd
import sqlite3

from itertools import product
from scipy import stats
from dateutil.relativedelta import relativedelta

import warnings

warnings.simplefilter("ignore")


class Arima:
    _def_syms = ['NOC', 'LUV', 'NI', 'SPGI', 'NTAP', 'EXR', 'AAPL']

    def invboxcox(self, y, lbd):
        if lbd == 0:
            return (np.exp(y))
        else:
            return (np.exp(np.log(lbd * y + 1) / lbd))

    def arima(self, X, syms):
        Xdict = dict()
        for i in range(len(X)):
            p = q = range(0, 2)
            P = Q = range(0, 2)
            D = 1
            d = 1
            parameters = product(p, q, P, Q)
            parameters_list = list(parameters)

            X[i]['close_1'], lmbda = stats.boxcox(X[i].close)
            X[i]['close_1_diff'] = X[i].close_1 - X[i].close_1.shift(12)
            X[i]['close_2'] = X[i]['close_1_diff'] - X[i]['close_1_diff'].shift(1)

            results = []
            best_aic = float("inf")
            warnings.filterwarnings('ignore')

            for param in parameters_list:
                try:
                    model = sm.tsa.statespace.SARIMAX(X[i].close_1, order=(param[0], d, param[1]),
                                                      seasonal_order=(param[2], D, param[3], 12)).fit(disp=-1)
                except ValueError:
                    continue
                aic = model.aic

                if aic < best_aic:
                    best_model = model
                    best_aic = aic
                    best_param = param
                results.append([param, model.aic])

            X[i]['model'] = self.invboxcox(best_model.fittedvalues, lmbda)

            last_month = (X[i].tail(1).index)[0]
            start = X[i].shape[0] - 1
            date_list = [last_month
                         + relativedelta(months=i) for i in range(1, 12)]
            future = pd.DataFrame(index=date_list, columns=X[i].columns)

            X[i] = pd.concat([X[i], future])
            X[i]['forecast'] = self.invboxcox(best_model.predict(start=start, end=start + 12), lmbda)
            X[i] = X[i].drop(['close_1', 'close_1_diff', 'close_2', 'model'], axis=1)
            Xdict[syms[i]] = X[i]

            with sqlite3.connect("db.sqlite3") as x:
                c = x.cursor()
                new_sym = syms[i]+"F"
                execute = ('drop table if exists {}').format(new_sym)
                c.executescript(execute)
                execute = ('CREATE TABLE {} (date DATE PRIMARY KEY, close FLOAT(15), forecast FLOAT(15))').format(new_sym)
                c.execute(execute)

                for j in range(X[i].shape[0]):
                    formatted_date = X[i].index[j].strftime('%Y-%m-%d')
                    c.execute("INSERT INTO " + new_sym + " (date, close, forecast) VALUES (?, ?, ?)", (formatted_date, str(X[i].close[j]), str(X[i].forecast[j])))
                x.commit()
            print(syms[i])

        return Xdict

    def get_data(self, syms=_def_syms):
        X = []
        with sqlite3.connect("db.sqlite3") as x:
            c = x.cursor()

            for s in syms:
                df = pd.DataFrame([i for i in c.execute(('SELECT date, Close FROM {} ORDER BY date').format(s))],
                                columns=["date", "close"])
                df['date'] = df['date'].apply(pd.to_datetime)
                df = df.set_index('date')
                X.append(df)

        return X

    #####################################################################

    def get_preds(self, syms=_def_syms):
        new_dict = dict()
        for s in syms:
            new_i = s+"F"
            try:
                with sqlite3.connect("db.sqlite3") as x:
                    c = x.cursor()
                    df = pd.DataFrame([i for i in c.execute(('SELECT date, close, forecast FROM {} ORDER BY date').format(new_i))],
                                      columns=["date", "close", "forecast"])
                    new_dict[s] = df
            except Exception:
                print('symbol is not found')
        return new_dict

    def make_predictions(self):
        try:
            x = self.get_data(self._syms)
            self.pred_dict = self.arima(x, self._syms)
            print("got a forecast")
        except Exception:
            print('data is not found')

    #####################################################################

    def __init__(self, symbols=_def_syms):
        self._syms = symbols
        self.pred_dict = None