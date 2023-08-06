# -*- coding: utf-8 -*-

import argparse


class ArgumentParser:
    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser()

        parser.add_argument("-v", "--verbose",
                            action="store_true", default=False, required=False,
                            help="run program in verbose/debug mode, lots of output!")
        parser.add_argument("--stdout",
                            action="store", choices=["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"],
                            default=["WARNING"], required=False,
                            help="change stdout logging level (logs INFO to file already)")

        group_init = argparse.ArgumentParser(add_help=False)
        group_init.add_argument("init_type", action="store",
                                choices=["repository", "conf"],
                                help="choose to initialize repository or conf")
        group_init.add_argument("path", action="store",
                                type=str, default=None,
                                help="this path will be the initialization root")

        group_checkconfig = argparse.ArgumentParser(add_help=False)
        group_checkconfig.add_argument("--config", action="store",
                                       type=str, default=None,
                                       help="path to the configuration file")

        group_diff = argparse.ArgumentParser(add_help=False)
        group_diff.add_argument("--diff", action="store_true", default=True, required=False)

        group_run = argparse.ArgumentParser(add_help=False)
        group_run.add_argument("--config", action="store", required=True,
                                       type=str, default=None,
                                       help="path to the configuration file")
        group_version = argparse.ArgumentParser(add_help=False)
        group_version.add_argument("--version", action="store_true", default=True, required=False)

        # acticate subparsers on main parser
        sp = parser.add_subparsers()

        sp_init = sp.add_parser("init", parents=[group_init], help="initialize configuration or repository")
        sp_init.set_defaults(which="init")

        sp_checkconfig = sp.add_parser("check", parents=[group_checkconfig],
                                       help="run sanity check on configuration")
        sp_checkconfig.set_defaults(which="check")

        sp_diff = sp.add_parser("diff", parents=[group_diff],
                                help="run converge and compare to previous version without committing changes to output")
        sp_diff.set_defaults(which="diff")

        sp_run = sp.add_parser("run", parents=[group_run], help="run converge fully (check, output)")
        sp_run.set_defaults(which="run")

        sp_version = sp.add_parser("version", parents=[group_version],
                                   help="get converge version and build information")
        sp_version.set_defaults(which="version")

        return parser
