# -*- coding: utf-8 -*-
import os


def main():
    # 路径分隔符
    print os.path.sep

    # 根目录
    print os.path.altsep

    # 当前目录
    print os.path.curdir

    # 父目录
    print os.path.pardir

    # 绝对路径
    print os.path.abspath(os.path.curdir)

    # 链接路径
    full_path = os.path.join(os.path.abspath(os.path.curdir), "dir", "a.txt")
    print full_path

    # 把path分为目录和文件两个部分，以列表返回
    print os.path.split(full_path)

    print os.path.exists('c:\\')

    print os.path.isabs(full_path)

    print os.path.isfile(full_path)

    print os.path.isdir('c:\\')

    # 取得对象的最后修改时间
    print os.path.getmtime('c:\\')

    # 取得对象的创建时间
    print os.path.getctime('c:\\')


if __name__ == '__main__':
    # main()

    f = []
    for (dirpath, dirnames, filenames) in os.walk('C:\\'):
        f.extend(dirnames)
        break

    print(f)
