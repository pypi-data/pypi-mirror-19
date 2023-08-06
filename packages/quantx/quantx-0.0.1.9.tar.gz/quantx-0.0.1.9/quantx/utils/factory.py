import importlib

from quantx.utils import convert


def cls(name, module_cls):
    pth, suf = module_cls.split("::")
    mod = importlib.import_module(pth)
    return getattr(mod, convert.cls_s(name, suf))
