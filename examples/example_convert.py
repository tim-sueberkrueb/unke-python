# -*- coding: utf-8

import unke
import unke.convert


def main():
    doc = unke.load('example_simple.unk')
    print('Loaded example_simple.unk.')

    print()

    mydict = unke.convert.document_to_dict(doc)
    print('Converted to dict:')
    print(mydict)

    print()

    myjson = unke.convert.document_to_json(doc, 2)
    print('Converted to json:')
    print(myjson)

    print()

    with open('example_convert.json') as json_file:
        print('Loaded example_convert.json:')
        mydocument = unke.convert.json_to_document(json_file.read())
        print(mydocument)

if __name__ == '__main__':
    main()
