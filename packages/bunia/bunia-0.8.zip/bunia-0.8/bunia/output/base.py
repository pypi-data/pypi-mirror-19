class Output(object):
    """
    An access to some form of output. Override and extend as needed. This is constructed
    by a Runner in response to command request.
    """

    def __init__(self, name=None):
        self.name = name

    def to(self, form='text'):
        """Output content in some particular form.

        It is mandatory to support 'text'.

        Possible values are 'text', 'html'. This is the last call to this objects,
        as Output can close its resources.

        :raises ValueError: form not supported
        :return: depends on form. unicode for text and html
        """
