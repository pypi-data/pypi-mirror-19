"""
Foldback data parsers
"""


from subprocess import Popen, PIPE
from systematic.shell import CommandPathCache


class ShellCommandParserError(Exception):
    pass


class ShellCommandParser(object):
    """Parser based on shell commands

    Run shell commands and parse output
    """
    def __init__(self):
        self.__command_cache__ = CommandPathCache()

    def execute(self, args):
        """Run shell command

        Run a shell command with subprocess
        """
        if isinstance(args, str):
            args = [args]

        if self.__command_cache__.which(args[0]) is None:
            raise ShellCommandParserError('Command not found: {0}'.format(args[0]))
        print command
