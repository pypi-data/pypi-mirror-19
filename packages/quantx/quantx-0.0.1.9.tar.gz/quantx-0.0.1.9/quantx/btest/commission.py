import abc


class Commission:
    @abc.abstractclassmethod
    def handle(self, symbol, price, amount):
        pass


class AStockCommission(Commission):
    """
    1、印花税：单向收取，卖出股票才收取，统一收取标准是：卖出成交金额的千分之一
    2、过户费：买卖上海股票才收取，每1000股收取1元，低于1000股也按照1元收取
    3、佣金：买卖双向收取，费率可以上下浮动，国家规定最低一笔收取5元
    """

    def __init__(self,
                 commission_rate=0.00025,
                 min_commission=5,
                 stamp_tax_rate=0.001,
                 transfer_fee=1,
                 transfer_fee_per=1000,
                 min_transfer_fee=1):
        self.commission_rate = commission_rate
        self.min_commission = min_commission
        self.stamp_tax_rate = stamp_tax_rate
        self.transfer_fee = transfer_fee
        self.transfer_fee_per = transfer_fee_per
        self.min_transfer_fee = min_transfer_fee

    def handle(self, symbol, price, amount):
        commission = max((price * abs(amount)) * self.commission_rate, self.min_commission)
        transfer = max(abs(amount) // self.transfer_fee_per, self.min_transfer_fee) if symbol[:2] == "60" else 0
        stamp = (price * abs(amount)) * self.stamp_tax_rate if amount < 0 else 0
        return commission + transfer + stamp
