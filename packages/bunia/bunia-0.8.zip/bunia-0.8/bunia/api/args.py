class Argument(object):
    """
    Definition of an argument
    """

    def __init__(self, name, default=None, required=True, description=''):
        """
        :param username: Name of argument. This must match run() signature
        :param default: default value
        :param required: Is it optional?
        :param description: description
        """
        self.description = description
        self.name = name
        self.default = default
        self.required = required

    def clean(self, val):
        """
        Validate and convert value to target format
        :param val: value of parameter
        :type val: unicode
        :return: a value to set as value of parameter
        :raise ValueError: invalid value
        """
        return val


class ValuelessArgument(Argument):
    """Base class for arguments, whose value will either be None or the default"""
    def __init__(self, name, default=True, description=''):
        Argument.__init__(self, name, default=default, required=False, description=description)


class ListedArgument(Argument):
    """Base class for arguments that additionally provides a list of values to choose from"""

    def get_values(self):
        """Return applicable values
        :return: iterable of tuple (value, value description::unicode)
        """
        return []


class ChoiceArgument(ListedArgument):
    """You can pick only values from the list"""
    def __init__(self, name, choices, *args, **kwargs):
        """
        :param choices: list of tuple (value, human-readable label)
        """
        ListedArgument.__init__(self, name, *args, **kwargs)
        self.choices = choices

    def get_values(self):
        return self.choices

    def clean(self, val):
        for v, lab in self.choices:
            if val == v:
                return val
        raise ValueError(val)

class Integer(Argument):
    """Argument is an integer"""
    def clean(self, val):
        return int(val)


class Float(Argument):
    """Argument is a float"""
    def clean(self, val):
        return float(val)


class Flag(ValuelessArgument):
    """This argument has value of False by default. Seeing it in command"""

    def clean(self, val):
        return val is not None
