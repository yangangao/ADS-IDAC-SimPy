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
import pickle, json, copy
import SimVM


def store(data, filename):
    # 序列化，写到本地磁盘文件
    with open(filename,'wb') as f:
        pickle.dump(data, f)

def grab(filename):
    # 反序列化，从本地文件读出原有的对象
    with open(filename,'rb') as f:
        return pickle.load(f)

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

# def Test1():
#     tree = Tree()
#     tree.create_node("Root", "1")  # root node
#     tree.create_node("root-child1", "2", parent="1")
#     tree.create_node("root-child1-child1", "5", parent="2")
#     tree.create_node("root-child2", "3", parent="1")
#     tree.create_node("root-child2-child1", "4", parent="3")
#     tree.create_node("root-child2-child2", "6", parent="3")
#     tree.show()
#     # store(tree, "test.dat")
#     return tree

# VMData = {"VMID": VM.id, "SimData": VM.GetSimData(), "NextStepData": VM.GetNextStepData(), "MET": VM.GetMetFlag()}
# NextStepData = {
#     "GoHead": GoHead,
#     "TurnLeft": TurnLeft,
#     "TurnRight": TurnRight
# }
# GoHead:  {'probability': 0.818733374651966, 'status': [{'time': 400, 'VMid': '2003282016042971', 'shipid': '10086', 'lon': 123.04399241470725, 'lat': 35.001, 'speed': 10, 'heading': 90, 'interval': 100}, {'time': 400, 'VMid': '2003282016042971', 'shipid': '10010', 'lon': 123.06920568604923, 'lat': 35.0, 'speed': 7, 'heading': 270, 'interval': 100}]}


def MySimTree():
    tree = Tree()
    initData = ''
    parent = None

    def CreatVMTree(tree, data, parent):
        """ 
        data looks like: 
        GoHead:  {'probability': 0.818733374651966, 'status': [
            {'time': 400, 'VMid': '2003282016042971', 'shipid': '10086', 'lon': 123.04399241470725, 'lat': 35.001, 'speed': 10, 'heading': 90, 'interval': 100}, 
            {'time': 400, 'VMid': '2003282016042971', 'shipid': '10010', 'lon': 123.06920568604923, 'lat': 35.0, 'speed': 7, 'heading': 270, 'interval': 100}
            ]}
         """
        def GetInitData(data):
            data = copy.deepcopy(data)
            sta0 = data["status"][0]
            sta1 = data["status"][1]
            shipData = {
                ship0: {
                    ShipID: sta0["shipid"],
                    Tick: sta0["time"], 
                    Lon: sta0["lon"],
                    Lat: sta0["lat"],
                    Speed: sta0["speed"],
                    Heading: sta0["heading"]
                },
                ship1: {ShipID: sta1["shipid"], Tick: sta1["time"], Lon: sta1["lon"], Lat: sta1["lat"], Speed: sta1["speed"], Heading: sta1["heading"]}
            }
            initData = copy.deepcopy(shipData)
            return initData

        VMInitData = GetInitData(data)
        Data = SimVM.RunVM(VMInitData, interval = 0.2, timeRatio = 100, runTimes = 8)
        tree.create_node(identifier=Data["VMID"], parent=parent)
        """
        方案1. tree.create_node(identifier=Data["VMID"], parent=parent)
        即 tree 的结点中只放仿真虚拟机的ID和父子关系，前端需要用到某的结点的Data时，再向后台请求，
        Data = SimVM.RunVM()结束后将结点的Data和对应的VMID存入数据库的一张表，仿真事件树另存在一张表.

        方案2. tree.create_node(identifier=Data["VMID"], data=Data, parent=parent)
        即 tree的结点中一次性将包括结点(仿真虚拟机)VMID,Data和父子关系全部存放，
        将一棵带有数据的完整的事件树作为一个整体存入一张表中.
        """
        if Data["MET"] == 0:
            # 船还未相遇，仿真继续，分支
            for item, data in Data["NextStepData"]:
                # Recursion: 递归调用 生成新的结点
                CreatVMTree(tree, data, parent=Data["VMID"])
        else:
            # 船已经相遇，仿真停止，不再分支
            pass
    
    return tree




def main():
    # sTree = Test1()
    # print(Tree_to_eChartsJSON(sTree))
    pass

if __name__ == '__main__':
    main()
