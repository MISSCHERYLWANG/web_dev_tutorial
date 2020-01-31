# ORM Learn
## 简介
ORM 到底是什么?

> 有人说ORM是天使，也有人说ORM是噩梦

ORM全称是：Object Relational Mapping(对象关系映射)，其主要作用是在编程中，把面向对象的概念跟数据库中表的概念对应起来。举例来说就是，我定义一个对象，那就对应着一张表，这个对象的实例，就对应着表中的一条记录。

从代码上来看吧。拿Django的model来举例:

```python
from django.db import models

class User1(models.Model):
    name = models.CharField(max_length=255)
```
对应的数据库中可能就是一个表:user,里面有一个字段（我们假设不定义的自动不存在，包括主键），那就是name 类型是varchar(255)。

那么，如果我们有一个User的实例，比如:

```python
user = User1()
user.name = 'the5fire'
user.save()   # 存入数据库
```

那么对应着数据库中就有一条记录，name为the5fire。此时的user实例，对应的正是这个表的这一条记录。

用ORM的好处就是你不用操作表，可以在程序中用面向对象的思路，直接操作对象即可。比如上面那个代码，我要插入一条语句，直接user.save()即可。ORM会帮我们产生一条SQL语句。

```sql
INSERT INTO user1(name) VALUES("the5fire");
```

当然这只是从对象到SQL的映射，还有从SQL到对象的映射，也是类似的过程。我在之前那篇文章Django分表的两个方案中也有提及到，可以一并看看。


## 练习
在本章中你需要学习一个简单的orm库peewee的使用, 与django的orm使用基本一样.

在peewee_learn中已经存在一个多对多的关系，用户和它的角色。
在开始前你可以查看[peewee QuickStart](http://docs.peewee-orm.com/en/latest/peewee/quickstart.html)

首先配置虚拟环境和安装依赖的库
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
执行脚本会创建内存中的sqlite数据库
```bash
python peewee_learn.py
```

你的作业如下:
1.将SqliteDatabase的参数":memory:"改为任意一个名字，会在同目录下创建一个sqlite数据库，使用sqlite命令连接该数据库，查看建立的表结构
> 在mac下通常已经安装了sqlite命令，假如已经建立了a.db这一sqlite数据库，可以通过sqlite3  a.db 进入交互环境，.schema 会打印当前数据库的建表语句， 你也可以通过.help查看其他命令

思考orm和使用直接使用sql的优劣

2. 尝试修改数据库为Mysql，并尝试使用sql语句建立完表后直接使用Orm进行操作，而不是使用create_table函数去建表

> Model需要和sql语句保持一致，请参考[peewee meta 文档](http://docs.peewee-orm.com/en/latest/peewee/models.html#model-options-and-table-metadata)

3.目前需要在该程序上拓展一个会议室预定系统，因此对目前的设计需要做出一定的修改。用户可以预定会议室，会议室预定时需要设定预定的时间，同一个会议室不能同时在同一时间被两个人预定,请你完成该程序.
要求
    能够查询同一用户在某一日的所有会议室预定
    能够查询同一会议室在某一日的所有预定