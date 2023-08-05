# -*- coding: utf-8 -*-
from xml.sax import handler, parseString
import sys
import pymysql

reload(sys)
sys.setdefaultencoding('utf-8')

in_sql = "insert into person(id,sex,address,fansNum,summary,wbNum,gzNum,blog,edu,work,renZh,brithday) \
values(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"
fields = ("id", "sex", "address", "fansNum", "summary", "wbNum", "gzNum", "blog", "edu", "work", "renZh", "brithday")
object_instance_name = "person"  # XML中的节点标记


class Db_Connect:
    def __init__(self, db_host, user, pwd, db_name, charset="utf8", use_unicode=True):
        print "init begin"
        print db_host, user, pwd, db_name, charset, use_unicode
        # self.conn = MySQLdb.Connection(db_host, user, pwd, db_name, charset=charset, use_unicode=use_unicode)
        print "init end"

    def insert(self, sql):
        try:
            n = self.conn.cursor().execute(sql)
            return n
        except pymysql.Warning, e:
            print "Error: execute sql '", sql, "' failed"

    def close(self):
        # self.conn.close()
        print "Close."


class ObjectHandler(handler.ContentHandler):
    def __init__(self, db_ops):
        """
        从外部传入的处理对象，此处是以数据库为处理模式
        :param db_ops:
        """
        self.object_instance = {}
        self.current_tag = ""
        self.in_quote = 0

        self.db_ops = db_ops

    def startElement(self, name, attr):
        if name == object_instance_name:
            # 此处还可以处理属性的值
            print attr["name"]
            self.object_instance = {}
        self.current_tag = name
        self.in_quote = 1

    def endElement(self, name):
        if name == object_instance_name:
            in_fields = tuple([('"''' + self.object_instance.get(i, "") + '"') for i in fields])
            print in_fields

            print in_sql % in_fields
            # db_ops.insert(in_sql % (in_fields))
        self.in_quote = 0

    def characters(self, content):
        # 若是在tag之间的内容，更新到map中
        if self.in_quote:
            self.object_instance.update({self.current_tag: content})


if __name__ == "__main__":
    f = open(r"D:\PythonCode\CodeLib\Template\persons.xml")
    # 如果源文件gbk  转码      若是utf-8，去掉decode.encode
    db_ops = Db_Connect("127.0.0.1", "root", "root", "test")
    parseString(f.read().decode("gbk").encode("utf-8"), ObjectHandler(db_ops))
    f.close()
    db_ops.close()
