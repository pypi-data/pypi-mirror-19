# -*- coding: utf-8 -*-

import xlrd


def open_excel(excel_file_path='1.xlsx'):
    try:
        data = xlrd.open_workbook(excel_file_path)
        return data
    except Exception, e:
        print str(e)


# 根据索引获取Excel表格中的数据
# 参数:file：Excel文件路径
# column_index：表头列名所在行的索引  ，
# sheet_index：表的索引
def excel_table_by_sheet_index(excel_file='1.xlsx', column_index=0, sheet_index=0):
    data = open_excel(excel_file)
    table = data.sheets()[sheet_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(column_index)  # 某一行数据
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


# 根据名称获取Excel表格中的数据
# 参数:file：Excel文件路径
# column_index：表头列名所在行
# by_name：Sheet1名称
def excel_table_by_sheet_name(excel_file='1.xlsx', column_index=0, sheet_name=u'Sheet1'):
    data = open_excel(excel_file)
    table = data.sheet_by_name(sheet_name)
    nrows = table.nrows  # 行数
    colnames = table.row_values(column_index)  # 某一行数据
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


def main():
    tables = excel_table_by_sheet_index()
    for row in tables:
        print row
    tables = excel_table_by_sheet_name()
    for row in tables:
        print row


if __name__ == "__main__":
    # main()
    tables = excel_table_by_sheet_index()
    for row in tables:
        print row
        a = row.values()
        k = row.keys()
        b = a[4]
        print "b=====", b
        print "k=====", k[0].encode('utf-8')
