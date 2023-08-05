# -*- coding: utf-8 -*-
import pandas as pd


def main():
    df = pd.read_csv(
        "C:\\Python27\\Lib\\site-packages\\CodeLibWrapper\\RobotFrameworkSample\\SampleData\\pandas_csv.csv",
        encoding='gbk', )
    # print df

    print df[u"商品编号"][1]

    rawtext = u'\u5e8f\u53f7'
    print rawtext


    # print len(df.index)
    # print len(df.columns)
    # print df.shape[0]
    # print df.shape[1]

    #
    # df2 = pd.DataFrame({'A': [15, 56, 23, 84], 'B': [10, 20, 33, 25]})
    # print df2
    #
    # print df2.loc[df2['A'] == 23, 'B'].values[0]
    #
    # x = df2[df2['A'] == 23]
    # print x


if __name__ == '__main__':
    main()