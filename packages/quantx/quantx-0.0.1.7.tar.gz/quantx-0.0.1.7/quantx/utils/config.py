import inspect
import os
from configparser import ConfigParser
from datetime import datetime, timedelta

from quantx.utils import pth
from quantx.utils.const import DateFormat


class Config(object):
    __section__ = "chinascope"
    __config__ = os.sep.join([pth.home(), ".%s" % __section__])

    rootdir = os.sep.join([pth.home(), __section__])
    cache_db = "memory"
    db = "local"
    source = "china_scope"
    container = "eval"
    latest_updated = (datetime.now() - timedelta(days=1)).strftime(DateFormat.day)

    def get(self, key, default=""):
        cp = ConfigParser()
        cp.read(Config.__config__)
        if not cp.has_section(Config.__section__) or not cp.has_option(Config.__section__, key):
            return default
        return cp.get(Config.__section__, key)

    def save(self):
        cp = ConfigParser()
        if not cp.has_section(Config.__section__):
            cp.add_section(Config.__section__)

        for attr in self.iter_attr():
            cp.set(Config.__section__, attr, getattr(self, attr, ""))

        with open(Config.__config__, "w") as conf:
            cp.write(conf)

    def iter_attr(self):
        for attr in dir(self):
            if inspect.isfunction(getattr(self, attr)) or inspect.ismethod(getattr(self, attr)) or attr[0] == '_':
                continue

            yield attr

    def __init__(self):
        for attr in self.iter_attr():
            value = self.get(attr)
            if value:
                setattr(self, attr, value)

    def get_cache_file(self, name):
        return os.sep.join([self.get_cache_dir(), name])

    @pth.mkdir
    def get_cache_dir(self):
        return os.sep.join([self.rootdir, "cache"])

    def get_root_file(self, name):
        return os.sep.join([self.rootdir, name])

    def get_cache_db(self):
        return self.get_root_file(self.cache_db + ".db")

    def get_db(self):
        return self.get_root_file(self.db + ".db")


Config = Config()
Config.save()
