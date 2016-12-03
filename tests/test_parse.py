# -*- coding: utf-8

import unittest
import unke


class ParseTest(unittest.TestCase):
    def test_object_properties(self):
        unke_text = """
        Object {
            stringprop: "Hello"
            intprop: 42
            floatprop: 3.14
            boolprop: true
        }
        """
        doc = unke.loads(unke_text)
        self.assertIsInstance(doc.root, unke.BaseObject)
        self.assertEqual(doc.root.properties["stringprop"], "Hello")
        self.assertEqual(doc.root.properties["intprop"], 42)
        self.assertEqual(doc.root.properties["floatprop"], 3.14)
        self.assertEqual(doc.root.properties["boolprop"], True)

    def test_no_root_tag(self):
        unke_text = "{}"
        doc = unke.loads(unke_text)
        self.assertIsInstance(doc.root, unke.BaseObject)

    def test_object_children(self):
        unke_text = """
        Root {
            LevelOne {
                LevelTwo {
                    property: "Some string"
                }
            }
            LevelOne {
                LevelTwo {

                }
            }
        }
        """
        doc = unke.loads(unke_text)
        self.assertEqual(len(doc.root.children), 2)
        self.assertEqual(doc.root.children[0].children[0].properties["property"], "Some string")

    def test_list(self):
        my_list = [1, 2, 35.781, True, False, "String 1", "String 2"]
        unke_text = """
        Root {
            emptylist: []
            mylist: [
                1,
                2,
                35.781,
                true,
                false,
                "String 1",
                "String 2"
            ]
            myobjectlist: [
                Object {

                },
                ObjectB {
                    Child {

                    }
                },
                {
                    // anonymous object
                },
                true,
                false
            ]
            sublists: [
                [
                    3,
                    6,
                    9,
                    12
                ],
                "ABC",
                "CDE",
                [
                    true,
                    false,
                    false
                ],
                [
                    [
                        [
                            1,
                            2,
                            [3]
                        ]
                    ]
                ]
            ]
        }
        """
        doc = unke.loads(unke_text)
        self.assertEqual(len(doc.root.children), 0)
        self.assertIsInstance(doc.root.properties["mylist"], list)
        self.assertEqual(doc.root.properties["mylist"], my_list)
        self.assertEqual(len(doc.root.properties["myobjectlist"]), 5)
        self.assertIsInstance(doc.root.properties["myobjectlist"][0], unke.objects.BaseObject)
        self.assertEqual(len(doc.root.properties["myobjectlist"][1].children), 1)
        self.assertEqual(doc.root.properties["myobjectlist"][1].children[0].name, "Child")

        self.assertEqual(len(doc.root.properties["sublists"]), 5)
        self.assertEqual(len(doc.root.properties["sublists"][0]), 4)
        self.assertEqual(doc.root.properties["sublists"][1], "ABC")
        self.assertEqual(doc.root.properties["sublists"][3], [True, False, False])
        self.assertEqual(doc.root.properties["sublists"][4][0][0], [1, 2, [3]])

    def test_list_illegal_trailing_comma(self):
        unke_text = """
            Root {
                illegallist: [
                    1,2,
                ]
            }
        """
        with self.assertRaises(unke.ParseException):
            unke.loads(unke_text)

    def test_list_illegal_no_comma(self):
        unke_text = """
            Root {
                illegallist: [
                    1
                    2
                ]
            }
        """
        with self.assertRaises(unke.ParseException):
            unke.loads(unke_text)

    def test_eod(self):
        unke_text = """
            Root {

            }
            // Root node already closed
            }
        """
        with self.assertRaises(unke.ParseException):
            unke.loads(unke_text)

    def test_minified(self):
        unke_text = "Tree{Trunk{Branch{props:[true,false,1,42,3.14,Apple{color:'red';size:1},Apple{}]};;;;Branch{}}}"
        # Also tests for multiple separators ";;;;"
        doc = unke.loads(unke_text)
        self.assertEqual(doc.root.children[0].children[0].properties["props"][5].properties["color"], "red")

    def test_illegal_semikolon(self):
        unke_text_1 = """
            Root {
                test: 21
                list: [
                    1;
                ]
            }
        """
        with self.assertRaises(unke.ParseException):
            unke.loads(unke_text_1)

        unke_text_2 = """
            Root {
                test: ; 0
            }
        """
        with self.assertRaises(unke.ParseException):
            unke.loads(unke_text_2)

    def test_illegal_property(self):
        unke_text = """
            Node {
                test: [
                    test:
                ]
            }
        """
        with self.assertRaises(unke.ParseException):
            unke.loads(unke_text)

    def test_object_type_and_hook(self):
        unke_text = "Root {}"

        class MyTestObject(unke.BaseObject):
            object_hook_called = False

            def __init__(self):
                unke.BaseObject.__init__(self)
                self.val = True

        def my_object_hook(obj):
            MyTestObject.object_hook_called = True
            self.assertIsInstance(obj, MyTestObject)

        doc = unke.loads(unke_text, object_type=MyTestObject, object_created_hook=my_object_hook)
        self.assertIsInstance(doc.root, MyTestObject)
        self.assertEqual(doc.root.val, True)
        self.assertEqual(MyTestObject.object_hook_called, True)
