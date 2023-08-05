# -*- coding: utf-8 -*-

# 更多setuptools信息，请参见http://www.360doc.com/content/14/0306/11/13084517_358166737.shtml
# from os.path import abspath, dirname
from CodeLibWrapper import CodeLibWrapper
from setuptools import setup,find_packages

# CURDIR = dirname (abspath (__file__))
with open ('requirements.txt') as f:
    required = f.read ().splitlines ()

setup (
    name="CodeLibWrapper",  # pip安装时的Package对外名称
    version=CodeLibWrapper.CodeLibWrapper.Version,  # 版本

    # trying to add files...
    # package_dir={'': 'CodeLibWrapper'},
    include_package_data=True,
    packages=find_packages(),
    package_data={
        'UserKeywords': ['*.txt'],
        'Template': ['Sample_EnvironmentConfig.xml'],
        'RobotFrameworkSample': ['SampleData/*.*','SimpleUsageTutorials/*.*','UserKeywordTestSuite/*.*'],
    },
    data_files=['CodeLibWrapper.py','README.txt','License.txt','Upgrade.bat','Uninstall.bat','requirements.txt'],
    author=CodeLibWrapper.CodeLibWrapper.Author,  # 作者
    author_email="Benjamin.Zhou@morningstar.com",  # 作者联系方式
    license='All Data Production/API QA team member use.',  # License
    long_description=open ('README.txt').read (),  # Readme File
    platforms="Python & Robot framework",
    url="https://pypi.python.org/pypi/CodeLibWrapper",
    maintainer="Benjamin Zhou",
    maintainer_email="Benjamin.Zhou@morningstar.com",
    keywords="Data Production, API, Robot Framework",
    description="Robot Framework util package for MorningStar DataProduct/API team.",
    install_requires=required

)
