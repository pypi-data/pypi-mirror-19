"""
Since it is expected for Bunia to be integrated into systems, no standalone launcher for provided
as for now. This may change.

Helper functions :)
"""


def _outc(output):
    a = []
    if output.name is not None:
        a.append(u'<h1>%s</h1>' % (output.name, ))

    a.append(u'<p>')
    a.append(output.to('html'))
    a.append(u'</p>')
    return a

def format_outputs(outputs):
    """Output a list of Outputs as HTML"""

    # Try to find default console
    for output in outputs:
        if output.name is None:
            default = output
            break
    else:
        default = None

    a = []
    if default is not None:
        a.extend(_outc(default))

    for output in outputs:
        if output is not default:
            a.extend(_outc(default))

    return u''.join(a)
