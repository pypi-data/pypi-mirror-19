# -*- coding: utf-8 -*-
import os
from xml.etree import ElementTree


class EnvironmentConfig:
    _config_file_path = ""

    def __init__(self, config_file_path):
        """
        不同环境下自定义变量的读取器
        :param config_file_path: xml的定义文件
        """
        self._config_file_path = config_file_path
        if not os.path.exists(self._config_file_path):
            raise IOError("The file isn't exist.")
        pass

    def read_environment_parameter_from_config(self, environment_name, parameter_name):
        """
        读取变量定义XML 文件中对应环境配置下的指定参数名
        :param environment_name: 环境名
        :param parameter_name: 自定义参数名
        :return:
        """
        root = ElementTree.parse(self._config_file_path)
        # root = ElementTree.fromstring(text)
        for elem in root.findall('Environment'):
            # How to make decisions based on attributes even in 2.6:
            if elem.attrib.get('Name') == environment_name:
                for parameter in elem.getchildren():
                    if parameter.attrib["Name"] == parameter_name:
                        return parameter.text
                        break
                raise Exception("The " + parameter_name + " is not exist in config file.")
        pass
