import datetime, functools

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
    username = CharField(index=True, unique=True)
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
    if User.get(User.username==username).password == password:
        print(User.get(User.username==username).password)
        session["username"] = username
        return {"message":"success"}
    else:
        return 'Username or password is incorrect.'

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

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/user_profile')
def user():
    # TODO: 增加权限校验, 仅登陆用户可访问该接口
    # TODO: 查询用户信息，并将息放在接口中, 使用User的to_data方法
    # e.g.: {"message":"success", "data": { "username": "wyy", "nickname": "wyy" }}
    # if 'username' in session:
    @login_required
    return {"message": "success", "data": User.get(username==username).to_data()}


if __name__ == "__main__":
    database.connect()
    database.create_tables([User])
    User.create(username='test', password='123456')