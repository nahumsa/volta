# In order to run all tests, just use:
# python runalltests.py

import unittest
loader = unittest.TestLoader()
start_dir = 'tests'
suite = loader.discover(start_dir)
runner = unittest.TextTestRunner()
runner.run(suite)