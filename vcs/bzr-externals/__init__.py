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

"""Support external branches like svn:externals.

Using hooks, this plugin supports external branches for these commands:

* branch
* checkout
* commit
* pull
* push
* update.

Works from any client including bzr, QBzr, TortoiseBzr and Bazaar Explorer.
To begin work with external branches please see ``bzr help externals-add``.

This plugin also provides a command to execute an arbitrary bzr or shell
command for each branch in the local workspace, see also
``bzr help externals-command``.

Works with snapshot external branches only for ``branch/checkout`` command with
revision options. The snapshot becomes at commit in the main project.

Known issues:

* Does not support ``^/`` expression in relative urls.
* pull command does not overwrite your newer working tree if you use a custom
  revision.
* update command does not support a custom revision and does not check
  externals if the branch tip is not changed.
* Does not support lightweight checkout.
* qcommit command does not support external snapshots via hooks, instead of it
  use ``ecmd qcommit`` or simple ``commit`` commands.

Plugin used config files::

  .bzrmeta/externals
  .bzrmeta/externals-snapshot

Format of config files the following::

  url directory [revisionspec]
"""

from bzrlib.lazy_import import lazy_import
lazy_import(globals(), """
from bzrlib.plugins.externals import externals as lazy_externals
from bzrlib.plugins.externals import commands as lazy_commands
""")

from bzrlib.branch import Branch
from bzrlib.mutabletree import MutableTree
from bzrlib.commands import Command, plugin_cmds

plugin_name = 'externals'
version_info = (1, 3, 2, 'final', 0)

def post_change_branch_tip_hook(params):
    if params.old_revno == 0 and params.branch.base.startswith('file:///'):
        # only branch or checkout commands
        lazy_externals.Externals(params.branch, params.new_revid).pull()

def post_pull_hook(result):
    if result.old_revno != 0:
        # only pull or update commands
        lazy_externals.Externals(result.target_branch, result.new_revid).pull()

def post_push_hook(result):
    lazy_externals.Externals(result.source_branch,
        result.new_revid).push(result.target_branch.base)

def start_commit_hook(mutable_tree):
    lazy_externals.Externals(mutable_tree.branch,
        mutable_tree.branch.last_revision(),
        root=mutable_tree.basedir).commit(mutable_tree)

def get_command_hook(cmd_or_None, command_name):
    if command_name in ('branch', 'get', 'clone'):
        return lazy_commands.cmd_branch()
    elif command_name in ('checkout', 'co'):
        return lazy_commands.cmd_checkout()
    return cmd_or_None

def install_hooks():
    Branch.hooks.install_named_hook('post_change_branch_tip',
        post_change_branch_tip_hook,
        'branch/checkout external branches')
    Branch.hooks.install_named_hook('post_pull',
        post_pull_hook,
        'pull/update external branches')
    Branch.hooks.install_named_hook('post_push',
        post_push_hook,
        'push external branches')
    MutableTree.hooks.install_named_hook('start_commit',
        start_commit_hook,
        'snapshot external branches')
    Command.hooks.install_named_hook('get_command',
        get_command_hook,
        'extend standard command to work with external branches')

install_hooks()

def register_commands():
    module = 'bzrlib.plugins.externals.commands'
    plugin_cmds.register_lazy('cmd_externals_add',
        ['eadd'], module)
    plugin_cmds.register_lazy('cmd_externals_command',
        ['ecmd'], module)

register_commands()

# monkey patching for sets branch.parent before call post_change_branch_tip
def new_copy_content_into(self, destination, revision_id=None):
    destination.set_parent(self.base)
    old_copy_content_into(self, destination, revision_id)

old_copy_content_into = Branch.copy_content_into
Branch.copy_content_into = new_copy_content_into

# monkey patching for fix trash after pull command
def new_finished(self):
    old_finished(self)
    # clear line
    from bzrlib.ui import ui_factory
    ui_factory.clear_term()

from bzrlib.progress import ProgressTask
old_finished = ProgressTask.finished
ProgressTask.finished = new_finished
