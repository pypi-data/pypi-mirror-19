import re
from inspect import signature

def _getname(original_name, name_func, idx, args):
    if name_func:
        sig_func = signature(name_func)
        if len(sig_func.parameters) > 2:
            return name_func(original_name, *args)
        else:
            return name_func(original_name, args)
    else:
        return (original_name +
                "_gentest_"
                + str(idx))

def _create_new_func(base_func, *args):
    return lambda other_self: base_func(other_self, *args)

def _getfunc(base_func, args):
    sig = signature(base_func)
    if len(sig.parameters) > 2:
        return _create_new_func(base_func, *args)
    else:
        return _create_new_func(base_func, args)

class _gentests(object):
    def __call__(self, cls):
        new_attrs = {}
        del_attrs = []
        for name, attr in vars(cls).items():
            if type(attr) is _metaTestFunc:
                del_attrs.append(name)
                mtf = attr
                for idx, val in enumerate(mtf.vals):
                    new_name = _getname(name, mtf.name, idx, val)
                    new_func = _getfunc(mtf.base_func, val)
                    new_attrs[new_name] = new_func
        for name, attr in new_attrs.items():
            setattr(cls, name, attr)
        for name in del_attrs:
            delattr(cls, name)
        return cls

gentests = _gentests()

class _metaTestFunc(object):
    def __init__(self, base_func, vals, name):
        self.base_func = base_func
        self.vals = vals
        self.name = name

class vals(object):
    def __init__(self, vals, name=None):
        self.vals = vals
        self.name = name

    def __call__(self, func):
        return _metaTestFunc(func, self.vals, self.name)
