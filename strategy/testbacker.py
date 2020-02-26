#回测器
import  importlib
import  strategy.istrategy
import  data.dataLoader
import  strategy.entity as en
global g

    

class TestbackEngine():
    def testback(self,strategyLibName,fromTime,toTime,initAssert:dict,runIntervalType,mainSymbol:str):
        strategyLib=__import__(strategyLibName)
        try:
            straegyObject=strategyLib.autoTradeScript.BS_DoubleTrade()
            if(not isinstance(straegyObject,strategy.istrategy.Istrategy)) :
                raise Exception('策略代码接口编写错误')
            so:strategy.istrategy.Istrategy
            so=straegyObject
            #准备 context对象
            cxObject=self.initContext(initAssert)
            #准备回测数据
            rbData= data.dataLoader.loadKlineData(mainSymbol,runIntervalType,fromTime,toTime)
            so.initialize(cxObject)
            so.process_initialize(cxObject)
            so.before_trading_start(cxObject)
            so.market_open(cxObject)
            #按记录执行回测
            for indexs in  range(1,len(rbData)):
                istart=0
                if(indexs-100>0):
                    istart=indexs-100
                dp= rbData.iloc[istart:indexs]
                so.handle_data(cxObject,dp)
            so.after_trading_end(cxObject)
            so.on_strategy_end()
        except Exception as e:
            print("算法执行错误:"+ str(e))


    def initContext(self,initAssert:dict):
        con=en.Context()
        con.takerCommission=0.0015
        con.makerCommission=0.0015
        for item in initAssert.keys():
            con.balances[item]=initAssert[item]
        return  con
        


        #调用接口

if __name__=='__main__':
    tb=TestbackEngine()
    initAssert={'BTC':1}
    tb.testback('strategy.autoTradeScript','2018-1-1 00:00:00','2018-1-30 23:59:59',initAssert,'1m','BTCUSDT')
        
    