# -*- coding: utf-8 -*-

import urllib2
import requests
from requests.auth import HTTPBasicAuth
from StringIO import StringIO
import gzip
import json
from bs4 import BeautifulSoup


# 关于Requests 库更多信息，请参见http://docs.python-requests.org/zh_CN/latest/user/quickstart.html


class APIReaderResult:
    """
    API Reader 类的结果返回呈现类
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = "0.1.1"

    def __init__ (self, request):
        self.url = request.url
        self.status_code = request.status_code
        self.content = request.content
        self.text = request.text
        self.encoding = request.encoding
        self.r = request

    def displayurl (self):
        """
        返回Request对象的URL 地址
        :return: String
        """
        url = getattr (self, "url")
        print url
        return url

    def displaystatuscode (self):
        """
        返回Request对象的HTTP返回码
        :return: HTTP Code(int)
        """
        return self.status_code

    def displaycontent (self):
        """
        返回Request对象的Response结果的内容
        :return: String
        """
        return str (self.content)

    def convert2json (self):
        """
        将API 返回对象转换为Json对象
        :return: Json 对象
        """
        try:
            return self.r.json ()
        except Exception, e:
            print "There is an error occured on JSON convertion. Details information is:" + e.message


class APIReader:
    """
    API Reader
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    VERSION = "0.0.1"

    def __init__ (self):
        pass

    @staticmethod
    def access_xoi (url, account, password):
        """
        访问XOI web service
        :param url: 你要访问的XOI URL 字符串
        :param account: 访问XOI的账号
        :param password: 访问XOI的密码
        :return: 此方法返回的是一个APIReaderResult对象。
        使用者可以通过displayurl，displaycontent和displaystatuscode方法取得相应的返回值
        """
        s = requests.session ()
        s.get ("http://xoi.morningstar.com/XOISuite/Login.aspx", auth=HTTPBasicAuth (account, password))
        try:
            r = s.get (url)
        except requests.exceptions.ConnectTimeout:
            network_status = False
        except requests.exceptions.Timeout:
            request_timeout = True
        finally:
            s.close ()

        return APIReaderResult (r)

    @staticmethod
    def access_price_xoi (url, account, password):
        """
             访问Price XOI web service
             :param url: 你要访问的Price XOI URL 字符串
             :param account: 访问Price XOI的账号
             :param password: 访问Price XOI的密码
             :return: 此方法返回的是一个APIReaderResult对象。
             使用者可以通过displayurl，displaycontent和displaystatuscode方法取得相应的返回值
             """
        s = requests.session ()
        s.get ("http://price.xoi.morningstar.com/DataPlatform/Login.aspx", auth=HTTPBasicAuth (account, password))
        try:
            r = s.get (url)
        except requests.exceptions.ConnectTimeout:
            network_status = False
        except requests.exceptions.Timeout:
            request_timeout = True
        finally:
            s.close ()

        return APIReaderResult (r)

    @staticmethod
    def access_fund_xoi (url, account, password):
        """
                     访问Price XOI web service
                     :param url: 你要访问的Price XOI URL 字符串
                     :param account: 访问Price XOI的账号
                     :param password: 访问Price XOI的密码
                     :return: 此方法返回的是一个APIReaderResult对象。
                     使用者可以通过displayurl，displaycontent和displaystatuscode方法取得相应的返回值
                     """
        s = requests.session ()
        s.get ("http://funddata.xoi.morningstar.com/XOISuite/Login.aspx", auth=HTTPBasicAuth (account, password))
        try:
            r = s.get (url)
        except requests.exceptions.ConnectTimeout:
            network_status = False
        except requests.exceptions.Timeout:
            request_timeout = True
        finally:
            s.close ()

        return APIReaderResult (r)

    @staticmethod
    def access_exoi_api (url, account, password):
        s = requests.session ()
        s.get ("http://equitydata.morningstar.com/login/login.aspx?username=" + account + "&password=" + password)
        try:
            r = s.get (url)
        except requests.exceptions.ConnectTimeout:
            network_status = False
        except requests.exceptions.Timeout:
            request_timeout = True
        finally:
            s.close ()

        return r

    @staticmethod
    def access_gid_api (url, account, password):
        s = requests.session ()
        login_url = "http://globalid.morningstar.com/GIDDataIO/reg/Login.aspx?action=autologin&email=" + account + "&password=" + password
        s.post (login_url)
        try:
            r = s.get (url)
            # r = s.post (url)
        except requests.exceptions.ConnectTimeout:
            network_status = False
        except requests.exceptions.Timeout:
            request_timeout = True
        finally:
            s.close ()

        return r

    @staticmethod
    def build_gid_url (output_dps, input_query_string):
        gid_url = "http://globalid.morningstar.com/GIDDataIO/feed/asmx/Axis.asmx/GetYAxisDataTable?outputDPs="
        gid_url = gid_url + output_dps + "&inputQueryString=" + input_query_string
        return gid_url

    @staticmethod
    def access_commonapi_by_get (url):
        """
        访问非校验的API Web service
        :param url: API URL 地址
        :return:此方法返回的是一个APIReaderResult对象。
        使用者可以通过displayurl，displaycontent和displaystatuscode方法取得相应的返回值
        """
        s = requests.session ()
        try:
            r = s.get (url)
        except requests.exceptions.ConnectTimeout:
            network_status = False
        except requests.exceptions.Timeout:
            request_timeout = True
        finally:
            s.close ()
        return APIReaderResult (r)

    @staticmethod
    def access_commonapi_by_post (url, payload):
        """
        通过POST方式
        :param url:
        :param payload: POST 提交的数据，例如： payload = {'key1': 'value1', 'key2': 'value2'}
        :return:
        """
        r = requests.post (url, data=payload)
        return r

    @staticmethod
    def access_dataapiv2 (apiurl):
        """
        访问DataAPI V2
        :param apiurl:
        其应该包含两个字段：X-API-ProductId=${productId}，X-API-UserId=${userId}
        例如   dict_head = {'X-API-ProductId': 'Direct', 'X-API-UserId': '42e5613b-49a0-4366-8cf7-480d21997883'}
        :return:
        """
        s = requests.session ()
        dict_head = {'X-API-ProductId': 'Direct', 'X-API-UserId': '42e5613b-49a0-4366-8cf7-480d21997883',
                     'ApiKey': 'zWWogHzs48gKRV09ZUmuKbgQG7Ts89GA'}
        r = s.get (url=apiurl, headers=dict_head)
        s.close ()
        return APIReaderResult (r)

    @staticmethod
    def access_rps_service (url):
        """
        访问RPS API
        :param url: URL 地址
        :return:
        """
        return APIReader.access_commonapi_by_get (url)

    @staticmethod
    def access_ownership (url):
        """
        访问Ownership API
        :param url: ownership API URL
        :return:
        """
        return APIReader.access_commonapi_by_get (url)

    @staticmethod
    def download_file (url, save_path):
        """
        下载文件
        :param url: url 地址
        :param save_path: 要保存的地址
        :return:是否成功下载
        """
        try:
            f = urllib2.urlopen (url)
            with open (save_path, "wb") as code:
                code.write (f.read ())
            return True
        except Exception, e:
            print e.message
            return False

    @staticmethod
    def load_data (url):
        request = urllib2.Request (url)
        request.add_header ('Accept-encoding', 'gzip')
        response = urllib2.urlopen (request)
        if response.info ().get ('Content-Encoding') == 'gzip':
            print 'gzip enabled'
            buf = StringIO (response.read ())
            f = gzip.GzipFile (fileobj=buf)
            data = f.read ()
        else:
            data = response.read ()
        return data

    @staticmethod
    def TimeSeriesReader (url):
        s = requests.session ()
        try:
            file_str = StringIO ()
            r = s.get (url)
            soup = BeautifulSoup (r.content, 'html.parser')
            tables = soup.find_all ('table')
            file_str.write ("<TimeSeriesResult><GeneralInfo>")

            rows2 = tables[1].find_all ('tr', recursive=False)

            TR1_Tds = rows2[0].findAll ('th', recursive=False)
            pair1 = TR1_Tds[0].text.strip ().split ("TSID:")
            Server = pair1[0].replace ("Server:", "")
            TSID = pair1[1]
            file_str.write ("<Server>" + Server + "</Server>")
            file_str.write ("<TSID>" + TSID + "</TSID>")

            TR2_Tds = rows2[1].findAll ('th', recursive=False)
            pair2 = TR2_Tds[0].text.strip ().split ("TSType:")
            ObjectID = pair2[0].replace ("ObjectID:", "")
            TSType = pair2[1]
            file_str.write ("<ObjectID>" + ObjectID + "</ObjectID>")
            file_str.write ("<TSType>" + TSType + "</TSType>")

            TR3_Tds = rows2[2].findAll ('th', recursive=False)
            pair3 = TR3_Tds[0].text.strip ().split ("Calendar:")
            Version = pair3[0].replace ("Ver:", "")
            pair3_1 = pair3[1].split ("Data Type:")
            Calendar = pair3_1[0]
            DataType = pair3_1[1]
            file_str.write ("<Version>" + Version + "</Version>")
            file_str.write ("<Calendar>" + Calendar + "</Calendar>")
            file_str.write ("<DataType>" + DataType + "</DataType>")

            TR4_Tds = rows2[3].findAll ('th', recursive=False)
            pair4 = TR4_Tds[0].text.strip ().split ("End:")
            Start = pair4[0].replace ("Start:", "")
            pair4_1 = pair4[1].split ("LastUpdate:")
            End = pair4_1[0]
            LastUpdate = pair4_1[1]
            file_str.write ("<Start>" + Start + "</Start>")
            file_str.write ("<End>" + End + "</End>")
            file_str.write ("<LastUpdate>" + LastUpdate + "</LastUpdate>")

            file_str.write ("</GeneralInfo>")
            file_str.write ("<TSValueList>")
            rows = tables[2].find_all ('tr', recursive=False)
            for row in rows:
                cols = row.findAll ('td', recursive=False)
                DateTime = cols[0].text.strip ()
                OpenValue = cols[1].text.strip ()
                HighValue = cols[2].text.strip ()
                LowValue = cols[3].text.strip ()
                CloseValue = cols[4].text.strip ()
                # record = (DateTime, OpenValue, HighValue, LowValue, CloseValue)
                # print record
                file_str.write ("<TSValue>")
                file_str.write ("<DateTime>" + DateTime + "</DateTime>")
                file_str.write ("<OpenValue>" + OpenValue + "</OpenValue>")
                file_str.write ("<HighValue>" + HighValue + "</HighValue>")
                file_str.write ("<LowValue>" + LowValue + "</LowValue>")
                file_str.write ("<CloseValue>" + CloseValue + "</CloseValue>")
                file_str.write ("</TSValue>")
            file_str.write ("</TSValueList>")
            file_str.write ("</TimeSeriesResult>")
        except requests.exceptions.ConnectTimeout:
            network_status = False
        except requests.exceptions.Timeout:
            request_timeout = True
        finally:
            s.close ()

        return file_str.getvalue ()

