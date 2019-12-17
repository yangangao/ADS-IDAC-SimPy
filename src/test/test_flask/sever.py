from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from pyecharts.charts import Tree

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar
import time

app = Flask(__name__, static_folder="templates")

data = [{'name': 'A', 'children':[{'name': 'B'}, {'name': 'C'}]}]
foo = {'0':[{'name': 'bar'}, {'name': 'Bar'}]}
# def bar_base() -> Bar:
#     c = (
#         Bar()
#         .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
#         .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
#         .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
#         .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
#     )
#     return c

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

def tree_base() -> Tree:
    # data = [
    #     {
    #         "children": [
    #             {"name": "B"},
    #             {
    #                 "children": [
    #                     {"children": [{"name": "I"}], "name": "E"},
    #                     {"name": "F"},
    #                 ],
    #                 "name": "C",
    #             },
    #             {
    #                 "children": [
    #                     {"children": [{"name": "J"}, {"name": "K"}], "name": "G"},
    #                     {"name": "H"},
    #                 ],
    #                 "name": "D",
    #             },
    #         ],
    #         "name": "A",
    #     }
    # ]
    data = addchildren(data, json.dumps(foo))
    c = (
        Tree()
        .add("", data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例"))
    )
    return c


@app.route("/")
def index():
    # c = bar_base()
    c = tree_base()
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run()