# -*- coding: utf-8 -*-
import unittest
from tag_processor import DataContainer, TagParser
from tag_processor.models import TernaryTag, ConstantTag, FunctionTag


class TagParserTest(unittest.TestCase):

    def test_single_attribute(self):
        data = DataContainer()
        parser = TagParser(data)
        input_string = u"[get_cost]"
        elements = parser._split_by_elements(input_string)
        self.assertEqual(elements[0], '[get_cost]')

    def test_attribute_parameter_with_double_underscores(self):
        data = DataContainer()
        data.warehouse = dict()
        data.warehouse['storage'] = dict()
        data.warehouse['storage']['cargo'] = [{
            'name': 'mirror',
            'quantity': 12
        }, {
            'name': 'wheel',
            'quantity': 45
        }]

        input = "[random__warehouse]__warehouse[get_name]__storage[max=cargo__quantity]__name_"
        parser = TagParser(data)
        elements = parser._split_by_elements(input)
        self.assertEqual(len(elements), 4)
        self.assertEqual(elements[0], "[random__warehouse]")
        self.assertEqual(elements[1], "warehouse[get_name]")
        self.assertEqual(elements[2], "storage[max=cargo__quantity]")
        self.assertEqual(elements[3], "name_")

    def test_inline_tags(self):
        input_string = "${${warning_message}|${error_message}}"
        parser = TagParser(None)
        tags = parser._get_raw_tags(input_string)

        self.assertEqual(tags[1], [ 'warning_message', 'error_message' ])
        self.assertEqual(tags[0], [
            '${warning_message}|${error_message}'
        ])

    def test_escaping(self):
        input_string = "${error?Error\: Not defined : OK}"
        parser = TagParser(None)
        tags = parser.parse(input_string)

        self.assertEqual(len(tags), 1)
        tag = tags[0]
        chain = tag['chain']
        self.assertEqual(len(chain), 1)
        ternary_tag = chain[0]
        self.assertIsInstance(ternary_tag, TernaryTag)
        self.assertIsInstance(ternary_tag.if_true, ConstantTag)
        self.assertIsInstance(ternary_tag.if_false, ConstantTag)

        self.assertEqual("Error\: Not defined ", ternary_tag.if_true.value)
        self.assertEqual(" OK", ternary_tag.if_false.value)

    def test_multiple_function_params(self):
        input_string = "${[function=f,s,t]}"
        parser = TagParser(None)
        tags = parser.parse(input_string)

        self.assertEqual(len(tags), 1)
        tag = tags[0]
        chain = tag['chain']
        self.assertEqual(len(chain), 1)
        function_tag = chain[0]
        self.assertIsInstance(function_tag, FunctionTag)
        self.assertEqual(3, len(function_tag.params))
