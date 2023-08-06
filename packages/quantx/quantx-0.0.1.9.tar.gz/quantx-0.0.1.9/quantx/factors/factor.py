import numpy


class Opt:
    def __add__(self, other):
        return FactorCal(self, other, "+", lambda x, y: x + y)

    def __sub__(self, other):
        return FactorCal(self, other, "-", lambda x, y: x - y)

    def __mul__(self, other):
        return FactorCal(self, other, "*", lambda x, y: x * y)

    def __truediv__(self, other):
        return FactorCal(self, other, "/", lambda x, y: x / y)

    def __floordiv__(self, other):
        return FactorCal(self, other, "//", lambda x, y: x // y)

    def __lt__(self, other):
        return FactorCal(self, other, "<", lambda x, y: x < y)

    def __le__(self, other):
        return FactorCal(self, other, "<=", lambda x, y: x <= y)

    def __eq__(self, other):
        return FactorCal(self, other, "==", lambda x, y: x == y)

    def __ne__(self, other):
        return FactorCal(self, other, "!=", lambda x, y: x != y)

    def __gt__(self, other):
        return FactorCal(self, other, ">", lambda x, y: x > y)

    def __ge__(self, other):
        return FactorCal(self, other, ">=", lambda x, y: x >= y)


class FactorCal(Opt):
    def __init__(self, factor_l, factor_r, opt, cal):
        self.opt = opt
        self.cal = cal
        self.factor_l = factor_l
        self.factor_r = factor_r


class Factor(Opt):
    def __init__(self, name=None, dtype=numpy.float, desc=None, index=False):
        self.dtype = dtype
        self.desc = desc
        self.index = index
        self._name = name
        self._bundle = None

    @property
    def name(self):
        names = self._name.split(".")
        return names[0] if len(names) == 1 else names[1]

    @property
    def full_name(self):
        return self._name

    @property
    def bundle(self):
        return self._bundle

    @bundle.setter
    def bundle(self, value):
        self._bundle = value

    @name.setter
    def name(self, value):
        self._name = value


class CustomFactor(Opt):
    def __init__(self, f_func, *args, **kwargs):
        self.f_func = f_func
        self.args = args
        self.kwargs = kwargs

    @property
    def name(self):
        return self.f_func.__name__
