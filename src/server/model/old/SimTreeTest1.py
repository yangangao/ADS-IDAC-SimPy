#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      Youan
#
# Created:     22-01-2020
# Copyright:   (c) Youan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from treelib import Node, Tree

import pickle

def store(data, filename):
    # 序列化，写到本地磁盘文件
    with open(filename,'wb') as f:
        pickle.dump(data, f)

def grab(filename):
    # 反序列化，从本地文件读出原有的对象
    with open(filename,'rb') as f:
        return pickle.load(f)

# TODO
# def my_create_node(tag, idstring, data, parent, ):
#     tree.create_node(tag, idstring, data, parent)
#     # TO-DO


def Test1():
    tree = Tree()
    tree.create_node("NodeRoot", "root", data = "root data" , parent = None)  # root node
    tree.create_node("Branch1", "node1", data = "node1 data", parent="root")
    tree.create_node("Branch2", "node2", parent="root")
    tree.create_node("Branch11", "node11", parent="node1")
    tree.create_node("Branch121", "node12", parent="node1")
    tree.create_node("Branch111", "node111", parent="node12")

    data = [{"name": "root", "value": 1, "children":[{"name": "root-child1", "value": 2},{"name": "root-child2", "value": 3, "children": [{"name": "root-child2-child1", "value": 4}]}]}]
    data3 = [{'name': 'A', 'children':[{'name': 'B', 'children': [{'name': 'bar', 'children': [{'name': 'bar'}, {'name': 'Bar'}]}, {'name': 'Bar'}]}, {'name': 'C'}]}]


    tree.show()
    # tree.
    # print(tree)
    store(tree, "test.dat")
    return tree

def Test3():
    tree = grab("test.dat")
    tree.show()
    print(tree.to_json(with_data=True))
    print(tree.to_json())
    tree.to_graphviz("test.gv")

from graphviz import Digraph, Source
def Test4():
    src=Source.from_file("test.gv", format='png', engine='dot')
    src.view()
    pass

def from_file():
    pass

def to_echarts_JSON():
    pass

def DoPreOrder(tree):
    return [tree[i] for i in tree.expand_tree()]
    pass

def main():
    sTree = Test1()
    R = DoPreOrder(sTree)
    print(R)
    # print(sTree.all_nodes())
    #Test2(sTree)
    Test3()
    #Test4()
    pass

if __name__ == '__main__':
    main()
