from redis import StrictRedis
# import json

# redis simtree db0
# redis simvm db1
# redis voimg db2

# =======================================
# 连接
# =======================================
def link_redis_master(selectdb = 0):
    # 连接数据库@写操作
    # redis simtree db0
    # redis simvm db1
    # redis voimg db2
    mydb = StrictRedis(
        host='localhost', 
        port = 6379, 
        db = selectdb, 
        password = '123456',
        decode_responses = True)
    return mydb

def link_redis_slave(selectdb = 0):
    # 连接数据库@读操作
    mydb = StrictRedis(
        host='localhost', 
        port = 6380, 
        db = selectdb, 
        password = '654321',
        decode_responses = True)
    return mydb

# =======================================
# 插入
# =======================================
def insert_into_simtree(TREEID, data):
    """
    将 仿真树 数据插入表 sim_tree 
    redis simtree db0
    :TREEID : varchar string 数字序列,
    :data ： JSON格式的字符串
    """
    sr = link_redis_master(0)
    try:
        result1 = sr.set(TREEID, data)
        result2 = sr.set('lastest', TREEID)
        print(result1 & result2)
    except Exception as e:
        print(e)
    pass

def insert_into_simvm(VMID, data):
    """ 
    将VM数据插入表sim_vm 
    redis simvm db1
    :VMID : varchar string 数字序列,
    :data : JSON格式的字符串
    """
    sr = link_redis_master(1)
    try:
        result = sr.set(VMID, data)
        print(result)
    except Exception as e:
        print(e)
    pass

# 将图片插入数据库的方式暂时不用
def insert_into_voimg(imgID, VMID, data):
    """ 
    将VM仿真过程中生成的voimg图片插入表 voimg 
    redis voimg db2
    :imgID : varchar string 数字序列,
    :VMID : 所属VM ,varchar string 数字序列,
    :data : 二进制字节流
    """
    sr = link_redis_master(2)
    try:
        result = sr.hset(imgID, VMID, data)
        print(result)
    except Exception as e:
        print(e)
    pass

# =======================================
# 查询
# =======================================
def select_from_simtree(TREEID):
    """ 
    从表sim_tree中查询tree数据
    redis simtree db0
    :TREEID : 查询的TREE,
    :return : data = (TREEID, data)
    """
    sr = link_redis_slave(0)
    data = (TREEID, sr.get(TREEID))
    return data


def select_lastest_tree():
    """
    从表sim_tree中查询最新的一条tree数据
    : return: (TREEID, data)
    """
    # redis simtree db0
    # redis simvm db1
    # redis voimg db2
    sr = link_redis_slave(0)
    try:
        TREEID = sr.get('lastest')
    except Exception as e:
        print(e)
    else:
        data = (TREEID, sr.get(TREEID))
    return data


def select_from_simvm(VMID):
    """ 
    从表sim_vm中查询VM数据 
    :VMID : 查询的VM,
    :return : data = (VMID, data)
    """
    # redis simtree db0
    # redis simvm db1
    # redis voimg db2
    sr = link_redis_slave(1)
    data = (VMID, sr.get(VMID))
    return data


# 从数据库中查询一张图片
def select_from_voimg(imgID):
    """ 
    从表voimg中查询标识为 imgID 的VM的imgs 
    :imageid : 查询img所属的ID,
    :return : data = (imgID, VMID, data)
    """
    # redis simtree db0
    # redis simvm db1
    # redis voimg db2
    sr = link_redis_slave(2)
    # imgdata = sr.hgetall(imgID)
    data = (imgID, sr.hkeys(imgID)[0], sr.hvals(imgID)[0])
    return data


# def deletdb_all(db = 0):
#     sr = link_redis_master(db)
#     result = sr.fulshall()
#     return result


# def insert_into_redis(val, param="one"):
#     '''
#     :val : 待插入数据
#     :param : "one"表示插入一条数据,"many"表示插入多条数据.
#     '''
#     mydb = link_redis_master()
#     if param == "one":
#         result = mydb.set(val)
#         # set(VMID, data)
#         if result == 'OK':
#             print("1 record has been inserted.")
#         # 无需主动关闭数据库连接
#         return
#     elif param == "many":
#         result = mydb.mset(val)
#         if result == 'OK':
#             print("records have been inserted.")
#         return       
#     else:
#         print("请输入正确的参数以确定要插入的数量.")
#         return


# def select_all_from_redis():
#     # 返回所有键值对
#     mydb = link_redis_slave()
#     keys = mydb.keys()
#     vals = mydb.mget(keys)
#     data = list(map(lambda x,y: dict(x, **y), keys, vals))
#     # index = 0
#     # for key in keys:
#     #     data[index] = [keys[index] , vals[index]]
#     return data


# def test_select_all():
#     mydata = select_from_mysql()
#     for item in mydata:
#         print(item, '\n')
#         item_data = json.loads(item[1])
#         print(item_data, '\n')
#         print(type(item_data))

    
# def test_insert_one(data):
#     data = json.dumps(data)
#     VMID = "1100"
#     val = (VMID, data)
#     insert_into_mysql(val, param="one")
#     pass

# def test_insert_many():
    
#     pass
