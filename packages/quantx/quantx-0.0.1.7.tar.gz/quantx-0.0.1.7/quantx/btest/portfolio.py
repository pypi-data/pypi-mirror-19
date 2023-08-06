from datetime import datetime

from quantx.btest.data import Data

from quantx.btest.position import Position
from quantx.btest.returns import Returns


class Portfolio:
    """
    starting_cash	        float	    回测或实盘交易给算法策略设置的初始资金
    cash	                float	    现在投资组合中剩余的现金
    total_returns	        float	    算法投资组合至今的累积百分比收益率。
        计算方法是现在的投资组合价值/投资组合的初始资金。投资组合价值包含剩余现金和其市场价值。
    daily_returns	        float	    当前最新一天的每日收益。
    market_value	        float	    投资组合当前的市场价值（未实现/平仓的价值）
    portfolio_value	        float	    当前投资组合的总共价值，包含市场价值和剩余现金。
    pnl	                    float	    当前投资组合的￥盈亏
    start_date	            DateTime	策略投资组合的回测/实时模拟交易的开始日期
    annualized_returns	    float	    投资组合的年化收益率
    positions	            Dictionary	一个包含所有仓位的字典，以id_or_symbol作为键，position对象作为值，
        关于position的更多的信息可以在下面的部分找到。
    dividend_receivable	    float	    投资组合在分红现金收到账面之前的应收分红部分。具体细节在分红部分
    """
    value = 0
    cash = 0
    free = 0
    freezed = 0
    market_value = 0
    starting_cash = 0
    pnl = 0
    returns = None
    start_date = None

    positions = dict()
    snapshots = dict()

    def __init__(self, starting_cash):
        self.starting_cash = starting_cash
        self.free = starting_cash
        self.cash = starting_cash
        self.value = starting_cash
        self.returns = Returns(starting_cash)

    def get_position(self, symbol) -> Position:
        if not self.positions.__contains__(symbol):
            self.positions[symbol] = Position()
        return self.positions[symbol]

    def update_freezed(self, freezed):
        self.freezed += freezed
        self.free = self.cash - self.freezed

    def update_transaction(self, trade):
        self.get_position(trade.symbol).update_transaction(trade)

        self.cash -= trade.cost
        self.update_freezed(trade.freezed)

    def update(self, data: Data):
        if not self.start_date:
            self.start_date = data.trading_day

        self.market_value = 0
        for symbol, pos in self.positions.items():
            bar = data.get_bar(symbol)
            self.cash += bar.abns * pos.amount
            pos.update(data.trading_day, bar)
            self.market_value += pos.market_value

        last_vaule = self.value
        self.value = self.market_value + self.cash
        self.pnl = self.value - last_vaule

        self.returns.update(data.trading_day, last_vaule, self.value)

        # self.snapshots[trading_day] = copy.deepcopy(self)
