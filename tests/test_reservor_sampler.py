from statistics.resevoir_sampler import WeightedReservoirSampler
from itertools import  chain,repeat
from random import shuffle

def test_weighted_sampler():
    weightedSampler = WeightedReservoirSampler(3, {1: .001, 4: 10, 5: 10})

    stream = chain(*repeat([1, 4, 5], 10000))
    shuffle(stream)
    
    for i in stream:
        weightedSampler.observe(i)
