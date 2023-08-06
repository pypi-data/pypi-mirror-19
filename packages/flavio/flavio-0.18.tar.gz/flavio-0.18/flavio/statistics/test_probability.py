import unittest
import numpy as np
import numpy.testing as npt
import flavio
import scipy.stats
from math import pi, sqrt, exp, log
from flavio.statistics.probability import *
import itertools

class TestProbability(unittest.TestCase):
    def test_multiv_normal(self):
        # test that the rescaling of the MultivariateNormalDistribution
        # does not affect the log PDF!
        c = np.array([1e-3, 2])
        cov = np.array([[(0.2e-3)**2, 0.2e-3*0.5*0.3],[0.2e-3*0.5*0.3, 0.5**2]])
        pdf = MultivariateNormalDistribution(c, cov)
        x=np.array([1.5e-3, 0.8])
        num_lpdf = pdf.logpdf(x)
        ana_lpdf = log(1/sqrt(4*pi**2*np.linalg.det(cov))*exp(-np.dot(np.dot(x-c,np.linalg.inv(cov)),x-c)/2))
        self.assertAlmostEqual(num_lpdf, ana_lpdf, delta=1e-6)
        self.assertEqual(len(pdf.get_random(10)), 10)

    def test_halfnormal(self):
        pdf_p_1 = HalfNormalDistribution(1.7, 0.3)
        pdf_n_1 = HalfNormalDistribution(1.7, -0.3)
        pdf_p_2 = AsymmetricNormalDistribution(1.7, 0.3, 0.0001)
        pdf_n_2 = AsymmetricNormalDistribution(1.7, 0.0001, 0.3)
        self.assertAlmostEqual(pdf_p_1.logpdf(1.99), pdf_p_2.logpdf(1.99), delta=0.001)
        self.assertEqual(pdf_p_1.logpdf(1.55), -np.inf)
        self.assertAlmostEqual(pdf_n_1.logpdf(1.55), pdf_n_2.logpdf(1.55), delta=0.001)
        self.assertEqual(pdf_n_1.logpdf(1.99), -np.inf)
        self.assertEqual(len(pdf_p_1.get_random(10)), 10)
        self.assertEqual(len(pdf_p_2.get_random(10)), 10)

    def test_limit(self):
        p1 = GaussianUpperLimit(2*1.78, 0.9544997)
        p2 = HalfNormalDistribution(0, 1.78)
        self.assertAlmostEqual(p1.logpdf(0.237), p2.logpdf(0.237), delta=0.0001)
        self.assertEqual(p2.logpdf(-1), -np.inf)
        self.assertAlmostEqual(p1.cdf(2*1.78), 0.9544997, delta=0.0001)

    def test_gamma(self):
        # check for loc above and below a-1
        for  loc in (-5, -15):
            p = GammaDistributionPositive(a=11, loc=loc, scale=1)
            self.assertEqual(p.central_value, max(loc + 10, 0))
            r = p.get_random(10)
            self.assertEqual(len(r), 10)
            self.assertTrue(np.min(r) >= 0)
            self.assertEqual(p.logpdf(-0.1), -np.inf)
            self.assertEqual(p.cdf(0), 0)
            self.assertAlmostEqual(p.cdf(p.support[1]), 1-2e-9, delta=0.1e-9)
            self.assertEqual(p.ppf(0), 0)
            self.assertAlmostEqual(p.ppf(1-2e-9), p.support[1], delta=0.0001)
            self.assertEqual(p.cdf(-1), 0)
        p = GammaDistributionPositive(a=11, loc=-9, scale=1)
        self.assertEqual(p.central_value, 1)
        self.assertEqual(p.error_left, 1)
        # nearly normal distribution
        p = GammaDistributionPositive(a=10001, loc=0, scale=1)
        self.assertAlmostEqual(p.error_left, sqrt(10000), delta=1)
        self.assertAlmostEqual(p.error_right, sqrt(10000), delta=1)

    def test_gamma_limit(self):
        p = GammaUpperLimit(counts_total=30, counts_background=10,
                            limit=2e-5, confidence_level=0.68)
        self.assertAlmostEqual(p.cdf(2e-5), 0.68, delta=0.0001)
        # background excess
        p = GammaUpperLimit(counts_total=30, counts_background=50,
                            limit=2e5, confidence_level=0.68)
        self.assertAlmostEqual(p.cdf(2e5), 0.68, delta=0.0001)
        p = GammaUpperLimit(counts_total=10000, counts_background=10000,
                            limit=3., confidence_level=0.95)
        p_norm = GaussianUpperLimit(limit=3., confidence_level=0.95)
        # check that large-statistics Gamma and Gauss give nearly same PDF
        for x in [0, 1, 2, 3, 4]:
            self.assertAlmostEqual(p.logpdf(x), p_norm.logpdf(x), delta=0.1)


    def test_numerical(self):
        x = np.arange(-5,7,0.01)
        y = scipy.stats.norm.pdf(x, loc=1)
        y_crazy = 14.7 * y # multiply PDF by crazy number
        p_num = NumericalDistribution(x, y_crazy)
        p_norm = NormalDistribution(1, 1)
        self.assertAlmostEqual(p_num.logpdf(0.237), p_norm.logpdf(0.237), delta=0.02)
        self.assertAlmostEqual(p_num.logpdf(-2.61), p_norm.logpdf(-2.61), delta=0.02)
        self.assertAlmostEqual(p_num.ppf_interp(0.1), scipy.stats.norm.ppf(0.1, loc=1), delta=0.02)
        self.assertAlmostEqual(p_num.ppf_interp(0.95), scipy.stats.norm.ppf(0.95, loc=1), delta=0.02)
        self.assertEqual(len(p_num.get_random(10)), 10)

    def test_multiv_numerical(self):
        x0 = np.arange(-5,5,0.01)
        x1 = np.arange(-4,6,0.02)
        cov = [[0.2**2, 0.5*0.2*0.4], [0.5*0.2*0.4, 0.4**2]]
        y = scipy.stats.multivariate_normal.pdf(np.array(list(itertools.product(x0, x1))), mean=[0, 1], cov=cov)
        y = y.reshape(len(x0), len(x1))
        y_crazy = 14.7 * y # multiply PDF by crazy number
        p_num = MultivariateNumericalDistribution((x0, x1), y_crazy)
        p_norm = MultivariateNormalDistribution([0, 1], cov)
        self.assertAlmostEqual(p_num.logpdf([0.237, 0.346]), p_norm.logpdf([0.237, 0.346]), delta=0.02)
        # test exceptions
        with self.assertRaises(NotImplementedError):
            p_num.error_left
        with self.assertRaises(NotImplementedError):
            p_num.error_right
        with self.assertRaises(NotImplementedError):
            p_num.logpdf([0.237, 0.346], exclude=(0))
        self.assertEqual(len(p_num.get_random(10)), 10)

    def test_numerical_from_analytic(self):
        p_norm = NormalDistribution(1.64, 0.32)
        p_norm_num = NumericalDistribution.from_pd(p_norm)
        self.assertEqual(p_norm.central_value, p_norm_num.central_value)
        self.assertEqual(p_norm.support, p_norm_num.support)
        npt.assert_array_almost_equal(p_norm.logpdf([0.7, 1.9]), p_norm_num.logpdf([0.7, 1.9]), decimal=3)
        p_asym = AsymmetricNormalDistribution(1.64, 0.32, 0.67)
        p_asym_num = NumericalDistribution.from_pd(p_asym)
        npt.assert_array_almost_equal(p_asym.logpdf([0.7, 1.9]), p_asym_num.logpdf([0.7, 1.9]), decimal=3)
        p_unif = UniformDistribution(1.64, 0.32)
        p_unif_num = NumericalDistribution.from_pd(p_unif)
        npt.assert_array_almost_equal(p_unif.logpdf([0.7, 1.9]), p_unif_num.logpdf([0.7, 1.9]), decimal=3)
        p_half = HalfNormalDistribution(1.64, -0.32)
        p_half_num = NumericalDistribution.from_pd(p_half)
        npt.assert_array_almost_equal(p_half.logpdf([0.7, 1.3]), p_half_num.logpdf([0.7, 1.3]), decimal=3)

    def test_convolve_normal(self):
        p_1 = NormalDistribution(12.4, 0.346)
        p_2 = NormalDistribution(12.4, 2.463)
        p_x = NormalDistribution(12.3, 2.463)
        from flavio.statistics.probability import convolve_distributions
        # error if not the same central value:
        with self.assertRaises(AssertionError):
            convolve_distributions([p_1, p_x])
        p_comb = convolve_distributions([p_1, p_2])
        self.assertIsInstance(p_comb, NormalDistribution)
        self.assertEqual(p_comb.central_value, 12.4)
        self.assertEqual(p_comb.standard_deviation, sqrt(0.346**2+2.463**2))

    def test_convolve_numerical(self):
        from flavio.statistics.probability import _convolve_numerical
        p_1 = NumericalDistribution.from_pd(NormalDistribution(12.4, 0.346))
        p_2 = NumericalDistribution.from_pd(NormalDistribution(12.4, 2.463))
        p_3 = NumericalDistribution.from_pd(NormalDistribution(12.4, 1.397))
        conv_p_12 = _convolve_numerical([p_1, p_2])
        comb_p_12 = NormalDistribution(12.4, sqrt(0.346**2 + 2.463**2))
        conv_p_123 = _convolve_numerical([p_1, p_2, p_3])
        comb_p_123 = NormalDistribution(12.4, sqrt(0.346**2 + 2.463**2 + 1.397**2))
        x = np.linspace(2, 20, 10)
        npt.assert_array_almost_equal(conv_p_12.logpdf(x), comb_p_12.logpdf(x), decimal=1)
        npt.assert_array_almost_equal(conv_p_123.logpdf(x), comb_p_123.logpdf(x), decimal=1)

    def test_1d_errors(self):
        p = NormalDistribution(3, 0.2)
        q = NumericalDistribution.from_pd(p)
        self.assertEqual(p.error_left, 0.2)
        self.assertEqual(p.error_right, 0.2)
        self.assertAlmostEqual(q.error_left, 0.2, places=2)
        self.assertAlmostEqual(q.error_right, 0.2, places=2)

        p = AsymmetricNormalDistribution(3, 0.2, 0.5)
        q = NumericalDistribution.from_pd(p)
        self.assertEqual(p.error_left, 0.5)
        self.assertEqual(p.error_right, 0.2)
        self.assertAlmostEqual(q.error_left, 0.5, places=2)
        self.assertAlmostEqual(q.error_right, 0.2, places=2)

        p = DeltaDistribution(3)
        self.assertEqual(p.error_left, 0)
        self.assertEqual(p.error_right, 0)

        p = UniformDistribution(3, 0.4)
        q = NumericalDistribution.from_pd(p)
        self.assertAlmostEqual(p.error_left, 0.4*0.68, places=2)
        self.assertAlmostEqual(p.error_right, 0.4*0.68, places=2)
        self.assertAlmostEqual(q.error_left, 0.4*0.68, places=2)
        self.assertAlmostEqual(q.error_right, 0.4*0.68, places=2)

        p = HalfNormalDistribution(3, +0.5)
        q = NumericalDistribution.from_pd(p)
        self.assertEqual(p.error_left, 0)
        self.assertEqual(p.error_right, 0.5)
        self.assertAlmostEqual(q.error_left, 0, places=2)
        self.assertAlmostEqual(q.error_right, 0.5, places=2)

        p = HalfNormalDistribution(3, -0.5)
        q = NumericalDistribution.from_pd(p)
        self.assertEqual(p.error_left, 0.5)
        self.assertEqual(p.error_right, 0)
        self.assertAlmostEqual(q.error_left, 0.5, places=2)
        self.assertAlmostEqual(q.error_right, 0, places=2)

    def test_multivariate_exclude(self):
        c2 = np.array([1e-3, 2])
        c3 = np.array([1e-3, 2, 0.4])
        cov22 = np.array([[(0.2e-3)**2, 0.2e-3*0.5*0.3],[0.2e-3*0.5*0.3, 0.5**2]])
        cov33 = np.array([[(0.2e-3)**2, 0.2e-3*0.5*0.3 , 0],[0.2e-3*0.5*0.3, 0.5**2, 0.01], [0, 0.01, 0.1**2]])
        pdf1 = NormalDistribution(2, 0.5)
        pdf2 = MultivariateNormalDistribution(c2, cov22)
        pdf3 = MultivariateNormalDistribution(c3, cov33)
        self.assertEqual(pdf2.logpdf([1.1e-3, 2.4]), pdf3.logpdf([1.1e-3, 2.4], exclude=2))
        self.assertEqual(pdf1.logpdf(2.4), pdf3.logpdf([2.4], exclude=(0,2)))
        with self.assertRaises(ValueError):
            # dimensions don't match
            self.assertEqual(pdf2.logpdf([1.1e-3, 2.4]), pdf3.logpdf([1.1e-3, 2.4, 0.2], exclude=2))
