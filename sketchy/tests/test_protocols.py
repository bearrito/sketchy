from sketchy.protocols import messages_pb2


def test_bloom_update():
    update = messages_pb2.BloomMerge()

    update.width = 1
    update.depth = 3
    update.ones_indices.append(1)
    update.ones_indices.append(2)
    update.ones_indices.append(93)
    stringy = update.SerializeToString().decode("utf-8")

    otherUpdate = messages_pb2.BloomMerge()
    s = otherUpdate.ParseFromString(stringy.encode("utf-8"))
    assert(True)


def test_bloom_update_2():
    update = messages_pb2.BloomMerge()
    update.width = 10000
    update.depth = 9
    update.ones_indices.append(1)
    update.ones_indices.append(839)
    update.ones_indices.append(5422)
    protobuf = update.SerializeToString()


    receiver = messages_pb2.BloomMerge()
    receiver.ParseFromString(protobuf)
    assert(receiver.width == update.width)