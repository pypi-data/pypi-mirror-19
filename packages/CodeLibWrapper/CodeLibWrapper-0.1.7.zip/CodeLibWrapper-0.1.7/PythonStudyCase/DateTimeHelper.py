# -*- coding: utf-8 -*-
import datetime
import calendar
import time


def main():
    print "Datetime demo sample."
    # get today
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    print (yesterday, today, tomorrow)

    # get last Friday
    today = datetime.date.today()
    target_day = calendar.FRIDAY
    this_day = today.weekday()
    delta_to_target = (this_day - target_day) % 7
    last_friday = today - datetime.timedelta(days=delta_to_target)

    print(last_friday.strftime("%d-%b-%Y"))

    start = time.clock()
    time.sleep(2)
    end = time.clock()
    print u"用时:%f s" % (end - start)

    print "Start : %s" % time.ctime()
    time.sleep(5)
    print "End : %s" % time.ctime()

    time.sleep(0.1)  # Sleep 0.1 second

    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 暂停一秒
    time.sleep(1)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

if __name__ == '__main__':
    main()
