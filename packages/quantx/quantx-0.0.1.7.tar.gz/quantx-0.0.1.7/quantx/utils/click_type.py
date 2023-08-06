import click
import pandas


class DateTime(click.ParamType):
    def convert(self, value, param, ctx):
        return pandas.to_datetime(value)

    @property
    def name(self):
        return type(self).__name__.upper()
