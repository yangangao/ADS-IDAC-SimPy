import json

# data = [{'name': 'A', 'children':[{'name': 'B'}, {'name': 'C'}]}]
def addchildren(data, foo):
    # foo = json.loads(foo)['0']
    # print(foo)
    for item in data:
        if 'children' in item:
            # print(item['children'])
            addchildren(item['children'], foo)
        else:
            # print('foo1:', type(foo), foo)
            foo = json.loads(foo)['0']
            # print('foo2:', type(foo), foo)
            item['children'] = foo
            # print(item)
            # print('foo3:', type(foo), foo)
            foo = {'0': foo}
            # print('foo4:', type(foo), foo)
            foo = json.dumps(foo)
            # print('foo5:', type(foo), foo)

        pass
    return data

data = [{'name': 'A'}]
data2 = data
foo = {'0':[{'name': 'bar'}, {'name': 'Bar'}]}
data = addchildren(data, json.dumps(foo))
print('data:', data)
print('foo:', foo)
data = addchildren(data, json.dumps(foo))
print('data:', data)
print('foo:', foo)
data = addchildren(data, json.dumps(foo))
print('data:', data)
print('foo:', foo)
data = addchildren(data, json.dumps(foo))
print('data:', data)
print('foo:', foo)
# import json
# root = {'root': 'A', 'node': {'root': 'B'}}
# node = {'root': 'Bar'}

# def addnode(root, node):
#     # print('root', type(root))
#     # print('node', type(node))
#     # root = json.loads(root)
#     node = json.loads(node)
#     if 'node' in root:
#         addnode(root['node'], json.dumps(node))
#     else:
#         root['node'] = node
#     return root
#     pass
# print(root)
# root = addnode(root, json.dumps(node))
# print(root)
# root = {'root': 'A', 'node': {'root': 'B', 'node': {'root': 'C'}}}
# root2 = addnode(root, json.dumps(node))
# print(root2)
# root3 = addnode(root2, json.dumps(node))
# print(root3)
# print(node)
