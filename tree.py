import math


class BNode:
    """
    Node
    [0, 1, 2 ,3 ,4 ,5]


    """

    def __init__(self, data: list):
        self.parent = None
        self.keys: list = data
        self.is_leaf: bool = False
        self.upper_bound: int = -1  # the biggest key
        self.children = []
        if len(self.keys) > 0:
            self.keys.sort()
            self.upper_bound = self.keys[-1]

    def add_child(self, *value):
        for n in value:
            n.parent = self
            self.children.append(n)

    def add_key(self, key):
        # sort
        self.keys.append(key)
        self.keys.sort()

    def remove_key(self, key):
        self.keys.remove(key)

    def remove_child(self, node):
        if node not in self.children:
            raise Exception("No node as child.")
        self.children.remove(node)

    def __repr__(self):
        child_keys = ','.join([str(x.keys) for x in self.children])
        parent_keys = self.parent.keys if self.parent is not None else "___"
        return f'Node[high_key: {self.upper_bound}' \
               f' keys: {self.keys}, ' \
               f' is_leaf: {self.is_leaf}' \
               f' children: [{child_keys}]' \
               f' parent: {parent_keys}]'


class BTree:

    def __init__(self, k=3):
        if k % 2 != 1:
            raise Exception("k must be an uneven number!")
        self.capacity = k
        self.root = BNode(list())
        self.root.is_leaf = True
        self.height = 0

    def _split(self, key, node: BNode) -> BNode:
        """
                  1. Sort Keys
                  2. Take the middle key from current node N
                  3. Create new node with separator key, M
                  4. Create new Left Node (all keys left from key)
                  5. Create new Right Node (all keys right from key)
                  6. Append left node to M, append Right Node to M
                  7. Check all old child nodes from N and append them to either left node
                  Or right node


                  For step 7 we need to find the child nodes of N and identify whether they
                  Belong now to the left or right node.

                  Steps:

                  1. Check highest key of left node
                  2. Iterate through child nodes from N and append to left node if
                  n.key[-1] < leftNode.key[-1] else append to right node
                  """

        if len(node.keys) < self.capacity - 1:
            raise Exception("Node is not full! No split needed")
        node.add_key(key)
        separator_index = self.capacity // 2
        separator = node.keys[separator_index]
        node.remove_key(separator)
        left_node = BNode(node.keys[0:separator_index])
        right_node = BNode(node.keys[separator_index::])
        left_node.is_leaf = len(node.children) == 0
        right_node.is_leaf = len(node.children) == 0
        parent = node.parent

        # check if node has children, then we need to append them
        for i in node.children:
            if i.keys[-1] < separator:
                left_node.add_child(i)
            else:
                right_node.add_child(i)

            left_node.children.sort(key=lambda x: x.keys[-1])
            right_node.children.sort(key=lambda x: x.keys[-1])

        if parent is not None:
            parent.remove_child(node)
            new_node = parent
            new_node.keys.sort()
            new_node.upper_bound = new_node.keys[-1]

            left_node.upper_bound = left_node.keys[-1]
            right_node.upper_bound = right_node.keys[-1]

            new_node.add_child(left_node)
            new_node.add_child(right_node)
            new_node.children.sort(key=lambda x: x.keys[-1])
            if len(parent.keys) < self.capacity - 1:
                parent.add_key(separator)
                parent.keys.sort()
                return new_node
            else:
                # need to split parent
                parent.keys.sort()
                return self._split(separator, parent)
        else:
            new_node = BNode([separator])
            new_node.upper_bound = new_node.keys[-1]
            left_node.upper_bound = left_node.keys[-1]
            right_node.upper_bound = right_node.keys[-1]

            new_node.add_child(left_node)
            new_node.add_child(right_node)
            new_node.children.sort(key=lambda x: x.keys[-1])
        if new_node is not None:
            new_node.is_leaf = False
        del node
        if new_node.parent is None:
            self.root = new_node
        return new_node

    def insert(self, key: int, node: BNode):
        if node is None:
            return self.insert(key, self.root)

        if node.is_leaf:
            # check if node is full
            if len(node.keys) >= self.capacity - 1:
                node = self._split(key, node)
                self.height += 1
            elif len(node.keys) > self.capacity - 1:
                raise Exception(f"Why are there more than {self.capacity - 1} keys?")
            else:
                node.add_key(key)
        # node is not leaf, we need to traverse down the right child
        else:
            node_idx = 0
            if len(node.children) == 0:
                raise Exception("No children found and node is not leaf. Something is wrong")
            for i in node.children:
                if key >= i.upper_bound:
                    node_idx += 1
            self.insert(key, node.children[node_idx - 1])

    def search(self, key, node=None) -> BNode:
        if node is None:
            return self.search(key, self.root)
        else:
            if node.is_leaf or key in node.keys:
                return node
            else:
                continuation = 0
                for idx, child in enumerate(node.children):
                    # lets brute force the child where it's found and then
                    # we look within its neighbor if it exists
                    if key <= child.upper_bound:
                        # lets see if key is also smaller than parents key idx
                        if key <= node.keys[idx]:
                            continuation = idx-1

                return self.search(key, node.children[continuation])

    def delete(self):
        pass

    def _merge(self):
        pass

    def get_root(self):
        return self.root

    def get_height(self):
        return self.height
