from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from threading import Timer
import time

symbols = ['TATASTEEL', 'MARUTI', 'WIPRO', 'HDFCBANK', 'SHREECEM', 'SBIN', 'IOC', 'UPL']

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        
        self.prices = deque(maxlen = AVG_LENGTH)
        self.moneyflows = deque(maxlen = MFI_PERIOD)
        
    
    def historicalData(self, reqId, bar):
        # Append the closing prices to the deque
        self.prices.append(bar.close)
        
        # Bollinger Band 
        # Compute the average if 100 values are available
        if len(self.prices) == AVG_LENGTH:
            avg = sum(self.prices) / len(self.prices)
            
            # Compute the standard deviation
            avg_array = np.array(self.prices)
            sigma = np.std(avg_array)
            
            # Update the containers
            self.avg_vals.append(avg)
            self.upper_band.append(avg + 2 * sigma)
            self.lower_band.append(avg - 2 * sigma)
            self.pct_b.append(((bar.close - avg + 2 * sigma) / (4 * sigma)) * 100)
            
        # MFI
        # Compute the money flow
        typical = (bar.close + bar.low + bar.close) / 3
        if old_typical > typical:
            old_typical = typical
            typical *= -1
        else:
            old_typical = typical
        
        money_flow = (bar.volume) * typical
        self.money_flows.append(money_flow)
        if len(self.money_flows) == MFI_PERIOD:
            mf_array = np.array(self.money_flows)
            pos_flow = np.sum(mf_array[mf_array > 0])
            neg_flow = -1.0 * np.sum(mf_array[mf_array < 0])
            mfi = 100 * pos_flow / (pos_flow + neg_flow)
        else:
            continue
        self.mfi_val.append(mfi)
        

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

def main():
    app = TestApp()
    app.connect("127.0.0.1", 4002, 1)
    
    
    # Initialize values
    old_typical = -1
    prices.clear()
    money_flows.clear()
    funds = init_funds
    inv_state = InvState.OUT
    positions.clear()
    
    
   #Contract specific information
    contract_size = 
    unit_size = int(0.01 * funds / contract_size)
    df = 
    
    for symbol in symbols:
        
        #Compute the money flow
        typical = () / 3

if __name__ == "__main__":
    main()
