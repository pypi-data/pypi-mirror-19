# -*- coding: utf-8 -*-
from robot.parsing.model import TestData


def get_test_suite_name(test_case_file_path):
    """
    取得Test Suite定义文件中TestSuite的名字
    :param test_case_file_path: Test Case 定义文件（*.txt或 *.robot）的路径, 例如：
    r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SimpleUsageTutorials\BasicBuiltInLibrarySample_BuiltInKeyword.txt"
    :return:
    """
    test_suite = TestData(parent=None,
                          source=test_case_file_path)
    return test_suite.name


def get_test_case_name(test_case_file_path):
    """
    返回特定TestSuite下包含的Test Case的名字清单
    :param test_case_file_path: Test Case 定义文件（*.txt或 *.robot）的路径, 例如：
     r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SimpleUsageTutorials\BasicBuiltInLibrarySample_BuiltInKeyword.txt"
    :return:
    """
    test_suite = TestData(parent=None,
                          source=test_case_file_path)

    case_name = []
    for case in test_suite.testcase_table:
        # print(case.name)
        case_name.append(case.name)
    return case_name


def get_tags(path):
    suite = TestData(parent=None, source=path)
    tags = __get_tags(suite)
    print ", ".join(sorted(set(tags)))


def __get_tags(suite):

    tags = []

    if suite.setting_table.force_tags:
        tags.extend(suite.setting_table.force_tags.value)

    if suite.setting_table.default_tags:
        tags.extend(suite.setting_table.default_tags.value)

    for test_case in suite.testcase_table.tests:
        if test_case.tags:
            tags.extend(test_case.tags.value)

    for child_suite in suite.children:
        tags.extend(__get_tags(child_suite))

    return tags


def print_suite(suite):
    print 'Suite:', suite.name
    for test in suite.testcase_table:
        print '-', test.name
    for child in suite.children:
        print_suite(child)


def main():
    source = r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SimpleUsageTutorials\BasicBuiltInLibrarySample_BuiltInKeyword.txt"
    for test_case in get_test_case_name(source):
        print(test_case)

    get_tags(source)


#
# @keyword('Resource Locator')
# def resource_locator():
#     name = EXECUTION_CONTEXTS.current.keywords[-1].name
#     libname = EXECUTION_CONTEXTS.current.get_handler(name).libname
#     resources = EXECUTION_CONTEXTS.current.namespace._kw_store.resources
#     path = ""
#     for key in resources._keys:
#         if resources[key].name == libname:
#             path = key
#             break
#     return {'name': name, 'path': path}



if __name__ == "__main__":
    main()
