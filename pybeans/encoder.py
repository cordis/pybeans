from pybeans.const import UNDEFINED
from pybeans.exceptions import EncodingException
from pybeans.nodes import *


class SchemaEncoder(object):
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

    def __call__(self, node, value, data):
        return self._visit_node(node, value, data)

    def _visit_bean(self, node, value, data):
        attr_node_list = node.bean.__pybeansschema__.get_nodes()
        for attr, node in attr_node_list:
            data[attr] = self._visit_node(node, getattr(value, attr, node.default), data.get(attr, {}), attr)
        return data

    @staticmethod
    def _visit_value(node, value, data):
        if node.encode:
            value = node.encode(value)
        return value

    def _visit_tuple(self, node, value, data):
        assert not data
        ret = []
        for item, item_node in zip(value, node.node_list):
            ret.append(self._visit_node(item_node, item, {}))
        return self._visit_value(node, value, data)

    def _visit_list(self, node, value, data):
        if not data:
            data = list()
        for item in value:
            data.append(self._visit_node(node.node, item, {}))
        return data

    def _visit_dict(self, node, value, data):
        for key, item in value.iteritems():
            key = self._visit_node(node.key_node, key, {})
            data[key] = self._visit_node(node.value_node, item, {})
        return data

    def _visit_node(self, node, value, data, attr=None):
        if value is UNDEFINED:
            raise EncodingException('{0} is not defined'.format(attr))
        if value is None:
            return value
        if value is NotImplemented:
            value = node.default
        visitor = self._get_visitor(node)
        return visitor(node, value, data)

    def _get_visitor(self, node):
        return self.visitors[type(node)]
