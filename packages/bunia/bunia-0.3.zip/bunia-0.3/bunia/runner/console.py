#!/usr/bin/env python
import sys
import argparse
from bunia.runner.base import Runner
from bunia.api import ValuelessArgument
from bunia.output import ConsoleOutput
from bunia.discovery import from_name
import io

class ConsoleRunner(Runner):
    """
    A console-based runner. Arguments are strings, output is utf8 text.
    """

    def __init__(self):
        self.consoles = []

    def new_console(self, name=None):
        con = ConsoleOutput(name)
        self.consoles.append(con)
        return con

    def new_table(self, name=None, headers=[]):
        raise NotImplementedError

    def run(self, cmd, args, stdout=None):
        """
        Run a command.

        :param cmd: Command instance to run
        :param args: list of str, command-line arguments
        :param stdout: optional file-like object to write output to
        :raise ValueError: argument was invalid
        """
        if stdout is None:
            self.stdout = io.StringIO()

        parser = argparse.ArgumentParser(description=cmd.DESCRIPTION)

        argument_by_name = {}

        for argument in cmd.ARGUMENTS:
            argument_by_name[argument.name] = argument

            # check. Is it optional? takes an argument?
            takes_argument = not isinstance(argument, ValuelessArgument)
            optional = not argument.required

            if isinstance(argument, ValuelessArgument):     #flag
                parser.add_argument(('--' if optional else '') + argument.name,
                                    action='store_const',
                                    const=argument.default,
                                    default=None,
                                    help=argument.description)
            else:       # takes an argument
                parser.add_argument(('--' if optional else '') + argument.name,
                                    nargs=1,
                                    default=argument.default,
                                    type=str,
                                    help=argument.description,
                                    metavar=argument.name.upper() if takes_argument else None
                                    )

        params = {}

        for argument_name, value in vars(parser.parse_args(args)).iteritems():
            try:
                v = value[0]
            except TypeError:
                v = value

            try:
                params[argument_name] = argument_by_name[argument_name].clean(v)
            except ValueError as e:
                raise ValueError('Invalid value of argument %s: %s' % (argument_name, e.message))

        cmd.run(self, **params)

        first = True

        for console in self.consoles:
            if not first:
                self.stdout.write('\n')
            else:
                first = True

            if console.name is not None:
                self.stdout.write(console.name)
                self.stdout.write('----------------')

            self.stdout.write(console.to('text').decode('utf8'))


def _run_from_console(cmd, args):
    # First argument is name of the module to run
    cr = ConsoleRunner()
    cr.run(cmd, args)
    sys.stdout.write(cr.stdout.getvalue())
    cr.stdout.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(u'''usage: python -m bunia.runner.console <command name> <arguments>

    Run a command using ConsoleRunner

    command name is in form name.of.module:CommandClass to set class explicitly
    or name.of.module, if it contains a module global variable COMMAND''')
        sys.exit(1)

    cmd = from_name(sys.argv[1])()
    _run_from_console(cmd, sys.argv[2:])
