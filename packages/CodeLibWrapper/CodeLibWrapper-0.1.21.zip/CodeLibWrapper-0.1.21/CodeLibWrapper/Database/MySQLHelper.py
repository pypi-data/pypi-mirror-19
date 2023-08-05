# -*- coding: utf-8 -*-
# http://www.jb51.net/article/92516.htm
import pymysql


class MySQLHelper:
    _host = ""
    _user = ""
    _password = ""
    _db = ""

    def __init__(self, host, user, password, db):
        self._host = host
        self._user = user
        self._password = password
        self._db = db
        pass

    def execute_sql_script(self, script_text):
        # 创建连接
        conn = pymysql.connect(host=self._host, port=3306, user=self._user, passwd=self._password, db=self._db,
                               charset='utf8')
        # 创建游标
        cursor = conn.cursor()

        # 执行SQL，并返回收影响行数
        effect_row = cursor.execute(script_text)
        # effect_row = cursor.execute("select * from tb7")
        print effect_row

        # 创建数据表
        # cursor.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

        # 插入一条数据
        # cursor.execute("insert into student values('2','Tom','3 year 2 class','9')")

        # 修改查询条件的数据
        # cursor.execute("update student set class='3 year 1 class' where name = 'Tom'")

        # 删除查询条件的数据
        # cursor.execute("delete from student where age='9'")

        # 执行SQL，并返回受影响行数
        # effect_row = cursor.execute("update tb7 set pass = '123' where nid = %s", (11,))

        # 执行SQL，并返回受影响行数,一次插入多条记录
        # effect_row = cursor.executemany("insert into tb7(user,pass,licnese) values(%s,%s,%s)", [
        #            ("u1","u1pass","11111"),
        #            ("u2","u2pass","22222")
        #            ])

        # 提交，不然无法保存新建或者修改的数据
        conn.commit()

        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()

    def execute_sql_insertrecord_get_max_identity_value(self, script_text):
        conn = pymysql.connect(host=self._host, port=3306, user=self._user, passwd=self._password, db=self._db,
                               charset='utf8')
        cursor = conn.cursor()
        effect_row = cursor.executemany("insert into tb7(user,pass,licnese)values(%s,%s,%s)",
                                        [("u3", "u3pass", "11113"), ("u4", "u4pass", "22224")])

        print effect_row
        conn.commit()
        cursor.close()
        conn.close()
        # 获取自增id
        new_id = cursor.lastrowid
        print new_id

    def call_no_property_storedprodure(self):
        # 创建连接
        conn = pymysql.connect(host=self._host, port=3306, user=self._user, passwd=self._password, db=self._db,
                               charset='utf8')
        # 游标设置为字典类型
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 无参数存储过程
        cursor.callproc('p2')  # 等价于cursor.execute("call p2()")

        row_1 = cursor.fetchone()
        print row_1

        conn.commit()
        cursor.close()
        conn.close()

    def call_properties_storedproceduce(self):
        # 创建连接
        conn = pymysql.connect(host=self._host, port=3306, user=self._user, passwd=self._password, db=self._db,
                               charset='utf8')

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.callproc('p1', args=(1, 22, 3, 4))
        # 获取执行完存储的参数,参数@开头
        cursor.execute(
            "select @p1,@_p1_1,@_p1_2,@_p1_3")  # {u'@_p1_1': 22, u'@p1': None, u'@_p1_2': 103, u'@_p1_3': 24}
        row_1 = cursor.fetchone()
        print row_1

        conn.commit()
        cursor.close()
        conn.close()

