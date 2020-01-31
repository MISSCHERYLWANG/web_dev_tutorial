import datetime

from typing import Iterable

from peewee import Model, CharField, IntegerField, AutoField, DateTimeField, SqliteDatabase, ForeignKeyField

db = SqliteDatabase(":memory:")


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
    nickname = CharField(default="null")
    username = CharField(index=True)
    password = CharField(help_text="密码")
    create_time = DateTimeField(
        default=datetime.datetime.now, help_text="账号创建时间")

    def __repr__(self):
        return "<User {}>".format(self.username)

    @property
    def roles(self)->Iterable[Role]:
        return Role.select().join(UserRoleRelationship, on=UserRoleRelationship.to_role).where(UserRoleRelationship.to_user == self).order_by(Role.name)

class UserRoleRelationship(BaseModel):
    id = AutoField()
    to_user = ForeignKeyField(User)
    to_role = ForeignKeyField(Role, backref='users')

# TODO: 完成会议室预定的实现
class Conferences(BaseModel):
    # TODO: 完成该方法，使得能够查询某一天的所有预定记录
    def queryOrderByDay(self, day: datetime.date):
        pass

class OrderRecord(BaseModel):
    # 在这个类中，你需要保存会议室预定的时间，预定的会议室，以及预定的用户
    # 可以参考UserRoleRelationship这一多对多关系的实现
    pass



def create_db():
    # 会创建数据库和相关的表
    db.connect()
    db.create_tables([User, Role, UserRoleRelationship])


def insert_user():
    user1 = User.create(username="lynskylate", password="test")
    user2 = User.create(username="jww", password="test")
    role1 = Role.create(name="admin")
    UserRoleRelationship.create(to_user=user1, to_role=role1)
    UserRoleRelationship.create(to_user=user2, to_role=role1)


if __name__ == "__main__":
    create_db()
    insert_user()
