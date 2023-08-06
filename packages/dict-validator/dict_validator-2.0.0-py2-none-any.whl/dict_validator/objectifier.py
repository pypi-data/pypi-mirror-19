class Payload(object):  # pylint: disable=too-few-public-methods
    """A base class for the data object to be used instead of a dict."""


def _transform_value(value, mapping_class, mapping_transformer):
    if isinstance(value, mapping_class):
        return mapping_transformer(value)
    elif isinstance(value, list):
        return [_transform_value(item, mapping_class, mapping_transformer)
                for item in value]
    else:
        return value


def dict_to_object(dict_payload):
    """
    Convert a dict into a Python object.

    :param dict_payload: Value to be converted
    :type dict_payload: dict
    :return: payload
    :rtype: Pythonic object

    >>> DICT = {
    ...    "parent": {
    ...        "name": "Sam",
    ...        "children": [
    ...            {
    ...                "name": "Bill",
    ...                "grandchildren": [
    ...                    {"name": "John"}
    ...                ]
    ...            }
    ...        ]
    ...    }
    ... }
    >>> value = dict_to_object(DICT)
    >>> value.parent.name
    'Sam'
    >>> value.parent.children[0].name
    'Bill'
    >>> value.parent.children[0].grandchildren[0].name
    'John'
    """
    placeholder = Payload()
    for key, value in dict_payload.iteritems():
        setattr(placeholder, key,
                _transform_value(value, dict, dict_to_object))
    return placeholder


def _not_builtin(name):
    return not (name.startswith("__") and name.endswith("__"))


def object_to_dict(object_payload):
    """
    Convert a Python object into a dict.

    :param object_payload: Value to be converted
    :type object_payload: Pythonic object
    :return: payload
    :rtype: dict

    >>> from pprint import  pprint

    >>> DICT = {
    ...    "parent": {
    ...        "name": "Sam",
    ...        "children": [
    ...            {
    ...                "name": "Bill",
    ...                "grandchildren": [
    ...                    {"name": "John"}
    ...                ]
    ...            }
    ...        ]
    ...    }
    ... }

    >>> pprint(object_to_dict(dict_to_object(DICT)))
    {'parent': {'children': [{'grandchildren': [{'name': 'John'}],
                              'name': 'Bill'}],
                'name': 'Sam'}}
    """
    placeholder = {}
    for key in filter(_not_builtin, dir(object_payload)):
        placeholder[key] = _transform_value(
            getattr(object_payload, key), Payload, object_to_dict)
    return placeholder
