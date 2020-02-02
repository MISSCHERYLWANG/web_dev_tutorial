# Auth Tutorial
## Intro
本章以flask为例介绍web端权限验证的基本实现，同时通过编写验证代码对web开发有进一步的了解.

首先阅读如下文章对cookies 和 JWT有一个基本的了解

[cookie](https://javascript.ruanyifeng.com/bom/cookie.html)
[Json Web Token](http://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)

本章练习以Flask框架为基础，请参考[flask官方文档](https://flask.palletsprojects.com/en/1.1.x/quickstart/#)

## Exercise
在作业开始前，阅读flask文档的[quick Start](https://dormousehole.readthedocs.io/en/latest/quickstart.html#)

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask peewee
```

```bash
# 创建必要的数据库
python app.py
# 运行flask应用
export FLASK_APP=app.py
flask run
```

1.完成app.py接口中需要对User查询的部分，同时完成权限验证部分

2.在完成1后，使用如下命令尝试登陆的接口，观察返回的响应中的header
```bash
curl -X POST \
  http://localhost:5000/login \
  -H 'content-type: application/json' \
  -d '{
	"username": "test",
	"password": "123456"
}'
```
header中的哪个字段会使得浏览器下次访问时会带上登陆信息?
cookies中是否会有账号密码等隐私信息？flask是怎么做的？

3.学习python的装饰器语法，将权限验证改写为装饰器
可以参考[flask tutorial](https://dormousehole.readthedocs.io/en/latest/tutorial/views.html#id6)