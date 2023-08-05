# -*- coding: utf-8 -*-
import pymssql


class SQLServerHelper:
    server = ""
    user = ""
    password = ""

    def __init__ (self, server_instance, login_user, login_password):
        global server
        server = server_instance
        global user
        user = login_user
        global password
        password = login_password

    def execute_sql_script_with_no_return (self, database_name, script):
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
        conn = pymssql.connect (server, user, password, database_name)
        cursor = conn.cursor ()
        cursor.execute (script)
        conn.commit ()
        conn.close ()

    def execute_sql_query_return_many_record (self, database_name, script):
        conn = pymssql.connect (server, user, password, database_name)
        cursor = conn.cursor ()
        cursor.execute (script)
        rows = cursor.fetchall ()
        conn.close ()
        return rows

    def execute_sql_query_return_one_record (self, database_name, script):
        """
        :param database_name: 要连接的数据库名，例如： tempdb
        :param script: 要执行的SQL命令文本。例如：
        :return:
        """
        conn = pymssql.connect (server, user, password, database_name)
        cursor = conn.cursor ()
        cursor.execute (script)
        row = cursor.fetchone ()

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

        conn.close ()
        return row

def main ():
    print "SQL Server Test"
    # helper = SQLServerHelper ("dp-db-prod", "DMClient", "h(4Xo(T5rbB0")
    # record = helper.execute_sql_query_return_one_record ("DoclibData", "select count(*) From Client")
    # print record[0]
    # record1 = helper.execute_sql_query_return_many_record ("DoclibData", "select * From Client")
    # print record1[0][0]
    # result3 = helper.execute_sql_query_return_one_record ("DoclibData", "Exec GetSequenceId")
    # print result3[0]


if __name__ == '__main__':
    main ()
