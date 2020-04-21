from flask import Flask, render_template, jsonify, send_file, request
import random, json, base64, os
import my_utils
# import opt_db
import opt_redis

app = Flask(__name__, 
    static_folder='../client/static', 
    template_folder='../client/templates')

data0 = [
    {'name': 'root', 'value': 10086,'children':[
        {'name': 'A', 'value': 1, 'children': [{'name': 'C', 'value': 3}, {'name': 'D', 'value': 4}]}, 
        {'name': 'B', 'value': 2, 'children': [{'name': 'E', 'value': 5}, {'name': 'F', 'value': 6}]}
        ]}]


# dataIndex = [data0, data1, data2, data3]
def get_data():
    # i = random.randint(0, 3)
    # return dataIndex[i]
    return data0


map_data0 = [{"lon": 122.226654, "lat": 31.210672}]
map_data1 = [{
    "lon": 122.226654,
    "lat": 31.210672
}, {
    "lon": 122.226654,
    "lat": 31.410672
}]
map_data2 = [{
    "lon": 122.226654,
    "lat": 31.210672
}, {
    "lon": 122.226654,
    "lat": 31.410672
}, {
    "lon": 122.426654,
    "lat": 31.210672
}]
map_data = [map_data0, map_data1, map_data2]


def get_map_data():
    i = random.randint(0, 2)
    return map_data[i]


# 根路由，首页页面
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("view.html")


# 英语版本的首页页面
@app.route("/en_version")
def index_en():
    return render_template("view-en.html")


# 初始加载的树数据，可删除之
@app.route("/tree")
def get_tree():
    return (jsonify({"data": get_data()}))


# 获取最新的仿真树data
@app.route("/tree/lastest")
def get_lastest_tree():
    # data = opt_db.select_lastest_tree()
    data = opt_redis.select_lastest_tree()
    return(jsonify({"TREEID": data[0], "TREEData": json.loads(data[1])}))
    # return opt_db.select_lastest_tree()[1]

# 从数据库中查询指定TREEID的data并返回
@app.route("/tree/<treeid>")
def get_tree_by_id(treeid):
    # data = opt_db.select_from_simtree(treeid)[1] # 此时是JSON格式的字符串
    data = opt_redis.select_from_simtree(treeid)[1] # 此时是JSON格式的字符串
    return data

# 从数据库中查询指定TREEID的data,并根据value值找到本支的所有VMID并返回
@app.route("/tree/branch/<name>")
def get_branch_by_name(name):
    # first get latest tree data to find out the very branch
    data = opt_redis.select_lastest_tree()
    # print(json.loads(data[1]))
    # print(isinstance(name, str))
    rout = my_utils.findoutRout(json.loads(data[1]), name)
    print(rout)
    return (jsonify(rout))

@app.route("/map")
def get_map():
    return (jsonify({"data": get_map_data()}))


@app.route("/userparameters" , methods=["POST", "GET"])
# /<int:user_speed><float:user_location_we><float:user_location_sn>
def get_userparameters():
    if request.method == "POST":
        # print("这里是map")
        mastership = request.form.get("mastership")
        user_speed = request.form.get("user_speed")
        user_location_we = request.form.get("user_location_we")
        user_location_sn = request.form.get("user_location_sn")
        
        if not all([mastership, user_speed, user_location_we, user_location_sn]):
            print('参数错误')
            return jsonify({'status': '-1', 'errmsg': '接收成功但是参数错误'})
        else:
            print(mastership, user_speed, user_location_we, user_location_sn)
    return jsonify({'status': mastership, 'errmsg': '接收成功'})

# 从数据库中查询指定VMID的data并返回
@app.route("/vm/<vmid>")
def get_vm_by_id(vmid):
    # data = opt_db.select_from_simvm(vmid)[1] # 此时是JSON格式的字符串
    data = opt_redis.select_from_simvm(vmid)[1] # 此时是JSON格式的字符串
    return data


@app.route("/img/<imageid>")
def img_index(imageid):
    # 方式1: 前端采用DOM操作img属性，采用http请求，后端从文件目录返回图片

    # filename = "../client/static/res/{}.png".format(imageid)
    # return send_file(filename, mimetype='image/png')
    
    # 方式2: 前端采用Ajax方式时，后端返回base64编码的字符串

	# 1. 从本地加载一条数据
    # with open("C:/Users/Bruce Lee/Documents/workspace/ADS-IDAC-SimPy/res/VOImg/{}.png".format(imageid), 'rb') as f:
    #     b64 = base64.b64encode(f.read())
    # return b64
	
	# 2. 从数据库加载已经Base64编码的图片数据
    # select_from_voimg返回结果格式为: data = (imgID, VMID, data)
    # return opt_db.select_from_voimg(imageid)[2]
    return opt_redis.select_from_voimg(imageid)[2]
    

if __name__ == "__main__":
    app.run(debug=True)
