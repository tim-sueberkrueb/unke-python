# -*- coding: utf-8

import unke
import unke.convert


def main():
    doc = unke.load('example_dump.unk')
    print(doc)
    print(unke.dumps(doc))
    unke_string = unke.dumps(doc, beautify=False)
    print(unke_string)


if __name__ == '__main__':
    main()
