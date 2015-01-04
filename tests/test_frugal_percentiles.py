from itertools import chain, repeat
from statistics.frugal_percentiles import FrugalMedian


def test_constant_stream():

    median_estimator = FrugalMedian()
    for observable in repeat(44, 1000):
        median_estimator.observe(observable)

    estimate = median_estimator.estimate()
    assert(estimate == 44)


def test_stream_when_clear_majority():

    sequence = chain(repeat(44, 1000),repeat(14, 100),repeat(44, 1000))
    median_estimator = FrugalMedian()
    for observable in sequence:
        median_estimator.observe(observable)

    estimate = median_estimator.estimate()
    assert(estimate == 44)


def test_stream_when_clustered():

    sequence = chain(repeat(44, 1000), repeat(45, 998), repeat(46, 998),repeat(44, 2))
    median_estimator = FrugalMedian()
    for observable in sequence:
        median_estimator.observe(observable)

    estimate = median_estimator.estimate()
    assert(estimate == 44)