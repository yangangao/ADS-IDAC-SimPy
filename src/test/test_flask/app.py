from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import json
import random
from pyecharts.charts import Tree

app = Flask(__name__, static_folder="templates")


# def bar_base() -> Bar:
#     c = (
#         Bar()
#         .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
#         .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
#         # .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
#         .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
#     )
#     return c


data = [{'name': 'A', 'value': 10}]
# data = [{'name': 'A', 'children': [{'name': 'bar', 'children': [{'name': 'bar', 'children': [{'name': 'bar'}, {'name': 'Bar'}]}, {'name': 'Bar'}]}, {'name': 'Bar'}]}]
# foo = {'0':[{'name': 'bar'}, {'name': 'Bar'}]}
def genfoo():
    ran = random.random()
    foo = {'0':[{'name': 'bar', 'value': ran}, {'name': 'Bar', 'value': 1-ran}]}
    return foo
    pass

def addchildren(data, foo):
    
    # foo = json.loads(foo)['0']
    # print(foo)
    for item in data:
        if 'children' in item:
            # print(item['children'])
            addchildren(item['children'], foo)
        else:
            if item['value'] > 0.5:
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
            else:
                pass

        pass
    return data
def tree_base(ge) -> Tree:
    c = (
        Tree()
        # .add("", data)
        .add("", 
        data = addchildren(data, json.dumps(ge)), 
        symbol_size = 16, 
        # collapse_interval = 8,
        initial_tree_depth = -1)
        # .add("", data , initial_tree_depth = -1)  
        .set_global_opts(title_opts=opts.TitleOpts(title="Tree-动态示例"))
    )
    return c


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/barChart")
def get_bar_chart():
    ge = genfoo()

    c = tree_base(ge)
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run()