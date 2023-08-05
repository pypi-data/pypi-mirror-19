import unittest
from unittest import TestCase

from myKerasCallbacks import StatsCallback

class TestStatsCallback(TestCase):
    def test_init(self):   
        assert StatsCallback('Model Name')

if __name__ == '__main__':
    unittest.main()
