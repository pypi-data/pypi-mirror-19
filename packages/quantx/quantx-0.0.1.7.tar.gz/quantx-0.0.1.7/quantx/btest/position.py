from quantx.btest.data import Data
from pandas import isnull


class Position:
    """
    amount	    int	    未平仓部分的总股数。
    bought_amount	int	    该证券的总买入股数，
        例如：如果你的投资组合并没有任何平安银行的成交，那么平安银行这个股票的仓位就是0.
    sold_amount	int	    该证券的总卖出股数，
        例如：如果你的投资组合曾经买入过平安银行股票200股并且卖出过100股，那么这个属性会返回100.
    bought_value	float	该证券的总买入的价值，等于每一个该证券的买入成交的价格*买入股数的总和。
    sold_value	    float	该证券的总卖出价值，等于每一个该证券的卖出成交的价格*卖出股数的总和。
    total_orders	int	    该仓位的总订单的次数。
    total_trades	int	    该仓位的总成交的次数。
    sellable	    int	    该仓位可卖出股数。T＋1的市场中sellable = 所有持仓-今日买入的仓位。
    average_cost	float	获得该持仓的买入均价，计算方法为每次买入的数量做加权平均。
    market_value	float	获得该持仓的实时市场价值。
    value_percent	float	获得该持仓的实时市场价值在总投资组合价值中所占比例，取值范围[0, 1]。
    """
    amount = 0
    sellable = 0
    market_value = 0
    bought_amount = 0
    sold_amount = 0
    bought_value = 0
    sold_value = 0
    avg_cost = 0

    locked = dict()

    def update_transaction(self, trade):
        self.amount += trade.amount

        if trade.amount > 0:
            self.bought_amount += trade.amount
            self.bought_value += trade.cost
            if trade.unlock_dt and trade.unlock_dt > trade.date:
                if not self.locked.__contains__(trade.unlock_dt):
                    self.locked[trade.unlock_dt] = 0
                self.locked[trade.unlock_dt] += trade.amount
        else:
            self.sold_amount += trade.amount
            self.sold_value += trade.cost

    def update(self, now, bar):
        self.amount = self.amount + int(self.amount * bar.givsr) if bar.close else 0
        self.market_value = self.amount * bar.close
        self.sellable = self.amount

        for dt in list(self.locked.keys()):
            if dt > now:
                self.sellable -= self.locked[dt]
            else:
                self.locked.pop(dt)
