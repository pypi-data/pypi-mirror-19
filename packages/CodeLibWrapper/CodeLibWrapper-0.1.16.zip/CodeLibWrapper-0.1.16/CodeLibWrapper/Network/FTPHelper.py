# -*- coding: utf-8 -*-
# http://www.pythonforbeginners.com/code-snippets-source-code/how-to-use-ftp-in-python

import ftplib
ftp = ftplib.FTP('ftp.sunet.se', 'anonymous', 'anonymous@sunet.se')
print "File List: "
files = ftp.dir()
print files
