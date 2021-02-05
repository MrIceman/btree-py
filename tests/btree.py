import unittest

from tree import BTree, BNode


class BTreeTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_should_find_values_in_root(self):
        root_node = BNode()
        root_node.keys.append(1)
        root_node.keys.append(2)
        root_node.keys.append(10)
        root_node.keys.append(12)
        root_node.keys.append(15)
        root_node.keys.append(30)

        tree = BTree(root_node)
        result = tree.search(10)

        self.assertEqual(result, root_node)

    def test_should_find_value_in_single_child(self):
        root_node = BNode()
        child_node = BNode()

        child_node.add_key(30)
        child_node.add_key(20)
        child_node.add_key(10)

        root_node.add_child(child_node)

        b_tree = BTree(root_node)
        result = b_tree.search(10)

        print(root_node.keys)
        print(child_node.keys)

        self.assertEqual(child_node, result)

    def test_should_find_value_in_nested_child(self):
        root_node = BNode()
        node_a = BNode()
        node_b = BNode()

        node_a.add_key(50)
        node_a.add_key(60)
        node_a.add_key(70)
        node_b.add_key(10)
        node_b.add_key(20)
        node_b.add_key(30)

        node_a.add_child(node_b)
        root_node.add_child(node_a)
        b_tree = BTree(root_node)
        result = b_tree.search(10)

        print(root_node.keys)
        print(node_b.keys)

        self.assertEqual(node_b, result)
