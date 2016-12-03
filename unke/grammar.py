# -*- coding: utf-8

import re


class Flag():
    (
        Value,
        Ignore
    ) = range(2)


class Tag():
    (BlockStart,
     BlockEnd,
     ListStart,
     ListEnd,
     ListSeparator,
     PropertySeparator,
     PropertyTag,
     PropertyValueInt,
     PropertyValueFloat,
     PropertyValueBool,
     PropertyValueString,
     ObjectTag,
     CommentSingleLine,
     CommentMultiLineStart,
     CommentMultiLineEnd,
     Br,
     Whitespace) = range(17)


patterns = (
    # Tag                           # Regex                                 # Flags             # Description
    (Tag.CommentSingleLine,         (re.compile(r'//+.*?'),),               (Flag.Ignore,)),    # Single line comment
    (Tag.BlockStart,                (re.compile(r'{'),),                    tuple()),           # Block start
    (Tag.BlockEnd,                  (re.compile(r'}'),),                    tuple()),           # Block end
    (Tag.ListStart,                 (re.compile(r'\['),),                   tuple()),           # List start
    (Tag.ListEnd,                   (re.compile(r'\]'),),                   tuple()),           # List end
    (Tag.ListSeparator,             (re.compile(r','),),                    tuple()),           # List separator (comma)
    (Tag.PropertySeparator,         (re.compile(r';'),),                    tuple()),           # Property separator (;)
    (Tag.PropertyTag,               (re.compile(r'[A-Za-z_]+:'),),           tuple()),           # Property tag
    (Tag.PropertyValueFloat,        (re.compile(r'[-+]?[0-9]*?\.[0-9]+'),), (Flag.Value,)),     # Float
    (Tag.PropertyValueInt,          (re.compile(r'[-+]?[0-9]+'),),          (Flag.Value,)),     # Int
    (Tag.PropertyValueBool,         (re.compile(r'true|false'),),           (Flag.Value,)),     # Boolean
    (Tag.PropertyValueString, (
        re.compile(r"'(?:[^'\\]|\\.)*?'"),                                                      # String (single quotes)
        re.compile(r'"(?:[^"\\]|\\.)*?"')                                                       # String (double quotes)
    ), (Flag.Value,)),
    (Tag.CommentMultiLineStart,     (re.compile(r'/\*'),),                  tuple()),           # Comment start
    (Tag.CommentMultiLineEnd,       (re.compile(r'\*/'),),                  tuple()),           # Comment end
    (Tag.ObjectTag,                 (re.compile(r'[A-Za-z]+'),),            tuple()),           # Object tag
    (Tag.Br,                        (re.compile(r'\n'),),                   tuple()),           # Line break (\n)
    (Tag.Whitespace,                (re.compile('\s+'),),                   (Flag.Ignore,))     # Whitespace
)
