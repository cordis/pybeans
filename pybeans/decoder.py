import copy

from pybeans.const import UNDEFINED
from pybeans.exceptions import DecodingException
from pybeans.nodes import *


class SchemaDecoder(object):
    visitors = None

    @classmethod
    def create_instance(cls):
        instance = cls()
        instance.visitors = {
            StrNode: instance._visit_value,
            UnicodeNode: instance._visit_value,
            IntNode: instance._visit_value,
            BoolNode: instance._visit_value,
            FloatNode: instance._visit_value,
            DecimalNode: instance._visit_value,
            TupleNode: instance._visit_tuple,
            ListNode: instance._visit_list,
            DictNode: instance._visit_dict,
            BeanNode: instance._visit_bean,
        }
        return instance

    def __call__(self, node, data):
        return self._visit_node(node, data)

    def _visit_bean(self, node, data):
        bean = copy.copy(node.bean)
        for attr, nested_node in bean.__pybeansschema__.get_nodes():
            value = self._visit_node(nested_node, data.get(attr, nested_node.default))
            setattr(bean, attr, value)
        return bean

    def _visit_node(self, node, value, attr=None):
        if value is UNDEFINED:
            raise DecodingException('{0} is not defined'.format(attr))
        if value is None:
            return value
        visitor = self._get_visitor(node)
        return visitor(node, value)

    def _get_visitor(self, node):
        return self.visitors[type(node)]

    @staticmethod
    def _visit_value(node, value):
        if node.decode:
            value = node.decode(value)
        return value

    def _visit_tuple(self, node, value):
        ret = []
        for item, item_node in zip(value, node.node_list):
            ret.append(self._visit_node(item_node, item))
        return self._visit_value(node, value)

    def _visit_list(self, node, value):
        ret = []
        for item in value:
            ret.append(self._visit_node(node.node, item))
        return ret

    def _visit_dict(self, node, value):
        ret = {}
        for key, item in value.iteritems():
            key = self._visit_node(node.key_node, key)
            ret[key] = self._visit_node(node.value_node, item)
        return ret