# region    暂时还没有测试 http://bulkan.github.io/robotframework-requests/#Post


def do_requests_post (url=None, data=None, headers={"Content-Type": "application/json"}):
    return requests.post (url, data=data, headers=json.loads (headers))


def do_requests_request (method="GET", url=None, data=None, headers={}):
    return requests.request (url, method=method, data=data, headers=json.loads (headers))


# endregion

def Test_GID ():
    url = APIReader.build_gid_url ("-2,1,2", "I2=0C000006WL")
    # bcee14b095766746177e10857ce6a0a56f3d0e978685c26b218fa295d3bf22de   ==  gdl.process@morningstar.com
    # fc6b8fc6a5b83dc6918f9cf79dfd1514   == Kglibdoc08
    result = APIReader.access_gid_api (url, "bcee14b095766746177e10857ce6a0a56f3d0e978685c26b218fa295d3bf22de",
                                       "fc6b8fc6a5b83dc6918f9cf79dfd1514")
    print result.content


def main ():
    # result =APIReader.access_price_xoi("http://price.xoi.morningstar.com/DataPlatform/DataOutput.aspx?Package=HistoricalData&ContentType=MarketPrice&IdType=PerformanceId&Id=0P000002RH&Dates=2012,2011,2010,2009,2008,2007,2006,2005,2004,2003&SplitAdjusted=1","GlobalEquityData@morningstar.com","GXy1q88E")
    # print result.content

    # result2= APIReader.access_fund_xoi("http://funddata.xoi.morningstar.com/xoisuite/DataOutput.aspx?Package=HistoricalData&Id=CU$OXAGUSD&IdType=CurrencyId&Dates=&Content=ExchangeRate&ContentType=TenforeCurrencyTradingPrice","GlobalEquityData@morningstar.com","GXy1q88E")
    # print result2.content

    result = APIReader.TimeSeriesReader (
        "http://tstool.morningstar.com/interface/NewWindow.aspx?Server=Production&objectid=0P000002RH&tstype=2&table=base")
    print result


if __name__ == '__main__':
    main ()
