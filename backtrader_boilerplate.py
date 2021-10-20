import backtrader as bt #  Import  Backtrader 

#  Create a strategy 
class MyStrategy(bt.Strategy):
    #  Initialize policy parameters 
    params = (
        (...,...), #  the last one “,” It's better not to delete ！
    )
    #  Log printing ： Official documents for reference 
    def log(self, txt, dt=None):
        ''' Function to build policy print log ： It can be used to print order records or transaction records, etc '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
  
    #  Initialization function 
    def __init__(self):
        ''' Initialization property 、 Calculation index, etc '''
        #  The index calculation can be referred to 《backtrader Indicators 》
        self.add_timer() #  Add timers 
        pass
    
    #  In the whole test cycle , Functions corresponding to different time periods 
    def start(self):
        ''' It is called before the test starts , Corresponding to the first 0 root bar'''
        #  The relevant processing logic before the start of backtesting can be written here 
        #  Empty... Is called by default  start()  function , Used to start backtesting  
        pass
    
    def prenext(self):
        ''' Strategy preparation phase , Corresponding to the first 1 root bar- The first  min_period-1  root bar'''
        #  This function is mainly used for waiting index calculation , Before the indicator calculation is completed, it will be called by default prenext() Empty function 
        # min_period  Namely  __init__  To complete all the indicators in the calculation 1 The minimum period of time required for each value 
        pass
    
  def nextstart(self):
        ''' The first time when the policy works properly , Corresponding to the first  min_period  root bar'''
        #  Only in  __init__  In the case that all the indicators in have values available , To start running the strategy 
        # nextstart() Only run once , It's mainly used to tell you that you can start later  next()  了 
        # nextstart() The default implementation of is to simply call next(), therefore next The logic of strategy in  min_period root bar It has already been implemented 
        pass
    
     def next(self):
        ''' The normal operation phase of the policy , Corresponding to the first min_period+1 root bar- The last one bar'''
        #  The main strategy logic is written under this function 
        #  After entering this stage , It's going to be in turn in each bar Up cycle running next function 
        #  Query function 
        print(' Current position ', self.getposition(self.data).size)
        print(' The current cost of holding ', self.getposition(self.data).price)
        # self.getpositionbyname(name=None, broker=None)
        print(' List of dataset names ',getdatanames())
        data = getdatabyname(name) #  Returns a dataset by name 
        #  General single function 
        self.order = self.buy( ...) #  purchase 、 Do more  long
        self.order = self.sell(...) #  sell 、 Short  short
        self.order = self.close(...) #  close a position  cover
        self.cancel(order) #  Cancellation of order 
        #  The objective is a single function 
        #  Order by target number 
        self.order = self.order_target_size(target=size) 
        #  Order by target amount 
        self.order = self.order_target_value(target=value) 
        #  Order by target percentage 
        self.order = self.order_target_percent(target=percent) 
        #  Order mix 
        brackets = self.buy_bracket()
        brackets = self.sell_bracket()
        pass
    
    def stop(self):
        ''' The end of the strategy , Corresponding to the last one bar'''
        #  Inform the system that the back test has been completed , You can reset the policy and sort out the test results 
        pass
    
  #  Print the test back log 
    def notify_order(self, order):
        ''' Notification of order information '''
        pass

    def notify_trade(self, trade):
        ''' Notification of trading information '''
        pass
    
    def notify_cashvalue(self, cash, value):
        ''' Inform current funds and total assets '''
        pass
    
    def notify_fund(self, cash, value, fundvalue, shares):
        ''' Return the current funds 、 total assets 、 The value of the Fund 、 Fund share '''
        pass
    
    def notify_store(self, msg, *args, **kwargs):
        ''' Return the information notification from the supplier '''
        pass
    
    def notify_data(self, data, status, *args, **kwargs):
        ''' Return data related notification '''
        pass
    
    def notify_timer(self, timer, when, *args, **kwargs)：
      ''' Return notification of timer '''
      #  The timer can be set by the function add_time() add to 
        pass
    
  #  All kinds of transaction functions and query functions ： Please check out 《 Trading （ On ）》 and 《 Trading （ Next ）》

......
#  Add strategy to the brain 
cerebro.addstrategy(MyStrategy)
