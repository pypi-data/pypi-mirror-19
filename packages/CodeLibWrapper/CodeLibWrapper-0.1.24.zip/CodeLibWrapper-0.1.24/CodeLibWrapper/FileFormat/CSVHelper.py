# -*- coding: utf-8 -*-

#  本模块中的函数还没有测试 Benjamin 2016/12/08
import sys
import json
import csv


def convert2json():
    separator = ","
    try:
        separator = str(sys.argv[4])
    except:
        pass

    try:
        datamodelfile = csv.reader(open(sys.argv[1], "rU"), delimiter=separator, dialect="excel")
        datafile = open(sys.argv[2], "rU")
        outfile = open(sys.argv[3], 'a')
    except:
        print "The parameters for this script are: csv_data_model_file csv_input_data_file output_file separator"

    datamodel = []
    for row in datamodelfile:
        datamodel = row

    data = csv.reader(datafile, delimiter=separator)

    for row in data:
        if len(row) == len(datamodel):
            dic = {}
            for i in range(len(datamodel)):
                dic[datamodel[i]] = row[i]
            json.dump(dic, outfile, sort_keys=True)
            outfile.write('\n')
        else:
            print "Datamodel does not correspond with the data"


def convert2json_help():
    help_text = """
    A python script to transform csv files to json files
Python version: 2.*
To read help, pass the argument help:
python CSVHelper.py help
The arguments for using this script are:
python CSVHelper.py csv_data_model_file csv_data_input_file json_output_file separator
All arguments are required, apart from the separator.
Data model (i.e. column names) and data itself, both in cdv format, are separated into two different files so that you can treat several files of data sharing the same data model (for instance, data files from multiple years).
The separator should be provided in the form of a string, like "," or ';'. It's the character used to separate columns in the csv input file. If a specific separator is not passed to the script, it will assume that it's a regular comma(',').
    """
    print help_text


def read_csv_file(self, filename):
    '''This creates a keyword named "Read CSV File"

    This keyword takes one argument, which is a path to a .csv file. It
    returns a list of rows, with each row being a list of the data in
    each column.

    Example test:

This test will use the csvLibrary to open up a .csv file, read it, and return the result as a list of lists:

*** Settings ***
| Library | CSVHelper.py

*** Test cases ***
| Reading a csv file
| | ${data}= | read csv file | test.csv
| | log | ${data[0][0]}



    '''
    data = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data


def main():
    if sys.argv[1] == 'help':
        convert2json_help()
    else:
        convert2json()


if __name__ == '__main__':
    main()
