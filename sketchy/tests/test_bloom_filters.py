from sketchy.existence.bloom_filters import BloomFilter, CountingBloomFilter
from sketchy.protocols.messages_pb2 import BloomMerge


def test_insert():
    test_key = "test_object"
    bloom_filter = BloomFilter(10000, 5)
    bloom_filter.insert(test_key)
    assert (bloom_filter.exists(test_key))


def test_hash_insert_count():
    test_key = "test_object"
    bloom_filter = BloomFilter(10000, 5)
    bloom_filter.insert(test_key)
    assert (bloom_filter.filter.count() == 5)


def test_non_existence():
    test_key = "test_key"
    bloom_filter = BloomFilter(10000, 5)
    assert (not bloom_filter.exists(test_key))


def test_merge_of_filter_into_empty():

    test_key = "test_object"
    bloom_filter0 = BloomFilter(10000, 5)
    bloom_filter1 = BloomFilter(10000, 5)

    bloom_filter1.insert(test_key)
    update = bloom_filter1.merge_view()
    stringy = update.SerializeToString()
    update = BloomMerge()
    update.ParseFromString(stringy)

    bloom_filter0.merge(update)
    assert(bloom_filter0.exists(test_key))

def test_error_rate():

    bloom_filter = BloomFilter(10000, 5)
    bloom_filter.insert("1")

    assert( bloom_filter.error_rate() < .000000001)



def test_insert_on_counter():
    test_key = "test_key"
    counting_bloom = CountingBloomFilter(10000, 5)
    counting_bloom.insert(test_key)
    assert(counting_bloom.exists(test_key))

def test_non_existence_on_counter():
    test_key = "test_key"
    counting_bloom = CountingBloomFilter(10000, 5)
    assert(not counting_bloom.exists(test_key))


def test_delete_on_counter():
    test_key = "test_key"
    counting_bloom = CountingBloomFilter(10000, 5)
    counting_bloom.insert(test_key)
    counting_bloom.delete(test_key)
    assert(not counting_bloom.exists(test_key))

