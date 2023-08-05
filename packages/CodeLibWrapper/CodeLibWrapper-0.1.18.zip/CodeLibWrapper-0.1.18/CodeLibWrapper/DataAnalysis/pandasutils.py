# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pymysql
from pandas.util.testing import assert_frame_equal
import sys


def diff_pd(df1, df2):
    """Identify differences between two pandas DataFrames"""
    assert (df1.columns == df2.columns).all(), "DataFrame column names are different"
    if df1.equals(df2):
        return None
    else:
        # need to account for np.nan != np.nan returning True
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        changed.index.names = ['id', 'col']
        difference_locations = np.where(diff_mask)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        return pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)


def generate_leftdataframe():
    mysql_con = pymysql.connect(host='geapidbdev81', port=3306, user='GeDataAgent', passwd='1234567#', charset="utf8",
                                db='GEAPIMGT')
    # read
    df = pd.read_sql("select * From User", con=mysql_con, index_col="UserId")
    mysql_con.close()
    df = df.reset_index(drop=False)
    return df


def generate_rightdataframe():
    mysql_con2 = pymysql.connect(host='geapidb61', port=3306, user='AgentUser', passwd='wow!2010', charset="utf8",
                                 db='GEAPIMGT')
    # read
    df2 = pd.read_sql("select * From User", con=mysql_con2, index_col='UserId')
    mysql_con2.close()
    df2 = df2.reset_index(drop=False, inplace=False)
    return df2


def choosecolumnsfromdataframe():
    df = generate_leftdataframe()
    newdf = pd.DataFrame(df, columns=['UserId', 'id', 'LoginEmail'])
    newdf.to_csv("d:\\test1.csv", sep='\t')
    print newdf


def showdataframeproperty():
    df = generate_leftdataframe()
    print df.info()
    # data type of columns
    print df.dtypes
    # show indexes
    print df.index
    # show the first N records in data frame
    print df.head(10)
    # show the last N records in data frame
    print df.tail(10)
    # return pandas.Index
    print df.columns
    # each row, return array[array]
    print df.values
    # show Row number and column number
    print ("data frame row count():" + str(len(df.index)))
    print ("Data Frame row count is " + str(df.shape[0]))
    print ("Data Frame column count is " + str(df.shape[1]))
    print (df.dtypes[0])


def compare_dataframe1():
    df = generate_leftdataframe()
    df2 = generate_rightdataframe()
    try:
        assert_frame_equal(df[0:10], df2[0:10])
        return True
    except AssertionError:
        return False


def diff_pd_demo1():
    if sys.version_info[0] < 3:
        from StringIO import StringIO
    else:
        from io import StringIO

    dfsource = StringIO("""id   Name   score                    isEnrolled           Comment
    111  Jack   2.17                     True                 "He was late to class"
    112  Nick   1.11                     False                "Graduated"
    113  Zoe    NaN                     True                  " "
    """)
    dftarget = StringIO("""id   Name   score                    isEnrolled           Comment
    111  Jack   2.17                     True                 "He was late to class"
    112  Nick   1.21                     False                "Graduated"
    113  Zoe    NaN                     False                "On vacation" """)
    df1 = pd.read_table(dfsource, sep='\s+', index_col='id')
    df2 = pd.read_table(dftarget, sep='\s+', index_col='id')
    print diff_pd(df1, df2)


def diff_pd_demo2():
    """
    目前这个Demo还有问题：Can only compare identically-labeled DataFrame objects， 还没找到答案Benjamin,20161010
    :return:
    """
    df1 = generate_leftdataframe()
    df2 = generate_rightdataframe()

    assert_frame_equal(df1, df2)

    # df = __diff_pd(df1, df2)
    # print df1
    # print df2
    # df.to_csv("d:\\result.csv", sep='\t')


def demo2():
    b = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                      'B': ['B4', 'B5', 'B6', 'B7'],
                      'C': ['C4', 'C5', 'C6', 'C7'],
                      'D': ['D4', 'D5', 'D6', 'D7']},
                     index=[4, 5, 6, 7])

    c = pd.DataFrame({'A': ['A7', 'A8', 'A9', 'A10', 'A11'],
                      'A': ['A7', 'A8', 'A9', 'A10', 'A11'],
                      'B': ['B7', 'B8', 'B9', 'B10', 'B11'],
                      'C': ['C7', 'C8', 'C9', 'C10', 'C11'],
                      'D': ['D7', 'D8', 'D9', 'D10', 'D11']},
                     index=[7, 8, 9, 10, 11])

    result = pd.concat([b, c])
    idx = np.unique(result["A"], return_index=True)[1]
    result.iloc[idx].sort()
    print result


def demo3():
    df1 = generate_rightdataframe()
    df2 = generate_leftdataframe()
    idx1 = pd.Index(df1)
    idx2 = pd.Index(df2)
    print idx1.difference(idx2)


def diff_pd_demo3():
    df1 = pd.DataFrame({'$a': [1, 2, 3], '$b': [10, 20, 15]})
    df1.columns = ['Id', 'Value']
    df2 = pd.DataFrame({'$a': [1, 2, 4], '$b': [10, 15, 20]})
    df2.columns = ['Id', 'Value']
    df = diff_pd(df1, df2)
    print df1
    print df2
    print df


if __name__ == "__main__":
    diff_pd_demo2()
