import datetime, functools

from flask import Flask, session, redirect, url_for, escape, request, jsonify
from peewee import *
from playhouse.flask_utils import FlaskDB

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

database = SqliteDatabase("test.db")
db_wrap = FlaskDB(app, database=database)

class Role(db_wrap.Model):
    id = AutoField()
    name = CharField(default="ordinary_user", help_text="角色名")

    def __repr__(self):
        return "<Role: {}>".format(self.name)

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

class UserRoleRelationship(db_wrap.Model):
    id = AutoField()
    to_user = ForeignKeyField(User)
    to_role = ForeignKeyField(Role, backref='users')

#插入数据
def insert_user():
    user1 = User.create(username="lynskylate", password="test")
    user2 = User.create(username="jww", password="test")
    role1 = Role.create(name="admin")
    UserRoleRelationship.create(to_user=user1, to_role=role1)
    UserRoleRelationship.create(to_user=user2, to_role=role1)



class Conference(db_wrap.Model):
    id = AutoField()
    location = CharField(help_text="会议室位置")
    name = CharField()
    capacity = IntegerField(default=0, help_text="容量")
    status = IntegerField(default=0)


    def to_data(self):
        return {
            "location": self.location,
            "name": self.name,
            "id": self.id,
            "status": self.status
        }

def insert_confer():
    confer1 = Conference.create(location="#8", name="103", capacity=100)
    confer2 = Conference.create(location="#8", name="104", capacity=80)
    confer3 = Conference.create(location="#8", name="105", capacity=80)
    confer4 = Conference.create(location="#8", name="106", capacity=80)
    confer5 = Conference.create(location="#8", name="201", capacity=200)
    confer6 = Conference.create(location="#8", name="202", capacity=100)


class OrderRecord(db_wrap.Model):
    id = AutoField()
    orderUser = ForeignKeyField(User)
    conference = ForeignKeyField(Conference)
    orderStartTime = DateTimeField(
        default=datetime.datetime.now)
    orderEndTime = DateTimeField(
        default=datetime.datetime.now)


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
    user = User.get_or_none(User.username==username)
    if user != None :
        if user.password == password:
            session["username"] = username
            return {"message":"success"}
        else :
            return 'Your password is incorrect.'
    else:
        return 'Please sign in.'

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
@login_required
def user():
    # TODO: 增加权限校验, 仅登陆用户可访问该接口
    # TODO: 查询用户信息，并将息放在接口中, 使用User的to_data方法
    # e.g.: {"message":"success", "data": { "username": "wyy", "nickname": "wyy" }}
    # if 'username' in session:
    name = session['username']
    return {"message": "success", "data": User.get(User.username==name).to_data()}

@app.route('/conferences')
#@login_required
def get_conference():
    conferNum = Conference.select().count()
    l = 5
    conferList = []
    for i in range(conferNum):
        temp = 0
        if i + l < conferNum:
            temp = l
        else:
            temp = conferNum - i
        conferPerPage = Conference.select().limit(temp).offset(i)
        i += temp
        
        for confer in conferPerPage:
            conferList.append(confer.to_data())
        return {
            "data": {
                "count": temp,
                "conferences": conferList
            },
            "message": "success"
        }


@app.route('/conferences/<int:id>/order', methods=["POST"])
@login_required
def order_conference(id):
    startTime = request.json['start_time']
    endTime = request.json['end_time']
    name = session['username']
    userId = User.get(User.username==name)
    OrderRecord.create(orderUser=userId, conference=id, 
                        orderStartTime=startTime, orderEndTime=endTime)
    q = Conference.update(status=1).where(Conference.id==id)
    q.execute()

    return {"message": "success"}

if __name__ == "__main__":
    database.connect()
    # database.create_tables([User, Role, UserRoleRelationship, Conference, OrderRecord])
    # insert_user()
    insert_confer()
    # User.create(username='test', password='123456')