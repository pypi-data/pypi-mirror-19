# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import sys
import os                 # NOQA

from ruamel.std.argparse import ProgramBase, option, CountAction, \
    SmartFormatter, sub_parser, version
from ruamel.appconfig import AppConfig
from . import __version__
from .nim import Nim


def to_stdout(*args):
    sys.stdout.write(' '.join(args))


class NimCmd(ProgramBase):
    def __init__(self):
        super(NimCmd, self).__init__(
            formatter_class=SmartFormatter,
            # aliases=True,
            # usage="""""",
        )

    # you can put these on __init__, but subclassing NimCmd
    # will cause that to break
    @option('--verbose', '-v',
            help='increase verbosity level', action=CountAction,
            const=1, nargs=0, default=0, global_option=True)
    @version('version: ' + __version__)
    def _pb_init(self):
        # special name for which attribs are included in help
        pass

    def run(self):
        self.nim = Nim(self._args, self._config)
        if hasattr(self._args, 'func'):  # not there if subparser selected
            return self._args.func()
        self._parse_args(['--help'])     # replace if you use not subparsers

    def parse_args(self):
        self._config = AppConfig(
            'nim',
            filename=AppConfig.check,
            parser=self._parser,  # sets --config option
            warning=to_stdout,
            add_save=False,  # add a --save-defaults (to config) option
        )
        # self._config._file_name can be handed to objects that need
        # to get other information from the configuration directory
        self._config.set_defaults()
        self._parse_args(
            # default_sub_parser="",
        )

    @sub_parser(help='some command specific help')
    # @option('--session-name', default='abc')
    def show(self):
        # from plumbum.cmd import tmux
        # from plumbum.commands.processes import ProcessExecutionError
        pass


def main():
    n = NimCmd()
    n.parse_args()
    sys.exit(n.run())

if __name__ == '__main__':
    main()
