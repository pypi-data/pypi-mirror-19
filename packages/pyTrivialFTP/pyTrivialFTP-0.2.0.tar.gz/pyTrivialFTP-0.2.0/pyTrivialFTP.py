# pyTrivialFTP
# The poor man's API for accessing data on a remote FTP repository

# The MIT License (MIT)
#
# Copyright (c) 2014-7 Roberto Reale
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import re
import os
import cmd
import getopt
import sys
from ftplib import FTP, error_perm


class pyTrivialFTP(object, FTP):

    def _log(self, priority, msg):
        # priority is ignored
        print msg

    def login(self):
        if not self.connected:
            FTP.login(self, self.username, self.password)
            self.connected = True
            self.log(20, "Connected to %s." % self.hostname)
            self.cwd(self.wd)
            self.log(20, "Changed working directory to %s." % self.wd)
        else:
            self.log(10, "Already connected.")

    def close(self):
        # logout from the remote site
        if self.connected:
            FTP.close(self)
            self.connected = False
            self.log(20, "Disconnected from %s." % self.hostname)
        else:
            self.log(10, "Already disconnected from %s." % self.hostname)

    def list(self):
        try:
            files = self.nlst()
            self.log(20, "Retrieved file list.")
        except error_perm, resp:
            if str(resp) == "550 No files found":
                self.log(10, "File list is empty.")
                return None
            else:
                raise
        return filter(self.pattern_compiled.match, files)

    def copy(self, filename, target, callback=None, binary=False):
        with open(target, 'w') as target_handler:
            def write_with_linesep(s):
                target_handler.write("%s\n" % s)
            self.log(20, "Start retrieval of remote file %s." % filename)
            if not callback:
                callback = write_with_linesep
            if binary:
                self.retrbinary("RETR " + filename, callback)
            else:
                self.retrlines("RETR " + filename, callback)
            self.log(20, "Retrieved file %s." % filename)
            target_handler.close()

    def __init__(self, hostname, username, password, wd, pattern=None, log=None, autologin=False):
        # read options
	self.hostname = hostname
	self.username = username
	self.password = password
	self.wd = wd
        if not pattern:
            self.pattern = ".*"
        else:
            self.pattern = pattern
        if not log:
            self.log = self._log
        else:
            self.log = log
        # set defaults
        self.connected = False
        self.pattern_compiled = re.compile(self.pattern)
        # initialize FTP connector
        FTP.__init__(self, self.hostname)
        # login to the remote site
        if autologin:
            self.login()

    def __del__(self):
        pass


class pyTrivialFTPShell(cmd.Cmd, pyTrivialFTP):
    intro = 'Welcome to the pyTrivialFTP shell.  Type help or ? to list commands.\n'
    prompt = '(pyTrivialFTP) '

    def do_login(self, arg):
        'Login to the remote site'
        self.login()
    def do_close(self, arg):
        'Logout from the remote site'
        self.close()
    def do_list(self, filename):
        'List contents of the remote working directory'
        for file in self.list():
            print file
    def do_copy(self, filename):
        'Copy a file onto the local working directory: COPY FILENAME'
        target = os.path.join(os.getcwd(), os.path.basename(filename))
        self.copy(filename, target)
    def do_quit(self, arg):
        'Exit'
        self.close()
        return True

    def __init__(self, hostname, username, password, wd, pattern=None, log=None, autologin=False):
	cmd.Cmd.__init__(self)
        pyTrivialFTP.__init__(self, hostname, username, password, wd, pattern, log, autologin)

    def __del__(self):
        pass


def short_usage():
    print >>sys.stderr, """Usage:
    pyTrivialFTP -H HOSTNAME -U USERNAME -P PASSWORD -w WORK_DIR [ -p PATTERN ]
Try `pyTrivialFTP --help' for more information."""


def full_usage():
    print >>sys.stderr, """Usage:
    pyTrivialFTP -H HOSTNAME -U USERNAME -P PASSWORD -w WORK_DIR [ -p PATTERN ]
The poor man's API for accessing data on a remote FTP repository.
      --help                        display this help and exit
  -H, --hostname       HOSTNAME     name of the cache
  -U, --username       USERNAME     base directory of the cache
  -P, --password       PASSWORD     apply a patter match
  -w, --wd             WORK_DIR     apply a patter match
  -p, --pattern        PATTERN      apply a patter match"""


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hH:U:P:w:p:",
                                   ["help", "hostname=", "username=", "password=", "wd=", "pattern=", ])
    except getopt.GetoptError, err:
        print >>sys.stderr, err
        short_usage()
        sys.exit(2)

    hostname = None
    username = None
    password = None
    wd = None
    pattern = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            full_usage()
            sys.exit()
        elif opt in ("-H", "--hostname"):
            hostname = arg
        elif opt in ("-U", "--username"):
            username = arg
        elif opt in ("-P", "--password"):
            password = arg
        elif opt in ("-w", "--wd"):
            wd = arg
        elif opt in ("-p", "--pattern"):
            pattern = arg

    # pre-flights sanity checks
    if not hostname:
        print >>sys.stderr, "Host name not specified!\n"\
            "A host name can be specified via the --hostname switch."
        sys.exit(2)
    if not username:
        print >>sys.stderr, "User name not specified!\n"\
            "A used name can be specified via the --username switch."
        sys.exit(2)
    if not password:
        print >>sys.stderr, "Password not specified!\n"\
            "A password can be specified via the --password switch."
        sys.exit(2)
    if not wd:
        print >>sys.stderr, "Working directory not specified!\n"\
            "A working directory can be specified via the --wd switch."
        sys.exit(2)

    # connect to the FTP shell
    pyTrivialFTPShell(hostname, username, password, wd, pattern).cmdloop()


if __name__ == "__main__":
    main(sys.argv[1:])


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
