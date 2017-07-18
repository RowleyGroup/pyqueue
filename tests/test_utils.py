"""
pyqueue tests.
"""

import unittest
from datetime import timedelta
from pyqueue.utils import strfdelta


class TestUtils(unittest.TestCase):
    """
    Test pyqueue's utils.
    """

    def setUp(self):
        pass

    def test_strfdelta(self):
        """
        Format the timedelta
        """
        answer = strfdelta(timedelta(minutes=10, seconds=50), '%M:%S')
        self.assertEqual(
            answer,
            '10:50'
        )

        answer = strfdelta(timedelta(days=1, hours=10), '%H:%M:%S')
        self.assertEqual(
            answer,
            '34:00:00'
        )
