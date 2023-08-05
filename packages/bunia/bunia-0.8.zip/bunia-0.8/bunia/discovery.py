import importlib
import inspect
import pkgutil

from bunia.api import Command


def from_name(name):
    """
    Return a command by it's class name.

    name is either some.module.path:ClassName if you need to specify it explicitly,
    or some.module.path if .path contains a variable COMMAND, which is that class
    :param name: name to load
    :return: Command class
    :raise NameError: not found
    """
    try:
        if ':' in name:
            module, clsname = name.split(':', 2)

            return importlib.import_module(module).__dict__[clsname]
        else:
            return importlib.import_module(name).COMMAND
    except (KeyError, ImportError):
        raise NameError(name)


def pick_from_module(module, name):
    """
    Walk a module hierarchy. Pick a command with NAME equal to target.

    :param module: module to examine
    :param name: Command name
    :return: Command class
    :raise NameError: command not found
    """
    for command in from_module(module):
        if command.NAME == name:
            return command
    raise NameError('command not found')


def from_module(module):
    """
    Walk a module (+ imported submodules) and return  Command instances found.

    Does not return duplicates, even if found.

    :param module: module to examine
    :return: list of Command instances found
    """
    # get all classes
    commands = []
    for name, member in inspect.getmembers(module):
        if inspect.isclass(member) and issubclass(member, Command) and (member is not Command) and (member not in commands):
            commands.append(member)

    # get submodules
    try:
        l = pkgutil.walk_packages(module.__path__, onerror=lambda x: None)
    except AttributeError:  # no __path__
        return commands

    for finder, modname, ispkg in l:
        commands.extend(from_module(finder.find_module(modname).load_module(modname)))

    return commands
