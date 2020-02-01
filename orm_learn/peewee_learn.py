import datetime

from typing import Iterable

from peewee import SqliteDatabase, MySQLDatabase, Model, CharField, IntegerField, AutoField, DateTimeField, ForeignKeyField

# db = SqliteDatabase("conference_sys.db")
db = MySQLDatabase('confer_db', host='127.0.0.1', port=3306, user='root', password='root')

class BaseModel(Model):
    class Meta:
        database = db


class Role(BaseModel):
    id = AutoField()
    name = CharField(help_text="角色名")

    def __repr__(self):
        return "<Role: {}>".format(self.name)


class User(BaseModel):
    id = AutoField()
    username = CharField(index=True)
    password = CharField(help_text="密码")
    email = CharField(help_text="邮箱")
    create_time = DateTimeField(
        default=datetime.datetime.now, help_text="账号创建时间")
    role = IntegerField(default=0)
    def __repr__(self):
        return "<User {}>".format(self.username)

    # @property
    # def roles(self)->Iterable[Role]:
    #     return Role.select().join(UserRoleRelationship, on=UserRoleRelationship.to_role).where(UserRoleRelationship.to_user == self).order_by(Role.name)

# class UserRoleRelationship(BaseModel):
#     id = AutoField()
#     to_user = ForeignKeyField(User)
#     to_role = ForeignKeyField(Role, backref='users')

# TODO: 完成会议室预定的实现
class Conference(BaseModel):
    id = AutoField()
    location = CharField(help_text="会议室位置")
    name = CharField()
    capacity = IntegerField(default=0, help_text="容量")

    # TODO: 完成该方法，使得能够查询某一天的所有预定记录
    def queryOrderByDay(self, day: datetime.date):
        return OrderRecord.select().where(OrderRecord.orderStartTime.date()==day)
    
        
class OrderRecord(BaseModel):
    # 在这个类中，你需要保存会议室预定的时间，预定的会议室，以及预定的用户
    # 可以参考UserRoleRelationship这一多对多关系的实现
    id = AutoField()
    orderUser = ForeignKeyField(User)
    conference = ForeignKeyField(Conference)
    orderStartTime = DateTimeField(
        default=datetime.datetime.now)
    orderEndTime = DateTimeField(
        default=datetime.datetime.now)
    


def create_db():
    # 会创建数据库和相关的表
    db.connect()
    # db.create_tables([User, Conference, OrderRecord])


def insert_user():
    user1 = User.create(username="lynskylate", password="test", 
                        email="lynskylate@gmail.com", role=1)
    user2 = User.create(username="jww", password="test",
                        email="wyy017@163.com", role=0)
def queryUser(n: CharField):
    q = User.select().where(User.username==n)
    print(q.dicts())
        

def insert_confer():
    con1 = Conference.create(name="107", location="Floor 1", capacity=40)


def insert_record():
    record1 = OrderRecord.create(orderUserId=2, conferenceId=1)

if __name__ == "__main__":
    create_db()
    # insert_user()
    # insert_confer()
    # insert_record()
    queryUser("jww")
