# -*- coding: utf-8

import typing

from .objects import BaseObject, BoostedObject
from .document import Document
from .parser import parse
from .dump import document_to_string
from .exceptions import ParseException


__author__ = 'Tim Süberkrüb'
__copyright__ = 'Copyright (C) 2016 Tim Süberkrüb'
__license__ = 'MIT'
__version__ = '0.1.0'


def loads(s: str, object_type: BaseObject=BoostedObject, object_created_hook: typing.Callable=None) -> Document:
    """
    Parse Unke string and return resulting document object
    :param s: String to parse
    :param object_type: Class to be used to instantiate objects
    :param object_created_hook: Function to be called after an object was created
    :return: Document
    """
    return parse(s, object_type, object_created_hook)


def dumps(doc: Document, beautify: bool=True, indent: int=4) -> str:
    """
    Serialize Unke document to string
    :param doc: Document to serialize
    :param beautify: Format for human-readability
    :param indent: Indentation in spaces
    :return: Resulting Unke string
    """
    return document_to_string(
        doc,
        indent=indent if beautify else 0,
        wrap_lines=beautify,
        spacing=beautify
    )


def load(filename: str, object_type: BaseObject=BoostedObject, object_created_hook: typing.Callable=None) -> Document:
    """
    Load Unke file and return resulting document object
    :param filename: Filename to open
    :param object_type: Class to be used to instantiate objects
    :param object_created_hook: Function to be called after an object was created
    :return: Document
    """
    with open(filename, 'r') as file:
        return loads(file.read(), object_type, object_created_hook)


def dump(filename: str, doc: Document, beautify: bool=True, indent: int=4) -> None:
    """
    Dump a Unke document to text file
    :param filename: Filename to dump to
    :param doc: Document to serialize
    :param beautify: Format for human-readability
    :param indent: Indentation in spaces
    """
    with open(filename, 'w') as file:
        file.write(dumps(doc, beautify, indent))
