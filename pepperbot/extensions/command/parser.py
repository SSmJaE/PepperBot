from argparse import Action, ArgumentParser

from pepperbot.exceptions import PatternFormatError
from pepperbot.store.command import ARGPARSE_HELP


class CustomArgumentParser(ArgumentParser):
    def error(self, message):
        raise PatternFormatError(message)

    def exit(self, status=0, message=None):
        raise PatternFormatError(message)


class CustomHelpAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        raise PatternFormatError(ARGPARSE_HELP, locals())
