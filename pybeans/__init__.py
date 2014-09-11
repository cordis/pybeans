from pybeans.const import UNDEFINED
from pybeans.schema import Schema
from pybeans.exceptions import *


def bean(_=None, **defaults):
    def _bean(cls):
        cls.__pybeansschema__ = Schema(cls.__dict__, defaults)
        for name, node in cls.__pybeansschema__.get_nodes():
            setattr(cls, name, NotImplemented)
        return cls

    if _ is not None:
        return _bean(_)
    return _bean


def bean_to_dict(source, target=None):
    """
    @param source: bean object or class
    @type target: C{dict}
    @rtype: C{dict}
    @returns: full filled target
    @raises L{pybeans.exceptions.EncodingError}
    """
    if target is None:
        target = {}
    return source.__pybeansschema__.encode(source, target)


def dict_to_bean(source, target):
    """
    @type source: C{dict}
    @param target: bean object or class
    @returns: full filled target
    @raises L{pybeans.exceptions.EncodingError}
    """
    if isinstance(target, type):
        target = target()
    return target.__pybeansschema__.decode(source, target)


__all__ = [
    'bean',
    'bean_to_dict',
    'dict_to_bean',
    'BeansException',
    'DecodingException',
    'EncodingException',
]
