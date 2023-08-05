quantx
======

安装方式
--------
    pip install quantx

更新方式
--------
    pip install quantx --upgrade


策略脚本示例
------
    from quantx.btest.api import order_percent
    from quantx.btest.core import ExchContext
    from quantx.btest.data import Data


    def initialize(context: ExchContext):
        context.fired = False
        context.cash = 1000000
        context.benchmark = "000001"


    def handle_bar(context: ExchContext, data: Data):
        if not context.fired:
            order_percent("600642", 1)
            context.fired = True


    if __name__ == '__main__':

        from quantx.btest.exch import SimulationExch
        from quantx.plotting import show_draw_result

        exch = SimulationExch()
        result = exch.run(
            start_date="2016-01-01",
            end_date="2016-03-01",
            handle_bar=handle_bar,
            initialize=initialize)

        analyse(result)

命令行工具
----------
    Usage: quantx [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      clean          清理数据
      config         配置文件
      import         导入因子数据
      plot           图表
      run            执行策略
      update_factor  更新因子数据
      update_market  更新行情数据
