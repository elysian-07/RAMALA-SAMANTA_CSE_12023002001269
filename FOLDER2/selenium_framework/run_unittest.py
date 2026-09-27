"""Run the unittest-style suite without pytest: python run_unittest.py"""
import sys
import unittest

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests", pattern="test_*_unittest.py",
                                                top_level_dir=".")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
