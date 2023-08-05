#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import argparse

import solvebio

from . import auth
from . import data
from .tutorial import print_tutorial
from .ipython import launch_ipython_shell
from ..utils.validators import validate_api_host_url


class SolveArgumentParser(argparse.ArgumentParser):
    """
    Main parser for the SolveBio command line client.
    """
    subcommands = {
        'login': {
            'func': auth.login,
            'help': 'Login and save credentials'
        },
        'logout': {
            'func': auth.logout,
            'help': 'Logout and delete saved credentials'
        },
        'whoami': {
            'func': auth.whoami,
            'help': 'Show your SolveBio email address'
        },
        'tutorial': {
            'func': print_tutorial,
            'help': 'Show the SolveBio Python Tutorial',
        },
        'shell': {
            'func': launch_ipython_shell,
            'help': 'Open the SolveBio Python shell'
        },
        'import': {
            'func': data.import_file,
            'help': 'Import a local file into a SolveBio dataset',
            'arguments': [
                {
                    'flags': '--create-dataset',
                    'action': 'store_true',
                    'help': 'Create the dataset if it doesn\'t exist',
                },
                {
                    'flags': '--template-id',
                    'help': 'The template ID used when '
                            'creating a new dataset (via --create-dataset)',
                },
                {
                    'flags': '--template-file',
                    'help': 'A local template file to be used when '
                            'creating a new dataset (via --create-dataset)',
                },
                {
                    'flags': '--genome-build',
                    'help': 'If the dataset template is genomic, provide a '
                            'genome build for your data (i.e. GRCh37)'
                },
                {
                    'flags': '--follow',
                    'action': 'store_true',
                    'default': False,
                    'help': 'Follow the import\'s progress until it completes'
                },
                {
                    'flags': '--auto-approve',
                    'action': 'store_true',
                    'default': False,
                    'help': 'Automatically approve all dataset commits for '
                            'the import (may require admin role)'
                },
                {
                    'name': 'dataset',
                    'help': 'The full name of the dataset '
                            '(<depository>/<version>/<dataset>)'
                },
                {
                    'name': 'file',
                    'help': 'One or more local files to import',
                    'nargs': '+'
                }
            ]
        }
    }

    def __init__(self, *args, **kwargs):
        super(SolveArgumentParser, self).__init__(*args, **kwargs)
        self._optionals.title = 'SolveBio Options'
        self.add_argument(
            '--version',
            action='version',
            version=solvebio.version.VERSION)
        self.add_argument(
            '--api-host',
            help='Override the default SolveBio API host',
            type=self.api_host_url)
        self.add_argument(
            '--api-key',
            help='Manually provide a SolveBio API key')
        self.add_argument(
            '--api-token',
            help='Manually provide a SolveBio OAuth API token')

    def _add_subcommands(self):
        """
            The _add_subcommands method must be separate from the __init__
            method, as infinite recursion will occur otherwise, due to the fact
            that the __init__ method itself will be called when instantiating
            a subparser, as we do below
        """
        subcmd_params = {
            'title': 'SolveBio Commands',
            'dest': 'subcommands'
        }
        subcmd = self.add_subparsers(
            **subcmd_params)  # pylint: disable=star-args

        for name, params in self.subcommands.items():
            p = subcmd.add_parser(name, help=params['help'])
            p.set_defaults(func=params['func'])
            for arg in params.get('arguments', []):
                name_or_flags = arg.pop('name', None) or arg.pop('flags', None)
                p.add_argument(name_or_flags, **arg)

    def parse_solvebio_args(self, args=None, namespace=None):
        """
            Try to parse the args first, and then add the subparsers. We want
            to do this so that we can check to see if there are any unknown
            args. We can assume that if, by this point, there are no unknown
            args, we can append shell to the unknown args as a default.
            However, to do this, we have to suppress stdout/stderr during the
            initial parsing, in case the user calls the help method (in which
            case we want to add the additional arguments and *then* call the
            help method. This is a hack to get around the fact that argparse
            doesn't allow default subcommands.
        """
        try:
            sys.stdout = sys.stderr = open(os.devnull, 'w')
            _, unknown_args = self.parse_known_args(args, namespace)
            if not unknown_args:
                args.insert(0, 'shell')
        except SystemExit:
            pass
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        self._add_subcommands()
        return super(SolveArgumentParser, self).parse_args(args, namespace)

    def api_host_url(self, value):
        validate_api_host_url(value)
        return value


def main(argv=sys.argv[1:]):
    """ Main entry point for SolveBio CLI """
    parser = SolveArgumentParser()
    args = parser.parse_solvebio_args(argv)

    if args.api_host:
        solvebio.api_host = args.api_host
    if args.api_key:
        solvebio.api_key = args.api_key

    args.func(args)


if __name__ == '__main__':
    main()
