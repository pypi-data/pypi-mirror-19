# -*- coding: utf-8 -*-
import numpy
import math


#
# lst = [1, 4, 2, 5, 2, 2.5]
# print numpy.array(lst).std()
#
# A_rank = [0.8, 0.4, 1.2, 3.7, 2.6, 5.8]
# print numpy.array(A_rank).std()
#


class MathUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_standard_deviation(qlist):
        """
        计算Double类型数组的标准差
        :param qlist:
        :return: 标准差值
        """
        avg = float(sum(qlist)) / len(qlist)
        # print(avg)
        dev = []
        for x in qlist:
            dev.append(x - avg)
        # print(dev)
        sqr = []
        for x in dev:
            sqr.append(x * x)
        # print(sqr)
        # mean = sum(sqr) / len(sqr)
        # print(mean)

        return math.sqrt(sum(sqr) / (len(sqr) - 1))


if __name__ == '__main__':
    lst = [1, 4, 2, 5, 2, 2.5]
    standard_dev = MathUtils().get_standard_deviation(lst)
    print("the standard deviation of set %s is %f" % (lst, standard_dev))
