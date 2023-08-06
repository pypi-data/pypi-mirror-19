from .static_plot import show_draw_result

from IPython.core import getipython



ip = getipython.get_ipython()
if ip and 'IPKernelApp' in ip.config:
    from . import pandas_highcharts
    from .pandas_highcharts import serialize, display_charts
    # running in notebook mode
    def analyse(result_df):
        df = result_df.loc[:, ['total_returns', 'benchmark_total_returns']]
        # todo: add more info
        display_charts(df, chart_type='stock')
else:
    def analyse(result_df):
        show_draw_result('', result_df)
