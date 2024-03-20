import unittest

from test.bold.bold_test import BoldTest
from test.hstack.hstack_test import HStackTest
from test.image.image_test import ImageTest
from test.list_items.list_items_test import ListItemsTest
from test.table.table_test import TableTest
from test.text.text_test import TextTest
from test.title.title_test import TitleTest
from test.vstack.vstack_test import VStackTest


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(HStackTest))
    test_suite.addTest(unittest.makeSuite(VStackTest))
    test_suite.addTest(unittest.makeSuite(ImageTest))
    test_suite.addTest(unittest.makeSuite(TableTest))
    test_suite.addTest(unittest.makeSuite(TextTest))
    test_suite.addTest(unittest.makeSuite(BoldTest))
    test_suite.addTest(unittest.makeSuite(TitleTest))
    test_suite.addTest(unittest.makeSuite(ListItemsTest))

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
