import  strategy.istrategy as tra
import  time
import strategy.util as util
import strategy.entity as en
import data.dataLoader as dl
import  pandas as pd
class BS_DoubleTrade(tra.Istrategy):
    '''
    两交易对双交易策略；当稳定币处于下降趋势时，卖出非稳定币，买入稳定币；当稳定币处于上升趋势时，买入非稳定币，卖出稳定币。
    '''
    min10Kdata=pd.DataFrame()
    min60KData=pd.DataFrame()
    shortMean=pd.DataFrame()
    midMean=pd.DataFrame()
    longMean=pd.DataFrame()
    shortMeanSize=5      #min
    midMeanSize=20       #min
    bigMeanSize=240  #hour
    def __init__(self):
        self.min10Kdata = pd.DataFrame()
        self.min60KData = pd.DataFrame()
        self.shortMean = pd.DataFrame()
        self.midMean = pd.DataFrame()
        self.longMean = pd.DataFrame()
        self.shortMeanSize = 5  # min
        self.midMeanSize = 20  # min
        self.bigMeanSize = 240  # hour

    def initialize(self, context):
        colNames = en.KlineColName
        colum = [colNames.opentime, colNames.open, colNames.high, colNames.low, colNames.close, colNames.volume,
                 colNames.closetime, colNames.assetvolume, colNames.numTrades,
                 colNames.baseVolume, colNames.quoteVolume, colNames.ignore]
        self.min10Kdata = pd.DataFrame(columns=colum)

        self.min60KData = pd.DataFrame(columns=colum)

        #加载EOSBTC价格集合


    def handle_data(self, context, data):
        self.__calculateKline(data)
        s=self.__getMeanValue(False,self.shortMeanSize)
        m=self.__getMeanValue(False,self.midMeanSize)
        l=self.__getMeanValue(True,self.bigMeanSize)
        key=data.iloc[-1][en.KlineColName.opentime]

        self.shortMean=self.shortMean.append({key:s},ignore_index=True)
        self.midMean=self.midMean.append({key: m},ignore_index=True)
        self.longMean=self.longMean.append({key:l},ignore_index=True)
        #短线下穿中线,买入btc,卖出eos
        if(m<s):
            if(context.balances[en.AssertName.eos]>0.1):
                price= dl.getKlineItem('EOSBTC','1m',data.iloc[-1]['closetime'])
                order=en.Order('EOSBTC',en.Side.SELL,context.balances[en.AssertName.eos],price,data.iloc[-1]['closetime'],
                               context.balances[en.AssertName.eos]*price*context.makerCommission)
                context.makeTrade(order)
        elif(m>s):
            if (context.balances[en.AssertName.btc] > 0.001):
                price = dl.getKlineItem('EOSBTC', '1m', data.iloc[-1]['closetime'])
                order = en.Order('EOSBTC', en.Side.BUY, int(context.balances[en.AssertName.btc]/(price*(1+context.takerCommission))), price,
                                 data.iloc[-1]['closetime'],
                                 context.balances[en.AssertName.eos] * price * context.makerCommission)
                context.makeTrade(order)
        


        #短线上传中线,买入eos,卖出btc



    def __getMeanValue(self,isHour:bool,size:int):
        cobject=pd.DataFrame()
        retData=0.0
        if(isHour):
            cobject=self.min60KData
        else:
            cobject=self.min10Kdata
        if (len(cobject)==0):
            return 0.0
        if(len(cobject)<size):
            retData=cobject[en.KlineColName.open].mean()
        else:
            retData=cobject[en.KlineColName.open][-1-size:-1].mean()
        return retData



    def __calculateKline(self,data:pd.DataFrame):
        #计算长、中、短、超短 趋势线,data为每分钟k线数据
        ts=data.iloc[-1][en.KlineColName.opentime]
        datetime=util.getTimeByTimestamp(ts)
        timearr=util.getTimeArrayByTimeStr(datetime)
        if(timearr.tm_min/10==0 & len(data)>=10 ):
            newItem=self.__buildKline(data,10)
            self.min10Kdata=self.min10Kdata.append(newItem,ignore_index=True)
        elif(len(data)==1):
            newItem=self.__buildKline(data,1)
            self.min10Kdata=self.min10Kdata.append(newItem,ignore_index=True)

        if(timearr.tm_min/60==0 & len(data)>=60 ):
            newItem=self.__buildKline(data,60)
            self.min60KData=self.min60KData.append(newItem,ignore_index=True)
        elif(len(data)==1):
            newItem=self.__buildKline(data,1)
            self.min60KData=self.min60KData.append(newItem,ignore_index=True)

            



    def __buildKline(self,data:pd.DataFrame,stepNum:int):
        colNames = en.KlineColName
        itemdict={}
        itemdict[colNames.opentime]=data.iloc[-stepNum][colNames.opentime]
        itemdict[colNames.open]=data.iloc[-stepNum][colNames.open]
        itemdict[colNames.high] = data.iloc[-stepNum:-1][ colNames.high].max()
        itemdict[colNames.low]=data.iloc[-stepNum:-1][colNames.low].min()
        itemdict[colNames.close]=data.iloc[-1][colNames.close]
        itemdict[colNames.volume]=data.iloc[-stepNum:-1][colNames.volume].sum()
        itemdict[colNames.closetime] = data.iloc[-1][colNames.closetime]
        itemdict[colNames.assetvolume]=data.iloc[-stepNum:-1][colNames.assetvolume].sum()
        itemdict[colNames.numTrades] = data.iloc[-stepNum:-1][ colNames.numTrades].sum()
        itemdict[colNames.baseVolume] = data.iloc[-stepNum:-1][ colNames.baseVolume].sum()
        itemdict[colNames.quoteVolume] = data.iloc[-stepNum:-1][ colNames.quoteVolume].sum()
        itemdict[colNames.ignore] = 0.0
        ret= pd.DataFrame(itemdict,pd.Index(range(1)))
        return ret



        








        

