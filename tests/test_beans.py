# -*- coding: utf-8 -*-

from decimal import Decimal
from pybeans import bean, dict_to_bean, bean_to_dict


def test_plain_schema():
    default_node_value = 5
    unicode_node_value = u'Unicode строка'
    str_node_value = 'just a string'
    int_node_value = 10
    float_node_value = 4.45
    decimal_node_value = Decimal('32.233')

    @bean(default_node=default_node_value)
    class TestBean(object):
        default_node = int()
        unicode_node = unicode()
        str_node = str()
        int_node = int()
        float_node = float()
        decimal_node = Decimal()

    test_data = {
        'unicode_node': unicode_node_value,
        'str_node': str_node_value,
        'int_node': int_node_value,
        'float_node': float_node_value,
        'decimal_node': str(decimal_node_value),
    }

    empty_test_bean = dict_to_bean(test_data, TestBean)
    assert isinstance(empty_test_bean, TestBean)
    assert empty_test_bean.default_node == default_node_value
    assert empty_test_bean.unicode_node == unicode_node_value
    assert empty_test_bean.str_node == str_node_value
    assert empty_test_bean.int_node == int_node_value
    assert empty_test_bean.float_node == float_node_value
    assert empty_test_bean.decimal_node == decimal_node_value

    test_data['default_node'] = default_node_value
    assert test_data == bean_to_dict(empty_test_bean)


def test_nested_schema():
    @bean(int_node=4)
    class TestNestedBean(object):
        int_node = int()

    @bean(item_node={})
    class TestBean(object):
        item_node = TestNestedBean()
        list_node = [TestNestedBean()]
        dict_node = {str(): int()}
        tuple_node = (str(), float(), [int()])

    test_data = {
        'list_node': [
            {
                'int_node': 1
            },
            {
                'int_node': 2
            },
            {
                'int_node': 3
            },
        ],
        'dict_node': {
            'apple': 1,
            'orange': 2,
        },
        'tuple_node': [
            'bla',
            4.5,
            [
                3,
                2,
                1
            ],
        ],
    }

    empty_test_bean = dict_to_bean(test_data, TestBean)
    assert isinstance(empty_test_bean, TestBean)
    assert isinstance(empty_test_bean, TestBean)
    for i in range(3):
        assert isinstance(empty_test_bean.list_node[i], TestNestedBean)
        assert empty_test_bean.list_node[i].int_node == i + 1
    assert empty_test_bean.dict_node['apple'] == 1
    assert empty_test_bean.dict_node['orange'] == 2
    assert empty_test_bean.tuple_node == ('bla', 4.5, [3, 2, 1])
    dict_with_defaults = dict(test_data.items() + [('item_node', {'int_node': 4})])
    assert dict_with_defaults == bean_to_dict(empty_test_bean)


def test_defaults():
    @bean(int_node=4)
    class TestNestedBean(object):
        int_node = int()

    @bean(item_node={}, list_node=[], dict_node={'a': 1})
    class TestBean(object):
        item_node = TestNestedBean()
        list_node = [TestNestedBean()]
        dict_node = {str(): int()}

    test_bean = TestBean()
    assert bean_to_dict(test_bean) == {
        'item_node': {
            'int_node': 4,
        },
        'list_node': [],
        'dict_node': {'a': 1}
    }
    test_bean = dict_to_bean({}, TestBean)
    assert isinstance(test_bean.item_node, TestNestedBean)
    assert test_bean.item_node.int_node == 4
    assert test_bean.list_node == []
    assert test_bean.dict_node == {'a': 1}


if __name__ == '__main__':
    test_plain_schema()
    test_nested_schema()
    test_defaults()
