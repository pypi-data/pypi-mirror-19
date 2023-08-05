import io
import six

from bunia.output.base import Output

class ConsoleOutput(Output):
    """
    Returns a unicode.

    You can silence and unsilence it by setting the .sink property to True/False.
    True silences output.
    """
    def __init__(self, name=None, eol='\n', stdout=None, sink=False):
        Output.__init__(self, name)
        self.io = stdout or io.StringIO()
        self.eol = six.text_type(eol)
        self.sink = sink    #: public, write to toggle sink


    def text(self, message, *args):
        """Write a message. It will be subject to processing with
        message % args. Appends an end of line"""
        if self.sink:
            return
        self.io.write((six.text_type(message) % args))
        self.io.write(self.eol)

    def to(self, form='text'):
        content = self.io.getvalue()
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

