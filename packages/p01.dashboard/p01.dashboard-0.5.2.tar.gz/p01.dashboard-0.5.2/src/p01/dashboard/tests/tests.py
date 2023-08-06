###############################################################################
#
# Copyright (c) 2016 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Tests
$Id: tests.py 4549 2017-01-05 15:08:07Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import doctest
import unittest


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('checker.txt'),
        doctest.DocFileSuite('../README.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
