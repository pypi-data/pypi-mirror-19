# -*- coding: utf-8 -*-
from decimal import Decimal
import unittest
import datetime
from tag_processor import DataContainer, TagProcessor


class TagProcessorTest(unittest.TestCase):
    def test_complex_message(self):
        data = DataContainer()

        def get_cargo(client_offer, *args, **kwargs):
            return u'Мука, Соль, Сахар'

        data.get_cargo = get_cargo
        data.client_offer = {
            'transportation_type': u'Земля',
            'send_date': u'18.10.2015',
            'delivery_date': u'21.10.2015',
            'total_cost': 150000,
            'order': {
                'sender': {
                    'name': u'А1',
                    'city': {
                        'name': u'Москва',
                        'region': {
                            'name': u'Москва'
                        }
                    },
                    'street': u'Ленина',
                    'house': u'1',
                    'office': u'3а'
                },
                'consignee': {
                    'name': u'B1',
                    'city': {
                        'name': u'Самара',
                        'region': {
                            'name': u'Самарская область'
                        }
                    },
                    'street': u'Уралово',
                    'house': u'3',
                    'office': u'1'
                }
            }
        }
        processor = TagProcessor(data)
        input_string = u"<pre>Поступили предложения:<br>\r\n\r\n" \
                       u"Откуда:<br>${client_offer__order__sender__name} " \
                       u"${client_offer__order__sender__city__name} ${client_offer__order__sender__city__region__name} " \
                       u"${client_offer__order__sender__street} " \
                       u"${client_offer__order__sender__house}, ${client_offer__order__sender__office} <br>\r\n\r\n" \
                       u"Куда:<br>${client_offer__order__consignee__name} " \
                       u"${client_offer__order__consignee__city__name} ${client_offer__order__consignee__city__region__name} " \
                       u"${client_offer__order__consignee__street} " \
                       u"${client_offer__order__consignee__house}, ${client_offer__order__consignee__office} <br>\r\n\r\n" \
                       u"Груз: <br>${client_offer[get_cargo]}\r\n\r\n" \
                       u"Дата отправки ${client_offer__send_date}\r\n\r\n" \
                       u"Дата доставки ${client_offer__delivery_date}\r\n\r\n" \
                       u"Стоимость ${client_offer__total_cost}\r\n\r\n" \
                       u"Тип перевозки ${client_offer__transportation_type}</pre><br/>"

        result = processor.execute(input_string)

        reference = u"<pre>Поступили предложения:<br>\r\n\r\n" \
                    u"Откуда:<br>А1 Москва Москва Ленина 1, 3а <br>\r\n\r\n" \
                    u"Куда:<br>B1 Самара Самарская область Уралово 3, 1 <br>\r\n\r\n" \
                    u"Груз: <br>Мука, Соль, Сахар\r\n\r\n" \
                    u"Дата отправки 18.10.2015\r\n\r\n" \
                    u"Дата доставки 21.10.2015\r\n\r\n" \
                    u"Стоимость 150000\r\n\r\n" \
                    u"Тип перевозки Земля</pre><br/>"
        self.assertEqual(result, reference)

    def test_process_array_tag(self):
        data = DataContainer()
        data.order = {
            'cargo_set': [{
                'name': 1
            }, {
                'name': 2
            }]
        }
        processor = TagProcessor(data)
        input_string = u"Первый груз ${order__cargo_set[first]__name}"
        self.assertEqual(u"Первый груз 1", processor.execute(input_string))

    def test_process_self_tag(self):
        data = DataContainer()
        data.cost = 123

        processor = TagProcessor(data)
        input_string = u"Стоимость ${cost}"
        self.assertEqual(u"Стоимость 123", processor.execute(input_string))

    def test_single_attribute(self):
        data = DataContainer()

        def get_cost(*args, **kwargs):
            return 123

        data.get_cost = get_cost

        processor = TagProcessor(data)
        input_string = u"Стоимость ${[get_cost]}"
        self.assertEqual(u"Стоимость 123", processor.execute(input_string))

    def test_numeric(self):
        data = DataContainer()
        data.numeric_value = 100

        processor = TagProcessor(data)
        input_string = u"${numeric_value}"
        self.assertEqual(100, processor.execute(input_string))

    def test_process_double_tag(self):
        data = DataContainer()

        date = datetime.datetime.now()
        data.invoice = {
            'name': u'R12S1420015',
            'date': date
        }

        processor = TagProcessor(data)

        input_string = u"Счет номер$__ ${invoice__name} от ${invoice__date[dateformat=%d.%m.%Y %H:%M]}"
        self.assertEqual(u"Счет номер$__ R12S1420015 от %s" % date.strftime('%d.%m.%Y %H:%M'),
                         processor.execute(input_string))

    def test_process_double_tag_but_only_one_with_data(self):
        data = DataContainer()
        data.invoice = {
            'name': u'R12S1420015'
        }

        processor = TagProcessor(data)

        input_string = u"Счет номер$__ ${invoice__name} от ${invoice__date[dateformat=%d.%m.%Y %H:%M]}"
        self.assertEqual(u"Счет номер$__ R12S1420015 от ", processor.execute(input_string))

    def test_process_simple_tag(self):
        data = DataContainer()
        data.invoice = 'R12S1420015'
        processor = TagProcessor(data)
        input_string = u"Счет номер ${invoice}"
        self.assertEqual(u"Счет номер R12S1420015", processor.execute(input_string))

    def test_disjunction(self):
        data = DataContainer()
        data.invoice = None
        data.empty_value = u"-"
        processor = TagProcessor(data)
        input_string = u"Счет номер ${${invoice}|${empty_value}}"
        self.assertEqual(u"Счет номер -", processor.execute(input_string))

    def test_multiple_disjunction(self):
        data = DataContainer()
        data.choice = {
            'alter_invoice': u"Счет #1",
            'empty_value': u"-"
        }
        processor = TagProcessor(data)
        input_string = u"Счет номер ${${choice__invoice}|${choice__alter_invoice}|${choice__empty_value}}"
        self.assertEqual(u"Счет номер Счет #1", processor.execute(input_string))

    def test_ternary_operator_true_result(self):
        data = DataContainer()
        data.choice = {
            'if_true': u"sleep",
            'if_false': u"work",
            'condition': True
        }
        processor = TagProcessor(data)
        input_string = u"go to ${choice__condition?${choice__if_true}:${choice__if_false}}"
        self.assertEqual(u"go to sleep", processor.execute(input_string))

    def test_ternary_operator_false_result(self):
        data = DataContainer()
        data.choice = {
            'if_true': u"sleep",
            'if_false': u"work",
            'condition': False
        }
        processor = TagProcessor(data)
        input_string = u"go to ${choice__condition?${choice__if_true}:${choice__if_false}}"
        self.assertEqual(u"go to work", processor.execute(input_string))

    def test_ternary_with_inline(self):
        data = DataContainer()
        data.choice = {
            'if_true': u"sleep",
            'if_false': u"work",
            'condition': False,
            'second_condition': True,
            'second_if_true': u'holiday'
        }
        processor = TagProcessor(data)
        input_string = u"go to ${choice__condition?${choice__second_condition?${choice__second_if_true}:${choice__second_if_false}}:${${choice__second_if_false}|awesome ${choice__second_if_true}}}"
        self.assertEqual(u"go to awesome holiday", processor.execute(input_string))

    def test_ternary_decimal_result(self):
        data = DataContainer()
        data.choice = {
            'if_true': Decimal("1.20"),
            'condition': True
        }
        processor = TagProcessor(data)
        input_string = u"${choice__condition?${choice__if_true}:${choice__if_false}}"
        self.assertEqual(Decimal("1.20"), processor.execute(input_string))

    def test_lonely_ternary(self):
        data = DataContainer()
        data.choice = {
            'if_true': Decimal("1.20"),
            'with_specification': True,
            'invoice': 'счет',
            'invoice_date': 'дата счета',
        }
        processor = TagProcessor(data)
        input_string = u"${choice__with_specification?${choice__if_true} согласно детализации Д${choice__invoice} от ${choice__invoice_date}:${service__description}}"
        self.assertEqual("1.20 согласно детализации Дсчет от дата счета", processor.execute(input_string))

    def test_parameter_tag(self):
        data = DataContainer()

        def double(value, param, *args, **kwargs):
            return param * 2

        data.double = double
        data.choice = {
            'param': 2
        }
        processor = TagProcessor(data)
        input_string = u"${choice__[double=${choice__param}]}"
        self.assertEqual(4, processor.execute(input_string))

    def test_multiple_tag_params(self):
        data = DataContainer()
        data.update({
            'vehicle_1': 'Cart',
            'driver_1': 'Meatwad',
            'vehicle_2': 'TV-set'
        })
        input_string = u"${[join=/,${vehicle_1},${driver_1}]}${[wrap=(,${[join=/,${vehicle_2},${driver_2}]},)]}"
        processor = TagProcessor(data)
        self.assertEqual("Cart/Meatwad(TV-set)", processor.execute(input_string))


if __name__ == "__main__":
    unittest.main()
