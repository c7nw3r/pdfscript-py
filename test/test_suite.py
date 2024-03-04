import unittest

from test.hstack.hstack_test import HStackTest
from test.image.image_test import ImageTest
from test.table.table_test import TableTest
from test.text.text_test import TextTest
from test.vstack.vstack_test import VStackTest


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(HStackTest))
    test_suite.addTest(unittest.makeSuite(VStackTest))
    test_suite.addTest(unittest.makeSuite(ImageTest))
    test_suite.addTest(unittest.makeSuite(TableTest))
    test_suite.addTest(unittest.makeSuite(TextTest))

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
