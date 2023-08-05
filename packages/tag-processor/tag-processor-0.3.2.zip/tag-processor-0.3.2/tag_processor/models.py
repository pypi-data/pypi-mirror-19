from builtins import object
import collections
import re
from tag_processor.services import execute_tag_chain

try:
    from django.db.models import Sum, Max, Min
except:
    pass

__all__ = [
    'DataContainer',
    'FunctionTag',
    'ObjectTag',
    'DisjunctionTag',
    'TernaryTag',
    'ConstantTag'
]


class DataContainer(dict):

    @staticmethod
    def dateformat(value, date_format):
        if not value:
            return None
        return value.strftime(date_format)

    @staticmethod
    def first(value, *args, **kwargs):
        return value[0]

    @staticmethod
    def str(value, *args, **kwargs):
        if value is None:
            return None
        return str(value)

    def __len__(self):
        return len(vars(self))

    @staticmethod
    def round(value, prec):
        return round(value, int(prec)) if value else None

    @staticmethod
    def join(value, separator, *args, **kwargs):
        return separator.join(v for v in args if v)

    @staticmethod
    def wrap(value, start_element, data, end_element, *args):
        if data:
            return start_element + str(data) + end_element
        return None

    def __getitem__(self, key):
        return getattr(self, key, None) or super(DataContainer, self).__getitem__(key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
        super(DataContainer, self).__setitem__(key, value)


class DjangoDataContainer(DataContainer):

    @staticmethod
    def first(queryset, *args, **kwargs):
        if queryset is None:
            return queryset
        all = queryset.all()
        if all.exists():
            return all[0]
        return None

    @staticmethod
    def count(queryset, *args, **kwargs):
        if queryset is None:
            return 0
        return queryset.count()

    @staticmethod
    def concat(queryset, field, *args, **kwargs):
        if queryset is None:
            return None
        values = set()
        for item in queryset.all():
            value = DjangoDataContainer._get_field_value(item, field, None)
            if value:
                values.add(str(value))
        return ",".join(values)

    @staticmethod
    def min(queryset, field, *args, **kwargs):
        if queryset is None:
            return None

        return queryset.aggregate(min=Min(field))['min']

    @staticmethod
    def max(queryset, field, *args, **kwargs):
        if queryset is None:
            return None
        return queryset.aggregate(max=Max(field))['max']

    @staticmethod
    def sum(queryset, field, *args, **kwargs):
        if queryset is None:
            return None
        return queryset.aggregate(sum=Sum(field))['sum']

    @staticmethod
    def _get_values(queryset, field):
        values = set()
        for item in queryset.all():
            value = DjangoDataContainer._get_field_value(item, field, None)
            if value:
                values.add(value)
        return values

    @staticmethod
    def _get_field_value(instance, field, default_value=None):
        field_path = field.split('__')
        attr = instance
        for elem in field_path:
            try:
                if isinstance(attr, list):
                    attr = attr[0]
                attr = getattr(attr, elem, None) or attr[elem]
            except AttributeError:
                return default_value
            except Exception:
                return default_value
        return attr


class FunctionTag(object):

    def __init__(self, value, params):
        self.value = value
        self.params = params

    @staticmethod
    def parse(input_string):
        function_elements = input_string[1:-1].split('=')
        function_parameters = None
        if len(function_elements) > 1:
            function_parameters = re.split(r'(?<!\\),', function_elements[1])
        return FunctionTag(function_elements[0], function_parameters)

    def execute(self, data, data_container):
        function = getattr(data_container, self.value, None)
        if not function or not hasattr(function, '__call__'):
            return data

        params = self.unbox_params(data_container)
        return function(data, *params)

    def unbox_params(self, data_container):
        if not self.params:
            return []

        params = []
        for param in self.params:
            param = param.replace("\\", "")
            if data_container is not None and param in data_container:
                params.append(data_container.get(param))
                continue
            params.append(param)
        return params


class ObjectTag(object):

    def __init__(self, value):
        self.value = value

    @staticmethod
    def parse(input_string):
        return ObjectTag(input_string)

    def execute(self, data, data_container):
        if data is None:
            return None
        result = getattr(data, self.value, None)
        if not result and callable(getattr(data, 'get', None)):
            result = data.get(self.value, None)
        return result


class DisjunctionTag(object):

    def __init__(self, elements):
        self.elements = elements

    @staticmethod
    def parse(input_string):
        disjunction_elements = []
        elements = re.split(r'(?<!\\)\|', input_string)
        for element in elements:
            disjunction_elements.append(ConstantTag(element))
        return DisjunctionTag(disjunction_elements)

    def execute(self, data, data_container):
        if not data:
            return None
        for element in self.elements:
            result = element.execute(data)

            if (result and data.get(result)) or result not in data.keys():
                return result
        return None


class TernaryTag(object):

    def __init__(self, condition, if_true, if_false):
        self.if_true = if_true
        self.if_false = if_false
        self.condition = condition

    def execute(self, data, data_container):
        if not data:
            return None
        if execute_tag_chain(self.condition, data):
            return self.if_true.execute()
        else:
            return self.if_false.execute()


class ConstantTag(object):

    def __init__(self, value):
        self.value = value

    def execute(self, *args, **kwargs):
        return self._remove_escaping(self.value)

    @staticmethod
    def _remove_escaping(input_string):
        return input_string.replace("\\", "")
