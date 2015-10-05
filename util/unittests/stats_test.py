# Copyright (c) 2015 Intracom util.stats.A. Telecom Solutionutil.stats.
#All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

"""Unittest Module for util/statutil.stats.py."""

import unittest
import util.stats
import math

class StatsAllFunctionsTest(unittest.TestCase):
    """Unittest that tests the different functionalities of stats Module
    in util/statutil.stats.py.
    """
    @classmethod
    def setUpClass(cls):
        """
        Creates the testing environment parameters
        """
        cls.l = [1, 4, 8, 10, 20, 30, 40, 50, 60]
        cls.mean = (sum(cls.l) * 1.0) / len(cls.l)
        cls.variance = \
        sum([y**2 for y in [x - cls.mean for x in cls.l]]) / len(cls.l)
        cls.stddev = math.sqrt(cls.variance)
        cls.coefvariance = cls.stddev / cls.mean

    def test01_mean(self):
        """
        Checks the mean() function of util/statutil.stats.py
        module.
        """
        self.assertEqual(self.mean, util.stats.mean(self.l),
                         'Testing mean')

    def test02_variance(self):
        """
        Checks the variance() function of util/statutil.stats.py
        module.
        """
        self.assertEqual(self.variance, util.stats.variance(self.l),
                         'Testing variance')

    def test03_stddev(self):
        """
        Checks the stddev() function of util/statutil.stats.py
        module.
        """
        self.assertEqual(self.stddev, util.stats.stddev(self.l),
                         'Testing stddev')

    def test04_coefvariance(self):
        """
        Checks the cv() function of util/statutil.stats.py module.
        """
        self.assertEqual(self.coefvariance, util.stats.coefvariance(self.l),
                         'Testing coefvariance method')

    @classmethod
    def tearDownClass(cls):
        """
        Cleans the testing environment parameters
        """
        del cls.l
        del cls.mean
        del cls.variance
        del cls.stddev
        del cls.coefvariance

if __name__ == '__main__':
    SUITE_STATSALLFUNCTIONSTESTS = \
    unittest.TestLoader().loadTestsFromTestCase(StatsAllFunctionsTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE_STATSALLFUNCTIONSTESTS)
