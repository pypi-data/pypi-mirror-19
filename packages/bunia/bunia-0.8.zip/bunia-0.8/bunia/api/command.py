class Command(object):
    """
    Base class for all StGeorge commands.

    You need to inherit from this, and override/extend what's needed
    """

    NAME = 'command'
    DESCRIPTION = 'Does nothing.'
    ARGUMENTS = [] # list of Argument instances

    def run(self, runner, **kwargs):
        """
        Run with specified arguments.
        :param runner: Runner instance - pertaining to where are you being ran
        """

    def __call__(self, *args, **kwargs):
        """Execute run() using InlineRunner"""
        from bunia.runner import InlineRunner

        ir = InlineRunner()
        return ir.run(self, *args, **kwargs)


COMMAND = Command   # for autodiscovery
