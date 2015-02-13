from sketchy.counting.conditional_heavy_hitter import  ConditionalParentChild

def test_insert():
    test_key = "test_object"
    parent = ConditionalParentChild()
    parent.observe("1")

    parent.observe("2")
    parent.observe("2")
    parent.observe("3")
    parent.observe("3")
    parent.observe("3")
    parent.observe("2")
    parent.observe("3")
    lfc = parent.least_frequent_child()

