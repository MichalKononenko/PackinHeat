"""
Contains unit tests for :mod:`python_src.message_handler`
"""
import unittest
from python_src.message_handling import SerialMessage

__author__ = 'Michal Kononenko'


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.message = SerialMessage(1, 1)


