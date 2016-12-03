# -*- coding: utf-8


class BaseObject:
    """
    Base Unke object type
    Represents a node in a document.
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.name = ''
        self.properties = {}

    @property
    def props(self):
        return self.properties

    @property
    def anonymous(self):
        return self.name is None

    @property
    def siblings(self):
        if self.parent:
            return list(filter(lambda sibling: sibling is not self, self.parent.children))
        else:
            return []

    def __repr__(self):
        return 'Object({}, {})'.format(self.name, id(self))


class BoostedObject(BaseObject):
    """
    Default Unke Object type with enhanced performance
    Represents a node in a document
    """

    # Making use of __slots__ to improve object creation performance
    __slots__ = ('parent', 'children', 'name', 'properties')

    def __init__(self):
        BaseObject.__init__(self)
