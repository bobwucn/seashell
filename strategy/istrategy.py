
class Istrategy():
    def initialize(self,context):
        '''
        策略初始化方法
        :return:
        '''
        return None

    def market_open(self,context):
        '''
        开市时执行
        :return:
        '''
        return None

    def before_trading_start(self,context):
        '''
        开盘前运行策略
        :return:
        '''
        return None
    def after_trading_end(self,context):
        '''
        收盘后运行策略
        :param context:
        :return:
        '''
    def on_strategy_end(self,context):
        '''
        在回测、模拟交易正常结束时被调用， 失败时不会被调用。
        在模拟交易到期结束时也会被调用， 手动在到期前关闭不会被调用。
        :param context:
        :return:
        '''
    def process_initialize(self,context):
        '''
        该函数会在每次模拟盘/回测进程重启时执行, 一般用来初始化一些不能持久化保存的内容. 在 initialize 后执行.
        :param context:
        :return:
        '''
    def after_code_changed(self,context):
        '''
        模拟交易更换代码后运行函数
        :param context:
        :return:
        '''
    def unschedule_all(self):
        '''
        取消所有定时运行
        :return:
        '''
    def  handle_data(self ,context, data):
        '''
        每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
        :param data:
        :return:
        '''
        print(data)
        print('***********************************************')
        return None