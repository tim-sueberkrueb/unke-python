# -*- coding: utf-8


class ParseException(Exception):
    """
    Thrown by Unke parser in case of syntax errors
    """
    def __init__(self, message, line, col):
        super(ParseException, self).__init__("{}, line {}:{}".format(message, line, col))
