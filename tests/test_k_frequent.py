from counting.k_frequent import  KFrequent

def test_k_frequent_observation():
    k_frequent = KFrequent(3)
    k_frequent.observe("1")
    k_frequent.observe("1")
    k_frequent.observe("1")
    k_frequent.observe("1")
    k_frequent.observe("2")
    k_frequent.observe("2")
    k_frequent.observe("3")
    k_frequent.observe("4")

    result = k_frequent.most_frequent_with_counts()

    assert(result["1"] == 4)
    assert(result["2"] == 2)
    assert(result["4"] == 2)
    assert("3" not in result)
