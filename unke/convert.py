# -*- coding: utf-8

import json

from . import document
from . import objects


def document_to_dict(doc: document.Document) -> dict:
    """
    Convert Unke document to Python dict
    :param doc: Document to convert
    :return: Resulting Python dict
    """
    return object_to_dict(doc.root)


def object_to_dict(obj: objects.BaseObject) -> dict:
    """
    Convert Unke object to Python dict
    :param obj: Object to convert
    :return: Resulting Python dict
    """
    properties = {}
    for property_name in obj.properties:
        property_value = obj.properties[property_name]
        if isinstance(property_value, objects.BaseObject):
            properties[property_name] = object_to_dict(property_value)
        elif type(property_value) == list:
            def handle_list(l):
                property_list = []
                for item in l:
                    if isinstance(item, objects.BaseObject):
                        property_list.append(object_to_dict(item))
                    elif type(item) == list:
                        property_list.append(handle_list(item))
                    else:
                        property_list.append(item)
                return property_list

            properties[property_name] = handle_list(property_value)
        else:
            properties[property_name] = property_value

    return {
        'name': obj.name,
        'properties': properties,
        'children': [object_to_dict(child) for child in obj.children]
    }


def document_to_json(doc: document.Document, indent: int = 0, minify: bool = False) -> str:
    """
    Convert Unke document to JSON string
    :param doc: Document to convert
    :param indent: Indentation in spaces
    :param minify: Compact encoding without spacing
    :return: Resulting JSON string
    """
    return json.dumps(
        document_to_dict(doc),
        indent=indent if indent > 0 else None,
        separators=(',', ':') if minify else None
    )


def object_to_json(obj: objects.BaseObject, indent: int = 0, minify: bool = False) -> str:
    """
    Convert Unke object to JSON string
    :param obj: Object to convert
    :param indent: Indentation in spaces
    :param minify: Compact encoding without spacing
    :return: Resulting JSON string
    """
    return json.dumps(
        object_to_dict(obj),
        indent=indent if indent > 0 else None,
        separators=(',', ':') if minify else None
    )


def dict_to_document(dict_value: dict) -> document.Document:
    """
    Convert Python dict to Unke document
    :param dict_value: Python dict to convert
    :return: Resulting document
    """
    doc = document.Document()
    doc.root = dict_to_object(dict_value)
    return doc


def dict_to_object(dict_value: dict, parent: objects.BaseObject = None) -> objects.BaseObject:
    """
    Convert Python dict to Unke object
    :param dict_value: Python dict to convert
    :param parent: Parent of resulting object
    :return: Resulting object
    """
    obj = objects.BoostedObject()
    obj.name = dict_value['name']
    obj.parent = parent
    for property_name in dict_value['properties']:
        property_value = dict_value['properties'][property_name]
        if type(property_value) == dict:
            obj.properties[property_name] = dict_to_object(property_value)
        elif type(property_value) == list:
            def handle_list(l):
                property_list = []
                for item in l:
                    if type(item) == dict:
                        property_list.append(dict_to_object(item))
                    elif type(item) == list:
                        property_list.append(handle_list(item))
                    else:
                        property_list.append(item)
                return property_list

            obj.properties[property_name] = handle_list(property_value)
        else:
            obj.properties[property_name] = property_value
    obj.children = [dict_to_object(child_dict, obj) for child_dict in dict_value['children']]
    return obj


def json_to_object(text: str) -> objects.BaseObject:
    """
    Convert JSON string to Unke object
    :param text: JSON string to convert
    :return: Resulting object
    """
    return dict_to_object(json.loads(text))


def json_to_document(text: str) -> document.Document:
    """
    Convert JSON string to document
    :param text: JSON string to convert
    :return: Resulting object
    """
    return dict_to_document(json.loads(text))
