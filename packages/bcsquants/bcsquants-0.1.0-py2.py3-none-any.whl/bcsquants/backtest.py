# -*- coding: utf-8 -*-
# Это упрощенная версия бэктеста, который используется на сервере https://bcsquants.com
# Разработчик Дмитрий Ивановский <dima-iv@mail.ru>

from __future__ import print_function
from datetime import datetime as dt
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plotticker

orderList = []
orderEvent = False
tickSizeToSeconds = {'s1': 1, 's5': 5, 'm1': 60, 'm5': 300}
dataKeys = ['time', 'open', 'high', 'low', 'close', 'volume', 'count']
tickKeys = ['direct', 'takeProfit', 'stopLoss', 'holdPeriod', 'datetime']
FEE = 0.0002 # комиссия
allTickers = ['ALRS', 'SNGS', 'MGNT', 'ROSN', 'MOEX', 'VTBR', 'LKOH', 'GAZP', 'SBERP', 'SBER', # акции
              'USD000UTSTOM', # валюта
              'RTSI', 'MICEXINDEXCF', # индексы
              'GZX', 'SIX', 'BRX'] # фъючерсы
_tickSize = 'm5'

def showBacktestResult(result):
    return pd.DataFrame(result, index=[x['ticker'] for x in result],
                                columns=['sumProcent', 'maxDrawdown', 'std',
                                         'minV', 'numDeals',
                                         'sumTakeProfit', 'sumHoldPeriod', 'sumStopLoss'])

def getBacktestResult(init, tick, tickers=allTickers, skipMessage=False, progressBar=True):
    result = []
    if not isinstance(tickers, list):
        tickers = [tickers]
    for ticker in tickers:
        orderList, orderEvent = [], False
        _tickSize, orderList, data = runTick(init, tick, ticker)
        res = runOrder(ticker, _tickSize, orderList, data)
        res['ticker'] = ticker
        res['_tickSize'] = _tickSize
        result.append(res)
        if progressBar:
            print(ticker, end='\n' if ticker == tickers[-1] else ', ')

    if not skipMessage:
        print('Не забудьте вы можете посмотреть тики и заявки в соответствующих файлах')
        print('tickFile = data/order/TICKER_{0}_tick.csv'.format(_tickSize))
        print('orderFile = data/order/TICKER_{0}_order.csv'.format(_tickSize))

    return result

def order(direct, takeProfit, stopLoss, holdPeriod):
    global orderList, orderEvent, tickSizeToSeconds, _tickSize
    if not isinstance(holdPeriod, int):
        raise Exception('Hold period must be int type. If you use division with operator /, ' +
                        'remember in python3 this operation converts result to float type, ' +
                        'use // instead or convert to int directly')
    if holdPeriod * tickSizeToSeconds[_tickSize] < 300:
        raise Exception('Hold period must be not less than 300 seconds')
    if takeProfit < 0.0004:
        raise Exception('Take profit must be not less than 0.0004')
    if stopLoss < 0.0004:
        raise Exception('Stop loss must be not less than 0.0004')
    orderList.append([direct, takeProfit, stopLoss, holdPeriod])
    orderEvent = True

def runTick(init, tick, ticker):
    global orderList, orderEvent, _tickSize
    orderList, orderEvent = [], False

    class Empty:
        pass
    self = Empty()
    init(self)

    _tickSize = getattr(self, '_tickSize', 'm5')
    _window = getattr(self, '_window', None)
    if _window is not None:
        _window = int(_window)

    data = {key: np.load('data/{0}/{1}/{2}.npy'.format(ticker, _tickSize, key), encoding='bytes') for key in dataKeys }

    for ind in range(1, len(data['time'])):
        if _window:
            if ind < _window:
                continue
            else:
                tick(self, { key: data[key][ind - _window:ind] for key in dataKeys })
        else:
            tick(self, { key: data[key][:ind] for key in dataKeys })

        if orderEvent:
            for jnd in range(len(orderList) - 1, -1, -1): # [len(orderList) - 1, ..., 0]
                if len(orderList[jnd]) == 4:
                    orderList[jnd].append(data['time'][ind])
                else:
                    break
            orderEvent = False

    with open('data/order/{0}_{1}_tick.csv'.format(ticker, _tickSize), 'w') as file:
        file.write(';'.join(tickKeys) + '\n')
        for order in orderList:
            file.write(';'.join([str(elem) for elem in order]) + '\n')

    return _tickSize, orderList, data

