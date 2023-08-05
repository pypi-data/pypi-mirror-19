import pickle

from pandas import HDFStore
from pandas import Series, DataFrame
from redis import StrictRedis

from quantx.utils import hash
from quantx.utils.sqlite import Sqlite


class Cache:
    def set(self, key, value):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError


class RedisCache(Cache):
    def __init__(self, host, port=6379):
        self.redis = StrictRedis(host, port)

    def set(self, key, value):
        return self.redis.set(key, pickle.dumps(value))

    def get(self, key, default=None):
        data = self.redis.get(key)
        return pickle.loads(data).sort_index() if data else default


class SqliteCache(Cache):
    __tablename__ = "quant_cache_data"

    def __init__(self, uri=None):
        self.db = Sqlite(uri)
        self.db.create_table(self.__tablename__, {
            "key": "TEXT",
            "value": "TEXT"
        })
        self.db.create_index(self.__tablename__, ["key"])

    def set(self, key, value):
        return self.db.replace(
            self.__tablename__,
            {
                "key": hash.md5(key.strip()),
                "value": pickle.dumps(value)
            }
        )

    def get(self, key, default=None):
        data = self.db.exec(
            "select value from %s where key = \'%s\'" % (
                self.__tablename__,
                hash.md5(key.strip())
            )
        ).fetchone()

        return pickle.loads(data[0]).sort_index() if data else default


class HdfCache(Cache):
    def __init__(self, uri=None):
        self._uri = uri

    def set(self, key, value):
        key = "_".join(["cache", hash.md5(key)])
        with HDFStore(self._uri, "a") as hdf:
            hdf.put(key, Series({key: value}))

    def get(self, key, default=None):
        key = "_".join(["cache", hash.md5(key)])
        with HDFStore(self._uri, "r") as hdf:
            data = hdf.get(key)[key]
            return data if not data.empty else default


class MemoryCache(Cache):
    _data_dict = dict()

    def __init__(self, uri):
        self._uri = uri

    def set(self, key, value):
        self._data_dict[hash.md5(key.strip())] = value

    def get(self, key, default=None):
        data = self._data_dict.get(hash.md5(key), default)

        return data if isinstance(data, (DataFrame, Series)) else default


if __name__ == '__main__':
    sc = SqliteCache(Sqlite("d:/work/my/quantx/py/datas/data.db"))
    sc.set("data", 5)

    print(sc.get("data"))
