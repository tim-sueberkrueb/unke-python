# -*- coding: utf-8

from . import document
from . import objects


def document_to_string(doc: document.Document, indent_level: int = 0, indent: int = 4,
                       wrap_lines=True, spacing=True) -> str:
    """
    Serialize Unke document to Unke string
    :param doc: Document to serialize
    :param indent_level: Level of indentation
    :param indent: Indentation in spaces
    :param wrap_lines: Wrap lines
    :param spacing: Insert space between property and value or object name and opening brace
    :param default_leading_comment: Insert default leading comment
    :return: Resulting Unke string
    """
    text = ''
    text += object_to_string(
        doc.root,
        indent_level,
        indent,
        wrap_lines,
        spacing
    )
    return text


def object_to_string(obj: objects.BaseObject, indent_level: int = 0, indent: int = 4,
                     wrap_lines=True, spacing=True, no_leading_indent=False) -> str:
    """
    Serialize Unke object to Unke string fragment
    :param obj: Object to serialize
    :param indent_level: Level of indentation
    :param indent: Indentation in spaces
    :param wrap_lines: Wrap lines
    :param spacing: Insert space between property and value or object name and opening brace
    :param no_leading_indent: No leading indentation
    :return: Resulting Unke string fragment
    """
    # Check if the object is empty
    empty = (len(obj.children) + len(obj.properties) == 0)

    # Object name, opening bracket
    text = '{}{}{}{}'.format(
        _whitespace(indent_level, indent) if not no_leading_indent else '',
        obj.name,
        ' {' if spacing else '{',
        '\n' if wrap_lines and not empty else ''
    )

    # Children
    for child in obj.children:
        text += object_to_string(child, indent_level + 1, indent, wrap_lines, spacing)
        text += '\n' if wrap_lines else ';'

    for property_name in obj.properties:
        property_value = obj.properties[property_name]
        text += property_to_string(
            property_name,
            property_value,
            indent_level + 1,
            indent,
            wrap_lines,
            spacing
        )

    # Closing bracket
    text += '{}{}'.format(
        _whitespace(indent_level, indent) if not empty else '',
        '}'
    )
    return text


def property_to_string(name: str, value, indent_level: int = 0, indent: int = 4, wrap_lines=True, spacing=True):
    """
    Serialize a property to Unke string fragment
    :param name:
    :param value: Python value to convert
    :param indent_level: Level of indentation
    :param indent: Indentation in spaces
    :param wrap_lines: Wrap lines
    :param spacing: Insert space between property and value or object name and opening brace
    :return: Resulting Unke string fragment
    """
    return '{}{}{}{}{}'.format(
        _whitespace(indent_level, indent),
        name,
        ': ' if spacing else ':',
        value_to_string(value, indent_level, indent, wrap_lines, spacing, no_leading_indent=True),
        '\n' if wrap_lines else ';'
    )


def value_to_string(value, indent_level: int = 0, indent: int = 4, wrap_lines=True,
                    spacing=True, no_leading_indent=False):
    """
    Serialize a Python value to Unke string fragment
    :param value: Python value to convert
    :param indent_level: Level of indentation
    :param indent: Indentation in spaces
    :param wrap_lines: Wrap lines
    :param spacing: Insert space between property and value or object name and opening brace
    :param no_leading_indent: No leading indentation
    :return: Resulting Unke string fragment
    """
    if isinstance(value, objects.BaseObject):
        return '{}{}'.format(
            _whitespace(indent_level, indent) if not no_leading_indent else '',
            object_to_string(value, indent_level, indent, wrap_lines, spacing, no_leading_indent=True)
        )
    elif type(value) == list:
        text = '{}[{}'.format(
            _whitespace(indent_level, indent) if not no_leading_indent else '',
            '\n' if wrap_lines else ''
        )
        for i, el in enumerate(value):
            text += value_to_string(el, indent_level + 1, indent, wrap_lines, spacing)
            if i < len(value) - 1:
                text += ','
            text += '\n' if wrap_lines else ''
        text += '{}]'.format(
            _whitespace(indent_level, indent)
        )
        return text
    elif type(value) == bool:
        return ('{}true' if value else '{}false').format(
            _whitespace(indent_level, indent) if not no_leading_indent else ''
        )
    else:
        return '{}{}'.format(
            _whitespace(indent_level, indent) if not no_leading_indent else '',
            repr(value)
        )


def _whitespace(indent_level, indent):
    return ' ' * (indent_level * indent)
