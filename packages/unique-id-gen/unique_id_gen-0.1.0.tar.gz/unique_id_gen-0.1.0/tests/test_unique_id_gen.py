#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_unique_id_gen
----------------------------------

Tests for `unique_id_gen` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from unique_id_gen import unique_id_gen
from unique_id_gen import cli



class TestUnique_id_gen(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gen(self):
        gen_string = unique_id_gen.generate(0);
        print(gen_string)
        assert type(gen_string) == type(str())

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'unique_id_gen.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output