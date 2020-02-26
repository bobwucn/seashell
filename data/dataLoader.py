import  pandas as pd
import time, datetime
import  os,sys
from pandas import Series, DataFrame
import strategy.entity as en
import strategy.util as util
import numpy as np
klineDatas={}
def loadKlineData(typeName,interval,fro,to,isall=False):
    dirname, tfile = os.path.split(os.path.abspath(sys.argv[0]))
    filename='~/bitData/' + typeName.upper()+'kline_'+interval +'.csv'
    colNames=en.KlineColName
    colum = [colNames.opentime, colNames.open, colNames.high, colNames.low, colNames.close, colNames.volume, colNames.closetime, colNames.assetvolume, colNames.numTrades,
             colNames.baseVolume, colNames.quoteVolume, colNames.ignore]
    df=pd.read_csv(filename,names=colum)
    if(isall):
        return df
    frots=__getTimestamp(fro)
    tots=__getTimestamp(to)
    temp=df.loc[(df['opentime']<tots) & (df['opentime']>frots)]
    return temp
def __getTimestamp(tss1:str):
    '''
    格式：'2013-10-10 23:40:00'
    :param tss1:
    :return:
    '''
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray)) *1000
    return  timeStamp

def getKlineItem(typeName,interval,startTime):
    df=DataFrame()
    if(klineDatas.__contains__(typeName)):
        df=klineDatas[typeName]
    else:
        df=loadKlineData(typeName,interval,0,0,True)
    frots = __getTimestamp(startTime)
    temp = df.loc[(df['opentime'] >= frots)].head(n=1)
    return temp






if __name__=='__main__':
    #data= loadKlineData('BTCUSDT','1m','2017-10-01 00:00:00','2018-09-30 23:59:59')
    data=getKlineItem('BTCUSDT','1m','2018-10-01 00:00:00')
    print(data)
    ts=int(data.iloc[-1]['opentime'])
    timstr= util.getTimeByTimestamp(ts)
    print(data.iloc[-1]['High'])
    print(timstr)
    