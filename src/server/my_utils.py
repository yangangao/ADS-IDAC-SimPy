# # -*- coding: utf-8 -*-
# import time
# ====================================================
# ===========由节点找分支==============================
VMtree = {
  "data": [
    {
      "name":  "2004162131127567",
       "value":  2004162131127567,
       "children":  [
        {
          "name":  "2004162131181256",
           "value":  2004162131181256,
           "children":  [
            {
              "name":  "2004162131238214",
               "value":  2004162131238214,
               "children":  [
                {
                  "name":  "2004162131281164",
                   "value":  2004162131281164
                },
                 {
                  "name":  "2004162131337947",
                   "value":  2004162131337947
                },
                 {
                  "name":  "2004162131391649",
                   "value":  2004162131391649
                }
              ]
            },
             {
              "name":  "2004162131447186",
               "value":  2004162131447186,
               "children":  [
                {
                  "name":  "2004162131493625",
                   "value":  2004162131493625
                },
                 {
                  "name":  "2004162131542577",
                   "value":  2004162131542577
                },
                 {
                  "name":  "2004162131599652",
                   "value":  2004162131599652
                }
              ]
            },
             {
              "name":  "2004162132054730",
               "value":  2004162132054730,
               "children":  [
                {
                  "name":  "2004162132105542",
                   "value":  2004162132105542
                },
                 {
                  "name":  "2004162132166668",
                   "value":  2004162132166668
                },
                 {
                  "name":  "2004162132212320",
                   "value":  2004162132212320
                }
              ]
            }
          ]
        },
         {
          "name":  "2004162132269704",
           "value":  2004162132269704,
           "children":  [
            {
              "name":  "2004162132313935",
               "value":  2004162132313935,
               "children":  [
                {
                  "name":  "2004162132363193",
                   "value":  2004162132363193
                },
                 {
                  "name":  "2004162132423131",
                   "value":  2004162132423131
                },
                 {
                  "name":  "2004162132479176",
                   "value":  2004162132479176
                }
              ]
            },
             {
              "name":  "2004162132522606",
               "value":  2004162132522606,
               "children":  [
                {
                  "name":  "2004162132575031",
                   "value":  2004162132575031
                },
                 {
                  "name":  "2004162133033314",
                   "value":  2004162133033314
                },
                 {
                  "name":  "2004162133081558",
                   "value":  2004162133081558
                }
              ]
            },
             {
              "name":  "2004162133146540",
               "value":  2004162133146540,
               "children":  [
                {
                  "name":  "2004162133194881",
                   "value":  2004162133194881
                },
                 {
                  "name":  "2004162133244506",
                   "value":  2004162133244506
                },
                 {
                  "name":  "2004162133302577",
                   "value":  2004162133302577
                }
              ]
            }
          ]
        },
         {
          "name":  "2004162133353371",
           "value":  2004162133353371,
           "children":  [
            {
              "name":  "2004162133409229",
               "value":  2004162133409229,
               "children":  [
                {
                  "name":  "2004162133456615",
                   "value":  2004162133456615
                },
                 {
                  "name":  "2004162133507017",
                   "value":  2004162133507017
                },
                 {
                  "name":  "2004162133567458",
                   "value":  2004162133567458
                }
              ]
            },
             {
              "name":  "2004162134014459",
               "value":  2004162134014459,
               "children":  [
                {
                  "name":  "2004162134063063",
                   "value":  2004162134063063
                },
                 {
                  "name":  "2004162134127856",
                   "value":  2004162134127856
                },
                 {
                  "name":  "2004162134174393",
                   "value":  2004162134174393
                }
              ]
            },
             {
              "name":  "2004162134221529",
               "value":  2004162134221529,
               "children":  [
                {
                  "name":  "2004162134282465",
                   "value":  2004162134282465
                },
                 {
                  "name":  "2004162134338477",
                   "value":  2004162134338477
                },
                 {
                  "name":  "2004162134384639",
                   "value":  2004162134384639
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}

nodeIndex = []
nodeValue = []
brunchRout = {'endin' : 0}

def list_dictionary(tree, layer = 0):
    if isinstance(tree, list):
        for i in tree:
            list_dictionary(i, layer)
    elif isinstance(tree, dict):
        layer += 1
        nodeIndex.append(layer)
        for key, value in tree.items():
            list_dictionary(value, layer)
    else:
        if isinstance(tree, str):
            nodeValue.append(tree)

def findoutRout(vmtree, keyvalue):
    list_dictionary(vmtree['data'])
    testindex = 0
    brunch = []
    for i in nodeIndex:
        brunchRout[str(i)] = str(testindex)
        if nodeValue[testindex] == keyvalue:
            brunchRout['endin'] = str(i)
            break
        testindex += 1
    i = 1
    while i <= int(brunchRout['endin']):
        brunchRout["in" + str(i)] = nodeValue[int(brunchRout[str(i)])]
        i += 1
    return brunchRout


# findoutRout(VMtree, '2004162134014459')

# ====================================================


# def get_time():
#     time_str = time.strftime("%Y{}%m{}%d{} %X")
#     return time_str.format("年", "月", "日")


# if __name__ == "__main__":
#     print(get_time())
# import base64
# with open('./res/static/ship1.png', 'rb') as f:
#     # f.read()
#     # print(f.read())
#     b64 = base64.b64encode(f.read())
#     print(type(b64))

# def EncodeImg2B64Stream(imageid):
#     """
#     ????:
#     ??????base64?
#     :param imageid:???????id
#     :return: ???
#     """
#     import base64
#     img_stream = ''
#     with open('path_to_img/{}.png'.format(imageid), 'rb') as img_f:
#         img_stream = img_f.read()
#         img_stream = base64.b64encode(img_stream)
#     return img_stream