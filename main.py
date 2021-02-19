from tree import BTree

# k defines the key capacity for each node. Note that the actual
# key capacity is k-1
k = 10195
# the amount of nodes you wanna enter
n = 450005
tree = BTree(k)
for i in range(0, n):
    tree.insert(i, None)
    if i % 100000 == 0:
        print(f'{i} inserted')

print(f"root after execution. Height: {tree.height}")

for i in range(0, n):
    result = tree.search(i)
    if i not in result.keys:
        # this code will never run :-) At least it shouldn't...
        raise Exception(f"{i} not contained. The tree is broken :(")
