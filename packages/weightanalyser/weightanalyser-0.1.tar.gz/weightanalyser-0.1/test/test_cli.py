#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest

import weightanalyser.cli as cli


class Test_check_date_format(unittest.TestCase):
    def test_check_date_format_for_letters(self):
        assert cli.check_date_format("a") == "Contains letter!"

    def test_check_date_format_right(self):
        assert cli.check_date_format("01-12-2016")

    def test_check_date_format_wrong_format(self):
        self.assertFalse(cli.check_date_format("01--2016"))
        self.assertFalse(cli.check_date_format("01-2016"))
        self.assertFalse(cli.check_date_format("-01-2016"))
        self.assertFalse(cli.check_date_format("01-1-2016"))
        self.assertFalse(cli.check_date_format("1-01-2016"))
        self.assertFalse(cli.check_date_format("01-01-16"))
