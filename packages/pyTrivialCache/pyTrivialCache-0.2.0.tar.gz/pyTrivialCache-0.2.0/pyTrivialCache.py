# pyTrivialCache - The poor man's API for manipulating a file system cache

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


import os
import re
import cmd
import getopt
import sys
import shutil


class pyTrivialCacheException(Exception):
    pass


class pyTrivialCacheLockException(pyTrivialCacheException):
    pass


class pyTrivialCache(object):

    def _log(self, priority, msg):
        # priority is ignored
        print msg

    def lock(self):
        if not self.connected:
            try:
                os.makedirs(self.lock_dir)
                self.connected = True
                self.log(20, "Connected to %s." % self.name)
            except:
                self.log(30, "Cannot acquire lock on %s." % self.name)
                raise pyTrivialCacheLockException
        else:
                self.log(10, "Already connected to %s." % self.name)

    def unlock(self):
        if self.connected:
            try:
                os.rmdir(self.lock_dir)
                self.connected = False
                self.log(20, "Disconnected from %s." % self.name)
            except:
                self.log(30, "Cannot release lock on %s." % self.name)
                raise
        else:
            self.log(10, "Already disconnected from %s." % self.name)

    def _filename2path(self, filename):
        match = self.pattern_compiled.match(filename)
        if match:
            intermediate = list(match.groups())
            return os.path.join(self.basedir, *intermediate)

    def _get_target_path(self, filename):
        return self._filename2path(filename)

    def get_full_path(self, filename):
        return os.path.join(self._get_target_path(filename), filename)

    def exists(self, filename, target_path=None):
        if not target_path:
            target_path = self._get_target_path(filename)
        full_target_path = os.path.join(target_path, filename)
        return os.path.exists(full_target_path)

    def push(self, filename, target_path=None):
        self.log(20, "Pushing %s unto %s." % (filename, self.name))
        if not target_path:
            target_path = self._get_target_path(filename)
        try:
            os.makedirs(target_path)
        except:
            pass
        shutil.copyfile(filename, os.path.join(target_path, filename))

    def unpush(self, filename):
        self.log(20, "Unpushing %s from %s." % (filename, self.name))
        target_path = self._get_target_path(filename)
        full_target_path = os.path.join(target_path, filename)
        try:
            os.unlink(full_target_path)
        except:
            pass

    def traverse(self, sorter=None, full_path=False):
        all_files = []
        for dir_name, dirs, files in os.walk(self.basedir):
            for filename in files:
                if full_path:
                    all_files.append(os.path.join(dir_name, filename))
                else:
                    all_files.append(filename)
        if sorter:
            return sorted(all_files, key=sorter)
        else:
            return all_files

    def purge(self):
        for filename in self.traverse():
            self.unpush(filename)

    def __init__(self, name, basedir, pattern=None, log=None):
        # read options
        self.name = name
        self.basedir = basedir
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
        self.lock_dir = os.path.join(self.basedir, '.lock_dir')
        self.pattern_compiled = re.compile(self.pattern)

    def __del__(self):
        pass


class pyTrivialCacheShell(cmd.Cmd, pyTrivialCache):
    intro = 'Welcome to the pyTrivialCache shell.  Type help or ? to list commands.\n'
    prompt = '(pyTrivialCache) '

    def do_lock(self, arg):
        'Acquire a lock'
        self.lock()
    def do_unlock(self, arg):
        'Release a lock'
        self.unlock()
    def do_exists(self, filename):
        'Tell if a file exists: EXISTS FILENAME'
        if filename:
            print self.exists(filename)
    def do_push(self, filename):
        'Push a file unto the cache: PUSH FILENAME'
        self.push(filename)
    def do_unpush(self, filename):
        'Unpush a file from the cache: UNPUSH FILENAME'
        self.unpush(filename)
    def do_list(self, arg):
        'List the contents of the cache: LIST'
        for filename in self.traverse(sorter=lambda x: x):
            print filename
    def do_purge(self, arg):
        'Purge the contents of the cache: LIST'
        self.purge()
    def do_quit(self, arg):
        'Exit'
        self.unlock()
        return True

    def __init__(self, name, basedir, pattern=None, log=None):
	cmd.Cmd.__init__(self)
        pyTrivialCache.__init__(self, name, basedir, pattern, log)

    def __del__(self):
        pass



def short_usage():
    print >>sys.stderr, """Usage:
    pyTrivialCache -n NAME -b BASEDIR [ -p PATTERN ]
Try `pyTrivialCache --help' for more information."""


def full_usage():
    print >>sys.stderr, """Usage:
    pyTrivialCache -n NAME -b BASEDIR [ -p PATTERN ]
The poor man's API for manipulating a file system cache.
      --help                       display this help and exit
  -n, --name          NAME         name of the cache
  -b, --basedir       BASEDIR      base directory of the cache
  -p, --pattern       PATTERN      apply a patter match"""


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hn:b:p:",
                                   ["help", "name=", "basedir=", "pattern=", ])
    except getopt.GetoptError, err:
        print >>sys.stderr, err
        short_usage()
        sys.exit(2)

    name = None
    basedir = None
    pattern = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            full_usage()
            sys.exit()
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-n", "--basedir"):
            basedir = arg
        elif opt in ("-p", "--pattern"):
            pattern = arg

    # pre-flights sanity checks
    if not name:
        print >>sys.stderr, "Cache name not specified!\n"\
            "A used-defined name can be specified via the --name switch."
        sys.exit(2)
    if not basedir:
        print >>sys.stderr, "Cache basedir not specified!\n"\
            "A used-defined basedir can be specified via the --basedir switch."
        sys.exit(2)

    # connect to the cache shell
    pyTrivialCacheShell(name, basedir, pattern).cmdloop()


if __name__ == "__main__":
    main(sys.argv[1:])


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
