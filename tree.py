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

    def split(self, key, node: BNode) -> BNode:
        if len(node.keys) < self.capacity - 1:
            raise Exception("Node is not full! No split needed")
        node.add_key(key)
        separator_index = self.capacity // 2
        separator = node.keys[separator_index]
        node.remove_key(separator)
        left_node = BNode(node.keys[0:separator_index])
        right_node = BNode(node.keys[separator_index::])
        parent = node.parent
        if parent is not None:
            parent.remove_child(node)
            new_node = parent
            new_node.keys.sort()
            new_node.upper_bound = new_node.keys[-1]
            left_node.is_leaf = True
            right_node.is_leaf = True
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
                return self.split(separator, parent)
        else:
            new_node = BNode([separator])
            new_node.upper_bound = new_node.keys[-1]
            left_node.is_leaf = len(left_node.children) == 0
            right_node.is_leaf = len(right_node.children) == 0
            left_node.upper_bound = left_node.keys[-1]
            right_node.upper_bound = right_node.keys[-1]

            new_node.add_child(left_node)
            new_node.add_child(right_node)
            new_node.children.sort(key=lambda x: x.keys[-1])
        if new_node is not None:
            new_node.is_leaf = False
        del node
        print(f'{new_node}')
        return new_node

    def insert(self, key: int, node: BNode):
        """
        we need to traverse down to the leaf and insert the key,
        if it is full then we call the split method. The method will then
        split itself up to the parent
        :param key:
        :param node:
        :return:
        """
        if node is None:
            return self.insert(key, self.root)
        # check if we are on leaf level
        if node.parent is None:
            node = self.root
        if node.is_leaf:
            # check if node is full
            if len(node.keys) >= self.capacity - 1:
                self.split(key, node)
                return
            elif len(node.keys) > self.capacity - 1:
                raise Exception(f"Why are there more than {self.capacity - 1} keys?")
            else:
                node.add_key(key)
                return

    def delete(self):
        pass

    def _split(self):
        pass

    def _merge(self):
        pass

    def get_root(self):
        return self.root
