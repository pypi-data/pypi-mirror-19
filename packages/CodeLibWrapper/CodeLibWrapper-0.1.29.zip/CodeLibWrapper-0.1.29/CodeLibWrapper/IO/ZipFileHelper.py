# -*- coding: utf-8 -*-
import os.path
import os
from zipfile import *
import zipfile
import StringIO


class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)

    def addfile(self, path, arcname=None):
        path = path.replace('//', '/')
        if not arcname:
            if path.startswith(self.basedir):
                arcname = path[len(self.basedir):]
            else:
                arcname = ''
        self.zfile.write(path, arcname)

    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)

    def close(self):
        self.zfile.close()

    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dirinfo = os.path.dirname(f)
            if not os.path.exists(dirinfo):
                os.makedirs(dirinfo)
            file(f, 'wb').write(self.zfile.read(filename))


class InMemoryZip(object):
    """
    python使用内存zipfile对象在内存中打包文件
    """

    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = StringIO.StringIO()

    def append(self, filename_in_zip, file_contents):
        """
        Appends a file with name filename_in_zip and contents of file_contents to the in-memory zip.
        :param filename_in_zip:
        :param file_contents:
        :return:
        """
        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        """Returns a string with the contents of the in-memory zip."""
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def writetofile(self, filename):
        """Writes the in-memory zip to a file."""
        f = file(filename, "w")
        f.write(self.read())
        f.close()


def create(zfile, files):
    z = ZFile(zfile, 'w')
    z.addfiles(files)
    z.close()


def extract(zfile, path):
    z = ZFile(zfile)
    z.extract_to(path)
    z.close()


def unzip(source_zip, target_dir):
    """
    解压zip文件
    :param source_zip:
    :param target_dir:
    :return:
    """
    myzip = ZipFile(source_zip)
    myfilelist = myzip.namelist()
    for name in myfilelist:
        f_handle = open(target_dir + name, "wb")
        f_handle.write(myzip.read(name))
        f_handle.close()
    myzip.close()


def addzip(originzipfile, addfilepath):
    """
    添加文件到已有的zip包中
    :param originzipfile:
    :param addfilepath:
    :return:
    """
    f = zipfile.ZipFile(originzipfile, 'w', zipfile.ZIP_DEFLATED)
    f.write(addfilepath)
    f.close()


def adddirfile(zipfilepath, startdir):
    """
    把整个文件夹内的文件打包
    :param zipfilepath:
    :param startdir:
    :return:
    """
    f = zipfile.ZipFile(zipfilepath, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()
