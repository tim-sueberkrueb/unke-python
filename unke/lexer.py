# -*- coding: utf-8

import re
from . import grammar
from . import exceptions


def lex(text: str) -> list:
    '''
    Converts a Unke string into a list of tokens that can be read by the Unke parser
    :param text: Input string
    :return: Resulting list of tokens
    '''
    tokens = []
    pos = 0
    comment = False
    current_line = 1
    current_line_pos = 0
    while pos < len(text):
        match = None
        if comment:
            match = re.compile(r'\*/').search(text, pos)
            if match:
                pos = match.end(0)
                comment = False
            else:
                raise exceptions.ParseException('End of comment expected', current_line, 0)
        else:
            for pattern in grammar.patterns:
                pattern_tag = pattern[0]
                pattern_regex_tuple = pattern[1]
                pattern_flags = pattern[2]
                for pattern_regex in pattern_regex_tuple:
                    match = pattern_regex.match(text, pos)
                    if match:
                        if grammar.Tag.CommentMultiLineStart == pattern_tag:
                            comment = True
                            break
                        elif grammar.Flag.Ignore in pattern_flags:
                            break
                        else:
                            tokens.append((pattern_tag, match.group(0), pattern_flags, pos))
                        break
                if match:
                    if grammar.Tag.Br == pattern_tag:
                        current_line += 1
                        current_line_pos = pos
                    break
            if match:
                pos = match.end(0)
            else:
                raise exceptions.ParseException(
                    'Illegal character "{}"'.format(text[pos]),
                    current_line,
                    pos - current_line_pos
                )
    return tokens
