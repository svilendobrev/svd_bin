# Copyright (C) 2010 Eugene Tarasenko, Marius Kruger
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

import os.path

from bzrlib.branch import Branch
from bzrlib.urlutils import local_path_from_url
from bzrlib.osutils import getcwd, get_user_encoding, isdir, isfile, pathjoin, relpath
from bzrlib.commands import Command, run_bzr_catch_user_errors
from bzrlib.option import Option
from bzrlib.trace import is_quiet, note
from bzrlib.bzrdir import BzrDir

import externals

_main_cwd = getcwd()
_main_base = None

class cmd_externals_add(Command):
    """Adds already existing or remote branch as an external branch.

    You can use relative urls like in svn:externals.

    This command adds or changes following configuration files::
      .bzrmeta/externals
      .bzrmeta/externals-snapshot
      .bzrignore.

    :Examples:
      bzr eadd bzr://example.com/repos/common/foo common/foo -r revno:100
      # relative to scheme
      bzr eadd //example.com/repos/common/foo common/foo
      # relative to the server hostname
      bzr eadd /repos/common/foo common/foo
      # relative to parent directory
      bzr eadd ../../common/foo common/foo
    """
    aliases = ['eadd']
    takes_args = ['from_location', 'to_location']
    takes_options = ['revision']

    def run(self, from_location, to_location, revision=None):
        branch = Branch.open_containing('.')[0]
        root = local_path_from_url(branch.base)

        # select what do it
        if isdir(pathjoin(root, to_location, '.bzr')) or isdir(pathjoin(root, to_location, '.svn')):
            if branch.get_bound_location():
                cmd = ['update', to_location]
            else:
                cmd = ['pull', from_location, '--directory', to_location]
        else:
            if branch.get_bound_location():
                cmd = ['checkout', from_location, to_location]
            else:
                cmd = ['branch', from_location, to_location]

            # command branch don't create recursive directory
            dirs = to_location.rpartition('/')
            if dirs[0] != '' and not isdir(dirs[0]):
                os.makedirs(dirs[0].encode(get_user_encoding()))

        # if use revision options but not for 'update'
        if revision is not None:# and cmd[0] != 'update':
            cmd += ['--revision', revision[0].user_spec]

        note('Add external ' + ' '.join(cmd))
        run_bzr_catch_user_errors(cmd)

        bzrmeta = pathjoin(root, '.bzrmeta')
        if not isdir(bzrmeta):
            os.mkdir(bzrmeta)

        # add new branch to config and snapshot files
        line = from_location + ' ' + self._quoted_if_need(to_location)
        if revision:
            line += ' ' + revision[0].user_spec
        self._add_to_file(root, externals.CONFIG_PATH, line)
        self._add_to_file(root, externals.SNAPSHOT_PATH, line)

        # add ignore mask
        from bzrlib import IGNORE_FILENAME
        self._add_to_file(root, IGNORE_FILENAME, './' + to_location)

        # add config files to repository
        cmd = ['add',
            '.bzrignore',
            '.bzrmeta/externals',
            '.bzrmeta/externals-snapshot']
        run_bzr_catch_user_errors(cmd)

    @staticmethod
    def _quoted_if_need(text):
        if text.find(' ') != -1:
            text = '"' + text + '"'
        return text

    def _add_to_file(self, root, file_name, line):
        content = ''
        path = pathjoin(root, file_name)
        if isfile(path):
            f = open(path, 'rU')
            try:
                content = f.read()
            finally:
                f.close()
            if not content.endswith('\n'):
                # add at end of file the char '\n' if needed
                content += '\n'

        content += line.encode('utf-8') + '\n'
        f = open(path, 'w')
        try:
            f.write(content)
        finally:
            f.close()

class cmd_externals_command(Command):
    """Run some command(s) for this and external branches.

    This command run your COMMAND at first for each external branches,
    then for main branch if not use ``--externals-only`` option.
    For using an additional command option please use ``--`` after main command.

    The variable {relpath} in the command with be replaced with the relative
    path of the external branch.

    :Examples:
      bzr ecmd status
      bzr ecmd -- log -r -1
    """
    aliases = ['ecmd']
    takes_args = ['command+']
    takes_options = [
        Option('externals-only', short_name='e',
            help='Don\'t run on the main branch.'),
        Option('shell', short_name='s',
            help='Run shell commands instead of bzr commands.'),
        #'dry-run'
        ]

    def run(self, command_list, externals_only=False, shell=False, dry_run=False):
        # TODO: support setting the base location with -d
        externals.disable_hooks = True
        (tree, branch, relpath) = BzrDir.open_containing_tree_or_branch('.')

        global _main_base
        if _main_base is None:
            _main_base = branch.base

        ex = externals.Externals(branch, branch.last_revision(),
            root=tree.basedir)
        if ex.read_config():
            # run ecmd command in each externals for multilevel
            ecmd = ['ecmd']
            if shell:
                ecmd += ['--shell']
            if dry_run:
                ecmd += ['--dry-run']
            ex.adjust_verbosity(ecmd)

            for location, rel_path, revision in ex.branch_iterator(): #@UnusedVariable
                os.chdir(os.path.join(ex.cwd, rel_path))
                run_bzr_catch_user_errors(ecmd + ['--'] + command_list)

        if not externals_only:
            # parse arguments of command and execute
            if not is_quiet():
                if branch.base != _main_base:
                    note('Run command in external: ' + self._relpath(ex.root))
                else:
                    note('Run command in main branch:')
            command_list = self._substitute_in_commandlist(
                command_list, self._relpath(ex.root))
            ex.adjust_verbosity(command_list)
            if not dry_run:
                os.chdir(ex.root)
                if shell:
                    os.system(' '.join(command_list))
                else:
                    run_bzr_catch_user_errors(command_list)

        os.chdir(ex.cwd)

    def _relpath(self, path):
        try:
            global _main_cwd
            return relpath(_main_cwd, path)
        except:
            pass
        return path

    def _substitute_in_commandlist(self, command_list, rel_path):
        return [x.replace('{relpath}', rel_path) for x in command_list]

import bzrlib.builtins

class cmd_branch(bzrlib.builtins.cmd_branch):
    __doc__ = bzrlib.builtins.cmd_branch.__doc__

    def plugin_name(self):
        return None

    def run(self, **kwargs):
        externals.command_kwargs = kwargs
        super(cmd_branch, self).run(**kwargs)

class cmd_checkout(bzrlib.builtins.cmd_checkout):
    __doc__ = bzrlib.builtins.cmd_checkout.__doc__

    def plugin_name(self):
        return None

    def run(self, **kwargs):
        externals.command_kwargs = kwargs
        super(cmd_checkout, self).run(**kwargs)
