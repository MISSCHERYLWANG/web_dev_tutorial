import datetime

from flask import Flask, session, redirect, url_for, escape, request, jsonify
from peewee import *
from playhouse.flask_utils import FlaskDB

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

database = SqliteDatabase("test.db")
db_wrap = FlaskDB(app, database=database)

class User(db_wrap.Model):
    id = AutoField()
    nickname = CharField(default="null")
    username = CharField(index=True)
    password = CharField(help_text="密码")
    create_time = DateTimeField(
        default=datetime.datetime.now, help_text="账号创建时间")

    def to_data(self):
        return {
            "username": self.username,
            "nickname": self.nickname,
            "create_time": self.create_time
        }

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    #TODO: 请从数据库中查询用户的账号密码，确定后才设置session
    session["username"] = username
    return {"message":"success"}

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=["POST"])
def register():
    username = request.json['username']
    password = request.json['password']
    User.create(username=username, password=password)
    return {"message": "success"}

@app.route('/user_profier')
def user():
    # TODO: 增加权限校验, 仅登陆用户可访问该接口
    # TODO: 查询用户信息，并将息放在接口中, 使用User的to_data方法
    # e.g.: {"message":"success", "data": { "username": "wyy", "nickname": "wyy" }}
    return {"message": "success"}


if __name__ == "__main__":
    database.connect()
    database.create_tables([User])