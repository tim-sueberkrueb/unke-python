# -*- coding: utf-8

import timeit
import json
import json.decoder
import json.scanner


# Custom JSON Decoder:
# To make the comparision fair, we force the Python JSON library
# to use the Python implementation of its JSON decoder.
# Per default it will try to use a C implementation for better performance
class CustomJSONDecoder(json.decoder.JSONDecoder):
    def __init__(self, **kwargs):
        json.decoder.JSONDecoder.__init__(self, **kwargs)
        self.scan_once = json.scanner.py_make_scanner(self)


# Number of test repetitions
test_repetitions = 100


def main():
    print('Please wait ... this will take some time depending on your machine')

    print('Running Unke load test ...')
    time_unke = timeit.timeit(
        'unke.loads(text)',
        'import unke\n' +
        'with open("example_performance.unk") as file:\n text=file.read()',
        number=test_repetitions
    )
    print('Done.')

    print('Running Unke lex test ...')
    time_unke_lex = timeit.timeit(
        'unke.lexer.lex(text)',
        'import unke.lexer\n' +
        'with open("example_performance.unk") as file:\n text=file.read()',
        number=test_repetitions
    )

    print('Running JSON test ...')
    time_json = timeit.timeit(
        'json.loads(text, cls=CustomJSONDecoder)',
        'import json\n' +
        'with open("example_performance.json") as file:\n text=file.read()',
        number=test_repetitions, globals=globals()
    )
    print('Done.')

    print()

    print('t[unke]\t\t: {}'.format(time_unke))
    print('t[json]\t\t\t: {}'.format(time_json))
    print()
    print('t[unke-json]\t: {}'.format(time_unke-time_json))
    print()
    print('In this test, loading the JSON file was {}x faster than Unke'.format(
        round((time_unke/time_json), 2)
    ))
    print('Lexing took {}% of the overall Unke parsing time'.format(
        round(time_unke_lex/time_unke*100, 2)
    ))
    print('Parsing the tokens took {}% of Unke parsing time'.format(
        round((time_unke-time_unke_lex)/time_unke * 100, 2)
    ))


if __name__ == '__main__':
    main()
