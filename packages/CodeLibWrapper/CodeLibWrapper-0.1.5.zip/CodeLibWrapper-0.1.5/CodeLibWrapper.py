# -*- coding: utf-8 -*-

# region   Import Library

import os
import sys
from Src.API.APIReader import APIReader
from Src.Database.SQLServerHelper import SQLServerHelper

from Src.Network.EmailUtils import EmailUtils
from Src.TextTools.RandomUtils import RandomUtils
from Src.IO.SimpleFileCompare import file_compare, dir_compare

from Src.XMLFunction.XmlUtils import parse_xml_from_string, parse_xpath_from_xml
from Src.XMLFunction.EnvironmentConfig import EnvironmentConfig
from Src.XMLFunction.ConvertXML2Obj import parse_xml_to_object, sort_list_by_name, sort_list_by_cdata, sort_list_by_attr
from Src.XMLFunction.XMLSortHelper import sort_xml_content, sort_xml_file
from Src.XMLFunction.xmlvalidatehelper import Validate_XSD

from Src.DataAnalysis.Pandas_DataCompare import mysql_table_compare


# endregion


class CodeLibWrapper:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    Author = "Benjamin Zhou"
    Version = "0.1.5"

    def __init__ (self):
        reload (sys)
        sys.setdefaultencoding ('utf8')
        pass

    # region    框架信息
    @staticmethod
    def show_about_information ():
        """
        显示“关于信息”和“版本信息”
        :return: 返回作者和最后编辑的日期
        """

        # TODO: [Global] Add version information for every module in this project.
        basic_version = "Author: %s, Version: %s\nPython version: %s" % (
            CodeLibWrapper.Author, CodeLibWrapper.Version, sys.version)
        module_api_version = "    API Modules\n" + "        APIReader Version: %s" % APIReader.VERSION
        output = """
    \n*************************************************************
    Generation Information\n
    %s
    \n*************************************************************
    Modules Version:\n
    %s
    """
        return output % (basic_version, module_api_version)

    @staticmethod
    def send_email_to_admin (from_address, email_body):
        """
        给这个框架的管理员发邮件，非常期待你的回馈
        :param from_address: 您的邮件地址，例如：Benjamin.zhou@morningstar.com
        :param email_body: 回馈内容.例如：Bug 报告，功能需求
        :return: 邮件发送成功标志
        """
        admin_address = ["Benjamin.Zhou@morningstar.com"]
        return EmailUtils.send_plainmail (admin_address, from_address, "Robot Framework Feedback", email_body)

    # endregion

    # region    文件系统

    @staticmethod
    def iofilesysgetcurrentpath ():
        """
        返回当前路径

        :return: path string
        """
        return os.getcwd ()

    @staticmethod
    def iofilesysremovefile (filepath):
        """
        删除指定路径的文件

        :param filepath: 要删除文件的路径

        :return: 是否删除成功标志
        """
        try:
            os.remove (filepath)
            return True
        except IOError, e:
            print e
            return False

    @staticmethod
    def iofilesysgetfilelist (dirpath):
        """
        获取某指定目录下的所有文件的列表
        :param dirpath: 指定的目录
        :return:
        """
        dirpath = str (dirpath)
        if dirpath == "":
            return []
        dirpath = dirpath.replace ("/", "\\")
        if dirpath[-1] != "\\":
            dirpath = dirpath + "\\"
        a = os.listdir (dirpath)
        b = [x for x in a if os.path.isfile (dirpath + x)]
        return b

    @staticmethod
    def iofilesysmakedir (dirpath):
        """
        创建指定目录
        :param dirpath:目录路径
        :return:
        """
        try:
            os.makedirs (dirpath)
            return True
        except IOError, e:
            print e
            return False

    # endregion

    # region 配置文件读取

    @staticmethod
    def config_get_parameter_value_by_name_and_environment (config_file_path, environment_name, parameter_name):
        """
        多环境参数配置读取。

        :param config_file_path: 参数配置文件的路径。在Windows环境下运行的RobotFramework中，需要用\\标识文件夹的分隔。例如：D:\\PythonCode\\CodeLib\\Template\\Sample_EnvironmentConfig.xml
        :param environment_name:要选取的环境变量名称
        :param parameter_name:要选取的参数名称
        :return: 返回参数值（string）
        """
        return EnvironmentConfig (config_file_path).read_environment_parameter_from_config (environment_name,
                                                                                            parameter_name)

    # endregion

    # region WebService/API访问
    @staticmethod
    def api_readwebservice_exoi (username, password, url):
        """
        访问EquityXOI(EXOI)
        :param username: 账号
        :param password: 密码
        :param url: EXOI的URL
        :return:
        """
        result = APIReader ().access_exoi_api (url, username, password)
        return result

    @staticmethod
    def api_readwebservice_gid (url, encrypt_email, encrypt_password):
        result = APIReader ().access_gid_api (url, encrypt_email, encrypt_password)
        return result

    @staticmethod
    def api_build_gid_url (input_string, output):
        """
        组装访问GID的URL
        :param input_string:
        :param output:
        :return:
        """
        result = APIReader ().build_gid_url (output_dps=output, input_query_string=input_string)
        return result

    @staticmethod
    def api_readwebservice_fundxoi (url, account, password):
        """
        访问Fund_XOI API Service, 并取得返回值
        :param url: Fund XOI的URL
        :param account: FundXOI 的账号
        :param password: FundXOI的密码
        :return:
        """
        result = APIReader ().access_fund_xoi (url, account=account, password=password)
        return result

    # endregion

    # region 数据库操作
    @staticmethod
    def database_sql_server_execute_script_no_return (server, user, password, database_name, scripts):
        return SQLServerHelper (server, user, password).execute_sql_script_with_no_return (database_name, scripts)

    @staticmethod
    def database_sql_server_execute_sql_query_return_one_record(server, user, password, database_name, scripts):
        return SQLServerHelper (server, user, password).execute_sql_query_return_one_record (database_name, scripts)

    @staticmethod
    def database_sql_server_execute_sql_query_return_many_record(server, user, password, database_name, scripts):
        return SQLServerHelper (server, user, password).execute_sql_query_return_many_record (database_name, scripts)

    @staticmethod
    def Assert_Compare_MySQL_Table (source_server, source_user, source_password, source_db, target_server, target_user,
                                    target_password, target_db, table_charset, sql_script, quick_assert, output_result):
        return mysql_table_compare (source_server, source_user, source_password, source_db, target_server, target_user,
                                    target_password, target_db, table_charset, sql_script, quick_assert, output_result)

    # endregion

    # region Utils
    @staticmethod
    def utils_generate_random_string (length):
        """
        生成随机字符串
        :param length: 要生成的随机字符串长度
        :return:
        """
        return RandomUtils.genrandomstring (length)

    @staticmethod
    def send_plain_email (from_address, subject, content, to_address_list):
        result = EmailUtils.send_plainmail (to_address_list, from_address, subject, content)
        return result

    # endregion

    # region 断言方法
    @staticmethod
    def assert_dir_compare (source_dir_path, target_dir_path, output_report_path):
        dir_compare (source_dir_path, target_dir_path, output_report_path)

    @staticmethod
    def assert_file_compare (source_file_path, target_file_path):
        return file_compare (source_file_path, target_file_path)

    # endregion

    # region    XML

    @staticmethod
    def xml_output_xpath_by_xml (xml_file_path):
        return parse_xpath_from_xml (xml_file_path)

    @staticmethod
    def xml_parse_xml_from_string (xml_content):
        return parse_xml_from_string (xml_content)

    @staticmethod
    def xml_convert_xml_to_object (xml_file_path):
        return parse_xml_to_object (xml_file_path)

    @staticmethod
    def xml_sort_xml_file (origin_input_xml_file, sorted_output_xml_file):
        sort_xml_file (origin_input_xml_file, sorted_output_xml_file)

    @staticmethod
    def xml_sort_xml_content (origin_input_xml_content):
        return sort_xml_content (origin_input_xml_content)

    @staticmethod
    def xml_schema_validate (xml_file_path, xsd_file_path):
        return Validate_XSD (xml_file_path, xsd_file_path)

    # endregion

    # region    Collection
    @staticmethod
    def collection_sort_list_by_name (m_list, reverse=False):
        return sort_list_by_name (m_list, reverse)

    @staticmethod
    def collection_sort_list_by_cdata (m_list, reverse=False):
        return sort_list_by_cdata (m_list, reverse)

    @staticmethod
    def collection_sort_list_by_attr (m_list, reverse=False):
        return sort_list_by_attr (m_list, reverse)

    # endregion


def main ():
    print "something."


if __name__ == '__main__':
    main ()
