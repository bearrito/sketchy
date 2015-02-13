from sketchy.common.sorted_linked_list import CountingNode,CountingLinkedList


def test_insert():

    linked_list = CountingLinkedList()
    linked_list.observe("first")
    linked_list.observe("second")
    linked_list.observe("third")
    x = str(linked_list)
    linked_list.observe("first")
    y = str(linked_list)
    linked_list.observe("second")
    linked_list.observe("second")
    linked_list.observe("second")
    z = str(linked_list)

    a = 1