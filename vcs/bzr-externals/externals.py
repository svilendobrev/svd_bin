# Copyright (C) 2009 Eugene Tarasenko, Alexander Belchenko
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os

from bzrlib.urlutils import join, local_path_from_url
from bzrlib.osutils import check_legal_path, getcwd, get_user_encoding, isdir, isfile, pathjoin, relpath
from bzrlib.commands import run_bzr_catch_user_errors
from bzrlib.trace import is_quiet, is_verbose, note, warning

try:
    from bzrlib.cmdline import split as cmdline_split   #2.2+
except:
    from bzrlib.commands import shlex_split_unicode as cmdline_split

CONFIG_PATH = '.bzrmeta/externals'
SNAPSHOT_PATH = '.bzrmeta/externals-snapshot'

disable_hooks = False # for prevent double running external command
command_kwargs = None # each new command changed value

class Externals:

    def __init__(self, branch, revid, root=None):
        self.branch = branch
        self.revid = revid
        if root is not None:
            self.root = root
        else:
            self.root = local_path_from_url(branch.base)
        self.cwd = getcwd()
        self.config = []
        self.bound = True
        self.use_snapshot = command_kwargs and 'revision' in command_kwargs

    def _set_config(self, text):
        lines = text.splitlines()
        for line in lines:
            if len(line.strip()) > 0 and not line.startswith('#'):
                # function shlex.split not support windows path separator '\'
                #line = line.decode('utf-8').replace('\\', '/')
                #arg = shlex_split_unicode(line)
                arg = cmdline_split( line)
                if arg not in self.config:
                    self.config.append(arg)

    def read_config(self):
        path = pathjoin(self.root, CONFIG_PATH)
        if self.use_snapshot or not isfile(path):
            # config file not exist in directory
            return False
        f = open(path, 'rU')
        try:
            self._set_config(f.read())
        finally:
            f.close()
        return len(self.config) > 0

    def read_config_from_repository(self):
        rev_tree = self.branch.repository.revision_tree(self.revid)
        if self.use_snapshot:
            file_id = rev_tree.path2id(SNAPSHOT_PATH)
            if not file_id:
                file_id = rev_tree.path2id(CONFIG_PATH)
                if file_id:
                    warning('warning: for this revision there is no snapshot of external branches!')
        else:
            file_id = rev_tree.path2id(CONFIG_PATH)
        if not file_id:
            # there is no config or snapshot files in repository
            return False
        rev_tree.lock_read()
        try:
            text = rev_tree.get_file_text(file_id)
            self._set_config(text)
        finally:
            rev_tree.unlock()
        return len(self.config) > 0

    def _relpath(self, path):
        try:
            return relpath(self.cwd, path)
        except:
            pass
        return path

    @staticmethod
    def _relurljoin(base, relative):
        if relative.startswith('//'):
            # urlutils.join not supports relative urls start with '//'
            scheme = base.partition('://')
            return scheme[0] + ':' + relative
        else:
            return join(base, relative)

    @staticmethod
    def _report(cmd):
        if not is_quiet():
            note('External ' + ' '.join(cmd))

    @staticmethod
    def adjust_verbosity(cmd):
        if is_quiet():
            cmd += ['-q']
        if is_verbose():
            cmd += ['-v']

    def branch_iterator(self, target_root=None):
        if len(self.config) == 0:
            # branch not have externals configuration
            return

        self.bound = True
        if not target_root:
            target_root = self.branch.get_bound_location()
            if not target_root:
                self.bound = False
                target_root = self.branch.get_parent()
                if not target_root:
                    # support new braches with no parent yet
                    target_root = self.branch.base

        for arg in self.config: # url directory [revisionspec]
            location = self._relurljoin(target_root, arg[0])
            if target_root.startswith('file:///'):
                # try to pull externals from the parent for the feature branch
                path = pathjoin(local_path_from_url(target_root), arg[1])
                if isdir(path):
                    location = self._relpath(path)
                else:
                    # parent is local master branch
                    if location.startswith('file:///'):
                        location = self._relpath(local_path_from_url(location))

            check_legal_path(arg[1])
            rel_path = self._relpath(pathjoin(self.root, arg[1]))

            revision = None
            if len(arg) > 2:
                revision = arg[2]
            yield location, rel_path, revision

    def pull(self):
        if disable_hooks:
            return

        # need use merged config from repository and working tree
        # because new added external branch from repository or working tree
        # need pull/update for correct snapshot
        self.read_config()
        self.read_config_from_repository()
        if len(self.config) == 0:
            return

        for location, path, revision in self.branch_iterator():
            if location == path:
                # not create feature branch for directory above the root
                continue

            # select what do it
            if isdir(pathjoin(path, '.bzr')) or isdir(pathjoin(path, '.svn')):
                if self.bound:
                    cmd = ['update', path]
                else:
                    cmd = ['pull', location, '--directory', path]
            else:
                if self.bound:
                    cmd = ['checkout', location, path]
                else:
                    cmd = ['branch', location, path]

                # command branch don't create recursive directory
                dirs = path.rpartition('/')
                if dirs[0] != '' and not isdir(dirs[0]):
                    os.makedirs(dirs[0].encode(get_user_encoding()))

            # if use revision options but not for 'update'
            if revision is not None:# and cmd[0] != 'update':
                cmd += ['--revision', revision]
            self.adjust_verbosity(cmd)
            self._report(cmd)
            run_bzr_catch_user_errors(cmd)

    def push(self, target):
        if disable_hooks or not self.read_config():
            return

        for location, path, revision in self.branch_iterator(target):
            if location == path:
                # don't push into itself
                continue

            # XXX: maybe he should rather decorate the push command
            # so that we can get the commandline args
            # alternatively the plugin infrastructure must provide it to us?!
            cmd = ['push', location, '--directory', path, '--no-strict']

            if revision is not None:
                # not push if use revision
                continue

            self.adjust_verbosity(cmd)
            self._report(cmd)
            run_bzr_catch_user_errors(cmd)

    @staticmethod
    def _quoted_if_need(text):
        if text.find(' ') != -1:
            text = '"' + text + '"'
        return text

    def commit(self, mutable_tree):
        # BUG: not run recursively if in above branch not have changes
        if disable_hooks or not self.read_config():
            return

        from bzrlib.workingtree import WorkingTree
        snapshot = []
        for arg in self.config: # url directory [revisionspec]
            wt = WorkingTree.open(pathjoin(self.root, arg[1]))
            if wt.has_changes(wt.basis_tree()):
                cmd = ['ci']
                os.chdir(wt.basedir)
                try:
                    run_bzr_catch_user_errors(cmd)
                finally:
                    os.chdir(self.cwd)

            if len(arg) < 3:
                arg.append('')
            arg[2] = 'revid:' + wt.last_revision()
            arg[1] = self._quoted_if_need(arg[1])
            snapshot.append(' '.join(arg).encode('utf-8'))

        path = pathjoin(self.root, SNAPSHOT_PATH)
        f = open(path, 'w')
        try:
            f.write('\n'.join(snapshot))
        finally:
            f.close()
