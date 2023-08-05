"""
awsmc.cli - command line interface
"""

import abc
import argparse

from awsmc.exc import UserError

_COMMANDS = []


class BaseCommand(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def name(self):
        return 'base'

    def arguments(self, parser):
        pass

    @abc.abstractmethod
    def execute(self, args):
        pass


def register_command(cmd):
    _COMMANDS.append(cmd())
    return cmd


def main():
    parser = argparse.ArgumentParser(prog='awsmc',
                                     description='AWS Minecraft control')
    subparsers = parser.add_subparsers()
    for command in _COMMANDS:
        sub = subparsers.add_parser(command.name())
        command.arguments(sub)
        sub.set_defaults(func=command.execute)
    args = parser.parse_args()
    try:
        args.func(args)
    except UserError as e:
        print(str(e))
