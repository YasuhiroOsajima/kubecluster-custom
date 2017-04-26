#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from check_inventory import CheckInventory

INVENTORY_FILE = './hosts'
VARS_FILE = './group_vars/cluster.yml'

class TestCheckInventory(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generate_hostlist(self):
        targetclass = CheckInventory()
        arglist = [INVENTORY_FILE, []]
        resultlist = targetclass._open_file(arglist)('r')

        val = [resultlist[0], []]

        test_resultlist = targetclass._generate_hostlist(resultlist)
        print test_resultlist[1]

        self.assertEqual(test_resultlist, val)

if __name__ == '__main__':
    unittest.main()
