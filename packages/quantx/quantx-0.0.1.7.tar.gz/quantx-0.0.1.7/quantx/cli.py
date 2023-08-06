import os
import click
import pandas
import shutil
from odo import odo
from quantx.btest.exch.simulation import SimulationExch
from quantx.factors.factor import Factor
from quantx.utils import click_type
from quantx.utils.config import Config
from quantx.utils.const import ModCls, DateDefault, DataSrc, DataCol, Func, DateFormat, BundleCls
from quantx.utils.convert import ts
from quantx.utils.factory import cls
from quantx.plotting import analyse as show_plot


@click.group()
def cli():
    pass


@cli.command("import")
@click.argument("path", type=click.Path(exists=True, dir_okay=False), metavar="[文件路径]")
@click.option("--dt_col", default=DataCol.dt, help="时间字段名")
@click.option("--symbol_col", default=DataCol.symbol, help="股票字段名")
def import_data(path, dt_col, symbol_col):
    """导入数据"""

    dframe = odo(path, pandas.DataFrame)
    dset = cls(Config.db, ModCls.dataset)(Config.get_db())

    for column in filter(lambda x: x not in [dt_col, symbol_col], dframe.columns):
        dset.drop(Factor(column))
        dset.update(
            Factor(column),
            dframe.loc[:, [dt_col, symbol_col, column]],
            dt_col=dt_col,
            symbol_col=symbol_col,
            anchor=(
                ts(dframe[dt_col].iloc[0]),
                ts(dframe[dt_col].iloc[-1])
            )
        )


@cli.command("update")
@click.option("-s", "--start_date", type=click_type.DateTime(), default=DateDefault.start.strftime(DateFormat.day),
              help="开始时间")
@click.option("-e", "--end_date", type=click_type.DateTime(), default=DateDefault.end.strftime(DateFormat.day),
              help="结束时间")
@click.option("-b", "--bundle", default=None, type=click.Choice([BundleCls.market]), help="数据集")
@click.option("-f", "--factor", default=None, help="因子数据")
@click.option("--src", default=DataSrc.china_scope, type=click.Choice([DataSrc.china_scope]), help="数据源")
def update(bundle, factor, start_date, end_date, src):
    """更新数据"""
    dsource = cls(src, ModCls.source)()

    if bundle:
        dsource.update(cls(bundle, ModCls.bundle), start_date, end_date)

    if factor:
        dsource.update(Factor(factor), start_date, end_date)


@cli.command("config")
@click.argument("name", default="", type=click.STRING, metavar="[配置参数]")
@click.option("-v", "--value", default="", type=click.STRING, help="设置新值")
def config(name, value):
    """配置文件"""

    if name and value:
        setattr(Config, name, value)
        Config.save()
    elif name:
        click.echo("%s=%s" % (name, getattr(Config, name)))
    elif value:
        pass
    else:
        for attr in Config.iter_attr():
            click.echo("%s=%s" % (attr, getattr(Config, attr)))


@cli.command("clean")
@click.option("-a", "--all", is_flag=True, help="全部")
@click.option("-f", "--factor", default=None, help="因子名称")
@click.option("-b", "--bundle", default=None, type=click.Choice([BundleCls.market]), help="数据集")
@click.option("--config", is_flag=True, help="配置文件")
@click.option("--cache", is_flag=True, help="缓存文件")
def clean(all, factor, bundle, config, cache):
    """清理数据"""
    dset = cls(Config.db, ModCls.dataset)(Config.get_db())

    if bundle:
        dset.drop(cls(bundle, ModCls.bundle))

    if cache:
        shutil.rmtree(Config.get_cache_dir())

    if factor:
        dset.drop(Factor(factor))

    if config or all:
        os.remove(Config.__config__)

    if all:
        shutil.rmtree(Config.rootdir)


@cli.command("run")
@click.argument("py", type=click.Path(True, dir_okay=False), metavar="[策略文件]")
@click.option("-s", "--start_date", type=click_type.DateTime(), default=DateDefault.start.strftime(DateFormat.day),
              help="回测开始时间")
@click.option("-e", "--end_date", type=click_type.DateTime(), default=DateDefault.end.strftime(DateFormat.day),
              help="回测结束时间")
@click.option("-o", "--out_file", default=None, type=click.Path(file_okay=True), help="输出结果")
@click.option("--plot", is_flag=True, help="输出图表")
@click.option("--initialize", default=Func.initialize)
@click.option("--handle_bar", default=Func.handle_bar)
@click.option("--analyse", default=Func.analyse)
def run(py, start_date, end_date, initialize, handle_bar, plot, out_file, analyse):
    """执行策略"""

    g = {
        Func.initialize: None,
        Func.analyse: None
    }
    with open(py) as f_py:
        c = compile(f_py.read(), py, "exec")
        exec(c, g)

    def _analyze(context, results):
        click.echo(results.tail(1).T)
        if plot:
            show_plot(results)

    se = SimulationExch()
    se.run(
        start_date=start_date,
        end_date=end_date,
        initialize=g[initialize],
        handle_bar=g[handle_bar],
        out_path=out_file,
        analyze=g[analyse] if g[analyse] else _analyze
    )


@cli.command("plot")
@click.argument("pickle", type=click.Path(True, file_okay=True), metavar="[文件路径]")
def plot(pickle):
    """图表"""
    show_plot(pandas.read_pickle(pickle))


def main():
    cli()
