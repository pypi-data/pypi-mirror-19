# -*- coding: utf-8 -*-


def main():
    """
    Print all chinese char in Python
    :return:
    """
    n = 0
    for ch in xrange(0x4e00, 0x9fa6):
        print unichr(ch),
        n = n + 1
        if (n % 50 == 0):
            print '\n'

    print n


if __name__ == '__main__':
    main()
