from pybeans.schema import Schema


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
    :param source: bean object or class
    :type target: dict or None
    :returns: full filled target
    :rtype: dict
    :raises pybeans.exceptions.EncodingError
    """
    if target is None:
        target = {}
    return source.__pybeansschema__.encode(source, target)


def dict_to_bean(source, target):
    """
    :type source: dict
    :param target: bean object or class
    :type target: type or T
    :returns: initialized instance of target
    :rtype: T
    :raises pybeans.exceptions.DecodingError
    """
    if isinstance(target, type):
        target = target()
    return target.__pybeansschema__.decode(source, target)
