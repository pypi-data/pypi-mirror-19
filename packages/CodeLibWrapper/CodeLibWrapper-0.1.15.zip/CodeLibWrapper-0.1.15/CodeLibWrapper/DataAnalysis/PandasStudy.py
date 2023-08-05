# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def generate_data ():
    raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
                'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
                'age': [42, 52, 36, 24, 73],
                'preTestScore': [4, 24, 31, ".", "."],
                'postTestScore': ["25,000", "94,000", 57, 62, 70]}
    df = pd.DataFrame (raw_data, columns=['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
    print df
    return df


def save_data_into_csv (df, csv_path):
    df.to_csv (csv_path)


def load_data_from_csv (csv_path):
    df = pd.read_csv (csv_path)
    return df


def main ():
    df1 = pd.read_csv ("http://pythonhow.com/wp-content/uploads/2016/01/Income_data.csv")
    df2 = df1.set_index ("State")

    #  extract a subset of the dataframe. the general syntax rule is df2.loc[startrow:endrow,startcolumn:endcolumn]
    df3 = df2.loc["Alaska":"Arkansas", "2005":"2007"]
    print df3

    # how to slice a column
    df4 = df2.loc[:, "2005"]
    print df4

    # To extract only a row
    df5 = df2.loc["California", :]
    print df5

    # To extract single cell value
    df6 = df2.loc["California", "2013"]
    print df6


if __name__ == '__main__':
    main ()
