# coding=UTF-8
from bunia.runner.base import Runner
from bunia.api import ValuelessArgument
from bunia.output import ConsoleOutput
import io
import six


class HTMLOutputBuilder(object):
    """
    Used to build output HTML.

    You can subclass it and pass to HTMLRunner for customization
    """

    def __init__(self):
        self.out = io.StringIO()

    def start(self):
        """Start of rendering"""

    def stop(self):
        """Stop of rendering"""

    def default_output(self, output):
        """Default (no-name) output is being displayed"""
        self.out.write(six.text_type(''.join(_output_to_html(output))))
        self.out.write(six.text_type('<br>'))

    def named_output(self, output):
        """Named output is being displayed"""
        self.out.write(six.text_type('<h3>'))
        self.out.write(six.text_type(output.name))
        self.out.write(six.text_type('</h3>'))
        self.out.write(six.text_type(''.join(_output_to_html(output))))
        self.out.write(six.text_type('<br>'))

    def to_html(self):
        q = self.out.getvalue()
        self.out.close()
        return q


class HTMLRunner(Runner):
    """
    A HTML-based runner. Arguments are a dictionary received by POST, output is utf8 HTML.
    """

    def __init__(self, output_builder=HTMLOutputBuilder):
        self.outputs = []
        self.builder = output_builder()

    def new_console(self, name=None, sink=False):
        con = ConsoleOutput(name, sink=sink)
        self.outputs.append(con)
        return con

    def get_html(self):
        """Return HTML generated with output_builder"""
        self.builder.start()

        for output in self.outputs:
            if output.name is None:
                default = output
                break
        else:
            default = None

        if default is not None:
            self.builder.default_output(default)

        for output in self.outputs:
            if output is not default:
                self.builder.named_output(output)

        self.builder.stop()

        return self.builder.to_html()

    def run(self, cmd, http_dict):
        """
        Run a command.

        :param cmd: Command instance to run
        :param http_dict: dictionary of variables
        :raise ValueError: argument was invalid or internal failure
        """
        cmd.run(self, **arguments_from_post(cmd, http_dict))


def _output_to_html(output):
    a = []
    if output.name is not None:
        a.append(six.text_type('<h1>%s</h1>' % (output.name, )))

    a.append(six.text_type('<p>'))
    a.append(output.to('html'))
    a.append(six.text_type('</p>'))
    return a

def arguments_from_post(command, post):
    """
    Convert a dictionary of HTTP variables (eg. POST) into dictionary of
    arguments passable to a command.
    :param command: command instance
    :param post: variable dictionary
    :return: kwargs for command
    :raise ValueError: argument validation failed
    """
    out = {}

    for argument in command.ARGUMENTS:
        try:
            v = post[argument.name]

            if isinstance(argument, ValuelessArgument):
                # if we're here, that means that checkbox was clicked
                v = argument.default

        except KeyError:
            if isinstance(argument, ValuelessArgument):
                v = None
            else:
                if argument.required:
                    raise ValueError('Argument %s is required' % (argument.name, ))
                else:
                    v = argument.default

        try:
            out[argument.name] = argument.clean(v)
        except ValueError as e:
            raise ValueError('Argument %s invalid: %s' % (argument.name, e.message))

    return out
