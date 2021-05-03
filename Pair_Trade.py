from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time
from copy import deepcopy
import numpy as np
from pandas import pd

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):  # Store initial next order ID sent back on connection
        self.nextValidOrderId = orderId
        self.start()

    def nextOrderId(self):  # There must be a larger ID for each new order
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining,
              ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)
    
    def historicalData(self, reqId:int, bar):
        if reqId not in self.data:
            self.data[reqId] = [{"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close, "Volume": bar.volume}]
        else:
            self.data[reqId].append({"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close, "Volume": bar.volume})
        print(`reqId: {}, Open: {}, High: {}, Low: {}, Close: {}, Volume: {}`.format(reqId, bar.open, bar.high, bar.low, bar.low, bar.close, bar.volume))

    def start(self):
        dpzStock = USStock("DPZ")
        dpzOrder = RelativePeggedToPrimary("BUY", 1, 0, 0)
        dpzOrder.transmit = False
        dpzOrderId = self.nextOrderId()
        self.placeOrder(dpzOrderId, dpzStock, dpzOrder)
        time.sleep(0.2) #planned to be no longer necessary in future

        # Pair trading documentation: http://interactivebrokers.github.io/tws-api/hedging.html
        pzzaStock = USStock("PZZA")
        # Size is 0 for hedge orders because it is calculated using the ratio
        pzzaOrder = RelativePeggedToPrimary("SELL", 0, 0, 0)
        pzzaOrder.parentId = dpzOrderId  # parent ID links child to parent order
        pzzaOrder.hedgeType = "P"  # "P" stands for Pair Trade
        pzzaOrder.hedgeParam = "5"  # 5 is the hedging ratio

        self.placeOrder(self.nextOrderId(), pzzaStock, pzzaOrder)

    def stop(self):
        self.done = True
        self.disconnect()

# The REL order type is adjusted by the system automatically with the bid (for Buy) or ask (for Sell ) orders
def RelativePeggedToPrimary(action: str, quantity: float, priceCap: float, offsetAmount: float):
    order = Order()
    order.action = action
    order.orderType = "REL"
    order.totalQuantity = quantity
    order.lmtPrice = priceCap
    order.auxPrice = offsetAmount
    return order

# API contract definition documentation: http://interactivebrokers.github.io/tws-api/basic_contracts.html#stk
def USStock(ticker: str):
    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NYSE"  # Should be native exchange of stock
    return contract

def histData(reqId, contract, duration, candle_size):
    app.reqHistoricalData	(tickerId=reqId,
                          contract=contract,
                          endDateTime="",
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow="ADJUSTED_LAST",
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=True,
                          chartOptions=[] 
                          )		
    

def main():
    app.run()
    
app = TestApp()
app.connect("127.0.0.1", 4797, 1)
con_thread = threading.Thread(target=main, daemon=True)
con_thread.start()
time.sleep(1)

tickers = ["ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB","DRREDDY", "EICHERMOT","GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO","HINDALCO","HINDUNILVR","HDFC","ICICIBANK","ITC","IOC","INDUSINDBK", "INFY","JSWSTEEL","KOTAKBANK","LT","M&M","MARUTI","NTPC","NESTLEIND","ONGC","POWERGRID", "RELIANCE","SBILIFE","SHREECEM","SBIN", "SUNPHARMA","TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM", "TITAN", "UPL","ULTRACEMCO", "WIPRO"]

pairs = list(itertools.permutations(tickers, 2))


#extracting historical data
for ticker in tickers:
    app.histData(tickers.index(ticker), USStock(ticker), "1 M", "5 mins")
    time.sleep(10)
    
def dataDataframe(symbols, obj):
    df_data = {}
    for symbol in symbols:
        df_data[symbol] = pd.DataFrame(obj.data[symbols.index(symbol)])
        df_data[symbol].set_index("Date", inplace=True)
    return df_data



def generate_pairs(data):
    pairs = {}
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            ratio = data[i]['Close'] / data[j]['Close']
            if adfuller(ratio) < 0.05:
                pairs['pair'] = pd.DataFrame((data[i], data[j]))
                pairs['ratio'] = pd.DataFrame(ratio)
                pairs.index = pd.to_datetime(pairs.index)
     return pairs
    
pairs['mavg'] = pairs.ratio.rolling(window=32).mean()  

pairs['std'] = pairs.ratio.rolling(window=32).std()

z_score = (pairs.ratio - pairs.mavg)/pairs.std

Timer(5, app.stop).start()

