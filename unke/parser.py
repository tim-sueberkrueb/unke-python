# -*- coding: utf-8

import typing

from . import lexer
from . import grammar
from . import document
from . import objects
from . import exceptions


def parse(text: str, object_type: objects.BaseObject=objects.BoostedObject,
          object_created_hook: typing.Callable = None, doc: document.Document=None):
    """
    Parse a Unke string and return resulting document object
    :param text: Text to parse
    :param object_type: Class to be used to instantiate objects
    :param doc: Document to use
    :param object_created_hook: Function to be called after an object was created
    :return: Japis document
    """

    # Lex: retrieve tokens
    tokens = lexer.lex(text)

    # Create a document if none is specified
    doc = doc or document.Document()

    # Helper class to store the current context used when parsing the token stream
    class Context:
        # The object hierarchy e.g.: [Object('Root'), Object('Child Lvl1'), List('Child Lvl1, property')]
        hierarchy = []
        # Current node tag. An open curly brace must follow
        current_node_tag = None
        # Current property tag. A primitive value, list or object must follow
        current_property_tag = None
        # Current line
        current_line = 1
        # Pos of current line
        current_line_pos = 0
        # Current pos in line
        current_pos = 0
        # End of document
        eod = False
        # Separator expected
        separator_expected = False
        # Separator allowed
        separator_allowed = True

    # Helper class for lists, only used internally to control lists in Context.hierarchy
    class List:
        def __init__(self, parent, property: str or None, value: list):
            # The parent of the list can either be a Object or List
            self.parent = parent
            # The property this list is attached to.
            # A list must either be attached to a property or a child of List
            self.property = property
            # The actual list
            self.value = value
            # Set to true if a separator (comma) is expected
            self.separator_expected = False

    # Reference to the current context
    ctx = Context()

    # Handle token one by one
    for token in tokens:
        # Every token is a tuple consisting of three entries:
        # token[0]: Tag
        # token[1]: Value
        # token[2]: Flags
        # token[3]: Position

        # Calculate line pos
        ctx.current_pos = token[3] - ctx.current_line_pos

        # Root node closed: document should end
        if ctx.eod and grammar.Tag.Br != token[0]:
            raise exceptions.ParseException('End of document expected', ctx.current_line, ctx.current_pos)

        # Node tag
        if grammar.Tag.ObjectTag == token[0]:
            if doc.root:
                parent = ctx.hierarchy[-1]
                if type(parent) == List:
                    # Check if there was a separator before this item
                    if parent.separator_expected:
                        raise exceptions.ParseException('Expected token ","', ctx.current_line, ctx.current_pos)
                else:
                    if ctx.separator_expected:
                        raise exceptions.ParseException('Expected token ";" or line break', ctx.current_line,
                                                        ctx.current_pos)
            ctx.current_node_tag = token[1]
        # Open curly brace
        elif grammar.Tag.BlockStart == token[0]:
            is_list = type(ctx.hierarchy[-1]) == List if doc.root else False

            # Raise exception if no opening brace is expected
            if doc.root and not (ctx.current_property_tag or ctx.current_node_tag or is_list):
                raise exceptions.ParseException('Unexpected token "{"', ctx.current_line, ctx.current_pos)

            current_node = object_type()
            current_node.name = ctx.current_node_tag
            ctx.current_node_tag = None
            ctx.separator_expected = False
            if not doc.root:
                doc.root = current_node
            else:
                parent = ctx.hierarchy[-1]
                if type(parent) == List:
                    if parent.separator_expected:
                        raise exceptions.ParseException('Expected token ","', ctx.current_line, ctx.current_pos)

                    parent.value.append(current_node)
                else:
                    if ctx.current_property_tag:
                        parent.properties[ctx.current_property_tag] = current_node
                        ctx.current_property_tag = None
                    else:
                        current_node.parent = parent
                        parent.children.append(current_node)
            ctx.hierarchy += [current_node]
        # Close curly brace
        elif grammar.Tag.BlockEnd == token[0]:
            if len(ctx.hierarchy) == 0 or isinstance(type(ctx.hierarchy[-1]), objects.BaseObject):
                raise exceptions.ParseException('Unexpected token "}"', ctx.current_line, ctx.current_pos)

            if ctx.current_property_tag:
                raise exceptions.ParseException('Expected value', ctx.current_line, ctx.current_pos)

            is_root = ctx.hierarchy[-1] == doc.root
            if isinstance(object_created_hook, typing.Callable):
                object_created_hook(ctx.hierarchy[-1])
            ctx.hierarchy.pop()

            if is_root:
                ctx.eod = True
            else:
                parent = ctx.hierarchy[-1]
                if type(parent) == List:
                    parent.separator_expected = True
                elif isinstance(parent, objects.BaseObject):
                    ctx.separator_expected = True
        # Open square bracket
        elif grammar.Tag.ListStart == token[0]:
            if type(ctx.hierarchy[-1]) == List:
                parent_list = ctx.hierarchy[-1]
                if parent_list.separator_expected:
                    raise exceptions.ParseException('Expected token ","', ctx.current_line, ctx.current_pos)
                current_list = List(parent_list, None, [])
                ctx.hierarchy += [current_list]
            else:
                if not ctx.current_property_tag:
                    raise exceptions.ParseException('Unexpected token "["', ctx.current_line, ctx.current_pos)
                current_node = ctx.hierarchy[-1]
                l = List(current_node, ctx.current_property_tag, [])
                ctx.hierarchy += [l]
                ctx.current_property_tag = None
        # Close square bracket
        elif grammar.Tag.ListEnd == token[0]:
            l = ctx.hierarchy[-1]
            if not type(l) == List:
                raise exceptions.ParseException('Unexpected token "]"', ctx.current_line, ctx.current_pos)

            # Check if there was a ',' before ']'
            if len(l.value) > 0 and not l.separator_expected:
                raise exceptions.ParseException('Unexpected token "," before "]"', ctx.current_line, ctx.current_pos)

            if type(l.parent) == List:
                l.parent.value.append(l.value)
                l.parent.separator_expected = True
            else:
                l.parent.properties[l.property] = l.value
                ctx.separator_expected = True
                ctx.separator_allowed = True
            ctx.hierarchy.pop()
        # List separator
        elif grammar.Tag.ListSeparator == token[0]:
            parent = ctx.hierarchy[-1]
            if type(parent) != List or not parent.separator_expected:
                raise exceptions.ParseException('Unexpected token ","', ctx.current_line, ctx.current_pos)
            parent.separator_expected = False
        # Property tag
        elif grammar.Tag.PropertyTag == token[0]:
            if ctx.separator_expected:
                raise exceptions.ParseException('Expected token ";" or line break', ctx.current_line, ctx.current_pos)
            if doc.root and isinstance(ctx.hierarchy[-1], List):
                raise exceptions.ParseException('Unexpected property', ctx.current_line, ctx.current_pos)
            ctx.current_property_tag = token[1].replace(' ', '')[:-1]
            ctx.separator_expected = False
            ctx.separator_allowed = False
        # Property values
        elif grammar.Flag.Value in token[2]:
            current_node = ctx.hierarchy[-1]
            value = None
            if grammar.Tag.PropertyValueInt == token[0]:
                value = int(token[1])
            elif grammar.Tag.PropertyValueFloat == token[0]:
                value = float(token[1])
            elif grammar.Tag.PropertyValueBool == token[0]:
                value = (token[1] == 'true')
            elif grammar.Tag.PropertyValueString == token[0]:
                value = token[1][1:len(token[1])-1]

            if type(current_node) == List:
                if current_node.separator_expected:
                    raise exceptions.ParseException('Expected token ","', ctx.current_line, ctx.current_pos)
                current_node.value.append(value)
                current_node.separator_expected = True
            else:
                if not ctx.current_property_tag:
                    raise exceptions.ParseException('Unexpected value "{}"'.format(str(value)),
                                                    ctx.current_line, ctx.current_pos)
                current_node.properties[ctx.current_property_tag] = value
                ctx.current_property_tag = None
                ctx.separator_expected = True
                ctx.separator_allowed = True
        # Line break
        elif grammar.Tag.Br == token[0]:
            ctx.current_line += 1
            ctx.current_line_pos = token[3]
            ctx.current_pos = 0
            ctx.separator_expected = False
        # Separator (Semicolon)
        elif grammar.Tag.PropertySeparator == token[0]:
            if not ctx.separator_allowed:
                raise exceptions.ParseException('Unexpected token ";"', ctx.current_line, ctx.current_pos)
            ctx.separator_expected = False

    # Detect missing closing curly brace(s)
    if len(ctx.hierarchy) > 0:
        raise exceptions.ParseException('Expected token "}"', ctx.current_line, ctx.current_pos)

    return doc
