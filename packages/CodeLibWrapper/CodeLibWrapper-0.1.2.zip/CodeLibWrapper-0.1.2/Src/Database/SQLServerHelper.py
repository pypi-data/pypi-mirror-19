# -*- coding: utf-8 -*-
import pymssql


class SQLServerHelper:
    server = ""
    user = ""
    password = ""

    def __init__(self, server_instance, login_user, login_password):
        global server
        server = server_instance
        global user
        user = login_user
        global password
        password = login_password

    def execute_sql_script(self, database_name, script):
        """
        :param database_name: 要连接的数据库名，例如： tempdb
        :param script: 要执行的SQL命令文本。例如：

        IF OBJECT_ID('persons', 'U') IS NOT NULL
            DROP TABLE persons
        CREATE TABLE persons (
            id INT NOT NULL,
            name VARCHAR(100),
            salesrep VARCHAR(100),
            PRIMARY KEY(id)
        )
        :return:
        """
        conn = pymssql.connect(server, user, password, database_name)
        cursor = conn.cursor()
        cursor.execute(script)
        conn.commit()
        conn.close()

    def execute_sql_query(self, database_name, script, output_query_to_xml):
        """
        :param database_name: 要连接的数据库名，例如： tempdb
        :param script: 要执行的SQL命令文本。例如：
        :param output_query_to_xml: 是否输出xml格式
        :return:
        """
        conn = pymssql.connect(server, user, password, database_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        row = cursor.fetchone()


        # cursor.executemany(
        #     "INSERT INTO persons VALUES (%d, %s, %s)",
        #     [(1, 'John Smith', 'John Doe'),
        #      (2, 'Jane Doe', 'Joe Dog'),
        #      (3, 'Mike T.', 'Sarah H.')])
        # # you must call commit() to persist your data if you don't set autocommit to True
        # conn.commit()
        #
        # cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        # row = cursor.fetchone()
        # while row:
        #     print("ID=%d, Name=%s" % (row[0], row[1]))
        #     row = cursor.fetchone()

        conn.close()


def aaa():
    print "aaaa"
