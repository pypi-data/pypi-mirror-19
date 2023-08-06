# /usr/bin/env python
# *-.- conding: utf8 -.-

import os
import matplotlib
from matplotlib import gridspec
import matplotlib.pyplot as plt

plt.style.use('ggplot')

__author__ = 'phil.zhang'
__email__ = 'phil.zhang@chinascope.com'


def show_draw_result(title, results_df):
    """

    :param title: str
    :param results_df: DataFrame, columns are: total_returns, annualized_returns, benchmark_total_returns,
                        benchmark_annualized_returns, alpha, beta, sharpe, sortino, information_rate, volatility,
                        max_drawdown, tracking_error, downside_risk
    :return:
    """

    red = "#aa4643"
    blue = "#4572a7"
    black = "#000000"

    figsize = (18, 6)
    f = plt.figure(title, figsize=figsize)
    gs = gridspec.GridSpec(10, 8)

    # draw logo
    ax = plt.subplot(gs[:3, -1:])
    ax.axis("off")
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resource")
    filename = os.path.join(filename, "ricequant-logo.png")
    #    img = mpimg.imread(filename)
    #    imgplot = ax.imshow(img, interpolation="nearest")
    ax.autoscale_view()

    # draw risk and portfolio
    series = results_df.iloc[-1]

    font_size = 12
    value_font_size = 11
    label_height, value_height = 0.8, 0.6
    label_height2, value_height2 = 0.35, 0.15

    fig_data = [
        (0.00, label_height, value_height, "Total Returns", "{0:.3%}".format(series.total_returns), red, black),
        (0.15, label_height, value_height, "Annual Returns", "{0:.3%}".format(series.annualized_returns), red, black),
        (0.00, label_height2, value_height2, "Benchmark Total", "{0:.3%}".format(series.benchmark_total_returns), blue,
         black),
        (0.15, label_height2, value_height2, "Benchmark Annual", "{0:.3%}".format(series.benchmark_annualized_returns),
         blue, black),

        (0.30, label_height, value_height, "Alpha", "{0:.4}".format(series.alpha), black, black),
        (0.40, label_height, value_height, "Beta", "{0:.4}".format(series.beta), black, black),
        (0.55, label_height, value_height, "Sharpe", "{0:.4}".format(series.sharpe), black, black),
        (0.70, label_height, value_height, "Sortino", "{0:.4}".format(series.sortino), black, black),
        (0.85, label_height, value_height, "Information Ratio", "{0:.4}".format(series.information_rate), black, black),

        (0.30, label_height2, value_height2, "Volatility", "{0:.4}".format(series.volatility), black, black),
        (0.40, label_height2, value_height2, "MaxDrawdown", "{0:.3%}".format(series.max_drawdown), black, black),
        (0.55, label_height2, value_height2, "Tracking Error", "{0:.4}".format(series.tracking_error), black, black),
        (0.70, label_height2, value_height2, "Downside Risk", "{0:.4}".format(series.downside_risk), black, black),
    ]

    ax = plt.subplot(gs[:3, :-1])
    ax.axis("off")
    for x, y1, y2, label, value, label_color, value_color in fig_data:
        ax.text(x, y1, label, color=label_color, fontsize=font_size)
        ax.text(x, y2, value, color=value_color, fontsize=value_font_size)

    # strategy vs benchmark
    ax = plt.subplot(gs[4:, :])

    ax.get_xaxis().set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.grid(b=True, which='minor', linewidth=.2)
    ax.grid(b=True, which='major', linewidth=1)

    ax.plot(results_df["benchmark_total_returns"], label="benchmark", alpha=1, linewidth=2, color=blue)
    ax.plot(results_df["total_returns"], label="strategy", alpha=1, linewidth=2, color=red)

    # manipulate
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])

    leg = plt.legend(loc="upper left")
    leg.get_frame().set_alpha(0.5)

    plt.show()
