from quantx.btest.exch import Exch


class ExchContext:
    __instance__ = None

    @staticmethod
    def get_exch()->Exch:
        return ExchContext.__instance__
