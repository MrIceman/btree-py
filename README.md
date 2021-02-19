# btree-py

![alt text](https://i.redd.it/3hxgspq64yx01.jpg)

An implementation of a balanced BTree. The heart of most modern databases :-) 
I did it because I was bored and I needed a distraction from android development.

Right now only insertion (+split/merge) and search is supported, I might add deletion and update in future.
Under tests/ you can find some testcases I wrote to assure that the btree works as intended. There's one test
where I set up a tree with k = 9 (key capacity) and n = 1.500.000 (amount of keys). You can use that test 
as comparision if you want to optimize that code. There's some code duplication within the split operation and I'm sure
the code can be also optimized in terms of performance and code quality. If it's bothering you and you need the code for some reason
then feel free to leave an issue and I will have a look on it

To read more about BTrees you can click here
https://en.wikipedia.org/wiki/B-tree
