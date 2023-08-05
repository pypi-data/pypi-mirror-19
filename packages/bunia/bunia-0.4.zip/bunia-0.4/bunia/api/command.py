import sys

class Command(object):
    """
    Base class for all StGeorge commands.

    You need to inherit from this, and override/extend what's needed
    """

    NAME = 'command'
    DESCRIPTION = u'Does nothing.'
    ARGUMENTS = [] # list of Argument instances

    def run(self, runner, **kwargs):
        """
        Run with specified arguments.
        :param runner: Runner instance - pertaining to where are you being ran
        """

    def run_using_main(self, args=None):
        """
        To be called in if __name__ == '__main__' sections.
        Uses sys.argv
        """
        from bunia.runner.console import _run_from_console
        _run_from_console(self, args or sys.argv[1:])



COMMAND = Command   # for autodiscovery
