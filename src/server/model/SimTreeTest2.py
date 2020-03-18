#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      Youan
#
# Created:     02-03-2020
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

import json
def Tree_to_eChartsJSON(tree):
    #Transform the whole tree into an eCharts_JSON.
    def to_dict(tree, nid):
        ntag = tree[nid].tag
        tree_dict = {'name': ntag, 'value': int(nid), "children": []}
        #if tree[nid].expanded:
        for elem in tree.children(nid):
            tree_dict["children"].append(to_dict(tree, elem.identifier))
        if len(tree_dict["children"]) == 0:
            tree_dict.pop('children', None)
        return tree_dict
    eChartsDict = {'data': [to_dict(tree, tree.root)]}
    return json.dumps(eChartsDict)
    pass

def Test1():
    tree = Tree()
    tree.create_node("Root", "1")  # root node
    tree.create_node("root-child1", "2", parent="1")
    tree.create_node("root-child1-child1", "5", parent="2")
    tree.create_node("root-child2", "3", parent="1")
    tree.create_node("root-child2-child1", "4", parent="3")
    tree.create_node("root-child2-child2", "6", parent="3")
    tree.show()
    # store(tree, "test.dat")
    return tree

def main():
    sTree = Test1()
    print(Tree_to_eChartsJSON(sTree))
    pass

if __name__ == '__main__':
    main()
