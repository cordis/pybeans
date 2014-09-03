from decimal import Decimal
from functools import partial

from pybeans.const import UNDEFINED
from pybeans.nodes import *
from pybeans.decoder import SchemaDecoder
from pybeans.encoder import SchemaEncoder


class Schema(object):
    __decoder__ = SchemaDecoder.create_instance()
    __encoder__ = SchemaEncoder.create_instance()

    equal_type_map = {
        str: StrNode,
        unicode: UnicodeNode,
        int: IntNode,
        bool: BoolNode,
        float: FloatNode,
        Decimal: DecimalNode,
    }

    @classmethod
    def decode(cls, data, bean):
        return cls.__decoder__(BeanNode(bean), data)

    @classmethod
    def encode(cls, bean, data):
        return cls.__encoder__(BeanNode(bean), bean, data)

    def __init__(self, attr_dict, default_dict):
        self.node_dict = self._create_node_dict(attr_dict, default_dict)

    def _create_node_dict(self, attr_dict, default_dict):
        ret = {}
        for name, attr in attr_dict.items():
            if name.startswith('__'):
                continue
            default = default_dict.get(name, UNDEFINED)
            ret[name] = self._create_node(name, attr, default)
        return ret

    def _create_node(self, name, attr, default=UNDEFINED):
        attr_type = type(attr)
        try:
            return self.equal_type_map[attr_type](default=default)
        except KeyError:
            pass
        if attr_type == tuple:
            item_node_list = []
            for index, item in enumerate(attr):
                item_node_list.append(self._create_node(name + '[{0}]'.format(index), item))
            return TupleNode(item_node_list, default=default)
        if attr_type == list:
            assert len(attr) == 1, '{0} list must content only item type'.format(name)
            item_node = self._create_node(name + '[item]', attr[0])
            return ListNode(item_node, default=default)
        if attr_type == dict:
            attr_items = attr.items()
            assert len(attr_items) == 1, '{0} dict must content only key and value types'.format(name)
            key_node, value_node = map(partial(self._create_node, name + '{key: value}'), attr_items[0])
            return DictNode(key_node, value_node, default=default)
        if hasattr(attr_type, '__pybeansschema__'):
            return BeanNode(attr, default=default)
        raise NotImplementedError('{0} type is not implemented'.format(name))

    def get_nodes(self):
        return self.node_dict.items()
