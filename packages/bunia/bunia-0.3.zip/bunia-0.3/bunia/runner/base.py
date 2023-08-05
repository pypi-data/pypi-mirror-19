class Runner(object):

    def new_console(self, name=None):
        """Return a new ConsoleOutput"""

    def new_table(self, name=None, headers=[]):
        """Return a new TableOutput
        :param name: table name
        :param headers: list of unicode, headers for the table.
            There will be as many columns as here
        """