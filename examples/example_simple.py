# -*- coding: utf-8

import unke


def main():
    doc = unke.load('example_simple.unk')
    print('Root name:', doc.root.name)
    trunk = doc.root.children[0]
    print('Trunk:', trunk)
    branch = trunk.children[0]
    print('Branch:', branch)
    print('Apples:', branch.properties['apples'])

if __name__ == '__main__':
    main()
