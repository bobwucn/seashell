
from enum import  Enum
class Side(Enum):
    '''
    订单类型（买或卖）
    '''
    BUY=1
    SELL=2

class Order():
    '''
    交易订单
    '''
    symbol:str
    side:Side
    qty:float
    price:float
    commission:float
    timestamp:int
    def __init__(self,sym:str,side:Side,num:float,price:float,ts:int,fee:float):
        self.symbol=sym
        self.side=side
        self.qty=num
        self.price=price
        self.timestamp=ts
        feerate=0
        self.commission=self.qty*self.price*fee




class AssertName():
    '''
    货币资产名称
    '''
    btc="BTC"
    eos="EOS"
    usdt="USDT"
    eth="ETH"
class KlineColName():
    opentime='opentime'
    open= 'Open'
    high='High'
    low='Low'
    close='Close'
    volume='Volume'      #成交量
    
    closetime='closetime'
    assetvolume='assetvolume' #成交额
    numTrades='NumTrades'   #成交笔数
    baseVolume='baseVolume'     #主动买入成交量
    quoteVolume='quoteVolume'    #主动买入成交额
    ignore='Ignore'
class Context():
    '''
    运行时上下文
    '''
    makerCommission:float
    takerCommission:float
    buyerCommission:float
    sellerCommission:float
    balances=dict()
    trades=[]
    def __init__(self):
        self.balances[AssertName.btc]=0.0
        self.balances[AssertName.eos] = 0.0
        self.balances[AssertName.eth] = 0.0
        self.balances[AssertName.usdt] = 0.0
        self.makerCommission=0.0015
        self.takerCommission=0.0015
    def makeTrade(self,order:Order):
        '''
        执行交易
        :param order:
        :return:  交易执行成功与否标志
        '''
        sy=order.symbol.upper().strip
        a1,a2 =''
        if(sy=='BTCUSDT'):
            a1=AssertName.btc
            a2=AssertName.usdt
        elif(sy=='ETHUSDT'):
            a1=AssertName.eth
            a2=AssertName.usdt
        elif(sy=='EOSUSDT'):
            a1=AssertName.eos
            a2=AssertName.usdt
        else:
            print('不存在交易对:'+sy +'交易执行不成功.'+str(order) )
            return  False
        if(order.side==Side.BUY):
            if(self.balances[a2]<order.price*order.qty*(1+self.takerCommission)) :
                print('账户资金不够,交易执行失败。'+str(order))
                return False
            self.balances[a1]+=order.qty
            self.balances[a2]-=order.price*order.qty*(1+self.takerCommission)
            self.trades.append(order)
        else:
            if(self.balances[a1]<order.qty):
                print("账户所售资产不够，无法完成交易。"+str(order))
                return False
            self.balances[a1]-=order.qty
            self.balances[a2]+=order.price*order.qty*(1-self.makerCommission)
        self.trades.append(order)
        print('执行交易成功'+str(order))
        return True
    def checkOrder(self,order:Order,showPrint:bool=False):
        sy=order.symbol.upper().strip
        a1,a2 =''
        if(sy=='BTCUSDT'):
            a1=AssertName.btc
            a2=AssertName.usdt
        elif(sy=='ETHUSDT'):
            a1=AssertName.eth
            a2=AssertName.usdt
        elif(sy=='EOSUSDT'):
            a1=AssertName.eos
            a2=AssertName.usdt
        else:
            if(showPrint):
                print('不存在交易对:'+sy +'交易执行不成功.'+str(order) )
            return  False
        if(order.side==Side.BUY):
            if(self.balances[a2]<order.price*order.qty*(1+self.takerCommission)) :
                if (showPrint):
                    print('账户资金不够,交易执行失败。'+str(order))
                return False
        else:
            if(self.balances[a1]<order.qty):
                if (showPrint):
                    print("账户所售资产不够，无法完成交易。"+str(order))
                return False













