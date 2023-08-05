import io

from bunia.output.base import Output

class ConsoleOutput(Output):
    """
    UTF-8 output.
    """
    def __init__(self, name=None, eol=u'\n', stdout=None, sink=False):
        Output.__init__(self, name)
        self.io = stdout or io.StringIO()
        self.eol = unicode(eol)
        self.sink = sink

    def sink(self, sink=True):
        """
        Make this console ignore all input.
        """
        self.sink = sink

    def text(self, message, *args):
        """Write a message. It will be subject to processing with
        message % args. Appends an end of line"""
        if self.sink:
            return
        self.io.write((unicode(message) % args))
        self.io.write(self.eol)

    def to(self, form='text'):
        content = self.io.getvalue().encode('utf8')
        self.io.close()

        if form == 'text':
            return content
        elif form == 'html':
            if len(content) == 0:
                return '<em> empty! </em>'
            else:
                return '<pre>' + content + '</pre>'
        else:
            raise ValueError('Unsupported form')

