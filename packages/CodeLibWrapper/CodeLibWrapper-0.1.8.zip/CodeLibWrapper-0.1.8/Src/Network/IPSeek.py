# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
import json


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    ip = '61.158.147.194'
    url = 'http://ip.taobao.com/service/getIpInfo.php?'  # 定义接口地址
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    headers = {'User-agent': 'Mozilla/5.0'}  # ---OK
    url_args = urllib.urlencode({"ip": ip})
    urls = '%s%s' % (url, url_args)
    req = urllib2.Request(url=urls, headers=headers)  # 需要添加一个header，否则会提示403forbidden
    res = urllib2.urlopen(req).read()  # 返回：aabb00

    res_d = json.loads(res)['data']
    # res_d = json.loads(res,strict=False,encoding='utf-8')
    print res_d[u'country'], res_d[u'region'], res_d[u'city'], res_d[u'isp']


if __name__ == '__main__':
    main()
