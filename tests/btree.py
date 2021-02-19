import unittest

from tree import BTree, BNode


class BTreeTest(unittest.TestCase):
    keys: {str: int} = {
        'k1': 8,
        'k2': 1,
        'k3': 5,
        'k4': 3,
        'k5': 2,
        'k6': 0,
    }
    amount_of_leafs = len(keys.keys())

    def setUp(self) -> None:
        pass

    def test_split_happens_as_expected(self):
        # k = 3 and input values 1..3
        k = 3
        expected_output = BNode([1])
        a = BNode([0])
        b = BNode([2])
        a.is_leaf = True
        b.is_leaf = True
        expected_output.add_child(a)
        expected_output.add_child(b)

        input_node = BNode([0, 1])
        tree = BTree(k)
        result = tree._split(2, input_node)

        self.assertTrue(result.keys, [1])
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].keys, [0])
        self.assertEqual(result.children[1].keys, [2])

    def test_split_happens_as_expected_part_2(self):
        # k = 5 and input values 1..5
        k = 5
        expected_output = BNode([3])
        a = BNode([1, 2])
        b = BNode([4, 5])
        a.is_leaf = True
        b.is_leaf = True
        expected_output.add_child(a)
        expected_output.add_child(b)

        tree = BTree(k)
        input_node = BNode([1, 2, 3, 4])
        result = tree._split(5, input_node)
        print(f'5 Values: {result}')
        self.assertTrue(result.keys, [3])
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].keys, [1, 2])
        self.assertEqual(result.children[1].keys, [4, 5])
        tree.insert(6, result)
        print(f'{tree.get_root()}')

    def test_split_balances_parents_parent(self):
        # k = 5 and input values 1..5
        k = 5
        input_node = BNode([3, 6, 9, 12])
        a = BNode([1, 2])
        b = BNode([4, 5])
        c = BNode([7, 8])
        d = BNode([10, 11])
        e = BNode([13, 14, 15, 16])
        a.is_leaf = True
        b.is_leaf = True
        b.is_leaf = True
        c.is_leaf = True
        d.is_leaf = True
        e.is_leaf = True

        input_node.add_child(a, b, c, d, e)

        tree = BTree(k)
        tree._split(17, e)
        result = tree.get_root()

        self.assertTrue(len(result.keys) == 1)
        self.assertTrue(result.keys == [9])
        first_child_layer = result.children
        self.assertTrue(len(first_child_layer) == 2)
        self.assertTrue(first_child_layer[0].keys == [3, 6])
        self.assertTrue(first_child_layer[1].keys == [12, 15])
        for i in first_child_layer:
            self.assertFalse(i.is_leaf)
        # first 3 leafs
        self.assertEquals([1, 2], first_child_layer[0].children[0].keys)
        self.assertEquals([4, 5], first_child_layer[0].children[1].keys)
        self.assertEquals([7, 8], first_child_layer[0].children[2].keys)
        self.assertEquals(True, first_child_layer[0].children[0].is_leaf)
        self.assertEquals(True, first_child_layer[0].children[1].is_leaf)
        self.assertEquals(True, first_child_layer[0].children[2].is_leaf)

        # last 3 leafs
        self.assertEquals([10, 11], first_child_layer[1].children[0].keys)
        self.assertEquals([13, 14], first_child_layer[1].children[1].keys)
        self.assertEquals([16, 17], first_child_layer[1].children[2].keys)
        self.assertEquals(True, first_child_layer[1].children[0].is_leaf)
        self.assertEquals(True, first_child_layer[1].children[1].is_leaf)
        self.assertEquals(True, first_child_layer[1].children[2].is_leaf)

    def test_insertion_happens_as_expected(self):
        # k = 5 and input values 1..10
        k = 5

        tree = BTree(k)
        for i in range(1, 18):
            tree.insert(i, None)
            print(f'Inserted {i} into tree. root: {tree.get_root()}')
            print('---')

        result = tree.get_root()

        self.assertTrue(result.keys == [9])
        first_child_layer = result.children
        self.assertTrue(len(first_child_layer) == 2)
        self.assertTrue(first_child_layer[0].keys == [3, 6])
        self.assertTrue(first_child_layer[1].keys == [12, 15])
        for i in first_child_layer:
            self.assertFalse(i.is_leaf)
        # first 3 leafs
        self.assertEquals([1, 2], first_child_layer[0].children[0].keys)
        self.assertEquals([4, 5], first_child_layer[0].children[1].keys)
        self.assertEquals([7, 8], first_child_layer[0].children[2].keys)
        self.assertEquals(True, first_child_layer[0].children[0].is_leaf)
        self.assertEquals(True, first_child_layer[0].children[1].is_leaf)
        self.assertEquals(True, first_child_layer[0].children[2].is_leaf)

        # last 3 leafs
        self.assertEquals([10, 11], first_child_layer[1].children[0].keys)
        self.assertEquals([13, 14], first_child_layer[1].children[1].keys)
        self.assertEquals([16, 17], first_child_layer[1].children[2].keys)
        self.assertEquals(True, first_child_layer[1].children[0].is_leaf)
        self.assertEquals(True, first_child_layer[1].children[1].is_leaf)
        self.assertEquals(True, first_child_layer[1].children[2].is_leaf)

    def test_finds_proper_node_that_holds_our_key(self):
        # k = 5 and input values 1..5
        k = 3

        tree = BTree(k)
        for i in range(1, 32):
            tree.insert(i, None)

        root = tree.get_root()

        self.assertTrue(8 in tree._get_next_biggest_smallest_child(3, root).keys)
        self.assertTrue(4 in tree._get_next_biggest_smallest_child(3, root.children[0]).keys)
        self.assertTrue(2 in tree._get_next_biggest_smallest_child(3, root.children[0].children[0]).keys)
        self.assertTrue(3 in tree._get_next_biggest_smallest_child(3, root.children[0].children[0].children[0]).keys)
        # let's look for 3

    def test_buggy_split(self):

        # this didn't work before
        tree = BTree(k=5)
        root = BNode([3, 6])
        root.add_child(BNode([1, 2]), BNode([4, 5]), BNode([7, 8, 9, 10]))
        tree.root = root
        print(f'result: {tree._split(11, root.children[2])}')

        new_root = tree.get_root()
        self.assertTrue([3, 6, 9] == new_root.keys)
        self.assertTrue(len(new_root.children) == 4)
        self.assertTrue([1, 2] == new_root.children[0].keys)
        self.assertTrue([4, 5] == new_root.children[1].keys)
        self.assertTrue([7, 8] == new_root.children[2].keys)
        self.assertTrue([10, 11] == new_root.children[3].keys)

    def test_search(self):
        # k = 5 and input values 1..10
        k = 195
        n = 1500000
        tree = BTree(k)
        for i in range(0, n):
            tree.insert(i, None)
            if i % 100000 == 0:
                print(f'{i} inserted')

        print(f"root after execution. Height: {tree.height}")

        for i in range(0, n):
            result = tree.search(i)
            self.assertTrue(i in result.keys)

    def test_pick_second_child_as_smallest(self):
        node = BNode(data=[125, 250, 375, 500])
        a = BNode([25, 50, 75, 100])
        b = BNode([150, 175, 200, 225])
        c = BNode([275, 300, 320, 350])
        d = BNode([400, 425, 450, 475])
        e = BNode([525, 550, 575, 600])
        node.add_child(a)
        node.add_child(b)
        node.add_child(c)
        node.add_child(d)
        node.add_child(e)
        k = 5
        tree = BTree(k)

        result = tree._get_next_biggest_smallest_child(128, node)

        self.assertEqual(b, result)

    def test_amount_of_leaf_nodes(self):
        # t = 4 so total amount: 6 + 1 = 7
        pass
