from numbers import Real
from random import random
from abc import ABCMeta,abstractmethod


class FrugalStatistics:
    __metaclass__ = ABCMeta

    @abstractmethod
    def observe(self, observable: Real):
        pass

    def estimate(self) -> Real:
        pass



class FrugalMedian(FrugalStatistics):
    def __init__(self, prior_median=0):
        self.median_estimate = prior_median

    def observe(self, observable : Real):
        if observable > self.median_estimate:
            self.median_estimate += 1
        elif observable < self.median_estimate:
            self.median_estimate -= 1

    def estimate(self):
        return self.median_estimate

class FrugalQuantile(FrugalStatistics):
    def __init__(self, quantile: Real, quantile_prior = 0):

        assert()
        self.quantile_estimate = quantile_prior
        self.quantile = quantile

    def observe(self, observable: Real):
        r = random()

        if observable > self.quantile_estimate and r > 1 - self.quantile:
            self.quantile_estimate += 1
        elif observable < self.quantile_estimate and r > self.quantile:
            self.quantile_estimate -= 1

    def estimate(self):
        return self.quantile_estimate