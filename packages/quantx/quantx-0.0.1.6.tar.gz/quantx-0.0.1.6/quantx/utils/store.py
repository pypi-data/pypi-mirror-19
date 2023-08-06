import pickle


class StoreDict:
    def __init__(self, path):
        self._path = path

    def pop(self, key):
        self.__delitem__(key)

    def _get_dict(self):
        try:
            with open(self._path, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, TypeError):
            return dict()

    def __setitem__(self, key, value):
        _dict = self._get_dict()
        with open(self._path, "wb") as f:
            _dict[key] = value
            pickle.dump(_dict, f)

    def __getitem__(self, item):
        return self._get_dict()[item]

    def __contains__(self, item):
        return self._get_dict().__contains__(item)

    def __delitem__(self, key):
        _dict = self._get_dict()
        if _dict.__contains__(key):
            with open(self._path, "wb") as f:
                _dict.pop(key)
                pickle.dump(_dict, f)
