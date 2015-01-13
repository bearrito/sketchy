from protocols import  messages_pb2

def test_bloom_update():
    update = messages_pb2.BloomUpdate()

    update.size = 1
    update.num_hashes = 3
    update.ones_indices.append(1)
    update.ones_indices.append(2)
    update.ones_indices.append(93)
    stringy = update.SerializeToString()

    otherUpdate = messages_pb2.BloomUpdate()
    otherUpdate.ParseFromString(stringy)
    print("boosh")