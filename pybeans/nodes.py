from decimal import Decimal

from pybeans.const import UNDEFINED


__all__ = [
    'AnyNode',
    'StrNode',
    'UnicodeNode',
    'IntNode',
    'BoolNode',
    'FloatNode',
    'DecimalNode',
    'TupleNode',
    'ListNode',
    'DictNode',
    'BeanNode',
    'Registry',
]


class AnyNode(object):
    decode = None
    encode = None

    def __init__(self, default=UNDEFINED):
        self.default = default


class StrNode(AnyNode):
    decode = str


class UnicodeNode(AnyNode):
    decode = unicode


class IntNode(AnyNode):
    decode = int


class BoolNode(AnyNode):
    decode = bool


class FloatNode(AnyNode):
    decode = float


class DecimalNode(AnyNode):
    decode = Decimal
    encode = str


class TupleNode(AnyNode):
    decode = tuple
    encode = list

    def __init__(self, node_list, **kwargs):
        super(TupleNode, self).__init__(**kwargs)
        self.node_list = node_list


class ListNode(AnyNode):
    decode = list
    encode = list

    def __init__(self, node, **kwargs):
        super(ListNode, self).__init__(**kwargs)
        self.node = node


class DictNode(AnyNode):
    decode = dict
    encode = dict

    def __init__(self, key_node, value_node, **kwargs):
        super(DictNode, self).__init__(**kwargs)
        self.value_node = value_node
        self.key_node = key_node or StrNode()


class BeanNode(AnyNode):
    decode = dict

    def __init__(self, bean, **kwargs):
        super(BeanNode, self).__init__(**kwargs)
        self.bean = bean


class Registry(AnyNode):
    def __init__(self, args_getter, registry, default):
        super(Registry, self).__init__(default=default)
        self.args_getter = args_getter
        self.registry = registry
