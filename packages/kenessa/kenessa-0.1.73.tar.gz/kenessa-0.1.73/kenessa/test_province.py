import unittest
from province import Province


class TestProvince(unittest.TestCase):

    def test_all_province(self):
        """test all province"""
        self.assertTrue(Province('all').province())

    def test_one_province(self):
        """test one province"""
        self.assertTrue(Province(1).province())

    def test_one_province_is_none(self):
        """test if is none"""
        self.assertIsNone(Province(12).province())


if __name__ == '__main__':
    unittest.main()