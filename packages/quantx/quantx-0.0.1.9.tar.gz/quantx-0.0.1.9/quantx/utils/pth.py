import os


def home():
    return os.path.expanduser("~")


def mkdir(func):
    def _func(*args, **kwargs):
        path = func(*args, **kwargs)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    return _func