def runOrder(ticker, _tickSize, orderList, dataNpy):
    measure = {'deals': [], 'sumProcent': 0.0, 'sumTakeProfit': 0, 'sumStopLoss': 0, 'sumHoldPeriod': 0, 'numDeals': 0}
    currentDataNum, firstTime, preLastCandle = -1, True, False
    for order in orderList:
        if preLastCandle:
            break
        order = dict(zip(tickKeys, order))

        mode = 'findOrder'
        if firstTime or data['time'] <= order['datetime']:
            while (not preLastCandle) and mode != 'Exit':
                currentDataNum += 1
                if currentDataNum >= len(dataNpy['time']) - 2:
                    preLastCandle = True

                data = {key: dataNpy[key][currentDataNum] for key in dataKeys}

                if mode == 'findOrder':
                    if data['time'] >= order['datetime']:
                        priceEnter = data['close']
                        numEnter = currentDataNum
                        datetimeEnter = data['time']
                        mode = 'doOrder'
                elif mode == 'doOrder':
                    currentDatetime = data['time']
                    procentUp = data['high'] / priceEnter - 1.
                    procentDown = data['low'] / priceEnter - 1.
                    holdPeriod = order['holdPeriod']
                    isHoldPeriod = preLastCandle or (currentDataNum - numEnter + 1 > holdPeriod)

                    if order['direct'] == 'buy':
                        takeProfit = (procentUp >= order['takeProfit'])
                        stopLoss = (procentDown <= -order['stopLoss'])
                    else: # order['direct'] == 'sell
                        takeProfit = (procentDown <= -order['takeProfit'])
                        stopLoss = (procentUp >= order['stopLoss'])

                    if takeProfit or stopLoss or isHoldPeriod:
                        event = 'holdPeriod'
                        nextDatetime = dataNpy['time'][currentDataNum + 1]
                        nextClose = dataNpy['close'][currentDataNum + 1]
                        direct = {'buy': 1, 'sell': -1}[order['direct']]
                        procent = (nextClose / priceEnter - 1.) * direct - 2 * FEE
                        if takeProfit:
                            event = 'takeProfit'
                        if stopLoss:
                            event = 'stopLoss'
                        measure['deals'].append({
                            'procent': procent,
                            'event': event,
                            'direct': order['direct'],
                            'datetimeEnter': datetimeEnter,
                            'datetimeExit': nextDatetime,
                            'priceEnter': priceEnter,
                            'priceExit': nextClose,
                            'datetimeEnterInd': numEnter,
                            'datetimeExitInd': currentDataNum + 1,
                        })
                        mode = 'Exit'
        firstTime = False

    mapEventDirect = {'takeProfit': 'sumTakeProfit', 'holdPeriod': 'sumHoldPeriod', 'stopLoss': 'sumStopLoss'}
    portfolio = []
    for deal in measure['deals']:
        portfolio.append(deal['procent'])
        measure[mapEventDirect[deal['event']]] += deal['procent']

    def calcMeasures(deals):
        def maxDrawdown(array):
            i = np.argmax(np.maximum.accumulate(array) - array) # end of the period
            if i == 0:
                return 0
            j = np.argmax(array[:i]) # start of period
            return array[j] - array[i]
        res = {};
        pnl = np.cumsum(deals)
        res['std'] = np.std(pnl)
        res['minV'] = min(np.min(pnl), 0)
        res['maxDrawdown'] = maxDrawdown(pnl)
        res['sumProcent'] = pnl[-1]
        res['numDeals'] = len(portfolio)
        return res

    measure['sumProcent'] = measure['minV'] = measure['maxDrawdown'] = 0
    measure['std'] = measure['numDeals'] = 0
    if portfolio:
        measureTest = calcMeasures(portfolio)
        measure.update(measureTest)

    toCSV = [deal for deal in measure['deals']]
    fieldnames = ['datetimeEnter', 'direct', 'priceEnter', 'procent', 'event', 'datetimeExit', 'priceExit']
    with open('data/order/{0}_{1}_order.csv'.format(ticker, _tickSize), 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=';', extrasaction='ignore')
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

    return measure

def plotChart(result, ticker):
    for res in result:
        if res['ticker'] == ticker:
            break
    _tickSize = res['_tickSize']

    data = {key: np.load('data/{0}/{1}/{2}.npy'.format(ticker, _tickSize, key), encoding='bytes') for key in dataKeys }

    N = len(data['time'])
    ind = np.arange(N)
    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, N - 1)
        return data['time'][thisind].strftime('%Y-%m-%d %H:%M:%S')
    fig, ax = plt.subplots()
    ax.plot(ind, data['close'], 'b-')

    ax.plot([x['datetimeEnterInd']
              for ind, x in enumerate(res['deals'])
              if x['direct'] == 'buy'],
             [x['priceEnter']
              for x in res['deals']
              if x['direct'] == 'buy'],
             'go', marker='^', ms=10)

    ax.plot([x['datetimeEnterInd']
              for x in res['deals']
              if x['direct'] == 'sell'],
             [x['priceEnter']
              for x in res['deals']
              if x['direct'] == 'sell'],
             'ro', marker='v', ms=15)

    ax.plot([x['datetimeExitInd']
              for x in res['deals']
              if x['event'] == 'takeProfit'],
             [x['priceExit']
              for x in res['deals']
              if x['event'] == 'takeProfit'],
             'go', marker='$ P $', ms=15)

    ax.plot([x['datetimeExitInd']
              for x in res['deals']
              if x['event'] == 'stopLoss'],
             [x['priceExit']
              for x in res['deals']
              if x['event'] == 'stopLoss'],
             'ro', marker='$ S $', ms=15)

    ax.plot([x['datetimeExitInd']
              for x in res['deals']
              if x['event'] == 'holdPeriod' and x['procent'] > 0],
             [x['priceExit']
              for x in res['deals']
              if x['event'] == 'holdPeriod' and x['procent'] > 0],
             'go', marker='$ H $', ms=15)

    ax.plot([x['datetimeExitInd']
              for x in res['deals']
              if x['event'] == 'holdPeriod' and x['procent'] <= 0],
             [x['priceExit']
              for x in res['deals']
              if x['event'] == 'holdPeriod' and x['procent'] <= 0],
             'ro', marker='$ H $', ms=15)

    ax.xaxis.set_major_formatter(plotticker.FuncFormatter(format_date))
    fig.autofmt_xdate()

    plt.show()