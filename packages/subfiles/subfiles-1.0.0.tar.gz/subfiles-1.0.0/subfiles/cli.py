"""
subfiles

Usage:
  subfiles hello
  subfiles -h | --help
  subfiles --version
  subfiles init

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  subfiles hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/mindey/subfiles
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import subfiles.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(subfiles.commands, k) and v:
            module = getattr(subfiles.commands, k)
            subfiles.commands = getmembers(module, isclass)
            command = [command[1] for command in subfiles.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
