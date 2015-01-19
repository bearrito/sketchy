from random import shuffle
from sketchy.statistics.moment_estimator import AMSEstimator
from itertools import repeat, chain
import pytest





@pytest.mark.parametrize("stream,trials,lower_bound,upper_bound",
    [
        (list(chain(*repeat([1, 2],100))), 500, 19000, 21000),
        (list(chain(*repeat([1, 2, 3, 4], 100))), 500, 37000, 43000),
        (list(chain(*chain(repeat([1, 2,], 100),repeat([3, 4], 1000)))), 500, 1700000, 2200000)
    ])
def test_sanity(stream, trials, lower_bound, upper_bound):
    estimations = []
    for trial in range(trials):

        estimator = AMSEstimator()
        shuffle(stream)
        for i in stream:
            estimator.observe(i)


        estimations.append(estimator.estimate())


    estimation = sum(estimations)/trials

    print(estimation)
    assert(lower_bound < estimation < upper_bound)
