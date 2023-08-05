# -*- coding: utf-8 -*-
import time
import os
import sys


class CompareUtils:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        pass

    @staticmethod
    def getprettytime(state):
        return time.strftime('%y-%m-%d %H:%M:%S', time.localtime(state.st_mtime))

    @staticmethod
    def comparedir(sourcepath, targetpath):
        A_files = []
        B_files = []
        for root, dirs, files in os.walk(sourcepath):
            for fileitem in files:
                A_files.append(root + "\\" + fileitem.decode('gbk'))
        for root, dirs, files in os.walk(targetpath):
            for fileitem in files:
                B_files.append(root + "\\" + fileitem.decode('gbk'))
        a_files = []
        b_files = []
        a_path_len = len(sourcepath)
        b_path_len = len(targetpath)
        for file in A_files:
            a_files.append(file[a_path_len:])
        for file in B_files:
            b_files.append(file[b_path_len:])
        setA = set(a_files)
        setB = set(b_files)
        commonfiles = setA & setB
        print "#================================="
        print "common in '", sourcepath, "' and '", targetpath, "'"
        print "#================================="
        print '\t\t\ta:\t\t\t\t\t\tb:'
        for f in sorted(commonfiles):
            print f + "\t\t" + CompareUtils.getprettytime(
                os.stat(sourcepath + "\\" + f)) + "\t\t" + CompareUtils.getprettytime(
                os.stat(targetpath + "\\" + f))
        onlyA = setA - setB
        print "#================================="
        print "only in A '", sourcepath
        print "#================================="
        print '\t\t\ta:\t\t\t\t\t\t\t\t\tb:'
        for f in sorted(onlyA):
            print f + "\t\t" + CompareUtils.getprettytime(os.stat(sourcepath + "\\" + f))
        onlyB = setB - setA
        print "#================================="
        print "only in B'", targetpath
        print "#================================="
        print '\t\t\ta:\t\t\t\t\t\tb:'
        for f in sorted(onlyB):
            print f + "\t\t" + CompareUtils.getprettytime(os.stat(targetpath + "\\" + f))
