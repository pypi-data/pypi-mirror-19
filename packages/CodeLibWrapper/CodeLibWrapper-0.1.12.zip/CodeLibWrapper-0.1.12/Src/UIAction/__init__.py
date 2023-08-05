# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import sys
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

Tag_A_Filter_Condition="entrylistItemTitle"
# Tag_A_Filter_Condition = "data-searchsession"


class hp(HTMLParser):
    def __init__(self):
        self.readingdata_a = False
        self.title = []
        self.usite = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        # print tag
        if tag == 'a':
            for h, v in attrs:
                if v == Tag_A_Filter_Condition:  # 选择标准为：Class 样式为entrylistItemTitle
                    self.readingdata_a = True
                    link = dict(attrs)["href"]
                    self.usite.append(link)

    def handle_data(self, data):
        if self.readingdata_a:
            self.title.append(data)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.readingdata_a = False

    def getdata(self):
        # return zip(self.title,self.usite) 通过zip函数将其一对一合并为tuple

        i = 0
        listr = []
        while i < len(self.title):
            listr.append(self.title[i] + ' : ' + self.usite[i])
            i = i + 1
        return listr


# 输出特定页面中具有特定样式的A标记的内文和链接
url = 'http://www.cnblogs.com/dreamer-fish/archive/2016/09.html'
# url = "http://stackoverflow.com/search?q=robot+framework"
request = urllib2.Request(url)
response = urllib2.urlopen(request).read()

yk = hp()
yk.feed(response)
dd = yk.getdata()

for i in dd:
    print i

yk.close
