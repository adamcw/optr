#!/usr/bin/env python

import unittest
from optr import Options

class OptrTestCase(unittest.TestCase):
    
    def setUp(self):
        self.default = dict(
            read = False,
            write = False,
            create = False,
            delete = False,
        )

        self.groups = dict(
            # A basic user can read files
            basic = dict(
                read = True,
            ),
            # An editor can do everything basic can do, but also write.
            editor = dict(
                mixin = ['basic'],
                write = True
            ),
            # An admin can do everything an editor can do, but also create/delete
            admin = dict(
                mixin = ['editor'],
                create = True,
                delete = True,
            ),
        )

        self.o = Options(groups=self.groups, default=self.default)

    def test_defaults(self):
        q = {'write': False, 'read': False, 'create': False, 'delete': False}
        self.assertEqual(self.o, q)

if __name__ == '__main__':
    unittest.main()

